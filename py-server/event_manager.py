import asyncio
from enum import Enum


class EventQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def put_event(self, event):
        await self.queue.put(event)

    async def get_event(self):
        return await self.queue.get()


class EventType(Enum):
    PLAYER_MOVED = "PlayerMoved"
    # Define other event types as necessary


class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    async def broadcast(self, event_type, data):
        if event_type in self.listeners:
            coroutines = [listener(data) for listener in self.listeners[event_type]]
            await asyncio.gather(*coroutines)