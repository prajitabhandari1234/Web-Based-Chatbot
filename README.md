# AI Study Assistant

AI Study Assistant is a web-based Large Language Model (LLM) chatbot designed to support university students with study-related questions. The application provides structured, student-friendly explanations and maintains conversational context so users can ask relevant follow-up questions.

The system integrates a responsive web interface with a FastAPI backend and the Google Gemini API. It also includes basic security controls, API error handling, conversation context management, and Docker-based deployment.

---

## Features

- AI-powered study assistance using Google Gemini
- Responsive web-based chatbot interface
- Context-aware follow-up conversations
- Structured and student-friendly AI responses
- Conversation history and context management
- Basic prompt-injection detection
- Input sanitisation and validation
- User-friendly API error handling
- Secure environment-variable configuration
- Docker containerisation
- RESTful API using FastAPI
- Interactive API documentation with Swagger UI

---

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Google Gemini API
- python-dotenv

### Frontend

- HTML5
- CSS3
- JavaScript

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

---

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

> **Note:** The `.env` file contains local configuration and is excluded from Git and Docker builds. It should never be committed to the repository.

---

## System Architecture

The application follows a client-server architecture in which the browser communicates with the FastAPI backend through an HTTP API.

```text
+----------------------+
|        User          |
+----------+-----------+
           |
           v
+----------------------+
|    Web Frontend      |
|  HTML / CSS / JS     |
+----------+-----------+
           |
           | POST /api/chat
           v
+----------------------+
|   FastAPI Backend    |
+----------+-----------+
           |
           +-----------------------------+
           |                             |
           v                             v
+--------------------+       +----------------------+
| Input Validation   |       | Security Processing  |
| & Sanitisation     |       | Prompt Injection     |
+--------------------+       +----------------------+
           |
           v
+----------------------+
| Conversation Context |
| Management            |
+----------+-------------+
           |
           v
+----------------------+
| Google Gemini API    |
+----------+-----------+
           |
           v
+----------------------+
| AI-Generated Response|
+----------+-----------+
           |
           v
+----------------------+
| FastAPI -> Frontend  |
+----------+-----------+
           |
           v
+----------------------+
|        User          |
+----------------------+
```

---

## How the Application Works

1. The user enters a study-related question in the web interface.
2. JavaScript validates the input and sends the request to the FastAPI backend.
3. The backend validates and sanitises the incoming request.
4. Basic security checks are applied before the request is processed.
5. Previous conversation messages are included to provide conversational context.
6. The backend sends the prepared request to the Google Gemini API.
7. Gemini generates an AI response.
8. FastAPI returns the response to the frontend.
9. The frontend displays the response in the conversation interface.
10. The assistant response is stored temporarily in browser memory for subsequent follow-up questions.

---

## Conversation Context

The application supports contextual follow-up questions during the current browser session.

For example:

```text
User:
What is Python?

Assistant:
Python is a high-level programming language...

User:
How is it useful in coding?
```

Relevant previous messages are sent with subsequent requests so the language model can understand that the follow-up question refers to the previous conversation.

Conversation history is currently stored temporarily in browser memory. Refreshing or closing the page clears the conversation history.

This design provides conversational context without requiring persistent user data storage for the current project scope.

---

## Security

The application implements basic security controls appropriate to the scope of the project.

These include:

- API credentials stored using environment variables
- `.env` excluded from Git using `.gitignore`
- `.env` excluded from Docker images using `.dockerignore`
- Input sanitisation
- Pydantic request validation
- Basic prompt-injection detection
- Controlled backend error responses
- Plain-text rendering of chatbot responses
- No API credentials exposed to frontend JavaScript

Requests attempting to reveal or override internal instructions can be detected before normal LLM processing.

> **Security:** Never commit API keys, access tokens, passwords, or other credentials to the repository.

---

## Error Handling

The application provides controlled responses when external AI requests fail.

Handled scenarios include:

- Gemini API failures
- Invalid API credentials
- Network or API communication failures
- Invalid HTTP responses
- Invalid request bodies
- Unexpected model responses

Instead of exposing internal technical information to users, the application displays a user-friendly message such as:

```text
The AI service is temporarily unavailable. Please try again shortly.
```

---

## Prerequisites

Before running the project, ensure the following are installed:

- Python 3.11 or later
- pip
- Git
- Docker Desktop (for container deployment)
- A valid Google Gemini API key

---

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

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

#### Windows

```powershell
pip install -r backend/requirements.txt
```

#### macOS / Linux

