"""
LLM module — generates beginner-friendly definitions via OpenAI.
"""

from typing import Optional

from openai import OpenAI

from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def get_definition(word: str) -> Optional[str]:
    prompt = (
        f"Translate the Irish word '{word}' in simple English."
        "If needed, give an explanation. Make it 1-2 sentences, clear and beginner-friendly."
        "Don't put the Irish word in the response."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a helpful Irish language tutor."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        content = response.choices[0].message.content
        return content.strip() if content else None
    except Exception as e:
        print(f"OpenAI error for '{word}': {e}")
        return None
