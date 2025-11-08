"""Monitoring package: forward events from in-process CrewAI event bus to backend WebSocket bridge.

Exports:
 - orchestrator.run_with_monitoring(...) to start forwarding and run the Crew.
"""

from .orchestrator import run_with_monitoring
from .forwarder import redis_forwarder, start_loop_in_thread
from .listener import setup_listeners

__all__ = [
    "run_with_monitoring",
    "redis_forwarder",
    "start_loop_in_thread",
    "setup_listeners"
]
