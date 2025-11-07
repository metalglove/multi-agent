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
                "(performance, accessibility)."
            ),
            expected_output='A Markdown requirements document.',
            agent=self._requirements_analyst,
        )

        self.task2 = Task(
            description=(
                "Based on requirements, outline the tech stack (Vue 3 + TS, Pinia, "
                "Vue Router, vis.js for graphs, Node.js/Express backend, OpenAI API for AI). "
                "Define data models (e.g., Note interface with id, content, tags, links[]), "
                "component hierarchy, and API endpoints (e.g., /notes, /suggest-links)."
            ),
            expected_output='Architecture diagram (text-based or PlantUML) and data schema in TypeScript interfaces.',
            agent=self._system_architect,
        )

        self.task3 = Task(
            description=(
                "Create wireframes for key screens (note editor, link manager, graph viewer). "
                "Specify Vue components (e.g., NoteCard.vue, GraphView.vue) and user flows for "
                "manual linking (drag-drop or select) and AI suggestions (button to trigger similarity scan)."
            ),
            expected_output='Wireframe sketches (text descriptions or ASCII art) and component specs.',
            agent=self._ui_ux_designer,
        )

        self.task4 = Task(
            description=(
                "Design backend routes, database schema (e.g., notes table with links as relations), "
                "and AI workflow (e.g., embed note content via OpenAI, compute cosine similarity for links, "
                "tag extraction using NLP)."
            ),
            expected_output='API spec (e.g., OpenAPI YAML) and AI pseudocode.',
            agent=self._backend_ai_developer,
        )

        self.task5 = Task(
            description=(
                "Write Vue + TS code for core components: note creation/editing, manual linking UI, "
                "graph rendering with vis.js (nodes as notes, edges as links). Integrate Pinia for state "
                "(e.g., notes store with mutations for links). Use file_write_tool to save code to files like src/components/NoteEditor.vue."
            ),
            expected_output='Source code files (e.g., src/components/NoteEditor.vue, src/stores/notes.ts).',
            agent=self._frontend_developer,
        )

        self.task6 = Task(
            description=(
                "Build Node.js server with Express, SQLite ORM (e.g., Sequelize), API endpoints for CRUD and /suggest-links "
                "(using OpenAI embeddings to find similar notes based on content/tags). Handle AI logic for auto-linking (threshold-based similarity)."
            ),
            expected_output='Backend source code (e.g., server.ts, models/note.ts, services/aiService.ts).',
            agent=self._backend_ai_developer,
        )

        self.task7 = Task(
            description=(
                "Connect frontend to backend APIs (e.g., Axios for HTTP calls), ensure AI suggestions populate in UI, "
                "and render graph dynamically from linked notes. Update and write integrated code files."
            ),
            expected_output='Updated codebase with integration (e.g., API calls in Vue components).',
            agent=self._frontend_developer,
        )

        self.task8 = Task(
            description=(
                "Write unit tests (Jest/Vitest for Vue components, logic for linking/graph), integration tests (API endpoints, AI accuracy), "
                "and end-to-end tests (e.g., Cypress for user flows like creating linked notes and viewing graph). Use directory_read_tool to access generated code."
            ),
            expected_output='Test suites and coverage report.',
            agent=self._tester,
        )

        self.task9 = Task(
            description=(
                "Add inline comments, generate README.md with setup instructions (e.g., npm install, run dev server), API docs, "
                "and usage guide for features like AI linking. Use file_write_tool to create docs."
            ),
            expected_output='Updated codebase with docs.',
            agent=self._documentation_agent,
        )

        self.task10 = Task(
            description=(
                "Conduct a final review for code quality, fix issues from tests, and ensure the platform is comprehensive "
                "(e.g., add search by tags, export graph as image). Update files as needed."
            ),
            expected_output='Final polished codebase repository structure.',
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

