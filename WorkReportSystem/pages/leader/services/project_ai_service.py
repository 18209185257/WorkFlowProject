import requests

from common.db import (
    OLLAMA_URL,
    MODEL_NAME
)

from .project_progress_service import (
    get_project_progress_for_ai
)

def generate_project_ai_report(project_id):
    rows = get_project_progress_for_ai(
        project_id
    )
    content = ""
    for row in rows:
        content += f"""
汇报人：{row[0]}

项目进展：
{row[1]}

风险：
{row[2]}

下一步：
{row[3]}

==================
"""

    prompt = f"""
你是项目管理专家。

根据以下项目进展记录，

请输出：

一、本周工作总结

二、风险分析

三、下周计划

四、项目健康度

评分规则：

90-100 健康

70-89 关注

50-69 风险

50以下 严重风险

项目数据：

{content}
"""

    try:

        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        return r.json()["response"]

    except Exception as e:

        return str(e)

