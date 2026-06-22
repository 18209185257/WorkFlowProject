import gradio as gr

from common.config import TODAY
from services.report_service import submit_meeting


def create_meeting_page():

    with gr.Column(
        visible=False,
        elem_id="meeting",
        elem_classes=["page-container"]
    ) as page:
        gr.HTML("""
        <div class="breadcrumb">
            工作台 &gt; 会议记录上传
        </div>
        """)

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                📋 基础信息
            </div>
            """)

            with gr.Row():
                title = gr.Textbox(label="会议主题")
                sponsor = gr.Textbox(label="发起人")

            with gr.Row():
                attendees = gr.Textbox(label="参会人")

                meet_date = gr.Textbox(
                    label="会议日期",
                    value=TODAY
                )

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                📝 会议内容
            </div>
            """)

            content = gr.Textbox(
                label="会议纪要",
                lines=8
            )

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                🎯 会议结论
            </div>
            """)

            task_problem = gr.Textbox(
                label="Task进展 / 问题",
                lines=4
            )

        with gr.Row(elem_classes=["action-row"]):
            back_btn = gr.Button(
                "返回工作台",
                elem_classes=["back-btn"]
            )

            submit_btn = gr.Button(
                "🚀 提交会议记录",
                variant="primary",
                elem_classes=["submit-btn"]
            )

            submit_btn.click(
                submit_meeting,
                [
                    title,
                    sponsor,
                    attendees,
                    meet_date,
                    content,
                    task_problem
                ],
                [
                    title,
                    sponsor,
                    attendees,
                    meet_date,
                    content,
                    task_problem
                ]
            )

    return (
        page,
        back_btn
    )