from .leader_ai_services import (
    get_not_submit_report_users,
    get_high_risk_projects,
    get_employee_recent_work
)

from .leader_prompt import *

from pages.user.services.ai_chat_service import (
    generate_ai_chat
)

from pages.user.services.agent_service import (
    get_user_real_name,
    extract_real_name
)

from .leader_tool_registry import (
    TOOLS
)

from .leader_planner import (
    plan_leader_task
)


def leader_agent(
        username,
        question
):
    plans = plan_leader_task(
        question
    )

    if plans:

        task = plans[0]

        tool = TOOLS.get(task)

        if tool:
            return tool["func"](
                username
            )

    q = question.lower()

    if "没交日报" in q:

        users = (
            get_not_submit_report_users()
        )

        return (
            "今日未交日报人员：\n\n"
            +
            "\n".join(users)
        )

    if "风险" in q:

        rows = (
            get_high_risk_projects()
        )

        text = ""

        for p,r in rows:

            text += f"""
项目：
{p}

风险：
{r}

"""

        return text

    if "最近工作" in q:

        real_name = (
            extract_real_name(
                question
            )
        )

        work = (
            get_employee_recent_work(
                real_name
            )
        )

        prompt = build_employee_summary_prompt(
            real_name,
            work
        )

        return generate_ai_chat(
            username,
            prompt
        )

    return generate_ai_chat(
        username,
        question
    )