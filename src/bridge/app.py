"""FastAPI bridge server: WebSocket endpoint + Redis subscriber.

This server bridges CrewAI events published to Redis (by runners) and streams them
to connected WebSocket clients (frontends). It is an optional infrastructure component
that enables decoupling of runners from frontends.
"""
import asyncio
import json
import os
from typing import Set
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

import redis.asyncio as aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to initialize and cleanup Redis subscriber."""
    redis_task = None
    redis_client = None
    try:
        async def _redis_subscriber(manager: "ConnectionManager", redis_url: str, channel: str):
            """Subscribe to Redis channel and broadcast received messages to connected WebSocket clients."""
            client = aioredis.from_url(redis_url)
            pubsub = client.pubsub()
            await pubsub.subscribe(channel)
            print(f"[bridge] subscribed to Redis channel '{channel}' at {redis_url}")
            try:
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                    if not message:
                        await asyncio.sleep(0.1)
                        continue
                    # Parse Redis pub/sub message format
                    data = message.get("data")
                    if isinstance(data, (bytes, bytearray)):
                        data = data.decode("utf-8")
                    try:
                        payload = json.loads(data)
                    except Exception as e:
                        print(f"[bridge] failed to parse message as JSON: {e}; raw={data}")
                        continue
                    await manager.broadcast(payload)
            finally:
                try:
                    await pubsub.unsubscribe(channel)
                except Exception:
                    pass
                try:
                    await client.close()
                except Exception:
                    pass

        redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        redis_channel = os.getenv("REDIS_CHANNEL", "crewai:events")
        redis_client = aioredis.from_url(redis_url)
        # Start subscriber as a background task
        redis_task = asyncio.create_task(_redis_subscriber(manager, redis_url, redis_channel))
        print("[bridge] Redis subscriber started")
    except Exception as e:
        print(f"[bridge] Redis subscriber setup failed: {e}")

    try:
        yield
    finally:
        # Cleanup
        if redis_task:
            try:
                redis_task.cancel()
            except Exception:
                pass
        if redis_client:
            try:
                await redis_client.close()
            except Exception:
                pass


app = FastAPI(title="CrewAI Event Bridge", lifespan=lifespan)

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    """Manages WebSocket connections and broadcasts messages to all connected clients."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected WebSocket clients."""
        if not self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"[bridge] error sending message: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections.discard(connection)


manager = ConnectionManager()


@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event streaming from Redis."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive; clients may send ping/pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("[bridge] WebSocket client disconnected")
    except Exception as e:
        print(f"[bridge] WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "connected_clients": len(manager.active_connections),
    }


@app.get("/api/config")
async def get_config():
    """Return bridge configuration (frontend can use to customize behavior)."""
    return {
        "ws_url": os.getenv("WS_URL", "ws://localhost:8000/ws/events"),
        "redis_channel": os.getenv("REDIS_CHANNEL", "crewai:events"),
    }


@app.post("/api/test-event")
async def send_test_event(payload: dict | None = None):
    """Send a test event to all connected WebSocket clients (for diagnostics)."""
    message = {
        "type": "test_event",
        "timestamp": str(asyncio.get_event_loop().time()),
        "payload": payload or {"msg": "hello from bridge test-event"},
    }
    await manager.broadcast(message)
    return {"status": "ok", "sent": message}


# Optionally serve static files (Vue build output) if present
if os.path.exists("src/frontend/dist"):
    app.mount("/", StaticFiles(directory="src/frontend/dist", html=True), name="static")


if __name__ == "__main__":
    port = int(os.getenv("BRIDGE_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
