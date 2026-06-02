import json
import os
from dotenv import load_dotenv
from google import genai

from src.llm.prompts import build_extraction_prompt


def clean_llm_json_output(raw_text: str) -> str:
    text = raw_text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    return text


def extract_transactions(user_input: str) -> dict:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise ValueError("GEMINI_API_KEY belum ditemukan. Cek file .env kamu.")

    client = genai.Client(api_key=api_key)
    prompt = build_extraction_prompt(user_input)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )

    raw_text = response.text.strip()
    cleaned_text = clean_llm_json_output(raw_text)

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM tidak mengembalikan JSON valid.\n\nOutput mentah:\n{raw_text}\n\nOutput setelah dibersihkan:\n{cleaned_text}"
        ) from exc