import os
from typing import List
from crewai import Agent
from crewai_tools import FileWriterTool, DirectoryReadTool
from core.artifacts import ArtifactOutput

def get_all_agents(artifact_output: ArtifactOutput) -> List[Agent]:
    """Return the list of all defined agents."""
    artifact_output_directory = artifact_output.get_base_output_path()
    file_write_tool = FileWriterTool(directory=artifact_output_directory)  # To write generated code to files
    directory_read_tool = DirectoryReadTool(directory=artifact_output_directory)  # To read directories if needed

    # Try to initialize the MCP server adapter if available. If the
    # optional `mcp` package or the MCP adapter isn't present, we
    # fall back to an empty search tool list so the module can be
    # imported without side-effects (no auto-install attempts).
    try:
        from crewai_tools import MCPServerAdapter
        from mcp import StdioServerParameters

        # Initialize tools
        server_params = StdioServerParameters(
            command="node",
            args=["C:/mcp-servers/web-search-mcp-v0.3.2/dist/index.js"],
            env=os.environ  # Pass environment variables if needed
        )

        mcp_server_adapter = MCPServerAdapter(server_params)
        try:
            mcp_server_adapter.start()
            search_tools = mcp_server_adapter.tools
        except Exception as e:
            # If adapter fails to start, warn and continue with empty tools
            print(f"Warning: MCPServerAdapter failed to start: {e}")
            search_tools = []
    except Exception as e:
        print(f"Optional MCP adapter not available: {e}")
        search_tools = []

    # Define Agents
    requirements_analyst = Agent(
        role='Requirements Analyst Agent',
        goal='Analyze and refine user requirements into detailed specs.',
        backstory='An experienced product manager specializing in educational tools, skilled at breaking down vague ideas into actionable specs.',
        tools=search_tools,
        verbose=True,
        allow_delegation=False
    )

    system_architect = Agent(
        role='System Architect Agent',
        goal='Design the overall architecture, including component structure, data models, and tech stack.',
        backstory='A software architect with expertise in full-stack web apps, focusing on graph-based systems.',
        verbose=True,
        allow_delegation=False
    )

    ui_ux_designer = Agent(
        role='UI/UX Designer Agent',
        goal='Produce wireframes, component designs, and Vue templates that are intuitive for educational users.',
        backstory='A frontend designer familiar with Vue and educational platforms, emphasizing usability.',
        verbose=True,
        allow_delegation=False
    )

    frontend_developer = Agent(
        role='Frontend Developer Agent',
        goal='Build responsive components for note management, manual linking, and graph rendering.',
        backstory='A Vue specialist with TypeScript proficiency, experienced in state management and visualization libraries.',
        tools=[file_write_tool],
        verbose=True,
        allow_delegation=True  # Can delegate if needed
    )

    backend_ai_developer = Agent(
        role='Backend & AI Developer Agent',
        goal='Handle data persistence, API endpoints, and AI-driven similarity detection for notes.',
        backstory='A full-stack developer with AI integration experience (e.g., using NLP APIs for content analysis).',
        tools=[file_write_tool] + search_tools,  # Search for AI best practices
        verbose=True,
        allow_delegation=True
    )

    tester = Agent(
        role='Tester Agent',
        goal='Ensure the platform is bug-free, with coverage for linking logic, graph rendering, and AI suggestions.',
        backstory='A QA engineer skilled in unit/integration testing for Vue apps and APIs.',
        tools=[directory_read_tool],  # To read generated code for testing
        verbose=True,
        allow_delegation=False
    )

    documentation_agent = Agent(
        role='Documentation Agent',
        goal='Make the codebase maintainable and easy to deploy/extend.',
        backstory='A technical writer focused on open-source educational tools.',
        tools=[file_write_tool, directory_read_tool],
        verbose=True,
        allow_delegation=False
    )

    return [
        requirements_analyst,
        system_architect,
        ui_ux_designer,
        frontend_developer,
        backend_ai_developer,
        tester,
        documentation_agent
    ]

__all__ = ['get_all_agents']
