import gradio as gr

from .services.business_dashboard_service import (
    get_business_stats,
    get_delay_projects,
    get_risk_projects
)


def create_business_dashboard_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📊 经营驾驶室</h2>"
        )
        gr.Markdown("### 🔴 延期项目")

        delay_df = gr.Dataframe(
            value=get_delay_projects(),
            headers=[
               "项目名称",
               "负责人"
            ]
        )

        gr.Markdown("### 🟠 风险项目")

        risk_df = gr.Dataframe(
            value=get_risk_projects(),
            headers=[
                "项目名称",
                "负责人",
                "风险"
            ]
        )

        btn_back = gr.Button(
            "返回管理后台"
        )

    return (
        page,
        btn_back
    )
