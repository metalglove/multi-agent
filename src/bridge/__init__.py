"""Bridge package: optional infrastructure to relay events from runners to frontends.

The bridge listens to a Redis channel (from runners) and broadcasts messages
to connected WebSocket clients (frontends). This is a separate concern from
the runner and allows decoupled scaling of multiple runners with multiple frontends.

Exports:
 - app: FastAPI application (run with: uvicorn src.bridge.app:app)
"""

from .app import app

__all__ = ["app"]
