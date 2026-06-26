import requests
import gradio as gr

from common.config import API_HOST
from common.config import TOKEN,TODAY



def submit_project(
    project_name,
    cycle_start,
    cycle_end,
    leader,
    participants,
    delay,
    risk_block,
    progress
):
    data = {
        "token": TOKEN,
        "project_name": project_name,
        "project_cycle": f"{cycle_start} ~ {cycle_end}",
        "main_leader": leader,
        "participants": participants,
        "is_delay": delay,
        "risk_block": risk_block,
        "progress": progress
    }

    requests.post(
        f"{API_HOST}/api/add_project",
        data=data
    )

    return "✅ 项目提交成功"


def submit_meeting(
    title,
    sponsor,
    attendees,
    meet_date,
    content,
    task_problem
):
    if not content.strip():
        raise gr.Error(
            "会议纪要不能为空"
        )
    data = {
        "token": TOKEN,
        "meet_title": title,
        "sponsor": sponsor,
        "attendees": attendees,
        "meet_date": meet_date,
        "meet_content": content,
        "task_problem": task_problem
    }

    requests.post(
        f"{API_HOST}/api/add_meeting",
        data=data
    )

    gr.Info("会议记录提交成功")

    return (
        "",
        "",
        "",
        TODAY,
        "",
        ""
    )


def submit_report(
    reporter,
    content,
    report_date,
    help_item
):
    if not content or not content.strip():
        raise gr.Error("工作内容不能为空！")

    data = {
        "token": TOKEN,
        "reporter": reporter,
        "report_content": content,
        "report_date": report_date,
        "help_item": help_item
    }

    requests.post(
        f"{API_HOST}/api/add_report",
        data=data
    )

    return (
        "",
        TODAY,
        "",
        gr.Info("日报提交成功")
    )