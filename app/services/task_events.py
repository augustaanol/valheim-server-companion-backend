import asyncio
from typing import Set


class TaskEventManager:
    def __init__(self):
        self.connections: Set[asyncio.Queue] = set()

    async def connect(self):
        queue = asyncio.Queue()
        self.connections.add(queue)
        return queue

    def disconnect(self, queue: asyncio.Queue):
        self.connections.discard(queue)

    async def notify(self, message: str):
        for queue in list(self.connections):
            await queue.put(message)


task_events = TaskEventManager()
