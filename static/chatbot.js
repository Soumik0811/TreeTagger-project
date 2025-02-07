// Toggle the chatbot window
function toggleChatbot() {
    const chatbotWindow = document.getElementById("chatbot-window");
    chatbotWindow.style.display = chatbotWindow.style.display === "none" ? "block" : "none";
}

// Handle Enter key press in input field
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

// Send message function
function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const chatMessages = document.getElementById("chat-messages");

    if (userInput.trim() === "") return;

    // Display user's message
    const userMessage = document.createElement("div");
    userMessage.classList.add("chat-message", "user-message");
    userMessage.innerText = userInput;
    chatMessages.appendChild(userMessage);

    // Clear input field
    document.getElementById("userInput").value = "";

    // Simulate a bot response (replace with actual bot logic)
    setTimeout(() => {
        const botMessage = document.createElement("div");
        botMessage.classList.add("chat-message", "bot-message");
        botMessage.innerText = "This is a bot response.";
        chatMessages.appendChild(botMessage);

        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}


