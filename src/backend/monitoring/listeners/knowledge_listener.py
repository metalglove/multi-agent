import asyncio

from crewai import Agent
from crewai.knowledge.knowledge import Knowledge
from crewai.events.types.knowledge_events import (
    KnowledgeSearchQueryFailedEvent,
    KnowledgeRetrievalStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    KnowledgeQueryCompletedEvent,
    KnowledgeQueryFailedEvent,
    KnowledgeQueryStartedEvent,
)

from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus


class KnowledgeListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(KnowledgeQueryStartedEvent)
        def on_knowledge_query_started(source: Knowledge, event: KnowledgeQueryStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "task_prompt": getattr(event, "task_prompt", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
            }
            self._push(payload)

        @crewai_event_bus.on(KnowledgeQueryCompletedEvent)
        def on_knowledge_query_completed(source: Agent, event: KnowledgeQueryCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "query": getattr(event, "query", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
            }
            self._push(payload)

        @crewai_event_bus.on(KnowledgeQueryFailedEvent)
        def on_knowledge_query_failed(source: Agent, event: KnowledgeQueryFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "error": getattr(event, "error", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
            }
            self._push(payload)

        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def on_knowledge_retrieval_started(source: Agent, event: KnowledgeRetrievalStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
                "query": getattr(event, "query", None),
            }
            self._push(payload)

        @crewai_event_bus.on(KnowledgeRetrievalCompletedEvent)
        def on_knowledge_retrieval_completed(source: Agent, event: KnowledgeRetrievalCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "retrieved_knowledge": getattr(event, "retrieved_knowledge", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
            }
            self._push(payload)

        @crewai_event_bus.on(KnowledgeSearchQueryFailedEvent)
        def on_knowledge_search_query_failed(source: Agent, event: KnowledgeSearchQueryFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "query": getattr(event, "query", None),
                "error": getattr(event, "error", None),
                "source_type": getattr(event, "source_type", None),
                "source_id": getattr(event, "source_fingerprint", None),
            }
            self._push(payload)
