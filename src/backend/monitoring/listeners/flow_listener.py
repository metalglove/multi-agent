from typing import Any
import asyncio

from crewai.flow.flow import Flow
from crewai.events.types.flow_events import (
    FlowStartedEvent,
    FlowCreatedEvent,
    FlowFinishedEvent,
    FlowPlotEvent,
    MethodExecutionFailedEvent,
    MethodExecutionFinishedEvent,
    MethodExecutionStartedEvent,
)

from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class FlowListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(FlowStartedEvent)
        def on_flow_started(source: Flow, event: FlowStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "inputs": getattr(event, "inputs", None),
            }
            self._push(payload)

        @crewai_event_bus.on(FlowCreatedEvent)
        def on_flow_created(source: Flow, event: FlowCreatedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
            }
            self._push(payload)

        @crewai_event_bus.on(FlowFinishedEvent)
        def on_flow_finished(source: Flow, event: FlowFinishedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "result": getattr(event, "result", None),
            }
            self._push(payload)

        @crewai_event_bus.on(FlowPlotEvent)
        def on_flow_plot(source: Flow, event: FlowPlotEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "meta": {k: v for k, v in getattr(event, "__dict__", {}).items() if k not in ("type", "timestamp", "flow_name")},
            }
            self._push(payload)

        @crewai_event_bus.on(MethodExecutionStartedEvent)
        def on_method_exec_started(source: Flow, event: MethodExecutionStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "method_name": getattr(event, "method_name", None),
                "state": getattr(event, "state", None),
                "params": getattr(event, "params", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MethodExecutionFinishedEvent)
        def on_method_exec_finished(source: Flow, event: MethodExecutionFinishedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "method_name": getattr(event, "method_name", None),
                "result": getattr(event, "result", None),
                "state": getattr(event, "state", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MethodExecutionFailedEvent)
        def on_method_exec_failed(source: Flow, event: MethodExecutionFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "flow_name": getattr(event, "flow_name", None),
                "method_name": getattr(event, "method_name", None),
                "error": getattr(event, "error", None),
            }
            self._push(payload)
