# ui/page.py

import gradio as gr

from WorkReportSystem.pages.leader.ai.chat_service import (
    user_send_msg,
    ai_reply,
    init_welcome
)


def build_page():

    with gr.Column(visible=False) as workflow_ai_page:

        gr.HTML("""
        <div class="header-wrap">
            <h1>🤖 华智瑞森特工作流智能AI查询系统</h1>
            <p>⚡项目进展/进度｜员工日报｜会议纪要</p>
        </div>
        """)

        chatbot = gr.Chatbot(
            value=init_welcome(),
            elem_classes = ["ai-chatbot"]
        )

        msg = gr.Textbox()

        back_ai = gr.Button("返回")

        msg.submit(
            user_send_msg,
            [msg, chatbot],
            [msg, chatbot]
        ).then(
            ai_reply,
            [msg, chatbot],
            [chatbot]
        )

    return (
        workflow_ai_page,
        chatbot,
        msg,
        back_ai
    )