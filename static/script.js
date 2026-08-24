const chatbox = document.getElementById("chatbox");
const optionsPanel = document.getElementById("optionsPanel");   // for model/spec options
const categoryPanel = document.getElementById("categoryPanel"); // NEW center category UI

const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

sendBtn.onclick = sendMessage;
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

/* Add message bubble */
function addMessage(text, sender) {
    const bubble = document.createElement("div");
    bubble.classList.add("message");
    bubble.classList.add(sender === "user" ? "user-msg" : "bot-msg");

    chatbox.appendChild(bubble);
    chatbox.scrollTop = chatbox.scrollHeight;

    // User messages – no typing effect
    if (sender === "user") {
        bubble.textContent = text;
        return;
    }

    // Bot messages – typewriter effect
    let i = 0;
    const speed = 8;

    function type() {
        if (i < text.length) {
            bubble.textContent += text[i];
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

/* Typing indicator */
function showTyping() {
    const bubble = document.createElement("div");
    bubble.classList.add("message", "bot-msg", "typing");
    bubble.innerHTML = "<span></span><span></span><span></span>";
    chatbox.appendChild(bubble);
    chatbox.scrollTop = chatbox.scrollHeight;
    return bubble;
}

/* Clear both option areas */
function clearAllOptions() {
    optionsPanel.innerHTML = "";
    categoryPanel.innerHTML = "";
    categoryPanel.style.display = "none";
}

/* Show CATEGORY buttons in CENTER panel */
function showCategoryOptions(categories) {
    categoryPanel.innerHTML = "";
    categoryPanel.style.display = "flex";

    categories.forEach(cat => {
        const btn = document.createElement("button");
        btn.className = "category-btn";
        btn.innerText = cat;

        btn.onclick = () => {
            addMessage(cat, "user");
            clearAllOptions();
            sendToBot(cat);
        };

        categoryPanel.appendChild(btn);
    });
}

/* Show OTHER option buttons in bottom panel */
function showOptions(options) {
    optionsPanel.innerHTML = "";
    if (!options || !options.length) return;

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.classList.add("option-btn");
        btn.innerText = opt;

        btn.onclick = () => {
            addMessage(opt, "user");
            optionsPanel.innerHTML = "";
            sendToBot(opt);
        };

        optionsPanel.appendChild(btn);
    });
}

/* Handle manual send */
function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    sendToBot(text);
}

/* Send text to backend */
function sendToBot(text) {
    const typingBubble = showTyping();

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {

        typingBubble.remove();
        addMessage(data.reply, "bot");

        // CATEGORY buttons (first step)
        if (data.options && data.options.length > 0 && data.options[0] === "Mobile") {
            // backend sends category list first
            showCategoryOptions(data.options);
            return;
        }

        // normal options
        if (data.options) {
            showOptions(data.options);
        } else {
            clearAllOptions();
        }
    })
    .catch(err => {
        typingBubble.remove();
        addMessage("⚠️ Error talking to server.", "bot");
        console.error(err);
    });
}

/* Auto-start conversation */
window.onload = () => {
    sendToBot("__start__");
};
