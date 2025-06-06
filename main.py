import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

INPUT_CSV = "irish_words.csv"
OUTPUT_CSV = "irish_words_with_definitions.csv"
MISSING_CSV = "missing_words.csv"
AUDIO_DIR = "audio_files"
BASE_URL = "https://www.teanglann.ie/en/fgb/"
AUDIO_URL = "https://www.teanglann.ie/CanC/"

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    translation_text = translation.text.strip() if translation else None

    return translation_text


def fetch_word_audio(word):

    audio_filename = f"{word}.mp3"
    audio_url = AUDIO_URL + audio_filename
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    audio_response = requests.get(audio_url)

    if audio_response.status_code != 200:
        return None

    with open(audio_path, "wb") as f:
        f.write(audio_response.content)

    # Add 1 second of silence because Anki cuts the end of the audio :(
    audio = AudioSegment.from_file(audio_path)
    silence = AudioSegment.silent(duration=1000)  # 1 second of silence
    audio_with_silence = audio + silence
    audio_with_silence.export(audio_path, format="mp3")  # Overwrite original

    return audio_filename


def get_simple_definition(word):
    prompt = (
        f"Translate the Irish word '{word}' in simple English."
        "If needed, give an explanation. Make it 1-2 sentences, clear and beginner-friendly."
        "Don't put the Irish word in the response."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You're a helpful Irish language tutor.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error for word {word}: {e}")
        return None


def process_csv(input_csv):
    df = pd.read_csv(input_csv)

    if "word" not in df.columns:
        raise ValueError("CSV must have a column named 'word'.")

    words = [str(word).strip() for word in df["word"]]

    results = []
    missing_data = []

    for word in words:
        print(f"Processing: {word}")
        time.sleep(1)
        translation = fetch_word_data(word)
        audio_filename = fetch_word_audio(word)
        definition = get_simple_definition(word)

        if translation and audio_filename and definition:
            results.append(
                {
                    "word": f"{word} [sound:{audio_filename}]",
                    "translation": f"{translation}<br>{definition}",
                }
            )
        else:
            missing_data.append(
                {
                    "word": word,
                    "missing translation": (
                        "yes" if translation is None else translation
                    ),
                    "missing audio": (
                        "yes" if audio_filename is None else audio_filename
                    ),
                    "missing definition": ("yes" if definition is None else definition),
                }
            )

    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)

    print()
    print(f"Done! Go check {OUTPUT_CSV}")

    if missing_data:
        pd.DataFrame(missing_data).to_csv(MISSING_CSV, index=False)
        print(f"Missing data saved to {MISSING_CSV}")
    else:
        print("No missing data found!")


if __name__ == "__main__":
    process_csv(INPUT_CSV)
