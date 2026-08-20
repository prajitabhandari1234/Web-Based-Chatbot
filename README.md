# AI Study Assistant

AI Study Assistant is a web-based Large Language Model (LLM) chatbot developed to support university students with study-related questions.

The application provides a simple and responsive conversational interface where students can ask academic questions and receive clear, concise, and student-friendly explanations. It also maintains short-term conversation context, allowing users to ask follow-up questions related to previous messages.

The system integrates an HTML, CSS, and JavaScript frontend with a Python FastAPI backend and the Google Gemini API. It also includes input validation, input sanitisation, basic prompt-injection detection, API error handling, environment-based API key management, and Docker containerisation.

## Features

- AI-powered study assistance using Google Gemini
- Responsive web-based chatbot interface
- Clear and student-friendly AI responses
- Context-aware follow-up conversations
- Temporary conversation history
- Conversation context management
- Input sanitisation
- Pydantic request validation
- Basic prompt-injection detection
- System instruction for chatbot behaviour
- User-friendly API error handling
- Secure environment-variable configuration
- RESTful API using FastAPI
- Health-check endpoint
- Interactive Swagger API documentation
- Docker containerisation

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- python-dotenv
- Google GenAI Python library

### AI Service

- Google Gemini API

### Development and Deployment

- Git
- GitHub
- Docker
- Docker Desktop
- Visual Studio Code

### Code Quality

- Black
- isort
- flake8

## Project Structure

```text
Web-Based-Chatbot/
│
├── backend/
│   ├── chatbot.py
│   ├── main.py
│   ├── requirements.txt
│   └── security.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
└── README.md
```

## System Architecture

The AI Study Assistant follows a client-server architecture.

The frontend provides the chatbot interface and communicates with the FastAPI backend through the `POST /api/chat` endpoint using JSON. The backend validates and sanitises the request, performs basic prompt-injection detection, processes recent conversation context, and forwards the prepared request to the Google Gemini API.

The generated response is returned through FastAPI as JSON and displayed by the frontend.

```text
User / University Student
          |
          v
HTML / CSS / JavaScript Frontend
          |
          | HTTP POST /api/chat
          | JSON Request
          v
FastAPI Backend
          |
          v
Request Validation
          |
          v
Input Sanitisation
          |
          v
Prompt-Injection Detection
          |
          v
Conversation Context Management
          |
          v
Gemini Integration
(chatbot.py)
          |
          | API Request
          v
Google Gemini API
          |
          v
AI-Generated Response
          |
          v
FastAPI Backend
          |
          v
JSON Response
          |
          v
Frontend
          |
          v
User
```

If communication with the external Gemini service fails, the backend handles the exception and returns an HTTP `503 Service Unavailable` response rather than exposing internal technical errors directly to the user.

## How the Application Works

1. The user enters a study-related question in the web interface.
2. JavaScript validates the input and sends a JSON request to `POST /api/chat`.
3. FastAPI validates the incoming request using Pydantic models.
4. The user's message is sanitised.
5. The application performs basic prompt-injection detection.
6. Recent conversation history is processed to provide conversational context.
7. The request is passed to the Gemini integration module in `chatbot.py`.
8. The system instruction defines the chatbot's role and response behaviour.
9. The prepared request is sent to the Google Gemini API.
10. Gemini generates an AI response.
11. FastAPI returns the response to the frontend as JSON.
12. The frontend displays the response in the chat interface.
13. The conversation is retained temporarily in browser memory for follow-up questions.

## Frontend Design

The frontend is implemented using HTML, CSS, and JavaScript.

The interface provides:

- A chatbot conversation area
- User message display
- AI-generated response display
- Text input field
- Send button
- Loading or "AI is thinking..." state
- Scrollable conversation history
- Responsive layout
- User-friendly error messages

JavaScript manages communication with the backend using the Fetch API.

The frontend sends requests to:

```http
POST /api/chat
```

The request is sent in JSON format and contains the user's current message and recent conversation history.

