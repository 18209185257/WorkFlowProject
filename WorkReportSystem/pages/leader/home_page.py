import gradio as gr
from pages.leader.services.leader_dashboard_service import (
    build_kpi_html
)
from pages.leader.services.leader_dashboard_service import (
    build_project_status_chart,
    build_project_trend_chart
)

from pages.leader.services.leader_dashboard_service import (
    build_daily_report_chart,
    build_risk_rank_html
)

from pages.leader.services.leader_dashboard_service import (
    build_ai_insight_html
)

from pages.leader.services.leader_dashboard_service import (
    build_auto_ai_insight
)

from pages.leader.services.warning_center_service import (
    build_warning_html
)

def create_leader_home_page():

    with gr.Column(
        visible=True,
        elem_id="leader_home"
    ) as page:

        gr.HTML("""
        <div class='leader-page-title'>
            🚀 AI智能驾驶舱
        </div>
        """)

        with gr.Row():
            kpi_html = gr.HTML(
                value=build_kpi_html()
            )

        with gr.Row():
            project_progress_chart = gr.HTML(
                value=build_project_trend_chart()
            )

            project_status_chart = gr.HTML(
                value=build_project_status_chart()
            )

        with gr.Row():
            ai_insight_html = gr.HTML(
                value=build_ai_insight_html()
            )

        with gr.Row():
            warning_html = gr.HTML(
                value=build_warning_html()
            )

        with gr.Row():
            auto_ai_html = gr.HTML(
                value=f"""

                <div class='leader-auto-ai'>

                {build_auto_ai_insight()}

                </div>

                """
            )

        with gr.Row():
            report_submit_chart = gr.HTML(
                value=build_daily_report_chart()
            )

            risk_rank_chart = gr.HTML(
                value=build_risk_rank_html()
            )

        ai_leader_box = gr.HTML(
            """
            <div class='leader-ai-entry'>
                🤖 AI领导助手
            </div>
            """
        )

    return (
        page,
        kpi_html,
        project_progress_chart,
        project_status_chart,
        ai_insight_html,
        warning_html,
        auto_ai_html,
        report_submit_chart,
        risk_rank_chart,
        ai_leader_box
    )