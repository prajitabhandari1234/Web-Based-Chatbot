/*
 * Front-end interaction logic for the AI Study Assistant.
 *
 * This file manages user input, sends messages to the FastAPI backend,
 * and displays both user and chatbot responses in the conversation area.
 */


// Retrieve the main interactive elements from the HTML document.
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const thinkingIndicator = document.getElementById("thinking");


/**
 * Adds a new message to the conversation area.
 *
 * @param {string} message - The text that will be displayed.
 * @param {string} sender - The sender of the message: "user" or "bot".
 */
function addMessage(message, sender) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("message");

    if (sender === "user") {
        messageElement.classList.add("user-message");
    } else {
        messageElement.classList.add("bot-message");
    }

    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    // Automatically scroll to the most recent message.
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


/**
 * Sends the user's message to the FastAPI backend and displays
 * the returned chatbot response.
 */
async function sendMessage() {

    const message = messageInput.value.trim();

    // Prevent empty messages from being submitted.
    if (!message) {
        return;
    }

    // Display the user's message immediately in the conversation.
    addMessage(message, "user");

    // Clear the input field after submission.
    messageInput.value = "";

    // Show the loading indicator while waiting for the backend.
    thinkingIndicator.classList.remove("hidden");

    // Temporarily disable the button to prevent duplicate submissions.
    sendButton.disabled = true;

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                `Server returned status ${response.status}`
            );
        }


        const data = await response.json();

        addMessage(data.response, "bot");


    } catch (error) {

        console.error(
            "Unable to communicate with the chatbot backend:",
            error
        );

        addMessage(
            "Sorry, I could not connect to the chatbot service. Please try again.",
            "bot"
        );


    } finally {

        // Hide the loading indicator regardless of success or failure.
        thinkingIndicator.classList.add("hidden");

        sendButton.disabled = false;

        // Return focus to the input field for the next question.
        messageInput.focus();
    }
}


// Send the message when the user clicks the Send button.
sendButton.addEventListener(
    "click",
    sendMessage
);


// Allow the Enter key to submit a message.
messageInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {
            sendMessage();
        }
    }
);