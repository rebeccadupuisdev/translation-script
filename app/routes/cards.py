"""
Cards router — endpoints for generating learning cards.
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.models import CardRequest, CardResponse, CardResult

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("/", response_model=CardResponse)
async def generate_cards(request: CardRequest) -> CardResponse:
    """
    Run the full NLP pipeline (scrape → LLM → audio) for a list of words
    and return structured learning cards.
    """
    # TODO: call pipeline steps and build CardResult list
    raise NotImplementedError


@router.get("/{word}", response_model=CardResult)
async def generate_card(word: str) -> CardResult:
    """
    Run the full NLP pipeline for a single word and return its learning card.
    """
    # TODO: call pipeline steps for a single word
    raise NotImplementedError


@router.get("/audio/{word}")
async def get_audio(word: str) -> FileResponse:
    """
    Serve the audio file for a given word.
    """
    # TODO: resolve path and return FileResponse
    raise NotImplementedError
