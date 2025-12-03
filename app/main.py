from fastapi import FastAPI
from app.core.config import get_settings
from app.api.agent_routes import router as agent_router

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(agent_router)

@app.get('/')
def root():
    return {"message": "Agentic Development API", "version": settings.VERSION}