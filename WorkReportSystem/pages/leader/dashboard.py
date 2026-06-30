import gradio as gr

from .home_page import *
from .project_page import *
from .risk_page import *
from .employee_page import *
from .customer_profile_page import *
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

from pages.leader.services.project_warning_service import (
    build_project_warning_html
)

from pages.leader.services.auto_ai_insight_service import (
    build_auto_ai_insight
)

from .weekly_report_page import create_weekly_report_page

from pages.leader.services.weekly_report_service import (
    build_weekly_report
)

from pages.leader.services.ai_weekly_report_service import (
    build_ai_weekly_report
)

from pages.leader.services.project_diagnosis_service import (
    project_diagnosis
)

from .project_diagnosis_page import create_project_diagnosis_page

from pages.leader.utils.page_router import (
    switch_page
)

from .employee_profile_page import (
    create_employee_profile_page
)

from .customer_profile_page import (
    create_customer_profile_page
)

from .analytics_page import *

from .ai_decision_page import create_ai_decision_page
from pages.leader.services.ai_decision_service import build_ai_decision

from .project_manager_page import create_project_manager_page

from pages.leader.services.agents.project_manager_agent import ai_project_manager

from .project_manager_page import (
    create_project_manager_page
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
                    "🏢 客户画像中心"
                )

                analytics_btn = gr.Button(
                    "📈 经营分析"
                )

                weekly_report_btn  = gr.Button(
                    "📋 AI周报"
                )

                project_manager_btn = gr.Button(
                    "🧠 AI项目经理"
                )

                diagnosis_menu_btn = gr.Button(
                    "🩺 AI项目诊断"
                )

                decision_menu_btn = gr.Button("🧠 AI经营决策")

                # report_center_btn = gr.Button(
                #     "📄 AI经营报告"
                # )

            with gr.Column(
                elem_id="leader_content"
            ) as content_column:

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

                # 创建weekly_report_page并确保被正确添加到DOM
                (
                    weekly_report_page,
                    generate_weekly_btn,
                    weekly_report_md
                ) = create_weekly_report_page()

                project_page = create_leader_project_page()

                risk_page = create_leader_risk_page()

                (
                    employee_profile_page,
                    employee_kpi_html,
                    workload_chart,
                    report_chart,
                    risk_html,
                    ai_insight_html
                ) = create_employee_profile_page()

                (
                    customer_profile_page,
                    customer_kpi_html,
                    customer_amount_chart,
                    customer_project_chart,
                    customer_industry_chart,
                    customer_active_chart,
                    customer_risk_html,
                    customer_ai_html
                ) = create_customer_profile_page()

                analytics_page = create_leader_analytics_page()

                report_page = create_leader_report_page()

                (
                    project_manager_page,
                    health_html,
                    auto_dispatch_btn,
                    dispatch_result,
                    pm_insight_html
                ) = create_project_manager_page()

                (
                    diagnosis_page,
                    diagnosis_project_name,
                    diagnosis_btn,
                    diagnosis_result
                ) = create_project_diagnosis_page()

                (
                    decision_page,
                    generate_decision_btn,
                    decision_md
                ) = create_ai_decision_page()

                all_pages = [

                    home_page,

                    ai_page,

                    project_page,

                    risk_page,

                    employee_profile_page,

                    customer_profile_page,

                    analytics_page,

                    report_page,

                    weekly_report_page,

                    project_manager_page,

                    diagnosis_page,

                    decision_page

                ]

                ai_ask_btn.click(
                    leader_agent,
                    inputs=[
                        username_state,
                        ai_question
                    ],
                    outputs=ai_answer
                )

                generate_weekly_btn.click(
                    build_ai_weekly_report,
                    outputs=weekly_report_md
                )

                diagnosis_btn.click(
                    project_diagnosis,
                    inputs=[
                        username_state,
                        diagnosis_project_name
                    ],
                    outputs=diagnosis_result
                )


        ai_float_panel = (
            create_ai_floating_panel_page()
        )

        home_btn.click(
            lambda: switch_page("home"),
            outputs=all_pages
        )

        ai_btn.click(
            lambda: switch_page("ai"),
            outputs=all_pages
        )

        project_btn.click(
            lambda: switch_page("project"),
            outputs=all_pages
        )

        risk_btn.click(
            lambda: switch_page("risk"),
            outputs=all_pages
        )

        employee_btn.click(
            lambda: switch_page("employee"),
            outputs=all_pages
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    500
                );
            }
            """
        )

        employee_btn.click(
            lambda: switch_page("employee_profile"),
            outputs=all_pages
        )

        customer_btn.click(
            lambda: switch_page("customer_profile"),
            outputs=all_pages
        ).then(
            fn=None,
            js="""
            ()=>{
                setTimeout(
                    renderLeaderCharts,
                    500
                );
            }
            """
        )

        analytics_btn.click(
            lambda: switch_page("analytics"),
            outputs=all_pages
        )

        weekly_report_btn.click(
            lambda: switch_page("weekly_report"),
            outputs=all_pages
        )

        diagnosis_menu_btn.click(
            lambda: switch_page("diagnosis"),
            outputs=all_pages
        )

        decision_menu_btn.click(
            lambda: switch_page("decision"),
            outputs=all_pages
        )

        project_manager_btn.click(
            lambda: switch_page(
                "project_manager"
            ),
            outputs=all_pages

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

        home_btn.click(
            build_project_warning_html,
            outputs=warning_html
        )

        home_btn.click(
            build_auto_ai_insight,
            outputs=ai_insight_html
        )

        generate_decision_btn.click(
            fn=build_ai_decision,
            inputs=[username_state],
            outputs=decision_md
        )

    return (
        dashboard,

        home_page,

        ai_page,

        project_page,

        risk_page,

        employee_profile_page,

        customer_profile_page,

        analytics_page,

        report_page,

        ai_float_panel,

        weekly_report_page,

        project_manager_page,

        diagnosis_page
    )