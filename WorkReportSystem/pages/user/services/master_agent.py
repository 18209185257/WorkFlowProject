import requests
from common.db import OLLAMA_URL

def build_final_answer(
        question,
        results
):

    context = ""

    for k, v in results.items():

        context += f"""

===== {k} =====

{v}

"""

    prompt = f"""
你是企业项目管理AI总监。

用户问题：

{question}

下面是多个Agent结果：

{context}

请：

1. 汇总关键内容
2. 给出最终结论
3. 给出建议

输出中文。
"""

    response = requests.post(

        OLLAMA_URL,

        json={

            "model":"qwen2.5:7b",

            "prompt":prompt,

            "stream":False

        },

        timeout=300

    )

    result = response.json()

    return result.get(
        "response",
        "AI汇总失败"
    )