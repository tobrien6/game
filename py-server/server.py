"""
Note: server should always generate subsequent state, and then check if it's a legal state.
This is easier than having a set of checks for every possible action.
"""

import asyncio
import websockets
import json
import random
from typing import Dict
from datetime import datetime, timedelta
from connection_manager import ConnectionManager, validate_session
from player import Player
from world import WorldState, WorldGrid
from rules_engine import RulesEngine
from game_engine import GE
from database import create_tables, get_player
from event_manager import EventManager, EventQueue, EventType

event_queue = EventQueue()
event_manager = EventManager()
connection_manager = ConnectionManager(event_manager)

world_grid = WorldGrid()
world = WorldState(world_grid, event_queue)

rules_engine = RulesEngine("CLIPS_rules.txt")
ge = GE(world, rules_engine, event_queue)

create_tables()


async def process_events():
    while True:
        event = await event_queue.get_event()
        await event_manager.broadcast(event['type'], event['data'])


async def handler(websocket, path):
    player = None
    #try:
    # Wait for the first message, which should contain the auth token
    auth_message = await websocket.recv()
    auth_data = json.loads(auth_message)
    token = auth_data.get('token')
    if not token:
        await websocket.close(reason='Authentication token not received')
        return

    is_valid_session, user_id = await validate_session(token)
    if not is_valid_session:
        await websocket.close(reason='Authentication failed')
        return

    # Load or create a new player for this user
    player_data = get_player(user_id)
    if not player_data:  # user has no characters yet -- for now just create one
        player_name = f"player_{''.join(random.choices('0123456789', k=5))}"
        player = Player.create_new_player(user_id, player_name, websocket)
    else:
        player = Player(websocket=websocket, **player_data)

    print(f"player logged in and ready: {player.player_id}")    
    
    # Register the player with the connection manager
    connection_manager.register(player)
    await world.add_player(player)

    # Main game loop for the WebSocket connection
    try:
        while True:
            message = await websocket.recv()
            print(f"received message: {json.loads(message)} for player {player.player_id}")
            await process_game_message(message, player)
    except websockets.exceptions.ConnectionClosed as e:
        print(e)
        # Clean up when the connection drops
        if player:
            player.save()
            connection_manager.unregister(player)
            print(f"connection lost for user: {player.player_id}")
    except Exception as e:
        if player:
            print(e)
            player.save()
            print(f"error for user {player.player_id}: {e}")


async def process_game_message(message, player):
    data = json.loads(message)
    print("received: " + str(data))

    if data['action'] == 'MovePlayerToTile':
        player_id = player.player_id
        tile_xy = data['tile_xy']
        try:
            await world.move_player_to_tile(player_id, tile_xy)
        except ValueError as e:
            await player.websocket.send(json.dumps({"action": "Error", "message": str(e)}))
        except KeyError as e:
            await player.websocket.send(json.dumps({"action": "Error", "message": "Player not found"}))

    if data['action'] == 'GetChunk':
        print(data)
        chunk = await world.get_chunk((data['x'], data['y']))
        # Send the chunk data back to the client
        await player.websocket.send(json.dumps(chunk))

    if data['action'] == 'UseTargetedAbility':
        ability_name = data['ability_name']
        x = data['x']
        y = data['y']
        print(player.abilities.items())
        try:
            await ge.use_ability(ability_name, player, (x,y), world, charge=False)
        except Exception as e:
            await player.websocket.send(json.dumps({"action": "Error", "message": str(e)}))

    if data['action'] == 'InitializePlayer':
        print(data)
        # Gather the locations of all other players
        other_players = [
            {"player_id": p.player_id,
             "x": p.x,
             "y": p.y,
             "health": p.health}
            for p in world.players.values() if p.player_id != player.player_id
        ]
        # Send initialization data including other players' locations
        resp = {
            "action": "InitializePlayer", 
            "player_id": player.player_id,
            "x": player.x,
            "y": player.y,
            "health": player.health,
            "other_players": other_players  # Add this line to include other players' locations
        }
        await player.websocket.send(json.dumps(resp))

# Server setup
async def main():
    asyncio.create_task(process_events())
    async with websockets.serve(handler, "localhost", 6789):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