Chatbot responses are rendered as plain text rather than executable HTML, reducing the risk of injected HTML or JavaScript being interpreted by the browser.

## Backend Architecture

The backend is implemented using Python and FastAPI.

FastAPI is responsible for:

- API routing
- Request validation
- Input processing
- Security processing
- Conversation context handling
- Gemini API integration
- Error handling
- Serving frontend static files

The primary application code is contained in:

```text
backend/main.py
```

The Gemini integration is separated into:

```text
backend/chatbot.py
```

Security-related functionality is separated into:

```text
backend/security.py
```

This separation improves modularity and makes the individual components easier to maintain.

## Request Validation

Pydantic models are used to validate incoming API requests.

Each conversation message contains:

```text
role
content
```

The supported roles are:

```text
user
assistant
```

A chat request contains:

```text
message
history
```

This ensures that incoming requests follow the expected data structure before they are processed by the application.

## Gemini API Integration

The Google Gemini API provides the Large Language Model functionality used by the chatbot.

Gemini communication is implemented in:

```text
backend/chatbot.py
```

The integration module:

- Loads the Gemini API key
- Creates the Gemini API client
- Applies the system instruction
- Processes recent conversation history
- Builds the LLM request
- Sends the request to Gemini
- Retrieves the generated response
- Handles API errors

The Gemini API key is loaded using the environment variable:

```text
GEMINI_API_KEY
```

The key is never hard-coded into the Python source code.

## System Instruction

The application uses a system instruction to define the role and behaviour of the chatbot.

The instruction directs the model to:

- Act as an AI Study Assistant
- Support university students
- Explain academic concepts clearly
- Use student-friendly language
- Provide examples where appropriate
- Use previous conversation context
- Handle follow-up questions
- Return plain-text responses
- Avoid unnecessary repetition

The system instruction is supplied separately from user input so that trusted application instructions remain separate from untrusted user messages.

## Conversation State Management

The application supports contextual follow-up questions during the current browser session.

For example:

```text
User:
What is an LLM?

Assistant:
An LLM is a Large Language Model...

User:
How is it implemented in a chatbot?
```

The second question does not explicitly repeat "LLM". However, recent conversation history is included in the next API request, allowing the model to understand what the user is referring to.

The frontend temporarily stores conversation history in browser memory.

The backend limits the context sent to Gemini to recent messages so that requests do not continue growing indefinitely.

Conversation history is not stored in a database.

Refreshing or closing the browser page clears the current conversation.

## Security

The project includes basic security controls appropriate for the scope of the application.

### Environment-Based API Key Management

The Gemini API key is stored using:

```text
GEMINI_API_KEY
```

The actual key is stored in `.env`.

The `.env` file is excluded from Git using `.gitignore` and excluded from Docker image builds using `.dockerignore`.

### Input Sanitisation

User messages are sanitised before being forwarded to the LLM.

Basic unnecessary whitespace is removed from incoming messages.

### Prompt-Injection Detection

The application checks user input for common patterns that may indicate attempts to override or reveal protected system instructions.

Examples include requests attempting to:

- Ignore previous instructions
- Reveal the system prompt
- Display internal instructions
- Override system instructions
- Bypass system instructions

Detected requests are handled before normal Gemini processing.

This is a basic security control and is not intended to provide comprehensive protection against every possible prompt-injection technique.

### Plain-Text Response Rendering

Chatbot responses are displayed as plain text rather than executable HTML.

### Backend Credential Protection

The Gemini API key is only available to the backend and is never exposed through frontend JavaScript.

## Error Handling

The application includes error handling for failures involving the external Gemini service.

Possible failures include:

- Gemini API service errors
- Network communication failures
- API quota or rate-limit errors
- Invalid credentials
- Empty model responses
- Unexpected API errors

When Gemini cannot successfully generate a response, the backend converts the failure into:

```text
HTTP 503 Service Unavailable
```

The frontend then displays a user-friendly message:

```text
The AI service is temporarily unavailable. Please try again shortly.
```

This prevents detailed internal API errors from being directly exposed through the chatbot interface.

