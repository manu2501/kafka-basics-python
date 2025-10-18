import asyncio
import json
from typing import Dict, List

# naive in-memory pubsub per user id
_listeners: Dict[int, List[asyncio.Queue]] = {}


def subscribe(user_id: int) -> asyncio.Queue:
    queue: asyncio.Queue = asyncio.Queue()
    _listeners.setdefault(user_id, []).append(queue)
    return queue


def unsubscribe(user_id: int, queue: asyncio.Queue) -> None:
    queues = _listeners.get(user_id)
    if not queues:
        return
    try:
        queues.remove(queue)
    except ValueError:
        pass
    if not queues:
        _listeners.pop(user_id, None)


def publish(user_id: int, data: dict) -> None:
    queues = _listeners.get(user_id, [])
    for q in list(queues):
        try:
            q.put_nowait(data)
        except asyncio.QueueFull:
            pass
