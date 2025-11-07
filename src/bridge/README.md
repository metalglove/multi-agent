# Bridge: Event Relay Infrastructure

The bridge is an **optional** infrastructure component that relays CrewAI events published to Redis by runners to connected WebSocket clients (frontends).

## Why separate?

- **Runners** (`src/backend/`) emit events to Redis and execute Crew workflows. They are the core concern.
- **Bridge** (`src/bridge/`) is infrastructure for local development or when you want decoupled frontend/runner scaling. It's not required.

## When to use the bridge

- **Development**: Running a single runner + frontend locally with Redis pub/sub transport.
- **Multiple frontends**: Multiple frontends subscribed to the same runner's events.
- **Decoupling**: Runners and frontends run independently; bridge relays events.

## When you don't need the bridge

- If you run a WebSocket server directly in the runner process (runner-hosted option).
- If you use a managed realtime service (Pusher, Ably, etc.) directly.

## Quick start

1. Ensure Redis is running:
   ```bash
   docker run -p 6379:6379 --name local-redis -d redis:7
   ```

2. Start the bridge:
   ```powershell
   uvicorn src.bridge.app:app --host 127.0.0.1 --port 8000 --reload
   ```

3. Start a runner:
   ```powershell
   python -m src.backend.runner_with_monitoring
   ```

4. Frontend connects to `ws://127.0.0.1:8000/ws/events` and receives forwarded events.

## Configuration

- `REDIS_URL`: Redis connection string (default: `redis://127.0.0.1:6379/0`)
- `REDIS_CHANNEL`: Redis channel to subscribe to (default: `crewai:events`)
- `BRIDGE_PORT`: Port to run the bridge on (default: `8000`)

## Architecture diagram

```
┌─────────────┐                      ┌─────────────┐
│   Runner    │ --Redis pub/sub--→  │   Bridge    │
│  (backend)  │    (crewai:events)  │   (bridge)  │
└─────────────┘                      └─────────────┘
                                           │
                                           │ WebSocket
                                           ↓
                                    ┌─────────────┐
                                    │  Frontend   │
                                    │  (browser)  │
                                    └─────────────┘
```
