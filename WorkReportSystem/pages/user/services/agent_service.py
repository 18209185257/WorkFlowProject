from pages.user.ai_assistant.ai_service import (
    generate_ai_daily,
    generate_ai_weekly,
)

from .planner_agent import (
    plan_task
)

from .executor_agent import (
    execute_plans
)

from .master_agent import (
    build_final_answer
)

from common.db import get_project_conn

import re

from .ai_service import (
    generate_project_summary,
    generate_ai_risk_report,
    generate_ai_meeting_summary,
)
from .ai_chat_service import generate_ai_chat

from .tool_registry import TOOLS

def detect_task(
        question
):
    question = question.lower()
    if "日报" in question:
        return "daily"

    if (
        "周报" in question
        or
        "工作总结" in question
        or
        "本周总结" in question
    ):
        return "weekly_agent"

    if "项目" in question:
        return "project"

    if "风险" in question:
        return "risk"

    if "会议" in question:
        return "meeting"

    return "chat"

def ai_agent(
        username,
        question
):
    print(
        "======== AI_AGENT ========"
    )

    print(
        username
    )

    print(
        question
    )

    target_name = extract_real_name(
        question
    )

    if target_name:
        username = target_name

    plans = plan_task(
        question
    )

    print(
        "任务规划:",
        plans
    )

    results = execute_plans(
        username,
        question,
        plans
    )

    print(
        "执行结果:",
        results
    )

    return build_final_answer(
        question,
        results
    )

def execute_tool(
        task,
        username,
        question
):

    tool = TOOLS.get(task)

    if not tool:

        return "未找到工具"

    func = tool["func"]

    if task == "chat":

        return func(
            username,
            question
        )

    return func(
        username
    )

def extract_name(question):

    stop_words = [

        "工作总结",

        "最近工作",

        "近期工作",

        "本周工作",

        "本月工作",

        "工作情况",

        "工作概览",

        "工作汇报",

        "总结",

        "的"

    ]

    q = question

    for word in stop_words:

        q = q.replace(
            word,
            ""
        )

    q = q.strip()

    names = re.findall(

        r'[\u4e00-\u9fa5]{2,4}',

        q

    )

    if names:

        return names[0]

    return None


def extract_real_name(
        question
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select real_name
        from user
        """
    )

    users = cur.fetchall()

    conn.close()

    for row in users:

        real_name = row[0]

        if (
            real_name
            and
            real_name in question
        ):
            return real_name

    return None

def get_user_real_name(username, question):

    # 1️⃣ 优先：问题中匹配真实姓名
    real_name = extract_real_name(question)

    if real_name:
        return real_name

    # 2️⃣ fallback：登录用户
    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select real_name
        from user
        where username=?
    """, (username,))

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return username