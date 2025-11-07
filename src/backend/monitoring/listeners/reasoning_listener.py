from typing import Any
import asyncio

from crewai import Agent
from crewai.events.types.reasoning_events import (
    AgentReasoningStartedEvent,
    AgentReasoningCompletedEvent,
    AgentReasoningFailedEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class ReasoningListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(AgentReasoningStartedEvent)
        def on_agent_reasoning_started(source: Agent, event: AgentReasoningStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "attempt": event.attempt,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
            }
            self._push(payload)

        @crewai_event_bus.on(AgentReasoningCompletedEvent)
        def on_agent_reasoning_completed(source: Agent, event: AgentReasoningCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "attempt": event.attempt,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "ready": getattr(event, "ready", None),
                "plan": getattr(event, "plan", None),
            }
            self._push(payload)

        @crewai_event_bus.on(AgentReasoningFailedEvent)
        def on_agent_reasoning_failed(source: Agent, event: AgentReasoningFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "attempt": event.attempt,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "error": getattr(event, "error", None),
            }
            self._push(payload)
