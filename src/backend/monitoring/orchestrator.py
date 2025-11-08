"""Orchestrator to wire AgentManager, ForwardingListener and forwarder loop.

This module provides a single entrypoint `run_with_monitoring()` which is a
near drop-in replacement for the previous `runner_with_monitoring.py` but with
responsibilities split for easier testing and maintenance.
"""
import os
import sys
import asyncio
import threading

from ..core.artifacts import ArtifactOutput
from ..core.agents import AgentManager
from ..core.tasks import TaskManager

from crewai import LLM, Crew, Process
from crewai.events import crewai_event_bus

from .forwarder import redis_forwarder, start_loop_in_thread
from .listener import setup_listeners


def run_with_monitoring():
    OUTPUT_FOLDER = os.getenv('CREW_OUTPUT_FOLDER', 'outputs')
    
    # Convert to absolute path to ensure FileWriterTool can save files
    OUTPUT_FOLDER = os.path.abspath(OUTPUT_FOLDER)

    # Build agents and tasks
    artifact_output = ArtifactOutput(OUTPUT_FOLDER)
    
    # Ensure output directory exists
    output_path = artifact_output.get_base_output_path()
    os.makedirs(output_path, exist_ok=True)
    print(f"\nCrewAI Output Directory: {output_path}")
    print(f"Directory created: {os.path.exists(output_path)}")
    print(f"Is writable: {os.access(output_path, os.W_OK)}\n")
    
    agent_manager = AgentManager(artifact_output)
    task_manager = TaskManager(agent_manager)
    agents = agent_manager.get_all_agents()
    tasks = task_manager.get_all_tasks()

    # LLM and embedder configuration (can be overridden via env). The defaults
    # are tuned for a local LM Studio instance running an OpenAI-compatible
    # endpoint (e.g. http://localhost:1234/v1). We keep model identifiers
    # separate so the same base_url can be used for both the LLM and the
    # embedder.
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", "8192"))  # per-response cap
    context_window = int(os.getenv("LLM_CONTEXT_WINDOW", "128000"))  # large extended context

    # LM Studio / local LLM defaults
    llm_model = os.getenv("LLM_MODEL", "openai/openai/gpt-oss-20b")
    api_base = os.getenv("LLM_API_BASE", "http://localhost:1234/v1")
    api_key = os.getenv("LLM_API_KEY", "sk-12345")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    top_p = float(os.getenv("LLM_TOP_P", "0.95"))

    # Embedder defaults (same base_url, different model id)
    embedder_model = os.getenv("EMBEDDER_MODEL", "text-embedding-nomic-embed-text-v1.5")
    embedder_dims = int(os.getenv("EMBEDDER_DIMS", "768"))

    # Log LLM configuration for debugging
    print(f"\n🧠 LLM Configuration:")
    print(f"   Model: {llm_model}")
    print(f"   Base URL: {api_base}")
    print(f"   Context Window: {context_window} tokens")
    print(f"   Max Output Tokens: {max_tokens} tokens")
    print(f"   Available for Input: {context_window - max_tokens} tokens\n")

    llm_config = {
        "model": llm_model,
        "base_url": api_base,
        "api_key": api_key,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    # Initialize the LLM instance used by the crew manager/chat
    local_llm = LLM(**llm_config)

    # Embedder configuration using the same OpenAI-compatible API surface
    embedder = {
        "provider": "openai",
        "config": {
            "api_key": api_key,
            "api_base": api_base,
            "model": embedder_model,
            "dimensions": embedder_dims,
        },
    }

    # Crew-level flags (can be tuned through environment variables)
    crew_verbose = os.getenv("CREW_VERBOSE", "true")
    crew_memory = os.getenv("CREW_MEMORY", "true").lower() in ("1", "true", "yes")
    crew_cache = os.getenv("CREW_CACHE", "true").lower() in ("1", "true", "yes")

    crew: Crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=local_llm,
        chat_llm=local_llm,
        verbose=crew_verbose,
        memory=crew_memory,
        embedder=embedder,
        cache=crew_cache,
    )

    project_details = """
    A platform to write notes and create a knowledge graph with manual linking 
    and graph visualization through tags, using a Vue frontend and TypeScript backend.
    Make sure to write the code and documentation in a modular way, with clear separation 
    using the file writer tool at each step of the process.
    """

    print("\n🚀 Starting CrewAI with Event Monitoring...")
    print("📊 Events are being streamed to WebSocket clients")
    print("🌐 Open http://localhost:5173 to view the dashboard\n")

    # Setup forwarder (Redis publisher)
    redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    redis_channel = os.getenv("REDIS_CHANNEL", "crewai:events")
    loop = asyncio.new_event_loop()
    send_queue: asyncio.Queue = asyncio.Queue()

    # Create listeners that forwards into the queue
    listeners = setup_listeners(loop, send_queue, crewai_event_bus)

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
