"""Backend runner: executes CrewAI workflows and publishes events to Redis.

This module defines the entry point for running CrewAI with event monitoring via Redis pub/sub.
The runner is independent from the bridge (optional WebSocket relay infrastructure).

Usage:
  python -m src.backend.runner_with_monitoring

Environment variables:
  REDIS_URL: Redis connection string (default: redis://127.0.0.1:6379/0)
  REDIS_CHANNEL: Redis pub/sub channel name (default: crewai:events)
  CREW_OUTPUT_FOLDER: Folder for Crew output artifacts (default: outputs)
  OPENAI_MODEL_NAME: LLM model name (default: openai/qwen/qwen3-4b-2507)
  OPENAI_API_BASE: LLM API base URL (default: http://localhost:1234/v1)
  OPENAI_API_KEY: LLM API key (default: not-needed for local models)
"""

from .monitoring import run_with_monitoring

if __name__ == "__main__":
    run_with_monitoring()
