from pages.user.ai_assistant.ai_db import (
        get_user_daily_reports,
        get_user_meetings,
        get_user_project_progress
)
from pages.user.ai_assistant.ai_prompt import build_daily_prompt,build_weekly_prompt

def generate_ai_daily(real_name):

    reports = \
        get_user_daily_reports(
            real_name,
            5
        )

    meetings = \
        get_user_meetings(
            real_name,
            5
        )

    progresses = \
        get_user_project_progress(
            real_name
        )

    prompt = \
        build_daily_prompt(
            reports,
            meetings,
            progresses
        )

    return prompt


def ai_meeting(text):

    return f"""
【AI会议纪要】

会议内容：

{text}

待办事项：

1、任务分配
2、进度跟踪
3、风险处理
"""


def generate_ai_weekly(real_name):

    reports = \
        get_user_daily_reports(
            real_name,
            50
        )

    meetings = \
        get_user_meetings(
            real_name,
            20
        )

    progresses = \
        get_user_project_progress(
            real_name
        )

    return build_weekly_prompt(
        reports,
        meetings,
        progresses
    )


def ai_project(project_name):

    return f"""
项目：

{project_name}

AI分析：

1、项目状态正常

2、建议持续跟踪关键节点

3、定期同步风险
"""

def generate_weekly_report(user):
    pass
    return f"""
        开发中
    """

def generate_project_analysis(user):
    pass


def generate_risk_analysis(user):
    pass