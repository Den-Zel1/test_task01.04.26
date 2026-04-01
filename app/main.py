from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}

# Здесь в будущем будет: app.include_router(api_router)
