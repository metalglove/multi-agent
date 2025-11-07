"""
FastAPI server for streaming CrewAI events to Vue frontend via WebSockets
"""
import asyncio
import json
from typing import Set
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

from crewai.events import BaseEventListener, crewai_event_bus
from crewai.events import (
    AgentReasoningStartedEvent,
    AgentReasoningCompletedEvent,
    AgentReasoningFailedEvent,
    TaskStartedEvent,
    TaskCompletedEvent,
    TaskFailedEvent,
)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to initialize and cleanup resources on startup/shutdown."""
    # Setup event listeners when server starts
    event_listener.setup_listeners(crewai_event_bus)
    print("Event listeners initialized")
    try:
        yield
    finally:
        # TODO: add cleanup logic here if crewai_event_bus supports unregistering listeners
        pass


app = FastAPI(title="CrewAI Event Server", lifespan=lifespan)

# CORS configuration for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track connected WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast event to all connected clients"""
        if not self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections.discard(connection)

manager = ConnectionManager()

# Event listener that broadcasts to WebSocket clients
class WebSocketEventListener(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(AgentReasoningStartedEvent)
        async def on_reasoning_started(source, event):
            message = {
                "type": "agent_reasoning_started",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "agent_role": event.agent.role if hasattr(event.agent, 'role') else str(event.agent),
                "agent_name": event.agent.name if hasattr(event.agent, 'name') else "Unknown",
            }
            await manager.broadcast(message)
            print(f"[EVENT] Agent reasoning started: {message['agent_role']}")
        
        @crewai_event_bus.on(AgentReasoningCompletedEvent)
        async def on_reasoning_completed(source, event):
            message = {
                "type": "agent_reasoning_completed",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "reasoning_plan": str(event.reasoning_plan) if hasattr(event, 'reasoning_plan') else "N/A",
                "agent_role": event.agent.role if hasattr(event.agent, 'role') else str(event.agent),
            }
            await manager.broadcast(message)
            print(f"[EVENT] Agent reasoning completed")
        
        @crewai_event_bus.on(AgentReasoningFailedEvent)
        async def on_reasoning_failed(source, event):
            message = {
                "type": "agent_reasoning_failed",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "error": str(event.error) if hasattr(event, 'error') else "Unknown error",
                "agent_role": event.agent.role if hasattr(event.agent, 'role') else str(event.agent),
            }
            await manager.broadcast(message)
            print(f"[EVENT] Agent reasoning failed: {message['error']}")
        
        @crewai_event_bus.on(TaskStartedEvent)
        async def on_task_started(source, event):
            message = {
                "type": "task_started",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "task_title": event.task.title if hasattr(event.task, 'title') else str(event.task),
                "task_description": event.task.description if hasattr(event.task, 'description') else "N/A",
            }
            await manager.broadcast(message)
            print(f"[EVENT] Task started: {message.get('task_title')}")
        
        @crewai_event_bus.on(TaskCompletedEvent)
        async def on_task_completed(source, event):
            message = {
                "type": "task_completed",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "task_title": event.task.title if hasattr(event.task, 'title') else str(event.task),
                "task_output": str(event.task_output)[:500] if hasattr(event, 'task_output') else "N/A",  # Truncate long outputs
            }
            await manager.broadcast(message)
            print(f"[EVENT] Task completed: {message.get('task_title')}")
        
        @crewai_event_bus.on(TaskFailedEvent)
        async def on_task_failed(source, event):
            message = {
                "type": "task_failed",
                "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None,
                "task_title": event.task.title if hasattr(event.task, 'title') else str(event.task),
                "error": str(event.error) if hasattr(event, 'error') else "Unknown error",
            }
            await manager.broadcast(message)
            print(f"[EVENT] Task failed: {message.get('task_title')}")

# Initialize the event listener
event_listener = WebSocketEventListener()

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back or handle commands from client
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "connected_clients": len(manager.active_connections)
    }

@app.get("/api/config")
async def get_config():
    """Get server configuration for frontend"""
    return {
        "ws_url": os.getenv("WS_URL", "ws://localhost:8000/ws/events"),
        "api_base_url": os.getenv("API_BASE_URL", "http://localhost:8000"),
    }

# Serve static files (Vue build output)
if os.path.exists("src/frontend/dist"):
    app.mount("/", StaticFiles(directory="src/frontend/dist", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
