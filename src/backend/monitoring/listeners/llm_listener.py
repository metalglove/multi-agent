import asyncio

from crewai import LLM
from crewai import LLM
from crewai.llms.base_llm import BaseLLM
from crewai.events.types.llm_events import (
    LLMCallStartedEvent,
    LLMCallCompletedEvent,
    LLMCallFailedEvent,
    LLMStreamChunkEvent,
)

from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class LLMListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source: BaseLLM | LLM, event: LLMCallStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "llm_name": getattr(event, "model", None),
                "messages": getattr(event, "messages", None),
                "tools": getattr(event, "tools", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "temperature": getattr(source, "temperature", None),
                "callbacks": getattr(event, "callbacks", None),
                "available_functions": getattr(event, "available_functions", None),
            }
            self._push(payload)

        @crewai_event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source: BaseLLM | LLM, event: LLMCallCompletedEvent):
            payload = {
                "type": event.type,
                "call_type": getattr(event, "call_type", None).value if getattr(event, "call_type", None) else None,
                "timestamp": event.timestamp,
                "llm_name": getattr(event, "model", None),
                "temperature": getattr(source, "temperature", None),
                "messages": getattr(event, "messages", None),
                "response": getattr(event, "response", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
            }
            self._push(payload)

        @crewai_event_bus.on(LLMCallFailedEvent)
        def on_llm_call_failed(source: BaseLLM | LLM, event: LLMCallFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "llm_name": getattr(source, "model", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "error": getattr(event, "error", None),
            }
            self._push(payload)

        @crewai_event_bus.on(LLMStreamChunkEvent)
        def on_llm_stream_chunk(source: BaseLLM | LLM, event: LLMStreamChunkEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "llm_name": getattr(source, "model", None),
                "chunk": getattr(event, "chunk", None),
                "tool_call": getattr(event, "tool_call", None),
            }
            self._push(payload)
