import os
import sys
from dotenv import load_dotenv
from crewai import LLM, Crew, Process

from core.artifacts import ArtifactOutput

# Ensure `src/` is on sys.path so imports like `from core.agents import ...`
# resolve to the `src/core` package rather than any top-level `core/` folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from core.agents import get_all_agents
from core.tasks import get_all_tasks

load_dotenv()

OUTPUT_FOLDER = os.getenv('CREW_OUTPUT_FOLDER', 'outputs')

def build_agents_and_tasks():
    artifact_output = ArtifactOutput(OUTPUT_FOLDER)
    agents = get_all_agents(artifact_output)
    tasks = get_all_tasks()
    return agents, tasks

# Explicit LLM setup for local LM Studio integration
local_llm = LLM(
    model=os.getenv("OPENAI_MODEL_NAME", "openai/qwen/qwen3-4b-2507"),
    base_url=os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
    temperature=0.7
)

def run_with_monitoring():
    """
    Run CrewAI with event monitoring enabled.
    
    Make sure the FastAPI backend is running:
    python src/backend/server.py
    
    Events will be streamed to connected WebSocket clients.
    """
    agents, tasks = build_agents_and_tasks()

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=local_llm,
        verbose=True,
        memory=True,
        embedder={
            "provider": "openai",
            "config": {
                "api_key": "not-needed",
                "api_base": "http://localhost:1234/v1",
                "model": "text-embedding-nomic-embed-text-v1.5"
            }
        }
    )

    project_details = """
    A platform to write notes and create a knowledge graph with manual linking 
    and graph visualization through tags, using a Vue frontend and TypeScript backend.
    """

    print("\n🚀 Starting CrewAI with Event Monitoring...")
    print("📊 Events are being streamed to WebSocket clients")
    print("🌐 Open http://localhost:5173 to view the dashboard\n")

    crew.kickoff(inputs={'project_details': project_details})

if __name__ == "__main__":
    run_with_monitoring()
