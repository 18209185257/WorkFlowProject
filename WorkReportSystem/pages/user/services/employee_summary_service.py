from common.db import get_project_conn,OLLAMA_URL
import requests

def generate_employee_summary(username):

    conn = get_project_conn()
    cur = conn.cursor()

    # 1️⃣ 查日报
    cur.execute("""
        select content
        from submit_report
        where username=?
        order by id desc
        limit 10
    """, (username,))

    reports = cur.fetchall()

    # 2️⃣ 查会议
    cur.execute("""
        select content
        from meeting_report
        where username=?
        order by id desc
        limit 10
    """, (username,))

    meetings = cur.fetchall()

    conn.close()

    # 3️⃣ 组装RAG上下文
    context = "员工真实数据如下：\n\n"

    context += "【日报】\n"
    for r in reports:
        context += f"- {r[0]}\n"

    context += "\n【会议】\n"
    for m in meetings:
        context += f"- {m[0]}\n"

    # 4️⃣ 强制模型基于数据回答（关键）
    prompt = f"""
你是企业AI分析系统，只能基于真实数据总结，不允许编造。

数据如下：

{context}

请生成：
- 工作总结
- 关键成果
- 问题分析
- 下一步计划
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]