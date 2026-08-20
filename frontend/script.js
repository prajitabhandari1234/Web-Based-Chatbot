/*
 * Front-end interaction logic for the AI Study Assistant.
 *
 * This module manages user input, displays conversation messages,
 * communicates with the FastAPI backend, and maintains conversation
 * history so that follow-up questions can use previous context.
 */


/*
 * Retrieve the main interactive elements from the HTML document.
 */
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const thinkingIndicator = document.getElementById("thinking");


/*
 * Stores previous user and assistant messages.
 *
 * The history is sent to the backend so that the language model
 * can understand follow-up questions within the conversation.
 */
const conversationHistory = [];


/**
 * Adds a message to the visible conversation area.
 *
 * @param {string} message - The text to display.
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

    /*
     * textContent is used instead of innerHTML so that message content
     * is displayed as plain text rather than interpreted as HTML.
     */
    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    /*
     * Automatically scroll to the newest message in the conversation.
     */
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


/**
 * Sends the user's latest message to the FastAPI backend and displays
 * the AI-generated response.
 */
async function sendMessage() {

    const message = messageInput.value.trim();

    /*
     * Prevent empty or whitespace-only messages from being submitted.
     */
    if (!message) {
        return;
    }


    /*
     * Display the user's message immediately in the chat interface.
     */
    addMessage(message, "user");


    /*
     * Store the user's latest message in the conversation history.
     */
    conversationHistory.push({
        role: "user",
        content: message
    });


    /*
     * Clear the input field after the message has been submitted.
     */
    messageInput.value = "";


    /*
     * Show the loading indicator while waiting for the backend.
     */
    thinkingIndicator.classList.remove("hidden");


    /*
     * Disable the Send button temporarily to prevent duplicate requests.
     */
    sendButton.disabled = true;


    try {

        /*
         * A relative API path is used so that the application works
         * locally, inside Docker, and on a future cloud deployment.
         */
        const response = await fetch(
        "http://127.0.0.1:8000/api/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory.slice(0, -1)
            })
        }
    );


        /*
         * Handle non-successful responses returned by the backend.
         */
        if (!response.ok) {

            let errorMessage =
                "Sorry, the chatbot service is currently unavailable.";

            try {

                const errorData = await response.json();

                if (errorData.detail) {
                    errorMessage = errorData.detail;
                }

            } catch (parseError) {

                console.error(
                    "Unable to parse backend error response:",
                    parseError
                );
            }

            throw new Error(errorMessage);
        }


        const data = await response.json();


        /*
         * Display the AI-generated response.
         */
        addMessage(data.response, "bot");


        /*
         * Store the assistant response so that future requests can use it
         * as part of the conversation context.
         */
        conversationHistory.push({
            role: "assistant",
            content: data.response
        });


    } catch (error) {

        console.error(
            "Unable to communicate with the chatbot backend:",
            error
        );


        /*
         * Remove the latest user message from conversation memory because
         * no successful assistant response was generated for it.
         */
        conversationHistory.pop();


        /*
         * Display a controlled user-friendly error message.
         */
        addMessage(
            error.message ||
            "Sorry, I could not connect to the chatbot service. Please try again.",
            "bot"
        );


    } finally {

        /*
         * Hide the loading indicator regardless of whether the request
         * succeeded or failed.
         */
        thinkingIndicator.classList.add("hidden");


        /*
         * Re-enable the Send button.
         */
        sendButton.disabled = false;


        /*
         * Return keyboard focus to the message input field.
         */
        messageInput.focus();
    }
}


/*
 * Submit the message when the user clicks the Send button.
 */
sendButton.addEventListener(
    "click",
    sendMessage
);


/*
 * Allow the Enter key to submit a message without requiring
 * the user to click the Send button.
 */
messageInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {
            sendMessage();
        }
    }
);