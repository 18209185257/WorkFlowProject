import json
import requests

from ..leader_config import (
    OLLAMA_URL,
    OLLAMA_TAG_URL,
    LLM_MODEL_NAME,
    OLLAMA_TIMEOUT
)


def check_ollama_online():
    """
    检查Ollama是否在线
    """

    try:

        res = requests.get(
            OLLAMA_TAG_URL,
            timeout=3
        )

        return res.status_code == 200

    except Exception:

        return False


USE_LLM = check_ollama_online()


def ollama_stream(
    prompt,
    temperature=0.3,
    num_ctx=1024
):
    """
    Ollama流式输出
    """

    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "temperature": temperature,
        "num_ctx": num_ctx
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=OLLAMA_TIMEOUT,
        stream=True
    )

    for line in response.iter_lines(
        decode_unicode=True
    ):

        if not line:
            continue

        try:

            obj = json.loads(line)

            chunk = obj.get(
                "response",
                ""
            )

            if chunk:
                yield chunk

        except Exception:
            continue


def normal_ai_answer_stream(question):
    """
    普通聊天
    """

    if not USE_LLM:

        yield "【AI离线】"

        return

    prompt = f"""
你是工作数据查询助手，仅简洁回答用户普通问题。

用户问题：
{question}

要求：
简洁精准回答。
"""

    answer = ""

    try:

        for chunk in ollama_stream(
            prompt,
            temperature=0.3,
            num_ctx=512
        ):

            answer += chunk

            yield answer

    except Exception:

        yield "回答失败"
