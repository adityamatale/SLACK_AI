from fastapi import FastAPI
from SLLACK.api.endpoints import msg_service, registration_service, user_profile_service

app = FastAPI(
    title="Message Service API",
    description="API to send user message to LLM and get feedback.",
)

# Include feedback routes
app.include_router(msg_service.router, tags=["Feedback"])
app.include_router(registration_service.router, tags=["User Registration"])
app.include_router(user_profile_service.router, tags=["User Profile"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)