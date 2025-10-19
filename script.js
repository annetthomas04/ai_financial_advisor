const chatContainer = document.getElementById("chat-container");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

// Your Flask backend URL
const API_URL = "http://127.0.0.1:5000/chat";

// Display message in chat
function addMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add(sender === "user" ? "user-message" : "bot-message");
  msg.textContent = text;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Send message to backend
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  userInput.value = "";

  // Add temporary loading bubble
  const loadingMsg = document.createElement("div");
  loadingMsg.classList.add("bot-message");
  loadingMsg.textContent = "💭 Thinking...";
  chatContainer.appendChild(loadingMsg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    loadingMsg.remove();
    addMessage("bot", data.response || "⚠️ Error: No response from AI.");

  } catch (error) {
    loadingMsg.remove();
    addMessage("bot", "⚠️ Could not connect to the server.");
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
