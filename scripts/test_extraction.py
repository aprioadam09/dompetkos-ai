import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise ValueError("GEMINI_API_KEY belum ditemukan. Cek file .env kamu.")

    client = genai.Client(api_key=api_key)

    prompt = """
    Kamu adalah sistem test koneksi API.
    Jawab hanya dengan kalimat berikut, tanpa tambahan lain:

    Gemini API berhasil terhubung.
    """

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    print(response.text)


if __name__ == "__main__":
    main()