import gradio as gr

from pages.leader.services.ai_decision_service import (
    build_ai_decision
)


def create_ai_decision_page():

    with gr.Column(
        visible=False,
        elem_id="page-ai_decision"
    ) as page:

        gr.HTML("""
        <h2>🧠 AI经营决策中心</h2>
        """)

        run_btn = gr.Button("生成AI经营决策")

        output = gr.Markdown()

    return page, run_btn, output