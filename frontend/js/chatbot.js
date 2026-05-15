const FLASK_URL  = "http://127.0.0.1:5000";
const GROQ_URL   = "http://127.0.0.1:8000";


const token = localStorage.getItem("token");
const role  = localStorage.getItem("role");

if (!token || role !== "user") {
    alert("Please login first!");
    window.location.href = "index.html";
}


function toggleMenu() {
    const navLinks = document.getElementById("nav-links");
    navLinks.classList.toggle("active");
}


document.getElementById("logoutBtn").addEventListener("click", function(e) {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "index.html";
});


let conversationHistory = [];


const state   = localStorage.getItem("state");
const city    = localStorage.getItem("city");
const country = localStorage.getItem("country");

if (state) {
    conversationHistory.push({
        role: "user",
        content: `I am currently located in ${city}, ${state}, ${country}.`
    });
    conversationHistory.push({
        role: "assistant",
        content: `Got it! I'll provide traffic rules and information specific to ${city}, ${state}. How can I help you?`
    });
}


document.getElementById("sendBtn").addEventListener("click", sendMessage);

document.getElementById("userInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const input    = document.getElementById("userInput");
    const errormsg = document.getElementById("errormsg");
    const message  = input.value.trim();

    errormsg.textContent = "";

    if (!message) return;


    appendMessage("user", message);
    input.value = "";


    conversationHistory.push({
        role: "user",
        content: message
    });


    const typingId = showTyping();

    try {
        const response = await fetch(`${GROQ_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: conversationHistory
            })
        });

        removeTyping(typingId);

        const result = await response.json();

        if (response.ok) {
            const reply = result.reply;


            conversationHistory.push({
                role: "assistant",
                content: reply
            });


            appendMessage("bot", reply);

        } else {
            errormsg.textContent = result.detail || "Failed to get response!";
        }

    } catch (error) {
        removeTyping(typingId);
        errormsg.textContent = "Cannot connect to DriveBot. Try again!";
    }
}


function appendMessage(sender, text) {
    const chatMessages = document.getElementById("chatMessages");
    const isBot = sender === "bot";
    const time  = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const group = document.createElement("div");
    group.className = "message-group";
    group.style.justifyContent = isBot ? "flex-start" : "flex-end";

    group.innerHTML = isBot ? `
        <div class="message-avatar">🤖</div>
        <div>
            <div class="message bot-message">
                <p>${text.replace(/\n/g, "<br>")}</p>
            </div>
            <div class="msg-time">${time}</div>
        </div>
    ` : `
        <div>
            <div class="message user-message">
                <p>${text.replace(/\n/g, "<br>")}</p>
            </div>
            <div class="msg-time" style="text-align:right">${time}</div>
        </div>
    `;

    chatMessages.appendChild(group);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function showTyping() {
    const chatMessages = document.getElementById("chatMessages");
    const div = document.createElement("div");
    const id  = "typing-" + Date.now();
    div.id    = id;
    div.className = "message bot-message typing";
    div.innerHTML = "<p>DriveBot is typing...</p>";
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function quickAsk(question) {
    document.getElementById("userInput").value = question;
    sendMessage();
}
