import os
from typing import List
from crewai import Agent
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool, MCPServerAdapter
from .artifacts import ArtifactOutput


class AgentManager:
    """Manage creation and access of the workflow agents."""
    def __init__(self, artifact_output: ArtifactOutput):
        self.artifact_output = artifact_output
        self.__initialize_tools__()
        self.__initialize_agents__()

    def __initialize_tools__(self):
        artifact_output_directory = self.artifact_output.get_base_output_path()
        self._file_write_tool = FileWriterTool(directory=artifact_output_directory)  # To write generated code to files
        self._directory_read_tool = DirectoryReadTool(directory=artifact_output_directory)  # To read directories if needed
        self._file_read_tool = FileReadTool()  # To read files if needed
        # Try to initialize the MCP server adapter if available. If the
        # optional `mcp` package or the MCP adapter isn't present, we
        # fall back to an empty search tool list so the module can be
        # imported without side-effects (no auto-install attempts).
        # Attempt to initialize an optional MCP server adapter. This is best-effort
        # so missing optional packages won't prevent module import. If the
        # adapter instance is created successfully we keep a reference on
        # `self._mcp_server_adapter` and expose `.shutdown()` to stop it later.
        self._mcp_server_adapter = None
        try:
            from crewai_tools import MCPServerAdapter
            from mcp import StdioServerParameters

            # Initialize server parameters (path may be project-specific)
            server_params = StdioServerParameters(
                command="node",
                args=["C:/mcp-servers/web-search-mcp-v0.3.2/dist/index.js"],
                env=os.environ  # Pass environment variables if needed
            )

            adapter = MCPServerAdapter(server_params)

            # If the adapter already reports it's running, skip double-start.
            already_running = False
            if hasattr(adapter, "is_running"):
                try:
                    already_running = bool(adapter.is_running())
                except Exception:
                    already_running = False
            elif hasattr(adapter, "running"):
                try:
                    already_running = bool(getattr(adapter, "running"))
                except Exception:
                    already_running = False

            if already_running:
                print("MCPServerAdapter appears to already be running; will reuse existing instance.")
                self._mcp_server_adapter = adapter
                self._search_tools = getattr(adapter, "tools", []) or []
            else:
                try:
                    # If this is the first time we start it in this process,
                    # record it as the global adapter to prevent double-starts
                    adapter.start()
                    self._mcp_server_adapter = adapter
                    self._search_tools = getattr(adapter, "tools", []) or []
                except Exception as e:
                    # Provide clearer diagnostics for common MCP adapter failures
                    msg = str(e)
                    if "threads can only be started once" in msg:
                        print("Warning: MCPServerAdapter.start() called twice in the same process.")
                        print("If you intentionally created multiple AgentManager instances, share a single adapter instead.")
                        # Attempt to reuse the adapter if possible
                        try:
                            self._mcp_server_adapter = adapter
                            self._search_tools = getattr(adapter, "tools", []) or []
                        except Exception:
                            self._mcp_server_adapter = None
                            self._search_tools = []
                    elif "Invalid JSON" in msg or "Failed to parse JSONRPC" in msg or "Waiting for MCP messages" in msg:
                        print("Warning: MCP server produced non-JSON stdout which breaks the JSON-RPC channel.")
                        print("Ensure the MCP server prints only JSON-RPC to stdout, and sends logs to stderr or a log file.")
                        self._mcp_server_adapter = None
                        self._search_tools = []
                    else:
                        print(f"Warning: MCPServerAdapter failed to start: {e}")
                        self._mcp_server_adapter = None
                        self._search_tools = []
        except Exception as e:
            # Optional dependencies not present or adapter couldn't be created
            print(f"Optional MCP adapter not available: {e}")
            self._mcp_server_adapter = None
            self._search_tools = []

    def __initialize_agents__(self):
        """Initialize agents with their roles, goals, backstories, and tools."""
        requirements_analyst = Agent(
            role='Requirements Analyst Agent',
            goal='Analyze and refine user requirements into detailed specs.',
            backstory='An experienced product manager specializing in educational tools, skilled at breaking down vague ideas into actionable specs.',
            tools=self._search_tools,
            verbose=True,
            allow_delegation=False
        )

        system_architect = Agent(
            role='System Architect Agent',
            goal='Design the overall architecture, including component structure, data models, and tech stack.',
            backstory='A software architect with expertise in full-stack web apps, focusing on graph-based systems.',
            tools=[self._file_read_tool],
            verbose=True,
            allow_delegation=False
        )

        ui_ux_designer = Agent(
            role='UI/UX Designer Agent',
            goal='Produce wireframes, component designs, and Vue templates that are intuitive for educational users.',
            backstory='A frontend designer familiar with Vue and educational platforms, emphasizing usability.',
            tools=[self._file_read_tool],
            verbose=True,
            allow_delegation=False
        )

        frontend_developer = Agent(
            role='Frontend Developer Agent',
            goal='Build responsive components for note management, manual linking, and graph rendering.',
            backstory='A Vue specialist with TypeScript expertise, experienced in state management and visualization libraries.',
            tools=[self._file_write_tool, self._file_read_tool],
            verbose=True,
            allow_delegation=True  # Can delegate if needed
        )

        backend_ai_developer = Agent(
            role='Backend & AI Developer Agent',
            goal='Handle data persistence, API endpoints, and AI-driven similarity detection for notes.',
            backstory='A full-stack developer with AI integration experience (e.g., using NLP APIs for content analysis).',
            tools=[self._file_write_tool, self._file_read_tool] + self._search_tools,  # Search for AI best practices
            verbose=True,
            allow_delegation=True
        )

        tester = Agent(
            role='Tester Agent',
            goal='Ensure the platform is bug-free, with coverage for linking logic, graph rendering, and AI suggestions.',
            backstory='A QA engineer skilled in unit/integration testing for Vue apps and APIs.',
            tools=[self._directory_read_tool, self._file_read_tool],  # To read generated code for testing
            verbose=True,
            allow_delegation=False
        )

        documentation_agent = Agent(
            role='Documentation Agent',
            goal='Make the codebase maintainable and easy to deploy/extend.',
            backstory='A technical writer focused on open-source educational tools.',
            tools=[self._file_write_tool, self._directory_read_tool, self._file_read_tool],
            verbose=True,
            allow_delegation=False
        )

        self._agents = [
            requirements_analyst,
            system_architect,
            ui_ux_designer,
            frontend_developer,
            backend_ai_developer,
            tester,
            documentation_agent
        ]
        
    def get_all_agents(self) -> List[Agent]:
        """Return the list of all defined agents."""
        return self._agents

    def shutdown(self):
        """Attempt to gracefully shutdown optional tools (e.g. MCP adapter).

        This method calls common shutdown/stop methods on the adapter if they
        exist and swallows exceptions to avoid raising during program shutdown.
        Call this from your application shutdown hook if you created an
        AgentManager instance that started the adapter.
        """
        if not self._mcp_server_adapter:
            return

         # Try explicit stop first
        # Best-effort: clear reference
        try:
            self._mcp_server_adapter.stop()
            self._mcp_server_adapter = None
        except Exception:
            pass

