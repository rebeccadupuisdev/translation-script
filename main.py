import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

INPUT_CSV = "irish_words.csv"
OUTPUT_CSV = "irish_words_with_definitions.csv"
AUDIO_DIR = "audio_files"
BASE_URL = "https://www.teanglann.ie/en/fgb/"
AUDIO_URL = "https://www.teanglann.ie/CanC/"

# Create audio directory if it doesn't exist
os.makedirs(AUDIO_DIR, exist_ok=True)


def fetch_word_data(word):
    url = BASE_URL + word
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Get the first English translation
    translation = soup.find("span", class_="trans")
    translation_text = translation.text.strip() if translation else "Not found"

    return translation_text


def fetch_word_audio(word):

    audio_filename = f"{word}.mp3"
    audio_url = AUDIO_URL + audio_filename
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    audio_response = requests.get(audio_url)
    if audio_response.status_code == 200:
        with open(audio_path, "wb") as f:
            f.write(audio_response.content)
    else:
        audio_filename = "Not found"

    return audio_filename


def process_csv(input_csv):
    df = pd.read_csv(input_csv)

    if "word" not in df.columns:
        raise ValueError("CSV must have a column named 'word'.")

    words = [str(word).strip() for word in df["word"]]

    results = []
    for word in words:
        print(f"Processing: {word}")
        time.sleep(1)
        translation = fetch_word_data(word)
        audio_filename = fetch_word_audio(word)
        results.append(
            {
                "word": f"{word} [sound:{audio_filename}]",
                "translation": translation,
            }
        )

    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
    print()
    print(f"Done! Go check {OUTPUT_CSV}")


if __name__ == "__main__":
    process_csv(INPUT_CSV)
