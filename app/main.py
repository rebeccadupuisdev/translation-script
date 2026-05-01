import os
from typing import Dict

from fastapi import FastAPI

from app.config import AUDIO_DIR
from app.routes.cards import router as cards_router

app = FastAPI(
    title="Irish Learning Cards API",
    description="NLP pipeline (scraping, LLM, audio) for generating Anki-ready learning cards.",
    version="0.1.0",
    redirect_slashes=False,
)

app.include_router(cards_router)

os.makedirs(AUDIO_DIR, exist_ok=True)

# Run with: uvicorn app.main:app --reload --port 8001

@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}
