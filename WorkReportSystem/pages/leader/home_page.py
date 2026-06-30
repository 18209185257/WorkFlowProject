import gradio as gr
from pages.leader.services.leader_dashboard_service import (
    build_kpi_html
)
from pages.leader.services.leader_dashboard_service import (
    build_project_status_chart,
    build_project_trend_chart
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

from pages.leader.services.project_heatmap_service import (
    build_project_heatmap_html
)

from pages.leader.services.leader_dashboard_service import (
    build_daily_report_chart,
    build_risk_rank_html
)

from pages.leader.services.project_warning_service import (
    build_project_warning_html
)

from pages.leader.services.auto_ai_insight_service import (
    build_auto_ai_insight
)

def create_leader_home_page():

    with gr.Column(
        visible=True,
        elem_id="leader_home"
    ) as page:

        # KPI
        kpi_html = gr.HTML(
            value=build_kpi_html(),
            elem_classes=["leader-kpi-row"]
        )

        # 项目趋势 + 项目状态
        with gr.Row(
            elem_classes=["leader-grid-row"]
        ):

            project_progress_chart = gr.HTML(
                value=build_project_trend_chart(),
                elem_classes=["leader-card"]
            )

            project_status_chart = gr.HTML(
                value=build_project_status_chart(),
                elem_classes=["leader-card"]
            )

        # AI洞察 + AI预警
        with gr.Row(
            elem_classes=["leader-grid-row"]
        ):

            ai_insight_html = gr.HTML(
                value= build_auto_ai_insight(),
                elem_classes=["leader-card"]
            )

            warning_html = gr.HTML(
                value=build_project_warning_html(),
                elem_classes=["leader-card"]
            )

        # 项目热力图（全宽）
        project_heatmap_html = gr.HTML(
            value=build_project_heatmap_html(),
            elem_classes=["leader-card-full"]
        )

        # 日报趋势 + 风险排行
        with gr.Row(
            elem_classes=["leader-grid-row"]
        ):

            report_submit_chart = gr.HTML(
                value=build_daily_report_chart(),
                elem_classes=["leader-card"]
            )

            risk_rank_chart = gr.HTML(
                value=build_risk_rank_html(),
                elem_classes=["leader-card"]
            )

    return (
        page,
        kpi_html,
        project_progress_chart,
        project_status_chart,
        ai_insight_html,
        warning_html,
        project_heatmap_html,
        report_submit_chart,
        risk_rank_chart,
    )