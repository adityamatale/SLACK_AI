from fastapi import FastAPI
from endpoints import msg_service

app = FastAPI(
    title="Message Service API",
    description="API to send user message to LLM and get feedback.",
)

# Include feedback routes
app.include_router(msg_service.router, tags=["Feedback"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)