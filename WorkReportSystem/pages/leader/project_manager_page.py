import gradio as gr

from pages.leader.services.project_manager.pm_service import (
    build_project_health_html,
    build_pm_insight
)

from pages.leader.services.project_manager.ai_task_service import (
    auto_create_tasks
)


def create_project_manager_page():

    with gr.Column(
        visible=False,
        elem_id="page-project_manager"
    ) as page:

        gr.HTML("""
        <h2>
        🧠 AI项目经理中心
        </h2>
        """)

        health_html = gr.HTML(
            value=build_project_health_html()
        )

        auto_dispatch_btn = gr.Button(
            "🚀 AI自动派发任务"
        )

        dispatch_result = gr.Markdown()

        pm_insight_html = gr.HTML(
            value=build_pm_insight()
        )

        auto_dispatch_btn.click(

            auto_create_tasks,

            outputs=dispatch_result

        )

    return (
        page,
        health_html,
        auto_dispatch_btn,
        dispatch_result,
        pm_insight_html
    )