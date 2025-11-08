import asyncio

from crewai.mcp.client import MCPClient
from crewai.events.types.mcp_events import (
    MCPConnectionCompletedEvent,
    MCPToolExecutionStartedEvent,
    MCPToolExecutionFailedEvent,
    MCPConnectionFailedEvent,
    MCPConnectionStartedEvent,
    MCPToolExecutionCompletedEvent,
)

from .forward_listener import ForwardingListener
from crewai.events.event_bus import CrewAIEventsBus

class MCPListener(ForwardingListener):
    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__(loop, queue)

    def setup_listeners(self, crewai_event_bus: CrewAIEventsBus) -> None:
        @crewai_event_bus.on(MCPConnectionStartedEvent)
        def on_mcp_conn_started(source: MCPClient, event: MCPConnectionStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "server_url": getattr(event, "server_url", None),
                "transport_type": getattr(event, "transport_type", None),
                "connect_timeout": getattr(event, "connect_timeout", None),
                "is_reconnect": getattr(event, "is_reconnect", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MCPConnectionCompletedEvent)
        def on_mcp_conn_completed(source: MCPClient, event: MCPConnectionCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "server_url": getattr(event, "server_url", None),
                "connection_duration_ms": getattr(event, "connection_duration_ms", None),
                "is_reconnect": getattr(event, "is_reconnect", None),
                "started_at": getattr(event, "started_at", None),
                "completed_at": getattr(event, "completed_at", None),
                "agent_id": getattr(event, "agent_id", None),
                "agent_role": getattr(event, "agent_role", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MCPConnectionFailedEvent)
        def on_mcp_conn_failed(source: MCPClient, event: MCPConnectionFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "server_url": getattr(event, "server_url", None),
                "error": getattr(event, "error", None),
                "error_type": getattr(event, "error_type", None),
                "started_at": getattr(event, "started_at", None),
                "failed_at": getattr(event, "failed_at", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MCPToolExecutionStartedEvent)
        def on_mcp_tool_started(source: MCPClient, event: MCPToolExecutionStartedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "tool_name": getattr(event, "tool_name", None),
                "tool_args": getattr(event, "tool_args", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MCPToolExecutionCompletedEvent)
        def on_mcp_tool_completed(source: MCPClient, event: MCPToolExecutionCompletedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "tool_name": getattr(event, "tool_name", None),
                "tool_args": getattr(event, "tool_args", None),
                "result": getattr(event, "result", None),
                "execution_duration_ms": getattr(event, "execution_duration_ms", None),
            }
            self._push(payload)

        @crewai_event_bus.on(MCPToolExecutionFailedEvent)
        def on_mcp_tool_failed(source: MCPClient, event: MCPToolExecutionFailedEvent):
            payload = {
                "type": event.type,
                "timestamp": getattr(event, "timestamp", None),
                "server_name": getattr(event, "server_name", None),
                "tool_name": getattr(event, "tool_name", None),
                "tool_args": getattr(event, "tool_args", None),
                "error": getattr(event, "error", None),
                "error_type": getattr(event, "error_type", None),
                "started_at": getattr(event, "started_at", None),
                "failed_at": getattr(event, "failed_at", None),
            }
            self._push(payload)