# Setup Instructions

## Prerequisites

Before running the application, ensure the following are installed:

- Python 3.11 or later
- pip
- Git
- Docker Desktop for Docker deployment
- A valid Google Gemini API key

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prajitabhandari1234/Web-Based-Chatbot.git
cd Web-Based-Chatbot
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root directory.

The included `.env.example` file can be used as a template.

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace:

```text
your_gemini_api_key_here
```

with a valid Gemini API key.

> **Important:** Never commit the real `.env` file or API key to GitHub.

# Running the Application Locally

From the project root directory, run:

```bash
uvicorn backend.main:app --reload
```

The server should start on:

```text
http://127.0.0.1:8000
```

Open the address in a web browser.

FastAPI serves both the frontend application and backend API through the same service.

## API Endpoints

### Backend Confirmation

```http
GET /api
```

Example response:

```json
{
  "message": "AI Study Assistant backend is running"
}
```

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

The health endpoint can be used to confirm that the FastAPI application is operational.

### Chat Endpoint

```http
POST /api/chat
```

Example request:

```json
{
  "message": "What is Python?",
  "history": []
}
```

Example successful response:

```json
{
  "response": "Python is a high-level programming language..."
}
```

The `history` array can contain previous user and assistant messages to provide conversation context.

Example:

```json
{
  "message": "How is it used in AI?",
  "history": [
    {
      "role": "user",
      "content": "What is Python?"
    },
    {
      "role": "assistant",
      "content": "Python is a high-level programming language..."
    }
  ]
}
```

## Swagger API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to inspect and test the available API endpoints.

For example, `POST /api/chat` can be tested directly by providing a JSON request body.

# Docker Deployment

The application can be deployed locally using Docker.

## 1. Start Docker

Ensure Docker Desktop is installed and the Docker engine is running.

Verify Docker:

```bash
docker --version
```

## 2. Build the Docker Image

From the project root directory, run:

```bash
docker build -t ai-study-assistant .
```

This creates the Docker image:

```text
ai-study-assistant
```

## 3. Run the Docker Container

Run:

```bash
docker run --name ai-study-chatbot --env-file .env -p 8000:8000 ai-study-assistant
```

This command:

- Creates a container named `ai-study-chatbot`
- Loads environment variables from `.env`
- Supplies the Gemini API key at runtime
- Maps host port `8000` to container port `8000`
- Starts the `ai-study-assistant` image

## 4. Open the Dockerised Application

Open:

```text
http://127.0.0.1:8000
```

The complete frontend and backend application should be available through this address.

## 5. Check Running Containers

```bash
docker ps
```

## 6. View Docker Logs

```bash
docker logs ai-study-chatbot
```

Successful requests should produce logs similar to:

```text
POST /api/chat HTTP/1.1 200 OK
```

## 7. Stop the Container

```bash
docker stop ai-study-chatbot
```

## 8. Restart the Container

```bash
docker start ai-study-chatbot
```

## 9. Remove the Container

Stop the container:

```bash
docker stop ai-study-chatbot
```

Then remove it:

```bash
docker rm ai-study-chatbot
```

The Gemini API key is provided to the container at runtime through `.env` and is not embedded in the Docker image.

# Testing and Validation

The application was tested across frontend functionality, backend functionality, LLM integration, conversation handling, security, API error handling, API endpoints, and Docker deployment.

| ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T01 | Normal study question | Gemini returns a relevant response | Correct student-friendly response displayed | Pass |
| T02 | Follow-up question | Previous context is understood | Follow-up response maintained conversation context | Pass |
| T03 | Prompt-injection attempt | Suspicious request is blocked or safely handled | Protected system instructions were not exposed | Pass |
| T04 | Gemini service failure | HTTP 503 returned and error handled | User-friendly service-unavailable message displayed | Pass |
| T05 | Health endpoint | `/health` confirms application status | `{"status":"healthy"}` returned | Pass |
| T06 | Chat API endpoint | Valid JSON request returns AI response | `POST /api/chat` returned successful response | Pass |
| T07 | Docker deployment | Application runs on port 8000 | Application accessible through Docker on port 8000 | Pass |

