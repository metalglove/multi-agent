from typing import Any
import asyncio

from crewai.events.types.llm_guardrail_events import (
    LLMGuardrailStartedEvent,
    LLMGuardrailCompletedEvent,
    LLMGuardrailFailedEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class GuardrailListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(LLMGuardrailStartedEvent)
        def on_guardrail_started(source: Any, event: LLMGuardrailStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
                "guardrail": getattr(event, "guardrail", None),
                "retry_count": getattr(event, "retry_count", None),
            }
            self._push(payload)

        @crewai_event_bus.on(LLMGuardrailCompletedEvent)
        def on_guardrail_completed(source: Any, event: LLMGuardrailCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
                "success": getattr(event, "success", None),
                "result": getattr(event, "result", None),
                "error": getattr(event, "error", None),
                "retry_count": getattr(event, "retry_count", None),
            }
            self._push(payload)

        @crewai_event_bus.on(LLMGuardrailFailedEvent)
        def on_guardrail_failed(source: Any, event: LLMGuardrailFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
                "error": getattr(event, "error", None),
                "retry_count": getattr(event, "retry_count", None),
            }
            self._push(payload)
