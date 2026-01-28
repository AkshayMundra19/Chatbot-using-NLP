function addMessage(text, className) {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    msg.className = className;
    msg.innerText = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value;
    if (!message) return;

    addMessage("You: " + message, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {
        addMessage("Bot: " + data.reply, "bot");
    });
}
