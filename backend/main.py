from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Initialise the FastAPI application and define basic API metadata.
app = FastAPI(
    title="AI Study Assistant",
    description="A web-based AI chatbot designed to help students with study questions.",
    version="1.0.0"
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

class ChatRequest(BaseModel):
    """
    Represents the expected request body for the chat endpoint.

    Attributes:
        message (str): The message submitted by the user to the chatbot.
    """
    message: str


@app.get("/")
def home():
    """
    Return a basic message confirming that the backend service is running.

    Returns:
        dict: A confirmation message from the application.
    """
    return {
        "message": "AI Study Assistant backend is running"
    }


@app.get("/health")
def health_check():
    """
    Check the operational status of the backend service.

    Returns:
        dict: The current health status of the application.
    """
    return {
        "status": "healthy"
    }


@app.post("/api/chat")
def chat(request: ChatRequest):
    """
    Process a user message submitted to the chatbot.

    This endpoint currently returns a temporary echo response. The response
    will be replaced with an LLM-generated response during API integration.

    Args:
        request (ChatRequest): The validated request containing the user's
            message.

    Returns:
        dict: A response containing the processed chatbot message.
    """
    user_message = request.message

    return {
        "response": f"You said: {user_message}"
    }