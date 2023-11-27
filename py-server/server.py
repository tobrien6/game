"""
Note: server should always generate subsequent state, and then check if it's a legal state.
This is easier than having a set of checks for every possible action.
"""


import asyncio
import websockets
import json
import random
from enum import Enum
from typing import Dict
from datetime import datetime, timedelta
from connection_manager import ConnectionManager
import aiohttp
import functools
from player import Player
from database import create_table, get_player

CHUNK_SIZE = 64

connection_manager = ConnectionManager()
create_table()

# Helper functions
def get_chunk_coords(x, y, chunk_size=CHUNK_SIZE):
    """Convert world coordinates to chunk coordinates."""
    return x // chunk_size, y // chunk_size

# Enums and class definitions would go here...
class TerrainType(Enum):
    Grass = 1
    Mountain = 2
    Water = 3
    Forest = 4
    Tree = 5
    # Additional terrain types...

class Tile:
    def __init__(self, terrain_type=TerrainType.Grass, is_occupied=False):
        self.terrain = terrain_type
        self.is_occupied = is_occupied

class Chunk:
    def __init__(self):
        self.tiles = []
        # Loop through each tile once to determine its terrain type
        for x in range(CHUNK_SIZE):
            row = []
            for y in range(CHUNK_SIZE):
                # Randomly decide if the tile is a tree or grass
                terrain_type = TerrainType.Tree if random.random() < 0.05 else TerrainType.Grass
                row.append(Tile(terrain_type=terrain_type))
            self.tiles.append(row)

    def get_tiles(self):
        return self.tiles

class WorldGrid:
    def __init__(self, world_grid, chunk_size=64):
        self.players = {}
        self.world_grid = world_grid
        self.chunk_size = chunk_size
        self.chunks = {}

    def load_chunk(self, chunk_coords):
        if chunk_coords not in self.chunks:
            # If the chunk doesn't exist, generate it and store it in self.chunks
            print("generating new chunk")
            self.chunks[chunk_coords] = Chunk() 
        return self.chunks[chunk_coords]

    def is_move_valid(self, chunk_coords, local_x, local_y):
        # Check if the tile within the chunk is not occupied and is within valid terrain, etc.
        chunk = self.load_chunk(chunk_coords)
        return 0 <= local_x < self.chunk_size and 0 <= local_y < self.chunk_size and not chunk.tiles[local_x][local_y].is_occupied

    def update_tile(self, chunk_coords, local_x, local_y, occupied):
        # Update the occupation status of the tile within the specified chunk.
        chunk = self.load_chunk(chunk_coords)
        chunk.tiles[local_x][local_y].is_occupied = occupied


class WorldStateService:
    def __init__(self, world_grid):
        self.players = {}
        self.world_grid = world_grid

    async def get_chunk(self, chunk_coords):
        chunk = self.world_grid.load_chunk(chunk_coords)
        tiles_data = [[tile.terrain.value for tile in row] for row in chunk.tiles]
        print(f"returning chunk: {chunk_coords[0]}, {chunk_coords[1]}")
        return {
            'action': 'ChunkData',
            'chunk_x': chunk_coords[0],
            'chunk_y': chunk_coords[1],
            'tiles': tiles_data
        }

    async def add_player(self, player):
        self.players[player.player_id] = player

    #async def get_player(self, player_id):
    #    return self.players[player_id]

    async def move_player_to_tile(self, player_id, tile_xy):
        tile_x = tile_xy[0]
        tile_y = tile_xy[1]
        player = self.players.get(player_id)
        
        print(player)
        
        if player:
            # First, update the player's action points.
            player.update_action_points()

            # Convert world coordinates to chunk coordinates and local coordinates within the chunk.
            chunk_coords = get_chunk_coords(tile_x, tile_y, CHUNK_SIZE)
            local_x = tile_x % CHUNK_SIZE
            local_y = tile_y % CHUNK_SIZE

            # Check if the move to the new tile within the chunk is valid.
            if self.world_grid.is_move_valid(chunk_coords, local_x, local_y):
                # Move the player to the tile and update the tile occupation status.
                player.move_to_tile(tile_x, tile_y, self.world_grid)  # This may need to be updated as well.
                self.world_grid.update_tile(chunk_coords, local_x, local_y, occupied=False)
                return {"x": player.position_x, "y": player.position_y}
            else:
                raise ValueError("Invalid move")
        else:
            raise KeyError("Player not found")


async def handler(websocket, path):
    try:
        # Wait for the first message, which should contain the auth token
        auth_message = await websocket.recv()
        auth_data = json.loads(auth_message)
        try:
            token = auth_data['token']
        except KeyError as e:
            await websocket.close(reason='Authentication token not received')
            raise

        is_valid_session, user_id = await validate_session(token)
        
        if not is_valid_session:
            await websocket.close(reason='Authentication failed')
            return

        # Add the connection to a pool with the associated user information
        connection_manager.register(websocket, user_id)

        # After authentication, load the first player for this user or create a new one
        player_data = get_player(user_id)
        if not player_data:  # user has no characters yet -- for now just create one
            player_name = f"player_{''.join(random.choices('0123456789', k=5))}"
            player = Player.create_new_player(user_id, player_name)
        else:
            player = Player(**player_data)
        await wss.add_player(player)

        # Main game loop for the WebSocket connection
        while True:
            message = await websocket.recv()
            # Process game messages without re-authenticating
            await process_game_message(message, websocket, player)

    except websockets.exceptions.ConnectionClosed as e:
        # If the connection drops, clean up
        player.save()
        connection_manager.remove_connection(websocket, user_id)
        print(f"connection lost for user: {user_id}")
        #handle_reconnection(user_id)
    #except Exception as e:
    #    player.save()
    #    print(f"error for user {user_id}: {e}")


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


async def process_game_message(message, websocket, player):
    async for message in websocket:
        data = json.loads(message)
        print("received: " + str(data))
        # Adjust the expected action and parameters based on your client's message format.
        if data['action'] == 'MovePlayerToTile':
            player_id = player.player_id
            tile_xy = data['tile_xy']
            try:
                result = await wss.move_player_to_tile(player_id, tile_xy)
                await websocket.send(json.dumps({"action": "PlayerMoved", "result": result}))  # Assuming result is an object with a .to_dict() method
            except ValueError as e:
                await websocket.send(json.dumps({"action": "Error", "message": str(e)}))
            except KeyError as e:
                await websocket.send(json.dumps({"action": "Error", "message": "Player not found"}))

        """
        elif data['action'] == 'CreateNewPlayer':
            player_id = str(data['player_id'])
            result = await wss.add_player(player_id)
            print("player created")
            await websocket.send(json.dumps({"action": "PlayerCreated", "result": result}))
        """

        if data['action'] == 'GetChunk':
            print(data)
            chunk = await wss.get_chunk((data['x'], data['y']))
            # Send the chunk data back to the client
            await websocket.send(json.dumps(chunk))


# Server setup
async def main():
    global world_grid
    global wss
    world_grid = WorldGrid(1000, 1000)
    wss = WorldStateService(world_grid)
    async with websockets.serve(handler, "localhost", 6789):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
