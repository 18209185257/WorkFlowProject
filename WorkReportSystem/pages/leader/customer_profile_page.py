import gradio as gr

from pages.leader.services.customer_profile_service import (
    build_customer_kpi_html,
    build_customer_amount_chart,
    build_customer_project_chart,
    build_customer_industry_chart,
    build_customer_active_chart,
    build_customer_risk_html,
    build_customer_ai_insight
)


def create_customer_profile_page():

    with gr.Column(
        visible=False,
        elem_id="page-customer_profile"
    ) as page:

        gr.HTML(
            "<div class='leader-page-title'>🏢 客户画像中心</div>"
        )

        kpi_html = gr.HTML(
            value=build_customer_kpi_html()
        )

        with gr.Row():

            amount_chart = gr.HTML(
                value=build_customer_amount_chart()
            )

            project_chart = gr.HTML(
                value=build_customer_project_chart()
            )

        with gr.Row():

            industry_chart = gr.HTML(
                value=build_customer_industry_chart()
            )

            active_chart = gr.HTML(
                value=build_customer_active_chart()
            )

        with gr.Row():

            risk_html = gr.HTML(
                value=build_customer_risk_html()
            )

            ai_html = gr.HTML(
                value=build_customer_ai_insight()
            )

    return (
        page,
        kpi_html,
        amount_chart,
        project_chart,
        industry_chart,
        active_chart,
        risk_html,
        ai_html
    )