"""Redis forwarder: publishes JSON messages from an asyncio.Queue to a Redis channel.

Uses the `redis.asyncio` client. The queue should yield dict-like messages which
will be JSON-serialized. Sending `None` signals shutdown.
"""
from typing import Any
import asyncio
import json

import redis.asyncio as aioredis

async def redis_forwarder(queue: asyncio.Queue, redis_url: str, channel: str):
    """Continuously publish messages from the queue to redis channel.

    Retries on connection failure with exponential backoff.
    """
    backoff = 1
    while True:
        try:
            client = aioredis.from_url(redis_url)
            # Test connection
            await client.ping()
            print(f"[forwarder] Connected to Redis at {redis_url}, publishing on '{channel}'")
            backoff = 1
            while True:
                msg = await queue.get()
                if msg is None:
                    # Shutdown signal
                    await client.close()
                    return
                try:
                    await client.publish(channel, json.dumps(msg))
                except Exception as e:
                    print(f"[forwarder] Error publishing to Redis, will reconnect: {e}")
                    # Re-enqueue and break to reconnect
                    await queue.put(msg)
                    break
        except Exception as e:
            print(f"[forwarder] Redis connection/publish failed: {e}; retrying in {backoff}s")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)


def start_loop_in_thread(loop: asyncio.AbstractEventLoop, coro: Any) -> Any:
    """Run coro (an awaitable) on loop in a new daemon thread and return the thread.

    This helper sets the event loop and runs until the coroutine completes.
    """
    import threading

    def _run():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coro)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t
