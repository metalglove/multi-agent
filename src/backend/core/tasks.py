from typing import List, Dict, Union
from crewai import Task

from .agents import AgentManager

class TaskManager:
    """Manage creation and access of the workflow tasks.

    TaskManager mirrors the pattern used by AgentManager: it accepts
    an optional AgentManager instance (or will create one using a
    default ArtifactOutput) and exposes the tasks via
    `get_all_tasks()`.
    """

    def __init__(self, agent_manager: AgentManager):

        self._agents = agent_manager.get_all_agents()
        self._output_directory = agent_manager.output_directory
        (
            self._requirements_analyst,
            self._system_architect,
            self._ui_ux_designer,
            self._frontend_developer,
            self._backend_ai_developer,
            self._tester,
            self._documentation_agent,
        ) = self._agents

        # Build tasks
        self.__build_tasks__()

    def batch_file_writer_description(self, file_map: Union[List[str], Dict[str, str]]) -> str:
        """Return a standardized instruction block for the Batch File Writer Tool.

        Accepts either:
        - a list of filenames (e.g. ["a.md", "b.ts"]) where each entry will use
          the TaskManager's top-level output directory for storage, or
        - a dict mapping path (optionally including subdirectories) to a content
          placeholder (e.g. {"docs/requirements.md": "<requirements markdown here>"}).

        For keys that include subdirectories (e.g. "docs/requirements.md"), the
        generated example will set the file's "directory" to the corresponding
        subdirectory under the configured output directory (e.g.
        "{self._output_directory}/docs").
        """
        example_lines = []

        # Helper to append a JSON object line for a filename/content tuple
        def add_entry(directory: str, filename: str, content_placeholder: str):
            # Escape double quotes inside placeholder (unlikely but safe)
            placeholder = content_placeholder.replace('"', '\\"')
            example_lines.append(
                f'    {{ "filename": "{filename}", "content": "{placeholder}", "directory": "{directory}", "overwrite": true }}'
            )

        if isinstance(file_map, dict):
            for path, placeholder in file_map.items():
                # Normalize: if path contains subdir(s), split them
                if "/" in path or "\\" in path:
                    # Use forward slashes in keys but handle both separators robustly
                    parts = path.replace("\\", "/").split("/")
                    filename = parts[-1]
                    subdir = "/".join(parts[:-1])
                    directory = f"{self._output_directory}/{subdir}"
                else:
                    filename = path
                    directory = self._output_directory
                add_entry(directory, filename, placeholder)
        else:
            # Assume it's a list of filenames
            for fn in file_map:
                add_entry(self._output_directory, fn, "<content here>")

        example_block = ",\n".join(example_lines)

        prefix = (
            "IMPORTANT: Save your files using the Batch File Writer Tool:\n"
            f"- Save to directory: '{self._output_directory}'\n"
            "- NOTE: Use the absolute path shown above. Do NOT send the literal string '<directory>' to the tool.\n"
            "- If your content contains quotes, newlines, or other characters that make JSON fragile, you can encode the file content as base64 and provide it using the 'content_b64' key (recommended for large/quote-heavy text).\n"
            "  To encode text, call the 'base64-encode' tool first and pass the returned 'content_b64' into the Batch File Writer entry.\n"
            "  Example flow:\n"
            "    1) Call base64-encode with the file text -> returns {\"content_b64\": \"...\"}\n"
            "    2) Call Batch File Writer with the JSON array including content_b64 instead of content.\n"
            "  Example Batch File Writer entry (single file):\n"
            "  [\n"
        )

        single_example = (
            '    { "filename": "REVIEW-SUMMARY.md", "content_b64": "<base64 here>", '
            '"directory": "' + self._output_directory + '", "overwrite": true }\n'
        )

        suffix = (
            "  ]\n"
            "- Use the Batch File Writer Tool to save all files in a single call by passing a JSON array of file objects exactly like this:\n"
            "  [\n"
            f"{example_block}\n"
            "  ]\n"
            "- Return only the JSON array as the tool call (no explanatory text).\n"
        )

        return prefix + single_example + suffix

    def __build_tasks__(self):
        self.task1 = Task(
            description=(
                "Analyze the platform description, research similar tools "
                "(e.g., graph-based note apps), and compile a detailed "
                "requirements doc including user stories, features (note CRUD, "
                "manual/AI linking, graph view), and non-functional reqs "
                "(performance, accessibility).\n\n"
                "IMPORTANT: You MUST save the requirements document using the File Writer Tool:\n"
                f"- Save to directory: '{self._output_directory}'\n"
                "- Create a file named 'requirements.md'\n"
                "- Write comprehensive Markdown format\n"
                "- Example single-file call (File Writer Tool):\n"
                "  { 'filename': 'requirements.md', 'content': '<markdown here>', 'directory': '<directory here>', 'overwrite': true }\n"
                "- Confirm in your final response that you saved the file"
            ),
            expected_output=f'A Markdown requirements document saved via File Writer Tool as {self._output_directory}/requirements.md.',
            agent=self._requirements_analyst,
        )

        self.task2 = Task(
            description=(
                "Based on requirements, outline the tech stack (Vue 3 + TS, Pinia, "
                "Vue Router, vis.js for graphs, Node.js/Express backend, OpenAI API for AI). "
                "Define data models (e.g., Note interface with id, content, tags, links[]), "
                "component hierarchy, and API endpoints (e.g., /notes, /suggest-links).\n\n"
                "1. Save architecture diagram to 'architecture.md' (use PlantUML or ASCII art)\n"
                "2. Save TypeScript data models to 'data-schema.ts' (with interfaces and types)\n"
                + self.batch_file_writer_description(["architecture.md", "data-schema.ts"]) \
                + "- Confirm in your response that both files were saved"
            ),
            expected_output=f'Architecture diagram and data schema saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._system_architect,
        )

        self.task3 = Task(
            description=(
                "Create wireframes for key screens (note editor, link manager, graph viewer). "
                "Specify Vue components (e.g., NoteCard.vue, GraphView.vue) and user flows for "
                "manual linking (drag-drop or select) and AI suggestions (button to trigger similarity scan).\n\n"
                "- Create 'wireframes.md' with ASCII art or text descriptions of key screens\n"
                "- Create 'component-specs.md' with detailed component specifications\n"
                + self.batch_file_writer_description(["wireframes.md", "component-specs.md"]) \
                + "- Confirm in your response that both files were saved"
            ),
            expected_output=f'Wireframes and component specs saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._ui_ux_designer,
        )

        self.task4 = Task(
            description=(
                "Design backend routes, database schema (e.g., notes table with links as relations), "
                "and AI workflow (e.g., embed note content via OpenAI, compute cosine similarity for links, "
                "tag extraction using NLP).\n\n"
                "1. Create 'database-schema.sql' with CREATE TABLE statements\n"
                "2. Create 'api-endpoints.yaml' with OpenAPI/Swagger spec for all endpoints\n"
                "3. Create 'ai-workflow.md' with pseudocode and workflow description\n"
                + self.batch_file_writer_description(["database-schema.sql", "api-endpoints.yaml", "ai-workflow.md"]) \
                + "- Confirm in your response that all files were saved"
            ),
            expected_output=f'API spec, database schema, and AI workflow saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._backend_ai_developer,
        )

        self.task5 = Task(
            description=(
                "Write Vue + TS code for core components: note creation/editing, manual linking UI, "
                "graph rendering with vis.js (nodes as notes, edges as links). Integrate Pinia for state "
                "(e.g., notes store with mutations for links).\n\n"
                "1. Create 'NoteEditor.vue' - Component for creating/editing notes\n"
                "2. Create 'GraphView.vue' - Vis.js graph visualization component\n"
                "3. Create 'notes.ts' - Pinia store for state management\n"
                + self.batch_file_writer_description(["NoteEditor.vue", "GraphView.vue", "notes.ts"]) \
                + "- Include full valid Vue + TypeScript code\n"
                + "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Source code files saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._frontend_developer,
        )

        self.task6 = Task(
            description=(
                "Build Node.js server with Express, SQLite ORM (e.g., Sequelize), API endpoints for CRUD and /suggest-links "
                "(using OpenAI embeddings to find similar notes based on content/tags). Handle AI logic for auto-linking (threshold-based similarity).\n\n"
                "1. Create 'server.ts' - Express server setup and main routes\n"
                "2. Create 'models.ts' - Database models and schema\n"
                "3. Create 'ai-service.ts' - AI/embedding logic for similarity detection\n"
                + self.batch_file_writer_description(["server.ts", "models.ts", "ai-service.ts"]) \
                + "- Include full valid Node.js/Express + TypeScript code\n"
                + "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Backend source code files saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._backend_ai_developer,
        )

        self.task7 = Task(
            description=(
                "Connect frontend to backend APIs (e.g., Axios for HTTP calls), ensure AI suggestions populate in UI, "
                "and render graph dynamically from linked notes. Update and write integrated code files.\n\n"
                "1. Create 'api-client.ts' - Axios API client for frontend-backend communication\n"
                "2. Create 'NoteEditorIntegrated.vue' - Updated NoteEditor with API integration\n"
                "3. Create 'GraphViewIntegrated.vue' - Updated GraphView with dynamic data loading\n"
                + self.batch_file_writer_description(["api-client.ts", "NoteEditorIntegrated.vue", "GraphViewIntegrated.vue"]) \
                + "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Integration code files saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._frontend_developer,
        )

        self.task8 = Task(
            description=(
                "Write unit tests (Jest/Vitest for Vue components, logic for linking/graph), integration tests (API endpoints, AI accuracy), "
                "and end-to-end tests (e.g., Cypress for user flows like creating linked notes and viewing graph). Use directory_read_tool to access generated code.\n\n"
                "1. Create 'NoteEditor.test.ts' - Unit tests for NoteEditor component\n"
                "2. Create 'api.integration.test.ts' - Integration tests for API endpoints\n"
                "3. Create 'linking.test.ts' - Tests for note linking and similarity detection\n"
                + self.batch_file_writer_description(["NoteEditor.test.ts", "api.integration.test.ts", "linking.test.ts"]) \
                + "- Include test configuration and complete test suites\n"
                + "- Confirm in your response that all test files were saved"
            ),
            expected_output=f'Test suite files saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._tester,
        )

        self.task9 = Task(
            description=(
                "Add inline comments, generate README.md with setup instructions (e.g., npm install, run dev server), API docs, "
                "and usage guide for features like AI linking.\n\n"
                "1. Create 'README.md' - Project overview, setup, and usage instructions\n"
                "2. Create 'API-DOCS.md' - Complete API documentation with examples\n"
                "3. Create 'CONTRIBUTING.md' - Guidelines for extending the platform\n"
                + self.batch_file_writer_description(["README.md", "API-DOCS.md", "CONTRIBUTING.md"]) \
                + "- Use Markdown format with clear sections\n"
                + "- Confirm in your response that all documentation files were saved"
            ),
            expected_output=f'Documentation files saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._documentation_agent,
        )

        self.task10 = Task(
            description=(
                "Conduct a final review for code quality, fix issues from tests, and ensure the platform is comprehensive "
                "(e.g., add search by tags, export graph as image). Update files as needed.\n\n"
                "1. Create 'REVIEW-SUMMARY.md' - Overall quality assessment and improvements made\n"
                "2. Create 'FINAL-CHECKLIST.md' - Feature completeness checklist\n"
                "3. Update any code files that needed fixes (e.g., improved NoteEditor.vue)\n"
                + self.batch_file_writer_description({
                    "REVIEW-SUMMARY.md": "<summary>",
                    "FINAL-CHECKLIST.md": "<checklist>",
                    "NoteEditor.vue": "<updated code>",
                }) \
                + "- Ensure all code is production-ready\n"
                + "- Confirm in your response which files were updated"
            ),
            expected_output=f'Final polished codebase with review summary saved via Batch File Writer Tool to {self._output_directory}/',
            agent=self._system_architect,
        )

        self._tasks = [
            self.task1,
            self.task2,
            self.task3,
            self.task4,
            self.task5,
            self.task6,
            self.task7,
            self.task8,
            self.task9,
            self.task10,
        ]

    def get_all_tasks(self) -> List[Task]:
        """Return the list of all defined tasks."""
        return self._tasks

