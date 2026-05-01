"""
Cards router — endpoints for generating learning cards.
"""

import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import AUDIO_DIR
from app.models import CardRequest, CardResponse, CardResult
from app.pipeline.audio import fetch_audio
from app.pipeline.llm import get_definition
from app.pipeline.scraper import fetch_translation

router = APIRouter(prefix="/cards", tags=["cards"])


def _build_card(word: str) -> CardResult:
    translation = fetch_translation(word)
    definition = get_definition(word)
    audio_filename = fetch_audio(word)

    all_present = translation is not None and definition is not None and audio_filename is not None
    return CardResult(
        word=word,
        translation=translation,
        definition=definition,
        audio_filename=audio_filename,
        status="ok" if all_present else "missing",
    )


@router.post("", response_model=CardResponse)
async def generate_cards(request: CardRequest) -> CardResponse:
    """
    Run the full NLP pipeline (scrape → LLM → audio) for a list of words
    and return structured learning cards.
    """
    results = [_build_card(word.strip()) for word in request.words]
    ok_count = sum(1 for r in results if r.status == "ok")
    return CardResponse(
        results=results,
        total=len(results),
        ok_count=ok_count,
        missing_count=len(results) - ok_count,
    )


@router.get("/audio/{word}")
async def get_audio(word: str) -> FileResponse:
    """
    Serve the audio file for a given word.
    """
    audio_path = os.path.join(AUDIO_DIR, f"{word}.mp3")
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail=f"No audio file found for '{word}'")
    return FileResponse(audio_path, media_type="audio/mpeg", filename=f"{word}.mp3")


@router.get("/{word}", response_model=CardResult)
async def generate_card(word: str) -> CardResult:
    """
    Run the full NLP pipeline for a single word and return its learning card.
    """
    return _build_card(word.strip())
