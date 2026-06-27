from common.db import get_project_conn
from pages.user.services.ai_chat_service import (
    generate_ai_chat
)


def get_weekly_context():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select report_content
    from daily_report
    order by id desc
    limit 50
    """)

    reports = "\n".join(
        x[0]
        for x in cur.fetchall()
    )

    cur.execute("""
    select meet_content
    from meeting
    order by id desc
    limit 20
    """)

    meetings = "\n".join(
        x[0]
        for x in cur.fetchall()
    )

    conn.close()

    return f"""

日报：

{reports}

会议：

{meetings}

"""

#领导周报
def generate_leader_weekly_report(
        username
):

    context = get_weekly_context()

    prompt = f"""
你是企业领导周报助手。

数据如下：

{context}

请输出：

# 本周工作总结

# 项目进展

# 风险问题

# 会议情况

# 下周计划

要求：

正式汇报风格。
"""

    return generate_ai_chat(
        username,
        prompt
    )

