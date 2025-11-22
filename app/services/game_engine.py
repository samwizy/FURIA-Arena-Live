from typing import List, Callable, Awaitable
from app.models.schemas import GameStateDTO

class GameEngine:
    def __init__(self):
        self._placar_furia = 0
        self._placar_adversario = 0
        self._nome_adversario = "NAVI"
        self._nome_jogo = "MAJOR SHANGHAI"
        self._mapa = "ANCIENT"
        self._temperatura = 50

        self._observers: List[Callable[[GameStateDTO], Awaitable[None]]] = []

    def subscribe(self, observer_func):
        self._observers.append(observer_func)

    def get_state(self) -> GameStateDTO:
        return GameStateDTO(
            placar_furia=self._placar_furia,
            placar_adversario=self._placar_adversario,
            nome_adversario=self._nome_adversario,
            nome_jogo=self._nome_jogo,
            mapa_atual=self._mapa,
            temperatura=self._temperatura
        )

    async def _notify(self):
        current_state = self.get_state()
        for observer in self._observers:
            await observer(current_state)

    async def processar_admin(self, comando: str):
        mudou = False
        evento = None

        if "/gol" in comando:
            self._placar_furia += 1
            self._temperatura = 100
            mudou = True
            evento = "gol_furia"
        elif "/perdeu" in comando:
            self._placar_adversario += 1
            self._temperatura = 20
            mudou = True
            evento = "ponto_adv"
        elif "/reset" in comando:
            self._placar_furia = 0
            self._placar_adversario = 0
            mudou = True
            evento = "reset"
        elif comando.startswith("/adv "):
            parts = comando.split(" ", 1)
            if len(parts) > 1:
                self._nome_adversario = parts[1]
                mudou = True
                evento = "mudou_adversario"
        elif comando.startswith("/mapa "):
            parts = comando.split(" ", 1)
            if len(parts) > 1:
                self._mapa = parts[1]
                mudou = True
                evento = "mudou_mapa"

        elif comando.startswith("/jogo "):
            parts = comando.split(" ", 1)
            if len(parts) > 1:
                self._nome_jogo = parts[1]
                mudou = True
                evento = "mudou_jogo"

        if mudou:
            await self._notify()

        return evento

    async def processar_sentimento(self, texto: str):
        positivos = ["vamos", "furia", "ganhar", "lenda", "gg", "wp"]
        negativos = ["ruim", "perder", "lixo", "noob", "entregou"]

        texto = texto.lower()
        mudou = False

        if any(p in texto for p in positivos):
            self._temperatura = min(100, self._temperatura + 5)
            mudou = True
        elif any(p in texto for p in negativos):
            self._temperatura = max(0, self._temperatura - 5)
            mudou = True

        if mudou:
            await self._notify()