import asyncio

from crewai import Agent
from crewai.events.types.logging_events import (
    AgentLogsStartedEvent,
    AgentLogsExecutionEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

from crewai.agent.core import LiteAgent

class LoggingListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(AgentLogsStartedEvent)
        def on_agent_logs_started(source: Agent, event: AgentLogsStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "agent_role": getattr(event, "agent_role", None),
                "task_description": getattr(event, "task_description", None),
                "verbose": getattr(event, "verbose", None),
            }
            self._push(payload)

        @crewai_event_bus.on(AgentLogsExecutionEvent)
        def on_agent_logs_exec(source: Agent | LiteAgent, event: AgentLogsExecutionEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "agent_role": getattr(event, "agent_role", None),
                "formatted_answer": getattr(event, "formatted_answer", None),
                "verbose": getattr(event, "verbose", None),
            }
            self._push(payload)
