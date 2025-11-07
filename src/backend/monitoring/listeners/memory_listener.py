from typing import Any
import asyncio

from crewai.events.types.memory_events import (
    MemoryRetrievalStartedEvent,
    MemoryRetrievalCompletedEvent,
    MemoryQueryCompletedEvent,
    MemoryQueryStartedEvent,
    MemoryQueryFailedEvent,
    MemorySaveCompletedEvent,
    MemorySaveStartedEvent,
    MemorySaveFailedEvent,
)
from crewai.memory.memory import Memory

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class MemoryListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(MemoryRetrievalStartedEvent)
        def on_memory_retrieval_started(source: Memory, event: MemoryRetrievalStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryRetrievalCompletedEvent)
        def on_memory_retrieval_completed(source: Memory, event: MemoryRetrievalCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "memory_content": getattr(event, "memory_content", None),
                "retrieval_time_ms": getattr(event, "retrieval_time_ms", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryStartedEvent)
        def on_memory_query_started(source: Memory, event: MemoryQueryStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source: Memory, event: MemoryQueryCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "results": getattr(event, "results", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
                "query_time_ms": getattr(event, "query_time_ms", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryFailedEvent)
        def on_memory_query_failed(source: Memory, event: MemoryQueryFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
                "error": getattr(event, "error", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveStartedEvent)
        def on_memory_save_started(source: Memory, event: MemorySaveStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveCompletedEvent)
        def on_memory_save_completed(source: Memory, event: MemorySaveCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
                "save_time_ms": getattr(event, "save_time_ms", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveFailedEvent)
        def on_memory_save_failed(source: Memory, event: MemorySaveFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
                "error": getattr(event, "error", None),
            }
            self._push(payload)
