const clientId = Math.floor(Math.random() * 9999);

const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsUrl = `${protocol}//${window.location.host}/ws/${clientId}`

const ws = new WebSocket(wsUrl);

ws.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    const state = payload.state;

    if (state) {
        document.getElementById("p-furia").innerText = state.placar_furia;
        document.getElementById("p-adv").innerText = state.placar_adversario;

        const elAdv = document.getElementById("ui-adv");
        elAdv.innerText = state.nome_adversario;

        const elJg = document.getElementById("ui-torneio");
        elJg.innerText = state.nome_jogo;

        const elMap = document.getElementById("ui-mapa");
        elMap.innerText = "MAPA: " + state.mapa_atual;

        const elBar = document.getElementById("thermo");
        elBar.style.width = state.temperatura + "%";

        const elVal = document.getElementById("thermo-val");
        elVal.innerText = state.temperatura + "%";
        elVal.style.color = state.temperatura > 80 ? "#f1c40f" : "#aaa";
    }

    const elTyping = document.getElementById("typing");
    elTyping.style.display = (
        payload.tipo === "digitando"
    ) ? "block" : "none";

    if (payload.tipo === "chat" && payload.chat) {
        const div = document.createElement("div");
        div.className = payload.chat.is_bot ? "msg bot" : "msg user";

        if (payload.chat.is_bot) {
            div.innerHTML = (
                `<span class="bot-badge">FURIÃO</span>` +
                payload.chat.texto
            );
        } else {
            div.innerText = payload.chat.texto;
        }

        const chat = document.getElementById("chat");
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }
};

function send() {
    const input = document.getElementById("msg");
    if(input.value) {
        ws.send(input.value);
        input.value = "";
    }
}