from fastapi import FastAPI
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get('/')
def root():
    return {"message": "Hello, World!"}