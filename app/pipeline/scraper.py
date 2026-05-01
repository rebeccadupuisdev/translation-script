"""
Scraping module — fetches word translations from teanglann.ie.
"""

from typing import Optional

import requests
from bs4 import BeautifulSoup

from app.config import BASE_URL


def fetch_translation(word: str) -> Optional[str]:
    response = requests.get(BASE_URL + word)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Get the first English translation
    translation = soup.find("span", class_="trans")
    return translation.text.strip() if translation else None
