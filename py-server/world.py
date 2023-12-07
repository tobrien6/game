from enum import Enum
import random
from event_manager import EventType
from tile_utils import cheb_dist


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
    def __init__(self, chunk_size=64):
        self.chunk_size = chunk_size
        self.chunks = {}

    def load_chunk(self, chunk_coords):
        if chunk_coords not in self.chunks:
            # If the chunk doesn't exist, generate it and store it in self.chunks
            print("generating new chunk")
            self.chunks[chunk_coords] = Chunk() 
        return self.chunks[chunk_coords]

    def is_move_valid(self, chunk_coords, local_x, local_y, player):
        # Check if the tile within the chunk is not occupied and is within valid terrain, etc.
        chunk = self.load_chunk(chunk_coords)

        # World conditions must be true
        in_bounds = 0 <= local_x < self.chunk_size and 0 <= local_y < self.chunk_size
        unoccupied = not chunk.tiles[local_x][local_y].is_occupied

        # Player conditions must be true
        # TODO: A list of player conditions, such as
        # max movement range, 
        # AP balance
        # any modifiers that affect movement 

        return all([in_bounds, unoccupied])

    def update_tile(self, chunk_coords, local_x, local_y, occupied):
        # Update the occupation status of the tile within the specified chunk.
        chunk = self.load_chunk(chunk_coords)
        chunk.tiles[local_x][local_y].is_occupied = occupied


class WorldState:
    def __init__(self, world_grid, event_queue):
        self.players = {}
        self.world_grid = world_grid
        self.event_queue = event_queue

    async def get_player(self, player_id):
        return self.players[player_id]

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

    async def get_entities_in_range(self, tile_xy, range, exclude_player_id=None):
        # for now, the only entities are players
        tile_x = tile_xy[0]
        tile_y = tile_xy[1]
        try:
            entities = []
            for pid, p in self.players.items():
                if pid != exclude_player_id and p.health > 0:
                    if cheb_dist((tile_x, tile_y), (p.x, p.y)) <= range:
                        entities.append(p)
            return entities
        except Exception as e:
            print(e)
            return None

    async def handle_ap_update(self, event):
        player = event['player']
        ap_change = event['ap_used']

        # Check if AP was used (negative change)
        if ap_change < 0:
            dist_range = 10  # Define the range for AP distribution
            player_loc = (player.x, player.y)
            pid = player.player_id
            nearby_players = await self.get_entities_in_range(player_loc, dist_range, exclude_player_id=pid)
            print(f"nearby players: {nearby_players}")
            if nearby_players:
                print(f"nearby players: {nearby_players}")
                distributed_ap = -ap_change / len(nearby_players)
                for player in nearby_players:

                    await player.update_action_points(distributed_ap)
                    event = {'action': 'PlayerAP',
                                     'player_id': player.player_id,
                                     'ap': player.action_points}
                    await player.send_event(event)


    async def move_player_to_tile(self, player_id, tile_xy):
        # DEBUG
        for pid, p in self.players.items():
            print(f"player {pid}: ({p.x},{p.y})")

        tile_x = tile_xy[0]
        tile_y = tile_xy[1]
        player = self.players.get(player_id)
        print(f"PLAYER ID: {player_id}")
        
        if player:
            # Player's current location
            cur_x, cur_y = (player.x, player.y)

            # Convert world coordinates to chunk coordinates and local coordinates within the chunk.
            chunk_coords = get_chunk_coords(tile_x, tile_y, CHUNK_SIZE)
            local_x = tile_x % CHUNK_SIZE
            local_y = tile_y % CHUNK_SIZE

            # Check if the move to the new tile within the chunk is valid.
            if self.world_grid.is_move_valid(chunk_coords, local_x, local_y, player):
                # Move the player to the tile and update the tile occupation status.
                n_entities_near = await self.get_entities_in_range(tile_xy, 10, exclude_player_id=player_id)
                await player.move_to_tile(tile_x, tile_y, self.world_grid, n_entities_near)  # This may need to be updated as well.
                #self.world_grid.update_tile(chunk_coords, local_x, local_y, occupied=True) # for this to work, I need to set previous tile to occupied false
                
                event = {'type': EventType.PLAYER_LOC,
                        'data': {'action': 'PlayerLoc',
                                 'player_id': player_id,
                                 'x': player.x,
                                 'y': player.y,
                                 'ap': player.action_points}}
                await self.event_queue.put_event(event)
                return True
            else:
                raise ValueError("Invalid move")
                return False
        else:
            raise KeyError("Player not found")