```bash
pip3 install -r backend/requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root directory.

The provided `.env.example` file can be used as a template:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your own Gemini API key.

> **Important:** The real `.env` file must remain local and must not be committed to GitHub.

---

## Running Locally

### Windows

From the project root directory:

```powershell
uvicorn backend.main:app --reload
```

### macOS / Linux

From the project root directory:

```bash
uvicorn backend.main:app --reload
```

After starting the server, open:

```text
http://127.0.0.1:8000
```

FastAPI serves both the backend API and frontend application.

---

## API Endpoints

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

### Chat Endpoint

```http
POST /api/chat
```

Example request:

```json
{
  "message": "What is machine learning?",
  "history": []
}
```

Example response:

```json
{
  "response": "Machine learning is..."
}
```

---

## API Documentation

FastAPI automatically provides interactive Swagger API documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to inspect and test the available API endpoints.

---

## Docker Deployment

The application can also be deployed locally using Docker.

The following Docker commands can be used on Windows, macOS, and Linux.

### 1. Start Docker

Ensure Docker Desktop is installed and the Docker engine is running.

Verify Docker:

```bash
docker --version
```

### 2. Build the Docker Image

From the project root directory:

```bash
docker build -t ai-study-assistant .
```

Docker will build the application image using the project's `Dockerfile`.

### 3. Run the Container

Run the application and provide the environment configuration at runtime:

```bash
docker run --name ai-study-chatbot --env-file .env -p 8000:8000 ai-study-assistant
```

This command:

- Creates a container named `ai-study-chatbot`
- Loads the Gemini API key from `.env`
- Maps host port `8000` to container port `8000`
- Runs the `ai-study-assistant` Docker image

### 4. Open the Application

Navigate to:

```text
http://127.0.0.1:8000
```

### 5. Check the Running Container

```bash
docker ps
```

### 6. View Container Logs

```bash
docker logs ai-study-chatbot
```

### 7. Stop the Container

```bash
docker stop ai-study-chatbot
```

### 8. Restart the Container

```bash
docker start ai-study-chatbot
```

### 9. Remove the Container

Stop the container first if it is currently running:

```bash
docker stop ai-study-chatbot
```

Then remove it:

```bash
docker rm ai-study-chatbot
```

The Gemini API key is supplied to the container at runtime through the `.env` file and is not embedded in the Docker image.

---

## Testing and Validation

The application is tested across backend functionality, AI integration, conversation management, security, error handling, frontend behaviour, and Docker deployment.

Key validation scenarios include:

| ID | Test | Expected Behaviour |
|---|---|---|
| T01 | Backend health check | Returns successful health status |
| T02 | Normal chatbot request | AI-generated response is returned |
| T03 | Conversation context | Follow-up question uses previous context |
| T04 | Empty input | Empty message is not submitted |
| T05 | Prompt-injection attempt | Suspicious request is handled appropriately |
| T06 | Normal academic question | Legitimate request is processed normally |
| T07 | Invalid API request | Request validation rejects invalid input |
| T08 | Gemini API failure | User-friendly error message is displayed |
| T09 | Docker deployment | Application runs successfully in a container |
| T10 | Frontend usability | Chat interface operates correctly |

The testing process also verifies that internal technical errors are not exposed directly to users.

---

## Code Quality

Backend Python code can be formatted and checked using the following development tools:

```bash
black backend
isort backend
flake8 backend
```

These tools help maintain:

- Consistent Python formatting
- Organised imports
- Improved readability
- Basic static code-quality checking

---

## Development Approach

The project was developed incrementally using Git and GitHub.

Major development stages include:

1. Initial project setup
2. FastAPI backend development
3. Chat API endpoint implementation
4. Responsive frontend development
5. Frontend and backend integration
6. Google Gemini LLM integration
7. Conversation history and context management
8. Basic security and prompt-injection controls
9. API error handling
10. Code-quality improvements
11. Docker containerisation and deployment
12. Testing and validation

Incremental Git commits provide a record of the project's implementation and development progress.

---

## Current Limitations

The current version has several limitations:

- Conversation history is not persisted after a page refresh.
- User authentication is not implemented.
- Conversation data is not stored in a database.
- Prompt-injection protection is basic rather than comprehensive.
- The application currently uses a single LLM provider.
- Docker deployment is currently intended for local execution.
- Automated test coverage can be expanded.

---

## Future Improvements

Potential future enhancements include:

- Persistent conversation storage
- User authentication and user profiles
- Database integration
- Multiple conversation sessions
- Advanced prompt-injection protection
- Automated unit and integration testing
- Streaming AI responses
- API rate limiting
- Improved accessibility
- Cloud deployment
- Application monitoring and logging
- Support for additional LLM providers

---

## Project Status

**Functional Prototype**

The current version includes:

- Web-based chatbot interface
- FastAPI backend
- Google Gemini integration
- Conversation context management
- Basic security controls
- API error handling
- Docker containerisation
- Functional testing

---

## Author

**Prajita Bhandari**

Bachelor of Information Technology  
CQUniversity Australia