
import requests
import re

def clean_text(text):
    # Remove numbering patterns like "1. ", "2. ", etc.
    text = re.sub(r'^\d+\.\s*', '', text)
    # Allow essential punctuation and alphanumeric characters, remove others
    return re.sub(r'[^a-zA-Z0-9\s.,?!\'\-:]', '', text)

'''def query_deepseek(prompt):
    url = "http://localhost:11434/api/generate"  # Change this if Ollama runs on a different port
    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        return response_json.get("response", "I couldn't understand that.")
    except Exception as e:
        return f"Error communicating with DeepSeek: {str(e)}"

'''


def query_deepseek(prompt, api_key):

    MODEL = "gemini-2.5-flash"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        data = requests.post(url, headers=headers, json=payload, timeout=20)
        data.raise_for_status()

        response = data.json()

        # Safely extract text response
        return response["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.HTTPError:
        return f"HTTP Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {e}"

