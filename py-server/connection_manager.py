import aiohttp
import asyncio
from event_manager import EventType

class ConnectionManager:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.connections = {}  # This will store player_id: Player pairs

    def register(self, player=None, world=None):
        if player:
            self.connections[player.player_id] = player
            # Subscribe the player to events
            self.event_manager.subscribe(EventType.PLAYER_LOC, player.send_event)
            self.event_manager.subscribe(EventType.PLAYER_HEALTH, player.send_event)
            self.event_manager.subscribe(EventType.PLAYER_ABILITIES, player.send_event)
            self.event_manager.subscribe(EventType.PLAYER_AP, player.send_event)
        if world:
            self.event_manager.subscribe(EventType.PLAYER_AP_USAGE, world.handle_ap_update)

    def unregister(self, player):
        # Unsubscribe the player from all events
        for event_type in EventType:
            self.event_manager.unsubscribe(event_type, player.send_event)
        # Remove the player from connections
        del self.connections[player.player_id]

    async def send_personal_message(self, message, player_id):
        player = self.connections.get(player_id)
        if player and player.websocket:
            await player.websocket.send(message)

    async def broadcast(self, message):
        # Using asyncio.gather to send concurrently
        await asyncio.gather(*(player.websocket.send(message) for player in self.connections.values() if player.websocket))


# This function would ideally be an async call to your auth server to validate the session token
async def validate_session(token):
    async with aiohttp.ClientSession() as session:
        headers = {'x-access-token': token}
        async with session.get('http://127.0.0.1:5000/validate', headers=headers) as response:
            print(response.text)
            if response.status == 200:
                # Parse the response as JSON and extract the user_id
                user_data = await response.json()
                user_id = user_data.get('user_id')
                return (True, user_id)
            else:
                return (False, None)