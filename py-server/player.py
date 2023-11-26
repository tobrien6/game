from datetime import datetime
from database import save_player, get_player
import time

class Player:
    def __init__(self, player_id, user_id, name, position_x=0, position_y=0, health=100, action_points=1000.0, last_update_time=None):
        self.player_id = player_id
        self.user_id = user_id
        self.name = name
        self.position_x = position_x
        self.position_y = position_y
        self.health = health
        self.action_points = action_points
        self.last_update_time = last_update_time if last_update_time is not None else time.time()

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'user_id': self.user_id,
            'name': self.name,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'health': self.health,
            'action_points': self.action_points,
            'last_update_time': self.last_update_time
        }

    def save(self):
        player_dict = self.to_dict()
        save_player(player_dict)

    def get_loc(self):
        return [self.position_x, self.position_y]

    @classmethod
    def create_new_player(self, user_id, name):
        # Here we create a new player with default values for everything but user_id and name
        new_player = self(
            player_id=None,  # None because it will be auto-incremented by the database
            user_id=user_id,
            name=name,
            position_x=0,  # Default position
            position_y=0,  # Default position
            health=100,  # Default health
            action_points=1000.0,  # Default action points
            last_update_time=time.time()  # Current time as last update
        )
        new_player.save()
        return new_player

    def update_action_points(self):
        now = time.time()
        time_elapsed = now - self.last_update_time  # time_elapsed is in milliseconds
        self.action_points += float(time_elapsed)
        self.action_points = max(self.action_points, 1000)
        self.last_update_time = now

    def move_to_tile(self, tile_x, tile_y, world_grid):
        # This function will be called with the tile's x and y the player wants to move to.
        # You need to calculate the cost to move to the new tile here.
        move_cost = self.calculate_move_cost(tile_x, tile_y, world_grid)
        if self.action_points >= move_cost:
            # If the move is valpid and the player has enough action points,
            # set the player's position to the new tile and deduct the action points.
            self.position_x = tile_x
            self.position_y = tile_y
            self.action_points -= move_cost
        else:
            raise ValueError("Not enough action points to move.")

    def calculate_move_cost(self, tile_x, tile_y, world_grpid):
        # Calculate the cost based on the distance to the new tile.
        # You can add more complex logic here based on terrain type or other factors.
        return 1.0  # Assuming a flat cost of 1.0 per tile for simplicity.