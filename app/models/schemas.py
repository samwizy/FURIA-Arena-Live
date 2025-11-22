from pydantic import BaseModel
from typing import Optional

# DTO: Situação do Jogo.
class GameStateDTO(BaseModel):
    placar_furia: int
    placar_adversario: int
    nome_adversario: str = "NAVI"
    nome_jogo: str = "MAJOR 2025"
    mapa_atual: str = "NUKE"
    temperatura: int

# DTO: Mensagem do Chat.
class ChatMessageDTO(BaseModel):
    autor: str
    texto: str
    is_bot: bool = False

# DTO: O pacote completo que viaja pelo WebSocket.
class WSPayload(BaseModel):
    tipo: str  # 'Digitando...', 'Pesquisando...', etc.
    state: GameStateDTO
    chat: Optional[ChatMessageDTO] = None