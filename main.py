import pandas as pd

INPUT_CSV = "irish_words.csv"
OUTPUT_CSV = "irish_words_with_definitions.csv"
AUDIO_DIR = "audio_files"
BASE_URL = "https://www.teanglann.ie/en/fgb/"


def process_csv(input_csv):
    df = pd.read_csv(input_csv)

    if "word" not in df.columns:
        raise ValueError("CSV must have a column named 'word'.")

    words = [str(word).strip() for word in df["word"]]

    results = []
    for word in words:
        print(f"Processing: {word}")
        # Process word
        results.append(
            {
                "word": word,
                "translation": "translation",
            }
        )

    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
    print()
    print(f"Done! Go check {OUTPUT_CSV}")


if __name__ == "__main__":
    process_csv(INPUT_CSV)
