import websocket
import json
import threading


# Global variable to control the flow
player_created = threading.Event()

# Define the callback for the connection's opening event
def on_open(ws):
    print("Connection opened")
    # create player
    ws.send(json.dumps({"action": "CreateNewPlayer", "player_id": "1"}))
    ws.send(json.dumps({"action": "GetChunk", "x": 0, "y": 0}))

# Define the callback for receiving messages
def on_message(ws, message):
    print("Received message:", message)
    response = json.loads(message)

    # Check if the player was created successfully
    if response.get("action") == "PlayerCreated":
        player_created.set()  # Set the event to signal that the player was created

    # If the player was created, then we can send the move command
    elif player_created.is_set() and response.get("action") == "PlayerMoved":
        # Close the connection after confirming the player moved
        ws.close()

# Define the callback for the connection's closing event
def on_close(ws, close_status_code, close_msg):
    print("Connection closed with status code:", close_status_code)
    print("Close message:", close_msg)

# Define the callback for handling errors
def on_error(ws, error):
    print("Error occurred:", error)

# Set up the WebSocket connection
def setup_websocket():
    # Create a WebSocketApp object with the defined callbacks
    websocket.enableTrace(True)  # Enable logging for debug purposes
    ws = websocket.WebSocketApp("ws://localhost:6789/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    return ws

# Function to send the move command
def send_move_command(ws):
    move_message = {
        "player_id": "1",
        "action": "MovePlayerToTile",
        "tile_xy": [2, 3]
    }
    ws.send(json.dumps(move_message))

# Run the WebSocket connection
if __name__ == "__main__":
    ws = setup_websocket()
    wst = threading.Thread(target=lambda: ws.run_forever())
    wst.daemon = True
    wst.start()

    # Wait until the player is created
    player_created.wait()
    send_move_command(ws)

    wst.join()
