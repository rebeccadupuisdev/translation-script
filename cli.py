"""
CLI entry point for batch-processing a CSV of Irish words.

Usage:
    python cli.py
    python cli.py --input my_words.csv --output results.csv --missing missing.csv
"""

import argparse
import time

import pandas as pd

from app.config import AUDIO_DIR
from app.pipeline.audio import fetch_audio
from app.pipeline.llm import get_definition
from app.pipeline.scraper import fetch_translation

import os

DEFAULT_INPUT = "irish_words.csv"
DEFAULT_OUTPUT = "irish_words_with_definitions.csv"
DEFAULT_MISSING = "missing_words.csv"


def process_csv(input_csv: str, output_csv: str, missing_csv: str) -> None:
    df = pd.read_csv(input_csv)

    if "word" not in df.columns:
        raise ValueError("CSV must have a column named 'word'.")

    words = [str(w).strip() for w in df["word"]]
    results = []
    missing_data = []

    for word in words:
        print(f"Processing: {word}")
        time.sleep(1)

        translation = fetch_translation(word)
        definition = get_definition(word)
        audio_filename = fetch_audio(word)

        if translation and definition and audio_filename:
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
                    "missing_translation": "yes" if translation is None else translation,
                    "missing_audio": "yes" if audio_filename is None else audio_filename,
                    "missing_definition": "yes" if definition is None else definition,
                }
            )

    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"\nDone! Results saved to {output_csv}")

    if missing_data:
        pd.DataFrame(missing_data).to_csv(missing_csv, index=False)
        print(f"Missing data saved to {missing_csv}")
    else:
        print("No missing data found!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-process Irish words from a CSV.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Input CSV path (needs a 'word' column)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output CSV path")
    parser.add_argument("--missing", default=DEFAULT_MISSING, help="Missing-data CSV path")
    args = parser.parse_args()

    os.makedirs(AUDIO_DIR, exist_ok=True)
    process_csv(args.input, args.output, args.missing)


if __name__ == "__main__":
    main()
