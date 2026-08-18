from typing import List, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.chatbot import generate_response
from backend.security import contains_prompt_injection, sanitise_message

# Initialise the FastAPI application and define basic API metadata.
app = FastAPI(
    title="AI Study Assistant",
    description="A web-based AI chatbot designed to help students with study questions.",
    version="1.0.0",
)

# Allow the front-end application to communicate with the FastAPI backend
# during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    """
    Represents a single message stored in the conversation history.

    Attributes:
        role (str): Identifies whether the message was created by the user
            or the assistant.
        content (str): The textual content of the message.
    """

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """
    Represents the request body submitted to the chat endpoint.

    Attributes:
        message (str): The user's latest message.
        history (List[Message]): Previous conversation messages used
            to maintain context.
    """

    message: str
    history: List[Message] = []


@app.get("/api")
def home():
    """
    Return a confirmation that the backend service is running.

    Returns:
        dict: A confirmation message from the application.
    """
    return {"message": "AI Study Assistant backend is running"}


@app.get("/health")
def health_check():
    """
    Check the operational status of the backend service.

    Returns:
        dict: The current health status of the application.
    """
    return {"status": "healthy"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Process a user message and return an AI-generated response.

    Args:
        request (ChatRequest): The validated chat request.

    Returns:
        dict: The generated chatbot response.

    Raises:
        HTTPException: If the AI service cannot process the request.
    """

    clean_message = sanitise_message(request.message)

    if contains_prompt_injection(clean_message):
        return {
            "response": (
                "I can help with study-related questions, but I cannot "
                "follow requests that attempt to override or reveal "
                "system instructions."
            )
        }

    history = [
        {
            "role": message.role,
            "content": sanitise_message(message.content),
        }
        for message in request.history
    ]

    try:
        ai_response = generate_response(
            user_message=clean_message,
            history=history,
        )

        return {"response": ai_response}

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service is temporarily unavailable. "
                "Please try again shortly."
            ),
        ) from error


# Serve the frontend application through FastAPI.
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)
