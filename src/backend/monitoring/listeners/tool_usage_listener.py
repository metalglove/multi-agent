from typing import Any
import asyncio

from crewai import LLM
from crewai.tools.tool_usage import ToolUsage
from crewai.llms.base_llm import BaseLLM
from crewai.events.types.tool_usage_events import (
    ToolUsageStartedEvent,
    ToolUsageErrorEvent,
    ToolUsageFinishedEvent,
    ToolSelectionErrorEvent,
    ToolExecutionErrorEvent,
)

from forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class ToolUsageListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(ToolUsageStartedEvent)
        def on_tool_usage_started(source: ToolUsage | BaseLLM | LLM, event: ToolUsageStartedEvent):
            payload = {
                "type": event.type,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "timestamp": event.timestamp,

                "tool_name": event.tool_name,
                "tools_args": event.tool_args,
            }

            if isinstance(source, BaseLLM) or isinstance(source, LLM):
                payload["llm_name"] = getattr(source, "model", None)

            if isinstance(source, ToolUsage):
                payload["tool_class"] = getattr(event, "tool_class", None)

            self._push(payload)

        @crewai_event_bus.on(ToolUsageErrorEvent)
        def on_tool_usage_error(source: ToolUsage | BaseLLM | LLM, event: ToolUsageErrorEvent):
            payload = {
                "type": event.type,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "timestamp": event.timestamp,

                "tool_name": event.tool_name,
                "tools_args": event.tool_args,
                "error": event.error,
            }

            if isinstance(source, BaseLLM) or isinstance(source, LLM):
                payload["llm_name"] = getattr(source, "model", None)

            if isinstance(source, ToolUsage):
                payload["tool_class"] = getattr(event, "tool_class", None)
                payload["delegations"] = getattr(event, "delegations", None)
                payload["run_attempts"] = getattr(event, "run_attempts", None)

            self._push(payload)

        @crewai_event_bus.on(ToolUsageFinishedEvent)
        def on_tool_usage_finished(source: ToolUsage | BaseLLM | LLM, event: ToolUsageFinishedEvent):
            payload = {
                "type": event.type,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "timestamp": event.timestamp,

                "started_at": getattr(event, "started_at", None),
                "finished_at": getattr(event, "finished_at", None),
                "from_cache": getattr(event, "from_cache", None),
                "tool_name": event.tool_name,
                "tool_args": event.tool_args,
                "output": getattr(event, "output", None),
            }
            if isinstance(source, BaseLLM) or isinstance(source, LLM):
                payload["llm_name"] = getattr(source, "model", None)

            if isinstance(source, ToolUsage):
                payload["tool_class"] = getattr(event, "tool_class", None)
                payload["delegations"] = getattr(event, "delegations", None)
                payload["run_attempts"] = getattr(event, "run_attempts", None)

            self._push(payload)

        @crewai_event_bus.on(ToolSelectionErrorEvent)
        def on_tool_selection_error(source: ToolUsage | BaseLLM | LLM, event: ToolSelectionErrorEvent):
            payload = {
                "type": event.type,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "timestamp": event.timestamp,

                "error": getattr(event, "error", None),
                "tool_name": getattr(event, "tool_name", None),
                "tool_args": getattr(event, "tool_args", None),
                "tool_class": getattr(event, "tool_class", None),
            }

            self._push(payload)

        @crewai_event_bus.on(ToolExecutionErrorEvent)
        def on_tool_execution_error(source: ToolUsage | BaseLLM | LLM, event: ToolExecutionErrorEvent):
            payload = {
                "type": event.type,
                "agent_id": event.agent_id,
                "agent_role": event.agent_role,
                "task_id": event.task_id,
                "task_name": event.task_name,
                "timestamp": event.timestamp,

                "error": getattr(event, "error", None),
                "tool_name": getattr(event, "tool_name", None),
                "tool_args": getattr(event, "tool_args", None),
                "tool_class": getattr(event, "tool_class", None),
            }

            self._push(payload)
