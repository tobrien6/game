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

CHUNK_SIZE = 64

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

class PlayerState:
    def __init__(self, player_id):
        self.player_id = player_id
        self.position_x = 0
        self.position_y = 0
        self.action_points = 1000.0
        self.last_update_time = datetime.utcnow()

    def get_loc(self):
        return [self.position_x, self.position_y]

    def update_action_points(self):
        now = datetime.utcnow()
        time_elapsed = (now - self.last_update_time).total_seconds()
        self.action_points += float(time_elapsed)
        self.action_points = max(self.action_points, 1000)
        self.last_update_time = now

    def move_to_tile(self, tile_x, tile_y, world_grid):
        # This function will be called with the tile's x and y the player wants to move to.
        # You need to calculate the cost to move to the new tile here.
        move_cost = self.calculate_move_cost(tile_x, tile_y, world_grid)
        if self.action_points >= move_cost:
            # If the move is valid and the player has enough action points,
            # set the player's position to the new tile and deduct the action points.
            self.position_x = tile_x
            self.position_y = tile_y
            self.action_points -= move_cost
        else:
            raise ValueError("Not enough action points to move.")

    def calculate_move_cost(self, tile_x, tile_y, world_grid):
        # Calculate the cost based on the distance to the new tile.
        # You can add more complex logic here based on terrain type or other factors.
        return 1.0  # Assuming a flat cost of 1.0 per tile for simplicity.

    def to_dict(self):
        return {
            'action': 'UpdatePos',
            'p_id': self.player_id,
            'x': self.position_x,
            'y': self.position_y,
            'ap': self.action_points,
            # Convert last_update_time to a string to ensure JSON serializability
            'last_update_time': self.last_update_time.isoformat()
        }

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

    def get_chunk(self, chunk_coords):
        return self.world_grid.load_chunk(chunk_coords)

    def add_player(self, player_id):
        self.players[player_id] = PlayerState(player_id)

    def get_player(self, player_id):
        return self.players[player_id]

    def move_player_to_tile(self, player_id, tile_xy):
        tile_x = tile_xy[0]
        tile_y = tile_xy[1]
        player_state = self.players.get(player_id)
        if player_state:
            # First, update the player's action points.
            player_state.update_action_points()

            # Convert world coordinates to chunk coordinates and local coordinates within the chunk.
            chunk_coords = get_chunk_coords(tile_x, tile_y, CHUNK_SIZE)
            local_x = tile_x % CHUNK_SIZE
            local_y = tile_y % CHUNK_SIZE

            # Check if the move to the new tile within the chunk is valid.
            if self.world_grid.is_move_valid(chunk_coords, local_x, local_y):
                # Move the player to the tile and update the tile occupation status.
                player_state.move_to_tile(tile_x, tile_y, self.world_grid)  # This may need to be updated as well.
                self.world_grid.update_tile(chunk_coords, local_x, local_y, occupied=False)
                return player_state.to_dict()
            else:
                raise ValueError("Invalid move")
        else:
            raise KeyError("Player not found")

# WebSocket server handler and methods
class GameHub:
    def __init__(self, world_state_service):
        self.world_state_service = world_state_service

    async def move_player_to_tile(self, player_id, tile_xy):
        if player_id not in self.world_state_service.players:
            raise Exception("player_id not found")
        return self.world_state_service.move_player_to_tile(player_id, tile_xy)

    async def add_player(self, player_id):
        self.world_state_service.add_player(player_id)
        return f"player {player_id} created"

    async def get_player(self, player_id):
        return self.world_state_service.get_player(player_id)

    async def get_map(self, center, radius):
        return self.world_state_service.get_map(center, radius)

    async def get_chunk(self, chunk_coords):
        chunk = self.world_state_service.get_chunk(chunk_coords)
        # Convert the Chunk object's tiles to a serializable format
        tiles_data = [[tile.terrain.value for tile in row] for row in chunk.tiles]
        return {
            'action': 'ChunkData',
            'chunk_x': chunk_coords[0],
            'chunk_y': chunk_coords[1],
            'tiles': tiles_data
        }


async def main_logic(websocket, path):
    game_hub = GameHub(world_state_service)
    async for message in websocket:
        data = json.loads(message)
        #print("received: " + str(data))
        # Adjust the expected action and parameters based on your client's message format.
        if data['action'] == 'MovePlayerToTile':
            player_id = str(data['player_id'])
            tile_xy = data['tile_xy']
            try:
                result = await game_hub.move_player_to_tile(player_id, tile_xy)
                await websocket.send(json.dumps({"action": "PlayerMoved", "result": result}))  # Assuming result is an object with a .to_dict() method
            except ValueError as e:
                await websocket.send(json.dumps({"action": "Error", "message": str(e)}))
            except KeyError as e:
                await websocket.send(json.dumps({"action": "Error", "message": "Player not found"}))
        elif data['action'] == 'CreateNewPlayer':
            player_id = str(data['player_id'])
            result = await game_hub.add_player(player_id)
            print("player created")
            await websocket.send(json.dumps({"action": "PlayerCreated", "result": result}))
        elif data['action'] == 'RequestMap':
            player_id = data['player_id']
            player = await game_hub.get_player(player_id)
            if data['cur_loc'] != player.get_loc():
                #print(data['cur_loc'], player.get_loc())
                # client is out of sync. Return a sync error along with corrected data
                await websocket.send(json.dumps({"error": "location", "result": player.get_loc() }))
            else:
                # return map data surrounding player
                map_data = await game_hub.get_map(center=data['cur_loc'], radius=10)
                await websocket.send(json.dumps({"action": "MapData", "map_data": map_data}))
        elif data['action'] == 'GetChunk':
            print(data)
            chunk = await game_hub.get_chunk((data['x'], data['y']))
            # Send the chunk data back to the client
            await websocket.send(json.dumps(chunk))


# Server setup
async def main():
    global world_state_service
    # Create a WorldGrid instance with the desired width and height
    world_grid = WorldGrid(1000, 1000)
    # Now pass the world_grid instance to the WorldStateService constructor
    world_state_service = WorldStateService(world_grid)
    async with websockets.serve(main_logic, "localhost", 6789):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
