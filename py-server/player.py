from datetime import datetime
from database import save_player, get_player
import time
import json

class Player:
    def __init__(self, player_id, user_id, name, websocket, x=0, y=0, health=100, action_points=1000.0, last_update_time=None):
        self.player_id = player_id
        self.user_id = user_id
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.action_points = action_points
        self.last_update_time = last_update_time if last_update_time is not None else time.time()
        self.websocket = websocket

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'user_id': self.user_id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'health': self.health,
            'action_points': self.action_points,
            'last_update_time': self.last_update_time
        }

    async def send_event(self, event):
        if self.websocket.open:
            try:
                await self.websocket.send(json.dumps(event))
            except Exception as e:
                # Handle exceptions, which can happen if the connection is closed
                print(f"Error sending event: {e}")

    def save(self):
        player_dict = self.to_dict()
        save_player(player_dict)

    def get_loc(self):
        return [self.x, self.y]

    @classmethod
    def create_new_player(self, user_id, name, websocket):
        # Here we create a new player with default values for everything but user_id and name
        new_player = self(
            player_id=None,  # None because it will be auto-incremented by the database
            user_id=user_id,
            name=name,
            x=0,  # Default position
            y=0,  # Default position
            health=100,  # Default health
            action_points=1000.0,  # Default action points
            last_update_time=time.time(),  # Current time as last update
            websocket=websocket
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
            self.x = tile_x
            self.y = tile_y
            self.action_points -= move_cost
        else:
            raise ValueError("Not enough action points to move.")

    def calculate_move_cost(self, tile_x, tile_y, world_grpid):
        # Calculate the cost based on the distance to the new tile.
        # You can add more complex logic here based on terrain type or other factors.
        return 1.0  # Assuming a flat cost of 1.0 per tile for simplicity.