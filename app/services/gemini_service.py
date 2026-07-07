import json
import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


class GeminiServiceError(Exception):
    """
    Raised when Gemini cannot return a valid response.
    """


def get_model_status():
    """
    Return Gemini model configuration status.
    """

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    return {
        "provider": "Google Gemini",
        "model": model_name,
        "enabled": bool(api_key) and api_key != "your_google_api_key_here",
    }


def get_gemini_model():
    """
    Create and return the Gemini model.
    """

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    if not api_key or api_key == "your_google_api_key_here":
        raise GeminiServiceError(
            "GOOGLE_API_KEY is missing. Add your Gemini API key in the .env file."
        )

    genai.configure(api_key=api_key)

    return genai.GenerativeModel(model_name)


def extract_json_from_response(response_text):
    """
    Extract JSON from Gemini response text.
    Handles normal JSON and JSON inside markdown code blocks.
    """

    if not response_text:
        raise GeminiServiceError("Gemini returned an empty response.")

    cleaned_text = response_text.strip()

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text.replace("```json", "", 1).strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.replace("```", "", 1).strip()

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3].strip()

    start_index = cleaned_text.find("{")
    end_index = cleaned_text.rfind("}")

    if start_index == -1 or end_index == -1:
        raise GeminiServiceError("Gemini did not return valid JSON.")

    json_text = cleaned_text[start_index:end_index + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as error:
        raise GeminiServiceError(f"Gemini returned invalid JSON: {error}")


def generate_json(prompt):
    """
    Send a prompt to Gemini and return parsed JSON.
    """

    model = get_gemini_model()

    response = model.generate_content(prompt)

    response_text = getattr(response, "text", "")

    return extract_json_from_response(response_text)