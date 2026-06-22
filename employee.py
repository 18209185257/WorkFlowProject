import os
# 关键：强制前端静态资源为https，解决混合内容被浏览器拦截
os.environ["GRADIO_ALLOW_HTTP_RESOURCES"] = "0"
os.environ["GRADIO_SERVER_URL"] = "http://98533gm8ut35.vicp.fun"
import gradio as gr
import requests
from datetime import datetime

API_HOST = "http://127.0.0.1:8000"
TOKEN = "WorkFlow2026"
today_str = datetime.now().strftime("%Y-%m-%d")

def submit_project(name, cycle_start, cycle_end, leader, participants, delay, risk_block, progress):
    cycle = f"{cycle_start} ~ {cycle_end}"
    data = {
        "token": TOKEN,
        "project_name": name,
        "project_cycle": cycle,
        "main_leader": leader,
        "participants": participants,
        "is_delay": delay,
        "risk_block": risk_block,
        "progress": progress
    }
    requests.post(f"{API_HOST}/api/add_project", data=data)

def submit_meeting(title, sponsor, attendees, meet_date, content, task_problem):
    if not meet_date:
        meet_date = today_str
    data = {
        "token": TOKEN,
        "meet_title": title,
        "sponsor": sponsor,
        "attendees": attendees,
        "meet_date": meet_date,
        "meet_content": content,
        "task_problem": task_problem
    }
    requests.post(f"{API_HOST}/api/add_meeting", data=data)

def submit_report(reporter, content, report_date, help_item):
    if not report_date:
        report_date = today_str
    data = {
        "token": TOKEN,
        "reporter": reporter,
        "report_content": content,
        "report_date": report_date,
        "help_item": help_item
    }
    requests.post(f"{API_HOST}/api/add_report", data=data)

# 精准适配当前Gradio标签样式CSS
css = """
h2 {
    text-align: center !important;
    font-weight: bold !important;
    color: #0056cc !important;
}
/* 选中Tab文字黑色 */
button[aria-selected="true"] {
    color: black !important;
}
/* 选中Tab底部下划线黑色，覆盖原有橙色 */
button[aria-selected="true"]::after {
    background-color: black !important;
}
"""

with gr.Blocks(title="员工工作上报系统", css=css) as demo:
    gr.Markdown("## 员工工作上报系统")
    with gr.Tabs():
        with gr.TabItem("项目汇报"):
            p_name = gr.Textbox(label="项目名称")
            with gr.Row():
                p_cycle_start = gr.DateTime(label="周期起始日期", type="date", value=today_str, include_time=False)
                p_cycle_end = gr.DateTime(label="周期结束日期", type="date", include_time=False)
            p_leader = gr.Textbox(label="项目主负责人")
            p_part = gr.Textbox(label="参与人及角色")
            p_delay = gr.Radio(["是", "否"], label="是否延期")
            p_risk = gr.Textbox(label="阻碍项、风险项")
            p_progress = gr.Textbox(label="项目进度")
            p_btn = gr.Button("提交")
            p_btn.click(submit_project, [p_name,p_cycle_start,p_cycle_end,p_leader,p_part,p_delay,p_risk,p_progress])

        with gr.TabItem("会议记录上传"):
            m_title = gr.Textbox(label="会议主题")
            m_sponsor = gr.Textbox(label="发起人")
            m_attend = gr.Textbox(label="参会人")
            m_date = gr.DateTime(label="会议日期", type="date", value=today_str, include_time=False)
            m_content = gr.Textbox(label="会议纪要", lines=6)
            m_task = gr.Textbox(label="Task进展/问题")
            m_btn = gr.Button("提交")
            m_btn.click(submit_meeting, [m_title,m_sponsor,m_attend,m_date,m_content,m_task])

        with gr.TabItem("日报上传"):
            r_user = gr.Textbox(label="汇报人")
            r_content = gr.Textbox(label="汇报内容（今日总结、明日计划）", lines=8)
            r_date = gr.DateTime(label="汇报日期", type="date", value=today_str, include_time=False)
            r_help = gr.Textbox(label="求助项", lines=3)
            r_btn = gr.Button("提交")
            r_btn.click(submit_report, [r_user,r_content,r_date,r_help])

demo.launch(
    server_name="0.0.0.0",
    server_port=7863,
    share=False,
    inbrowser=False,
)