# Irish Learning Cards API

FastAPI integrating an NLP pipeline (scraping, LLM, audio) for generating Anki-ready learning cards from Irish words.

## Architecture

```
app/
├── main.py            # FastAPI entry point
├── config.py          # Environment variables & constants
├── models.py          # Pydantic request/response schemas
├── pipeline/
│   ├── scraper.py     # Scrape translations from teanglann.ie
│   ├── llm.py         # Generate definitions via OpenAI
│   └── audio.py       # Download & post-process audio files
└── routes/
    └── cards.py       # POST /cards, GET /cards/{word}, GET /cards/audio/{word}
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY
```

## Run

```bash
uvicorn app.main:app --reload
```

Docs available at `http://localhost:8000/docs`
