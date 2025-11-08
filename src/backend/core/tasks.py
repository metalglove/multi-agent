from typing import List
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

    def __build_tasks__(self):
        self.task1 = Task(
            description=(
                "Analyze the platform description, research similar tools "
                "(e.g., graph-based note apps), and compile a detailed "
                "requirements doc including user stories, features (note CRUD, "
                "manual/AI linking, graph view), and non-functional reqs "
                "(performance, accessibility).\n\n"
                "IMPORTANT: You MUST save the requirements document using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "- Create a file named 'requirements.md'\n"
                "- Write comprehensive Markdown format\n"
                "- Use the File Writer Tool with directory parameter set to the above path\n"
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
                "IMPORTANT: Save your architecture work using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Save architecture diagram to 'architecture.md' (use PlantUML or ASCII art)\n"
                "2. Save TypeScript data models to 'data-schema.ts' (with interfaces and types)\n"
                "- Use the File Writer Tool with directory parameter for BOTH files\n"
                "- Confirm in your response that both files were saved"
            ),
            expected_output=f'Architecture diagram and data schema saved via File Writer Tool to {self._output_directory}/',
            agent=self._system_architect,
        )

        self.task3 = Task(
            description=(
                "Create wireframes for key screens (note editor, link manager, graph viewer). "
                "Specify Vue components (e.g., NoteCard.vue, GraphView.vue) and user flows for "
                "manual linking (drag-drop or select) and AI suggestions (button to trigger similarity scan).\n\n"
                "IMPORTANT: Save your wireframes using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "- Create 'wireframes.md' with ASCII art or text descriptions of key screens\n"
                "- Create 'component-specs.md' with detailed component specifications\n"
                "- Use the File Writer Tool with directory parameter for BOTH files\n"
                "- Confirm in your response that both files were saved"
            ),
            expected_output=f'Wireframes and component specs saved via File Writer Tool to {self._output_directory}/',
            agent=self._ui_ux_designer,
        )

        self.task4 = Task(
            description=(
                "Design backend routes, database schema (e.g., notes table with links as relations), "
                "and AI workflow (e.g., embed note content via OpenAI, compute cosine similarity for links, "
                "tag extraction using NLP).\n\n"
                "IMPORTANT: Save your backend design using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'database-schema.sql' with CREATE TABLE statements\n"
                "2. Create 'api-endpoints.yaml' with OpenAPI/Swagger spec for all endpoints\n"
                "3. Create 'ai-workflow.md' with pseudocode and workflow description\n"
                "- Use the File Writer Tool with directory parameter to save ALL THREE files\n"
                "- Confirm in your response that all files were saved"
            ),
            expected_output=f'API spec, database schema, and AI workflow saved via File Writer Tool to {self._output_directory}/',
            agent=self._backend_ai_developer,
        )

        self.task5 = Task(
            description=(
                "Write Vue + TS code for core components: note creation/editing, manual linking UI, "
                "graph rendering with vis.js (nodes as notes, edges as links). Integrate Pinia for state "
                "(e.g., notes store with mutations for links).\n\n"
                "IMPORTANT: Save your Vue components and store using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'NoteEditor.vue' - Component for creating/editing notes\n"
                "2. Create 'GraphView.vue' - Vis.js graph visualization component\n"
                "3. Create 'notes.ts' - Pinia store for state management\n"
                "- Use the File Writer Tool with directory parameter for EACH file\n"
                "- Include full valid Vue + TypeScript code\n"
                "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Source code files saved via File Writer Tool to {self._output_directory}/',
            agent=self._frontend_developer,
        )

        self.task6 = Task(
            description=(
                "Build Node.js server with Express, SQLite ORM (e.g., Sequelize), API endpoints for CRUD and /suggest-links "
                "(using OpenAI embeddings to find similar notes based on content/tags). Handle AI logic for auto-linking (threshold-based similarity).\n\n"
                "IMPORTANT: Save your backend code using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'server.ts' - Express server setup and main routes\n"
                "2. Create 'models.ts' - Database models and schema\n"
                "3. Create 'ai-service.ts' - AI/embedding logic for similarity detection\n"
                "- Use the File Writer Tool with directory parameter for EACH file\n"
                "- Include full valid Node.js/Express + TypeScript code\n"
                "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Backend source code files saved via File Writer Tool to {self._output_directory}/',
            agent=self._backend_ai_developer,
        )

        self.task7 = Task(
            description=(
                "Connect frontend to backend APIs (e.g., Axios for HTTP calls), ensure AI suggestions populate in UI, "
                "and render graph dynamically from linked notes. Update and write integrated code files.\n\n"
                "IMPORTANT: Save your integration code using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'api-client.ts' - Axios API client for frontend-backend communication\n"
                "2. Create 'NoteEditorIntegrated.vue' - Updated NoteEditor with API integration\n"
                "3. Create 'GraphViewIntegrated.vue' - Updated GraphView with dynamic data loading\n"
                "- Use the File Writer Tool with directory parameter for EACH file\n"
                "- Confirm in your response that all three files were saved"
            ),
            expected_output=f'Integration code files saved via File Writer Tool to {self._output_directory}/',
            agent=self._frontend_developer,
        )

        self.task8 = Task(
            description=(
                "Write unit tests (Jest/Vitest for Vue components, logic for linking/graph), integration tests (API endpoints, AI accuracy), "
                "and end-to-end tests (e.g., Cypress for user flows like creating linked notes and viewing graph). Use directory_read_tool to access generated code.\n\n"
                "IMPORTANT: Save your test files using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'NoteEditor.test.ts' - Unit tests for NoteEditor component\n"
                "2. Create 'api.integration.test.ts' - Integration tests for API endpoints\n"
                "3. Create 'linking.test.ts' - Tests for note linking and similarity detection\n"
                "- Use the File Writer Tool with directory parameter for EACH test file\n"
                "- Include test configuration and complete test suites\n"
                "- Confirm in your response that all test files were saved"
            ),
            expected_output=f'Test suite files saved via File Writer Tool to {self._output_directory}/',
            agent=self._tester,
        )

        self.task9 = Task(
            description=(
                "Add inline comments, generate README.md with setup instructions (e.g., npm install, run dev server), API docs, "
                "and usage guide for features like AI linking. Use file_write_tool to create docs.\n\n"
                "IMPORTANT: Save your documentation using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'README.md' - Project overview, setup, and usage instructions\n"
                "2. Create 'API-DOCS.md' - Complete API documentation with examples\n"
                "3. Create 'CONTRIBUTING.md' - Guidelines for extending the platform\n"
                "- Use the File Writer Tool with directory parameter for EACH documentation file\n"
                "- Use Markdown format with clear sections\n"
                "- Confirm in your response that all documentation files were saved"
            ),
            expected_output=f'Documentation files saved via File Writer Tool to {self._output_directory}/',
            agent=self._documentation_agent,
        )

        self.task10 = Task(
            description=(
                "Conduct a final review for code quality, fix issues from tests, and ensure the platform is comprehensive "
                "(e.g., add search by tags, export graph as image). Update files as needed.\n\n"
                "IMPORTANT: Save your final review and improvements using the File Writer Tool:\n"
                f"- Save to directory: {self._output_directory}\n"
                "1. Create 'REVIEW-SUMMARY.md' - Overall quality assessment and improvements made\n"
                "2. Create 'FINAL-CHECKLIST.md' - Feature completeness checklist\n"
                "3. Update any code files that needed fixes (e.g., improved NoteEditor.vue)\n"
                "- Use the File Writer Tool with directory parameter to save ALL updates\n"
                "- Ensure all code is production-ready\n"
                "- Confirm in your response which files were updated"
            ),
            expected_output=f'Final polished codebase with review summary saved via File Writer Tool to {self._output_directory}/',
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

