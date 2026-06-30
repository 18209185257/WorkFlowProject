import gradio as gr

from pages.leader.services.employee_profile_service import (
    build_employee_kpi_html,
    build_employee_workload_chart,
    build_employee_report_chart,
    build_employee_risk_html,
    build_employee_ai_insight
)


def create_employee_profile_page():

    with gr.Column(
        visible=False,
        elem_id="page-employee_profile"
    ) as page:

        gr.HTML(
            """
            <div class='leader-page-title'>
                👥 员工画像中心
            </div>
            """
        )

        employee_kpi_html = gr.HTML(
            value=build_employee_kpi_html()
        )

        with gr.Row():

            workload_chart = gr.HTML(
                value=build_employee_workload_chart()
            )

            report_chart = gr.HTML(
                value=build_employee_report_chart()
            )

        with gr.Row():

            risk_html = gr.HTML(
                value=build_employee_risk_html()
            )

            ai_insight_html = gr.HTML(
                value=build_employee_ai_insight()
            )

    return (
        page,
        employee_kpi_html,
        workload_chart,
        report_chart,
        risk_html,
        ai_insight_html
    )