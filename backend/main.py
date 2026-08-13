from fastapi import FastAPI


app = FastAPI(
    title="AI Study Assistant",
    description="A web-based AI chatbot designed to help students with study questions.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Study Assistant backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }