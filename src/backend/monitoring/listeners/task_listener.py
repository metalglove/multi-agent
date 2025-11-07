from typing import Any
import asyncio

from crewai import Task, TaskOutput
from crewai.events.types.task_events import (
    TaskStartedEvent,
    TaskCompletedEvent,
    TaskFailedEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class TaskListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(TaskStartedEvent)
        def on_task_started(source: Task, event: TaskStartedEvent):
            payload = {
                "type": event.type,
                "start_time": source.start_time,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_title": source.name,
                "task": source.description,
                "prompt_context": getattr(source, "prompt_context", None),
            }
            self._push(payload)

        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source: Task, event: TaskCompletedEvent):
            to: TaskOutput = event.task_output
            payload = {
                "type": event.type,
                "start_time": source.start_time,
                "end_time": source.end_time,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_title": source.name,
                "task": source.description,
                "output": to.to_dict() if hasattr(to, "to_dict") else str(to),
                "prompt_context": getattr(source, "prompt_context", None),
            }
            self._push(payload)

        @crewai_event_bus.on(TaskFailedEvent)
        def on_task_failed(source: Task, event: TaskFailedEvent):
            payload = {
                "type": event.type,
                "start_time": getattr(source, "start_time", None),
                "end_time": getattr(source, "end_time", None),
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_title": getattr(source, "name", None),
                "task": getattr(source, "description", None),
                "error": getattr(event, "error", None),
            }
            self._push(payload)
