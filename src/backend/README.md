# Backend Runner

The backend is the core concern of the system: executing CrewAI workflows and publishing events to Redis pub/sub for consumption by optional bridge services or other subscribers.

## Structure

```
src/backend/
├── core/                           # CrewAI workflow definitions
│   ├── agents.py                   # Agent definitions and AgentManager
│   ├── tasks.py                    # Task definitions and TaskManager
│   ├── tools.py                    # Tool definitions
│   ├── models.py                   # Data models
│   ├── artifacts.py                # Artifact output handling
│   └── __init__.py
├── monitoring/                     # Event monitoring and forwarding
│   ├── orchestrator.py             # Main entry point (run_with_monitoring)
│   ├── listener.py                 # ForwardingListener (in-process event listener)
│   ├── forwarder.py                # Redis publisher coroutine
│   └── __init__.py
├── runner_with_monitoring.py       # Entry point for python -m invocation
├── requirements.txt                # Python dependencies
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Redis server running (or use docker-compose)

### Installation

```bash
# Install dependencies
pip install -r src/backend/requirements.txt
```

### Running the Runner

```bash
# With environment variables
export REDIS_URL=redis://127.0.0.1:6379/0
export REDIS_CHANNEL=crewai:events
export OPENAI_API_KEY=sk-...
python -m src.backend.runner_with_monitoring

# Or from root with python module invocation
python -m src.backend.runner_with_monitoring
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://127.0.0.1:6379/0` | Redis connection string |
| `REDIS_CHANNEL` | `crewai:events` | Redis pub/sub channel for events |
| `CREW_OUTPUT_FOLDER` | `outputs` | Folder for Crew output artifacts |
| `OPENAI_MODEL_NAME` | `openai/qwen/qwen3-4b-2507` | LLM model to use |
| `OPENAI_API_BASE` | `http://localhost:1234/v1` | LLM API base URL |
| `OPENAI_API_KEY` | `not-needed` | LLM API key (for remote models) |

## Architecture

### Event Flow

```
┌──────────────────────┐
│  CrewAI Workflow     │
│  (agents + tasks)    │
└──────────┬───────────┘
           │
           │ emits events
           ▼
┌──────────────────────┐
│ ForwardingListener   │ (in-process event listener)
│ (core/events)        │
└──────────┬───────────┘
           │
           │ enqueues payloads
           ▼
┌──────────────────────┐
│ asyncio.Queue        │ (thread-safe IPC)
└──────────┬───────────┘
           │
           │ publishes JSON
           ▼
┌──────────────────────┐
│ Redis Forwarder      │ (async pub/sub publisher)
│ (monitoring/         │
│  forwarder.py)       │
└──────────┬───────────┘
           │
           │ publishes to channel
           ▼
┌──────────────────────┐
│ Redis Pub/Sub        │ (crewai:events channel)
│ (external consumers) │
└──────────────────────┘
```

### Concurrency Model

The runner uses three threads:

1. **Main Thread**: Orchestrates startup and shutdown
2. **Asyncio Event Loop Thread**: Runs the Redis forwarder coroutine
3. **Worker Thread**: Executes crew.kickoff() (blocking operation)

This allows the event listener (running in the worker thread) to safely push events to the asyncio queue using `loop.call_soon_threadsafe()`.

## Components

### Core Module (`core/`)

Defines CrewAI agents, tasks, tools, and models:

- **agents.py**: Agent definitions and AgentManager for lifecycle management
- **tasks.py**: Task definitions and TaskManager
- **tools.py**: Tool integrations (MCP adapters, etc.)
- **models.py**: Pydantic data models for serialization
- **artifacts.py**: Output artifact handling and file storage

### Monitoring Module (`monitoring/`)

Handles event forwarding and monitoring:

- **orchestrator.py**: Main entry point `run_with_monitoring()` that wires all components
- **listener.py**: `ForwardingListener` class that registers CrewAI event handlers
- **forwarder.py**: `redis_forwarder()` coroutine that publishes events to Redis with reconnection/backoff

### Entry Point (`runner_with_monitoring.py`)

Simple shim that imports and calls `run_with_monitoring()` for `python -m` invocation.

## Development

### Running Locally (No Docker)

```bash
# Terminal 1: Start Redis
docker run -p 6379:6379 redis:7-alpine
# Or: redis-server

# Terminal 2: Run the runner
export REDIS_URL=redis://127.0.0.1:6379/0
python -m src.backend.runner_with_monitoring
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Debugging

Monitor events being published to Redis:

```bash
# In a separate terminal
redis-cli SUBSCRIBE crewai:events

# You should see events like:
# {
#   "type": "agent_reasoning_started",
#   "agent": "research_agent",
#   "timestamp": "2024-11-07T..."
# }
```

## Performance Considerations

1. **Event Queue Size**: Events are queued in memory; large workflows may need queue size tuning
2. **Redis Connection**: Uses connection pooling; adjust pool size for high-throughput scenarios
3. **Thread Safety**: ForwardingListener uses `loop.call_soon_threadsafe()` for thread-safe event pushing
4. **Backoff**: Redis forwarder uses exponential backoff on connection failure

## Troubleshooting

### Runner Won't Start

```bash
# Check Redis is running
redis-cli ping
# Expected: PONG

# Check Python dependencies
pip check

# Check REDIS_URL environment variable
echo $REDIS_URL
```

### Events Not Publishing

```bash
# Monitor Redis channel
redis-cli SUBSCRIBE crewai:events

# Check runner logs for forwarder errors
# Look for "[forwarder]" log messages
```

### High Memory Usage

- Monitor crew execution; large workflows may accumulate artifacts
- Check `outputs/` folder for large generated files
- Consider clearing artifacts between runs: `rm -rf outputs/*`

## Integration with Bridge

The runner publishes to Redis; optional bridge service subscribes:

```bash
# Terminal 1: Redis (Docker)
docker run -p 6379:6379 redis:7-alpine

# Terminal 2: Runner (local)
python -m src.backend.runner_with_monitoring

# Terminal 3: Bridge (Docker) - optional
docker-compose up -d bridge

# Terminal 4: Frontend (Docker) - optional
docker-compose up -d frontend
```

The bridge and frontend are optional; runners can publish to Redis and other subscribers can consume events directly.

## Related Files

- [Docker Setup Guide](../../docs/DOCKER_GETTING_STARTED.md)
- [Architecture Guide](../../docs/ARCHITECTURE.md)
- [Bridge Documentation](../bridge/README.md)

