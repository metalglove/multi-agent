"""Listener that pushes CrewAI events onto an asyncio.Queue for forwarding."""
from typing import Any
import asyncio

from crewai.events import BaseEventListener


class ForwardingListener(BaseEventListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__()
        self._loop = loop
        self._queue = queue

    def _push(self, payload: dict) -> None:
        try:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, payload)
        except Exception as e:
            print(f"[listener] Failed to enqueue event: {e}")

    def setup_listeners(self, crewai_event_bus: Any) -> None:
        # Import event types lazily so module imports don't fail if crewai is missing
        from crewai.events import (
            AgentReasoningStartedEvent,
        )

        @crewai_event_bus.on(AgentReasoningStartedEvent)
        def on_reasoning_started(source, event):
            payload = {
                "type": "agent_reasoning_started",
                "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                "agent_role": getattr(event.agent, "role", str(getattr(event, "agent", "unknown")))
            }
            self._push(payload)

        # Register additional common event types if available
        try:
            from crewai.events import (
                TaskStartedEvent,
                TaskCompletedEvent,
                TaskFailedEvent,
                AgentReasoningCompletedEvent,
                AgentReasoningFailedEvent,
            )

            @crewai_event_bus.on(TaskStartedEvent)
            def on_task_started(source, event):
                payload = {
                    "type": "task_started",
                    "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                    "task_title": getattr(event.task, "title", str(getattr(event, "task", "unknown")))
                }
                self._push(payload)

            @crewai_event_bus.on(TaskCompletedEvent)
            def on_task_completed(source, event):
                payload = {
                    "type": "task_completed",
                    "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                    "task_title": getattr(event.task, "title", str(getattr(event, "task", "unknown"))),
                    "task_output": str(getattr(event, "task_output", ""))[:1000]
                }
                self._push(payload)

            @crewai_event_bus.on(TaskFailedEvent)
            def on_task_failed(source, event):
                payload = {
                    "type": "task_failed",
                    "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                    "task_title": getattr(event, "task", "unknown"),
                    "error": str(getattr(event, "error", ""))
                }
                self._push(payload)

            @crewai_event_bus.on(AgentReasoningCompletedEvent)
            def on_reasoning_completed(source, event):
                payload = {
                    "type": "agent_reasoning_completed",
                    "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                    "agent_role": getattr(event.agent, "role", str(getattr(event, "agent", "unknown")))
                }
                self._push(payload)

            @crewai_event_bus.on(AgentReasoningFailedEvent)
            def on_reasoning_failed(source, event):
                payload = {
                    "type": "agent_reasoning_failed",
                    "timestamp": getattr(event, "timestamp", None) and str(event.timestamp) or None,
                    "agent_role": getattr(event.agent, "role", str(getattr(event, "agent", "unknown"))),
                    "error": str(getattr(event, "error", ""))
                }
                self._push(payload)
        except Exception:
            # Not all event types may be available depending on crewai version
            pass
