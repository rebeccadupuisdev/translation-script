"""
Audio module — downloads and post-processes pronunciation audio files.
"""

import os
from typing import Optional

import requests
from pydub import AudioSegment

from app.config import AUDIO_DIR, AUDIO_URL


def fetch_audio(word: str) -> Optional[str]:
    audio_filename = f"{word}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    response = requests.get(AUDIO_URL + audio_filename)

    if response.status_code != 200:
        return None

    with open(audio_path, "wb") as f:
        f.write(response.content)

    # Add 1 second of silence because Anki cuts the end of the audio :(
    audio = AudioSegment.from_file(audio_path)
    audio_with_silence = audio + AudioSegment.silent(duration=1000)
    audio_with_silence.export(audio_path, format="mp3")

    return audio_filename
