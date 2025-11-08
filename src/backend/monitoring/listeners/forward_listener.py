import asyncio
from datetime import datetime
from typing import Any
from crewai.events import BaseEventListener

class ForwardingListener(BaseEventListener):
    """Base forwarding listener that delegates registration to per-group listener classes.

    pushes normalized payloads into the shared asyncio.Queue.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__()
        self._loop = loop
        self._queue = queue

    @staticmethod
    def _serialize(obj: Any) -> Any:
        """Recursively serialize datetime and other non-JSON-serializable objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: ForwardingListener._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [ForwardingListener._serialize(item) for item in obj]
        # Check if object is a basic JSON-serializable type
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        # For anything else (custom objects, TokenCalcHandler, etc.), convert to string
        else:
            return str(obj)

    def _push(self, payload: dict) -> None:
        try:
            # Serialize any datetime objects in the payload
            serialized = self._serialize(payload)
            self._loop.call_soon_threadsafe(self._queue.put_nowait, serialized)
        except Exception as e:
            print(f"[listener] Failed to enqueue event: {e}")