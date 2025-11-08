import asyncio
from typing import Union

from crewai import Agent
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
# from crewai.memory import EntityMemory, ExternalMemory, LongTermMemory, ShortTermMemory
from crewai.memory.memory import Memory
from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class MemoryListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(MemoryRetrievalStartedEvent)
        def on_memory_retrieval_started(source: Agent | Memory, event: MemoryRetrievalStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryRetrievalCompletedEvent)
        def on_memory_retrieval_completed(source: Agent | Memory, event: MemoryRetrievalCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "memory_content": getattr(event, "memory_content", None),
                "retrieval_time_ms": getattr(event, "retrieval_time_ms", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryStartedEvent)
        def on_memory_query_started(source: Memory | Agent, event: MemoryQueryStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source: Memory | Agent, event: MemoryQueryCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "results": getattr(event, "results", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
                "query_time_ms": getattr(event, "query_time_ms", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemoryQueryFailedEvent)
        def on_memory_query_failed(source: Agent | Memory, event: MemoryQueryFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "limit": getattr(event, "limit", None),
                "score_threshold": getattr(event, "score_threshold", None),
                "error": getattr(event, "error", None),
                "task_id": getattr(event, "task_id", None),
                "task_name": getattr(event, "task_name", None),
                "from_task": getattr(event, "from_task", None),
                "from_agent": getattr(event, "from_agent", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveStartedEvent)
        def on_memory_save_started(source: Memory | Agent, event: MemorySaveStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveCompletedEvent)
        def on_memory_save_completed(source: Memory | Agent, event: MemorySaveCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
                "save_time_ms": getattr(event, "save_time_ms", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MemorySaveFailedEvent)
        def on_memory_save_failed(source: Memory | Agent, event: MemorySaveFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "value": getattr(event, "value", None),
                "metadata": getattr(event, "metadata", None),
                "error": getattr(event, "error", None),
                "agent_role": getattr(event, "agent_role", None),
                "agent_id": getattr(event, "agent_id", None),
            }
            self._push(payload)
