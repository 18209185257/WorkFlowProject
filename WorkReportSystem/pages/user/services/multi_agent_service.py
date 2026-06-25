import requests
from common.db import OLLAMA_URL

from .ai_service import (
    generate_ai_daily,
    generate_ai_meeting_summary,
    generate_project_summary,
    generate_ai_risk_report
)

#日报agent
def daily_agent(username):

    return generate_ai_daily(
        username
    )

#会议agent
def meeting_agent(username):

    return generate_ai_meeting_summary(
        username
    )

#项目agent
def project_agent(username):

    return generate_project_summary(
        username
    )

#风险agent
def risk_agent(username):

    return generate_ai_risk_report(
        username
    )

#Master Agent
def weekly_master_agent(
        username
):
    daily_result = daily_agent(
        username
    )

    meeting_result = meeting_agent(
        username
    )

    project_result = project_agent(
        username
    )

    risk_result = risk_agent(
        username
    )

    context = f"""
    日报分析：

    {daily_result}

    会议分析：

    {meeting_result}

    项目分析：

    {project_result}

    风险分析：

    {risk_result}
    """

    prompt = f"""
    你是企业项目管理总监。

    请根据以下多个Agent分析结果，

    生成：

    本周工作总结

    本周成果

    问题与风险

    下周计划

    ================

    {context}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()[
        "response"
    ]

