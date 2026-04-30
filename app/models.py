from typing import Literal

from pydantic import BaseModel


class CardRequest(BaseModel):
    words: list[str]


class CardResult(BaseModel):
    word: str
    translation: str | None
    definition: str | None
    audio_filename: str | None
    status: Literal["ok", "missing"]


class CardResponse(BaseModel):
    results: list[CardResult]
    total: int
    ok_count: int
    missing_count: int
