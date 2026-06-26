from .ai_service import (
    generate_ai_daily,
    generate_ai_weekly,
    generate_project_summary,
    generate_ai_meeting_summary,
    generate_ai_risk_report
)

from .ai_chat_service import generate_ai_chat
from .multi_agent_service import weekly_master_agent
from .employee_summary_service import (
    generate_employee_summary
)

TOOLS = {

     "daily": {
        "name":"AI日报生成",
        "desc":"生成今日日报",
        "func":generate_ai_daily,
        "need_question":False
    },

    "weekly": {
        "name": "AI周报生成",
        "desc":"生成AI周报",
        "func": generate_ai_weekly,
        "need_question":False
    },

    "project": {
        "name": "AI项目分析",
        "desc": "生成项目分析报告",
        "func": generate_project_summary,
        "need_question":False
    },

    "meeting": {
        "name": "AI会议纪要",
        "desc": "生成会议纪要",
        "func": generate_ai_meeting_summary,
        "need_question":False
    },

    "risk": {
        "name": "AI风险分析",
        "desc": "生成风险分析",
        "func": generate_ai_risk_report,
        "need_question":False
    },

    "chat": {
        "name": "AI问答",
        "desc": "AI问答",
        "func": generate_ai_chat,
        "need_question":True
    },

    "weekly_agent": {
        "name":"AI智能周报",
        "desc":"多Agent协同生成周报",
        "func":weekly_master_agent,
        "need_question":False
    },
    "employee_summary":{

        "func":
        generate_employee_summary

    },
}

def get_tool_list():

    result = []

    for k,v in TOOLS.items():

        result.append(
            {
                "key": k,
                "name": v["name"],
                "desc": v["desc"]
            }
        )

    return result
