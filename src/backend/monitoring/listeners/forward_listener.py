import asyncio
from crewai.events import BaseEventListener

class ForwardingListener(BaseEventListener):
    """Base forwarding listener that delegates registration to per-group listener classes.

    pushes normalized payloads into the shared asyncio.Queue.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue):
        super().__init__()
        self._loop = loop
        self._queue = queue

    def _push(self, payload: dict) -> None:
        try:
            self._loop.call_soon_threadsafe(self._queue.put_nowait, payload)
        except Exception as e:
            print(f"[listener] Failed to enqueue event: {e}")