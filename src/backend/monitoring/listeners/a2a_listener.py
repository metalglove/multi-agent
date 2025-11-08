from typing import Any
import asyncio

from crewai import Agent
from crewai.events.types.a2a_events import (
    A2ADelegationStartedEvent,
    A2ADelegationCompletedEvent,
    A2AConversationStartedEvent,
    A2AConversationCompletedEvent,
    A2AMessageSentEvent,
    A2AResponseReceivedEvent,
)

from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class A2AListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(A2ADelegationStartedEvent)
        def on_a2a_delegation_started(source: Agent | None, event: A2ADelegationStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "endpoint": getattr(event, "endpoint", None),
                "task_description": getattr(event, "task_description", None),
                "is_multiturn": getattr(event, "is_multiturn", None),
                "turn_number": getattr(event, "turn_number", None),
            }
            self._push(payload)

        @crewai_event_bus.on(A2ADelegationCompletedEvent)
        def on_a2a_delegation_completed(source: Agent | None, event: A2ADelegationCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "status": getattr(event, "status", None),
                "result": getattr(event, "result", None),
                "error": getattr(event, "error", None),
                "is_multiturn": getattr(event, "is_multiturn", None),
            }
            self._push(payload)

        @crewai_event_bus.on(A2AConversationStartedEvent)
        def on_a2a_conversation_started(source: Agent | None, event: A2AConversationStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "endpoint": getattr(event, "endpoint", None),
                "a2a_agent_name": getattr(event, "a2a_agent_name", None),
            }
            self._push(payload)

        @crewai_event_bus.on(A2AConversationCompletedEvent)
        def on_a2a_conversation_completed(source: Agent | None, event: A2AConversationCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "status": getattr(event, "status", None),
                "final_result": getattr(event, "final_result", None),
                "error": getattr(event, "error", None),
                "total_turns": getattr(event, "total_turns", None),
            }
            self._push(payload)

        @crewai_event_bus.on(A2AMessageSentEvent)
        def on_a2a_message_sent(source: Agent | None, event: A2AMessageSentEvent):
            from_agent_id = None
            from_agent_role = None
            if isinstance(event.from_agent, Agent):
                from_agent_id = event.from_agent.id
                from_agent_role = event.from_agent.role

            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "from_agent_id": from_agent_id,
                "from_agent_role": from_agent_role,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "message": getattr(event, "message", None),
                "is_multiturn": getattr(event, "is_multiturn", None),
                "turn_number": getattr(event, "turn_number", None),
            }
            self._push(payload)

        @crewai_event_bus.on(A2AResponseReceivedEvent)
        def on_a2a_response_received(source: Agent | None, event: A2AResponseReceivedEvent):
            from_agent_id = None
            from_agent_role = None
            if isinstance(event.from_agent, Agent):
                from_agent_id = event.from_agent.id
                from_agent_role = event.from_agent.role

            payload = {
                "type": event.type,
                "timestamp": event.timestamp,
                "from_agent_id": from_agent_id,
                "from_agent_role": from_agent_role,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,

                "response": getattr(event, "response", None),
                "is_multiturn": getattr(event, "is_multiturn", None),
                "turn_number": getattr(event, "turn_number", None),
                "status": getattr(event, "status", None),
            }
            self._push(payload)
