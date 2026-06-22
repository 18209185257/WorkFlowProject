import json
import requests

from ..leader_config import *
def check_ollama_online():
    try:
        res = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        return res.status_code == 200
    except Exception:
        return False

# 【核心修复：删除异常过滤代码，正常返回token】
def ollama_stream(prompt, temperature=0.3, num_ctx=1024):
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "temperature": temperature,
        "num_ctx": num_ctx
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT, stream=True)
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            obj = json.loads(line)
            chunk = obj.get("response", "")
            if chunk:
                yield chunk
        except:
            continue