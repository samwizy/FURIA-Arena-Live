from typing import List
from fastapi import WebSocket
from app.models.schemas import WSPayload, GameStateDTO

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def on_game_state_change(self, new_state: GameStateDTO):
        payload = WSPayload(tipo="update_state", state=new_state)
        await self.broadcast_json(payload)

    async def broadcast_json(self, payload: WSPayload):
        json_str = payload.model_dump_json()
        for connection in self.active_connections:
            await connection.send_text(json_str)