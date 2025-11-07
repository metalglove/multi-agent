"""Orchestrator to wire AgentManager, ForwardingListener and forwarder loop.

This module provides a single entrypoint `run_with_monitoring()` which is a
near drop-in replacement for the previous `runner_with_monitoring.py` but with
responsibilities split for easier testing and maintenance.
"""
import os
import sys
import asyncio
import threading

# Ensure src/ is on sys.path so we can import core packages with plain names
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.artifacts import ArtifactOutput
from core.agents import AgentManager
from core.tasks import TaskManager
from crewai import LLM, Crew, Process
from crewai.events import crewai_event_bus

from .forwarder import redis_forwarder, start_loop_in_thread
from .listener import ForwardingListener


def run_with_monitoring():
    OUTPUT_FOLDER = os.getenv('CREW_OUTPUT_FOLDER', 'outputs')

    # Build agents and tasks
    artifact_output = ArtifactOutput(OUTPUT_FOLDER)
    agent_manager = AgentManager(artifact_output)
    task_manager = TaskManager(agent_manager)
    agents = agent_manager.get_all_agents()
    tasks = task_manager.get_all_tasks()

    # LLM configuration (can be overridden via env)
    local_llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "openai/qwen/qwen3-4b-2507"),
        base_url=os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
        temperature=0.7,
    )

    crew: Crew = Crew(
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
                "model": "text-embedding-nomic-embed-text-v1.5",
            },
        },
    )

    project_details = """
    A platform to write notes and create a knowledge graph with manual linking 
    and graph visualization through tags, using a Vue frontend and TypeScript backend.
    """

    print("\n🚀 Starting CrewAI with Event Monitoring...")
    print("📊 Events are being streamed to WebSocket clients")
    print("🌐 Open http://localhost:5173 to view the dashboard\n")

    # Setup forwarder (Redis publisher)
    redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    redis_channel = os.getenv("REDIS_CHANNEL", "crewai:events")
    loop = asyncio.new_event_loop()
    send_queue: asyncio.Queue = asyncio.Queue()

    # Create listener that forwards into the queue
    forwarding_listener = ForwardingListener(loop, send_queue)
    forwarding_listener.setup_listeners(crewai_event_bus)

    # Start forwarder in background thread (publishes to Redis)
    forwarder_coro = redis_forwarder(send_queue, redis_url, redis_channel)
    forwarder_thread = start_loop_in_thread(loop, forwarder_coro)

    # Run the crew in a worker thread
    def _run_crew():
        try:
            print("🏁 Kicking off CrewAI process...\n")
            crew.kickoff(inputs={'project_details': project_details})
        except Exception as e:
            print(f"Error during CrewAI kickoff: {e}")
        finally:
            # Signal forwarder to stop and attempt graceful agent manager shutdown
            try:
                loop.call_soon_threadsafe(send_queue.put_nowait, None)
            except Exception:
                pass
            try:
                agent_manager.shutdown()
            except Exception:
                pass

    crew_thread = threading.Thread(target=_run_crew, daemon=True)
    crew_thread.start()
    crew_thread.join()

    # wait briefly for forwarder to finish
    forwarder_thread.join(timeout=5)


if __name__ == "__main__":
    run_with_monitoring()
