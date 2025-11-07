from typing import Any
import asyncio

from crewai import Crew
from crewai.events.types.crew_events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    CrewKickoffFailedEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class CrewListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_kickoff_started(source: Crew, event: CrewKickoffStartedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "inputs": getattr(event, "inputs", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_kickoff_completed(source: Crew, event: CrewKickoffCompletedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "output": getattr(event, "output", None),
                "total_tokens": getattr(event, "total_tokens", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewKickoffFailedEvent)
        def on_crew_kickoff_failed(source: Crew, event: CrewKickoffFailedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "error": getattr(event, "error", None),
            }
            self._push(payload)
