from typing import List, Dict

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connection_groups: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id_ = self.get_conversationgroup_id(websocket)
        connections = self.connection_groups.setdefault(id_, [])
        if websocket not in connections:
            connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        id_ = self.get_conversationgroup_id(websocket)
        connections = self.connection_groups[id_]
        connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender_websocket):
        id_ = self.get_conversationgroup_id(sender_websocket)
        connections = self.connection_groups[id_]
        for connection in connections:
            await connection.send_text(message)

    @staticmethod
    def get_conversationgroup_id(websocket):
        return websocket.path_params['conversationgroup_id']
