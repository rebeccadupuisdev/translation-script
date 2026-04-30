import os

from fastapi import FastAPI

from app.config import AUDIO_DIR
from app.routes.cards import router as cards_router

app = FastAPI(
    title="Irish Learning Cards API",
    description="NLP pipeline (scraping, LLM, audio) for generating Anki-ready learning cards.",
    version="0.1.0",
)

app.include_router(cards_router)

os.makedirs(AUDIO_DIR, exist_ok=True)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
