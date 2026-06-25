import requests
from common.db import OLLAMA_URL

def call_model(
        model,
        prompt,
        timeout=300
):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=timeout
    )
    result = response.json()

    return result.get(
        "response",
        ""
    )