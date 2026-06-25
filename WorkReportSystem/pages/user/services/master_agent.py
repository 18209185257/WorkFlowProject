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

        请输出最终结论。
        """
        requests.post(
            OLLAMA_URL
        )