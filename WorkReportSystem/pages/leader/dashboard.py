import gradio as gr

from .home_page import *
from .project_page import *
from .risk_page import *
from .employee_page import *
from .customer_page import *
from .analytics_page import *
from .report_page import *
from .ai_page import *
from pages.leader.services.leader_agent import (
    leader_agent
)

from pages.leader.components.ai_floating_panel import (
    create_ai_floating_panel_page
)

from pages.leader.services.leader_dashboard_service import (
    build_project_status_chart,
    build_project_trend_chart
)

from pages.leader.services.project_heatmap_service import (
    build_project_heatmap_html
)

from pages.leader.services.leader_dashboard_service import (
    build_daily_report_chart,
    build_risk_rank_html
)

from pages.leader.services.dashboard_refresh_service import (
    refresh_dashboard
)

def create_leader_dashboard(
        username_state
):

    with gr.Column(
        visible=False,
        elem_id="leader_dashboard"
    ) as dashboard:

        with gr.Row(
            elem_id="leader_main_layout",
            equal_height=False
        ):

            with gr.Column(
                elem_id="leader_sidebar"
            ):

                home_btn = gr.Button(
                    "🏠 首页驾驶舱"
                )

                ai_btn = gr.Button(
                    "🤖 AI领导助手"
                )

                project_btn = gr.Button(
                    "📁 项目管理"
                )

                risk_btn = gr.Button(
                    "⚠️ 风险预警"
                )

                employee_btn = gr.Button(
                    "👥 员工画像"
                )

                customer_btn = gr.Button(
                    "🏢 客户管理"
                )

                analytics_btn = gr.Button(
                    "📈 数据分析"
                )

                report_btn = gr.Button(
                    "📋 周报中心"
                )

            with gr.Column(
                elem_id="leader_content"
            ):

                (
                    home_page,
                    kpi_html,
                    project_progress_chart,
                    project_status_chart,
                    ai_insight_html,
                    warning_html,
                    project_heatmap_html,
                    report_submit_chart,
                    risk_rank_chart,
                ) = create_leader_home_page()

                (
                    ai_page,
                    ai_question,
                    ai_answer,
                    ai_ask_btn
                ) = create_leader_ai_page()

                project_page = create_leader_project_page()

                risk_page = create_leader_risk_page()

                employee_page = create_leader_employee_page()

                customer_page = create_leader_customer_page()

                analytics_page = create_leader_analytics_page()

                report_page = create_leader_report_page()

                ai_ask_btn.click(

                    leader_agent,

                    inputs=[
                        username_state,
                        ai_question
                    ],

                    outputs=ai_answer

                )
        ai_float_panel = (
            create_ai_floating_panel_page()
        )

        home_btn.click(
            build_project_trend_chart,
            outputs=project_progress_chart
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    300
                );
            }
            """
        )
        home_btn.click(
            build_project_status_chart,
            outputs=project_status_chart
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    300
                );
            }
            """
        )

        home_btn.click(
            build_project_heatmap_html,
            outputs=project_heatmap_html
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    300
                );
            }
            """
        )

        home_btn.click(
            build_daily_report_chart,
            outputs=report_submit_chart
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    300
                );
            }
            """
        )

        home_btn.click(
            build_risk_rank_html,
            outputs=risk_rank_chart
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    300
                );
            }
            """
        )
    return (
        dashboard,
        home_page,
        ai_page,
        project_page,
        risk_page,
        employee_page,
        customer_page,
        analytics_page,
        report_page,
        ai_float_panel
    )