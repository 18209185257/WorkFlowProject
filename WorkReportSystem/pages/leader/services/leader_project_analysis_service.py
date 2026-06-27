from common.db import get_project_conn

from pages.user.services.ai_chat_service import (
    generate_ai_chat
)


def generate_project_analysis(
        username
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        project_name,

        main_leader,

        progress,

        is_delay,

        risk_block

    from project
    """)

    rows = cur.fetchall()

    conn.close()

    context = ""

    for row in rows:

        context += f"""
项目：

{row[0]}

负责人：

{row[1]}

进展：

{row[2]}

延期：

{row[3]}

风险：

{row[4]}

"""

    prompt = f"""
你是企业项目管理总监。

请根据以下项目数据：

{context}

输出：

1、项目总体情况

2、延期项目

3、高风险项目

4、重点关注项目

5、管理建议
"""

    return generate_ai_chat(
        username,
        prompt
    )