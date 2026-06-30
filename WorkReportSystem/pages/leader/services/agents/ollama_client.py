import requests
from common.db import OLLAMA_URL,MODEL_NAME

def call_ollama(
        prompt,
        model=MODEL_NAME
):

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        return (
            res.json()
            .get("response", "")
        )
    except Exception as e:

        return f"AI调用失败：{e}"