Testing confirmed that the main functional and technical components of the AI Study Assistant operated as intended.

## Code Quality

The backend Python code can be formatted and checked using:

```bash
black backend
```

```bash
isort backend
```

```bash
flake8 backend
```

These tools help maintain:

- Consistent Python formatting
- Organised imports
- Improved readability
- Basic static code-quality checking

# Design Decisions

## FastAPI

FastAPI was selected for the backend because it provides lightweight Python API development, Pydantic validation, automatic API documentation, and straightforward integration with Python-based AI libraries.

## Modular Backend Structure

The backend is divided into separate responsibilities:

```text
main.py
```

handles API routing, request validation, security processing, and HTTP responses.

```text
chatbot.py
```

handles system instructions, conversation context preparation, Gemini API communication, and AI response processing.

```text
security.py
```

handles input sanitisation and basic prompt-injection detection.

This separation improves readability, maintainability, and modularity.

## Google Gemini

Google Gemini was selected as the external LLM service because it provides an API that can be integrated with Python and used to generate natural-language responses.

## Message-Based Conversation Context

Conversation history is stored temporarily on the frontend and included with subsequent API requests.

This approach provides contextual conversations without requiring a persistent database for the current prototype.

## Environment Variables

Sensitive API credentials are supplied through environment variables instead of being hard-coded into source files.

## Docker

Docker was selected to package the application and its dependencies into a consistent runtime environment.

# Current Limitations

The current implementation is a functional prototype and has several limitations:

- Conversation history is not persisted after page refresh.
- Conversation data is not stored in a database.
- User authentication is not implemented.
- Prompt-injection detection is basic rather than comprehensive.
- The application currently depends on a single external LLM provider.
- Gemini API availability and usage limits can affect chatbot availability.
- Docker deployment is currently intended for local execution.
- Automated unit and integration testing can be expanded.

# Future Improvements

Potential future enhancements include:

- Persistent conversation storage
- Database integration
- User authentication
- User profiles
- Multiple conversation sessions
- More advanced prompt-injection protection
- Automated unit testing
- Automated integration testing
- API rate limiting
- Streaming AI responses
- Improved accessibility
- Cloud deployment
- Application monitoring
- Structured logging
- Support for additional LLM providers

# AI Usage Statement

Generative AI tools were used as supporting tools during the development of this project.

AI assistance was used for activities including:

- Understanding technical concepts
- Troubleshooting implementation issues
- Reviewing code structure
- Improving code comments and documentation
- Reviewing architecture
- Supporting testing and debugging
- Improving README and technical report wording

AI-generated suggestions were reviewed and adapted before being incorporated into the project.

The final implementation was manually tested through the frontend interface, FastAPI backend, Google Gemini API integration, Swagger API documentation, and Docker environment.

Git and GitHub were used throughout development to maintain version history and document incremental implementation progress.

# Development Approach

The project was developed incrementally using Git and GitHub.

Major development stages included:

1. Initial project setup
2. FastAPI backend development
3. Chat API endpoint implementation
4. Frontend interface development
5. Frontend and backend integration
6. Google Gemini API integration
7. Conversation context management
8. Input sanitisation
9. Basic prompt-injection protection
10. API error handling
11. Code-quality improvements
12. Docker containerisation
13. Testing and validation
14. Documentation

Incremental Git commits provide a record of the project's implementation and development progress.

# Project Status

**Functional Prototype**

The current version includes:

- Web-based chatbot interface
- Responsive frontend
- FastAPI backend
- RESTful chat API
- Google Gemini integration
- System instruction
- Conversation context management
- Input sanitisation
- Basic prompt-injection detection
- API error handling
- Health-check endpoint
- Swagger API documentation
- Environment-based API key management
- Docker containerisation
- Functional testing

# Repository

GitHub Repository:

https://github.com/prajitabhandari1234/Web-Based-Chatbot
