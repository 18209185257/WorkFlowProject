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
    if not question:
        return "请输入问题"

    plans = plan_task(
        question
    )

    results = execute_plans(
        username,
        question,
        plans
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
