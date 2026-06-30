import gradio as gr

from pages.leader.services.business_analysis_service import (
    build_business_kpi_html,
    build_project_trend_chart,
    build_customer_growth_chart,
    build_risk_trend_chart,
    build_employee_activity_chart,
    build_business_ai_html
)


def create_leader_analytics_page():

    with gr.Column(
        visible=False,
        elem_id="page-analytics"
    ) as page:

        gr.HTML(
            "<div class='leader-page-title'>📈经营分析中心</div>"
        )

        kpi_html = gr.HTML(
            value=build_business_kpi_html()
        )

        with gr.Row():

            project_growth = gr.HTML(
                value=build_project_trend_chart()
            )

            customer_growth = gr.HTML(
                value=build_customer_growth_chart()
            )

        with gr.Row():

            risk_chart = gr.HTML(
                value=build_risk_trend_chart()
            )

            employee_chart = gr.HTML(
                value=build_employee_activity_chart()
            )

        ai_html = gr.HTML(
            value=build_business_ai_html()
        )

    return page