import gradio as gr

from pages.leader.services.project_manager.ai_task_service import (
    detect_project_risk
)


def create_leader_risk_page():

    risks = detect_project_risk()

    risk_text = "\n\n".join(
        [
            r["risk_text"]
            for r in risks
        ]
    )

    with gr.Column(
        visible=False,
        elem_id="page-risk"
    ) as page:

        gr.HTML(
            "<h2>⚠️ 风险预警中心</h2>"
        )

        risk_md = gr.Markdown(
            value=risk_text
        )

    return page