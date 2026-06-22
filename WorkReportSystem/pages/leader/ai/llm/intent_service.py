import json
import requests

from pages.leader.leader_config import (
    OLLAMA_URL,
    LLM_MODEL_NAME,
    OLLAMA_TIMEOUT
)

from ..ollama_service import USE_LLM

def llm_parse_question(
    user_question
    ):
    if not USE_LLM:
        return {
            "type":"report",
            "name":"",
            "is_week":False,
            "start_date":""
        }
    prompt = f"""
    分类规则：
    
    项目相关：
    project
    
    会议相关：
    meet
    
    工作日报相关：
    report
    
    输出JSON：
    
    {{
    "type":"",
    "name":"",
    "is_week":false,
    "start_date":""
    }}
    
    问题：
    
    {user_question}
    """

    try:

        payload = {
            "model":LLM_MODEL_NAME,
            "prompt":prompt,
            "stream":False,
            "temperature":0
        }

        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )

        raw = res.json()["response"]

        start = raw.find("{")
        end = raw.rfind("}")

        return json.loads(
            raw[start:end+1]
        )

    except Exception:

        return {
            "type":"report",
            "name":"",
            "is_week":False,
            "start_date":""
        }
