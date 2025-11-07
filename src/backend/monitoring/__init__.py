"""Monitoring package: forward events from in-process CrewAI event bus to backend WebSocket bridge.

Exports:
 - orchestrator.run_with_monitoring(...) to start forwarding and run the Crew.
"""

from .orchestrator import run_with_monitoring

__all__ = ["run_with_monitoring"]
