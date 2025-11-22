import google.generativeai as genai
from app.core.config import settings

class AIService:
    def __init__(self):
        # Cláusula de guarda: API Key precisa ter um valor.
        if not settings.API_KEY:
            raise ValueError("API Key not set.")

        # Se o If der False, o GenAI tem sua API Key configurada.
        genai.configure(api_key=settings.API_KEY)

        # Ensinado ao Gemini como agir.
        self.system_prompt = """
        Você é o FURIÃO, torcedor fanático da FURIA.
        - Responda de forma curta, vibrante e usando gírias de e-esports.
        - Se perguntarem do placar: responda com o placar do jogo ocorrendo 
        ao vivo.
        - Se perguntarem da Loja: indique 'furia.gg/loja' e informe todos os 
        produtos.
        - Se perguntarem da História: Procure em fontes oficiais e responda.
        - Se perguntarem do Histórico de Jogos: Procure em fontes oficiais e 
        responda.
        """

        self.model = genai.GenerativeModel(
            settings.MODEL_NAME,
            system_instruction=self.system_prompt
        )
        self.chat = self.model.start_chat(history=[])

    def reset_memory(self):
        self.chat = self.model.start_chat(history=[])

    async def get_response(self, user_text: str, game_context: str) -> str:
        try:
            full_prompt = (f"[CONTEXTO DO JOGO: {game_context}] Fã disse: "
                           f"{user_text}")
            response = await self.chat.send_message_async(full_prompt)
            return (response.text.replace("**", "").replace("#", "")
                    .replace("  ", " "))
        except Exception as e:
            print(f"IA Error: {e}")
            return "A conexão caiu, mas a torcida continua! (Erro IA)"