from typing import Any
import asyncio

from crewai import Crew
from crewai.events.types.crew_events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    CrewKickoffFailedEvent,
    CrewTrainStartedEvent,
    CrewTrainCompletedEvent,
    CrewTrainFailedEvent,
    CrewTestStartedEvent,
    CrewTestCompletedEvent,
    CrewTestFailedEvent,
    CrewTestResultEvent,
)

from .forward_listener import ForwardingListener
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

        @crewai_event_bus.on(CrewTrainStartedEvent)
        def on_crew_train_started(source: Crew, event: CrewTrainStartedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "n_iterations": getattr(event, "n_iterations", None),
                "filename": getattr(event, "filename", None),
                "inputs": getattr(event, "inputs", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTrainCompletedEvent)
        def on_crew_train_completed(source: Crew, event: CrewTrainCompletedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "n_iterations": getattr(event, "n_iterations", None),
                "filename": getattr(event, "filename", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTrainFailedEvent)
        def on_crew_train_failed(source: Crew, event: CrewTrainFailedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "error": getattr(event, "error", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTestStartedEvent)
        def on_crew_test_started(source: Crew, event: CrewTestStartedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "n_iterations": getattr(event, "n_iterations", None),
                "eval_llm": getattr(event, "eval_llm", None),
                "inputs": getattr(event, "inputs", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTestCompletedEvent)
        def on_crew_test_completed(source: Crew, event: CrewTestCompletedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTestFailedEvent)
        def on_crew_test_failed(source: Crew, event: CrewTestFailedEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "error": getattr(event, "error", None),
            }
            self._push(payload)

        @crewai_event_bus.on(CrewTestResultEvent)
        def on_crew_test_result(source: Crew, event: CrewTestResultEvent):
            payload = {
                "type": event.type,
                "crew_name": event.crew_name,
                "quality": getattr(event, "quality", None),
                "execution_duration": getattr(event, "execution_duration", None),
                "model": getattr(event, "model", None),
            }
            self._push(payload)
