from enum import Enum
import random
from event_manager import EventType


CHUNK_SIZE = 64

# Helper functions
def get_chunk_coords(x, y, chunk_size=CHUNK_SIZE):
    """Convert world coordinates to chunk coordinates."""
    return x // chunk_size, y // chunk_size


# Enums and class definitions would go here...
class TerrainType(Enum):
    Grass = 1
    Rock = 2
    Water = 3
    Tree = 5
    # Additional terrain types...


# A mapping to determine if a terrain type is occupied
terrain_occupation = {
    TerrainType.Grass: False,
    TerrainType.Tree: True,
    TerrainType.Rock: True,
    TerrainType.Water: False,
}


class Tile:
    def __init__(self, terrain_type=TerrainType.Grass):
        self.terrain = terrain_type
        self.is_occupied = terrain_occupation[terrain_type]


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


class WorldState:
    def __init__(self, world_grid, event_queue):
        self.players = {}
        self.world_grid = world_grid
        self.event_queue = event_queue

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
        # DEBUG
        for p in self.players:
            print(f"player {p.player_id}: ({p.x},{p.y})")

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

            event = {'type': EventType.PLAYER_MOVED, 'data': {'action': 'PlayerMoved', 'player_id': player_id, 'x': player.x, 'y': player.y}}
            await self.event_queue.put_event(event)
            #return {"x": player.x, "y": player.y} # position not updated if move not valid, but still returned
        else:
            raise KeyError("Player not found")