class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    def register(self, websocket, username):
        self.active_connections[username] = websocket

    def unregister(self, username):
        self.active_connections.pop(username, None)

    async def send_personal_message(self, message, username):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send(message)

    async def broadcast(self, message):
        for websocket in self.active_connections.values():
            await websocket.send(message)