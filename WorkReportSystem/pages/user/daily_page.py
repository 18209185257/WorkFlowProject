import gradio as gr

from common.config import TODAY
from services.report_service import submit_report


def create_daily_page():

    with gr.Column(
        visible=False,
        elem_id="daily",
        elem_classes=["page-container"]
    ) as page:
        gr.HTML("""
        <div class="breadcrumb">
            工作台 &gt; 日报上传
        </div>
        """)

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                📋 基础信息
            </div>
            """)

            with gr.Row():
                reporter = gr.Textbox(
                    label="汇报人",
                    interactive=False
                )

                report_date = gr.Textbox(
                    label="汇报日期",
                    value=TODAY
                )

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                📝 工作内容
            </div>
            """)

            content = gr.Textbox(
                label="今日总结 / 明日计划",
                lines=5
            )

        with gr.Group(elem_classes=["section-card"]):
            gr.HTML("""
            <div class="card-header">
                ⚠ 需要协助事项
            </div>
            """)

            help_item = gr.Textbox(
                label="求助项",
                lines=2
            )

        # result = gr.Textbox(
        #     label="提交结果",
        #     interactive=False
        # )

        with gr.Row(elem_classes=["action-row"]):
            back_btn = gr.Button(
                "返回工作台",
                elem_classes=["back-btn"]
            )

            submit_btn = gr.Button(
                "🚀 提交日报",
                variant="primary",
                elem_classes=["submit-btn"]
            )

            submit_btn.click(
                submit_report,
                [
                    reporter,
                    content,
                    report_date,
                    help_item
                ],
                None
            )

    return (
        page,
        reporter,
        back_btn
    )