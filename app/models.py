from typing import List, Literal, Optional

from pydantic import BaseModel


class CardRequest(BaseModel):
    words: List[str]


class CardResult(BaseModel):
    word: str
    translation: Optional[str]
    definition: Optional[str]
    audio_filename: Optional[str]
    status: Literal["ok", "missing"]


class CardResponse(BaseModel):
    results: List[CardResult]
    total: int
    ok_count: int
    missing_count: int
