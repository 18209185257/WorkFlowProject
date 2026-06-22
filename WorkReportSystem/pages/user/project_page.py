import gradio as gr
from common.config import TODAY
from services.report_service import submit_project
from pages.leader.ai.services.project_service import query_all_project
from pages.user.services.my_project_service import query_project_info

def create_project_page():

    with gr.Column(
        visible=False,
        elem_id="projectReport",
        elem_classes=["project-page"]
    ) as page:

        with gr.Column(
            elem_classes=["project-content"]
        ):

            gr.HTML("""
            <div class="breadcrumb">
                工作台 &gt; 项目汇报
            </div>
            """)

            # =====================
            # 项目概览
            # =====================

            with gr.Group(
                elem_classes=["project-summary-card"]
            ):

                gr.HTML("""
                <div class="card-header">
                    📋 项目概览
                </div>
                """)

                project_name = gr.Dropdown(
                    label="项目名称",
                    choices=load_project_names(),
                    value="",
                    interactive=True,
                    info="请选择项目"
                )

                with gr.Row():

                    leader = gr.Textbox(
                        label="项目负责人"
                    )

                    cycle_start = gr.Textbox(
                        label="开始日期",
                        value=TODAY
                    )

                    cycle_end = gr.Textbox(
                        label="结束日期"
                    )

                participants = gr.Textbox(
                    label="参与人员（逗号分隔）"
                )

                project_name.change(
                    fn=query_project_info,
                    inputs=project_name,
                    outputs=[
                        leader,
                        cycle_start,
                        cycle_end,
                        participants
                    ]
                )

            # =====================
            # 项目进展
            # =====================

            with gr.Row():

                with gr.Column(scale=3):

                    with gr.Group(
                        elem_classes=["section-card"]
                    ):

                        gr.HTML("""
                        <div class="card-header">
                            📈 项目进展
                        </div>
                        """)

                        progress = gr.Textbox(
                            lines=10,
                            label="项目完成情况"
                        )

                with gr.Column(scale=2):

                    with gr.Group(
                        elem_classes=["section-card"]
                    ):

                        gr.HTML("""
                        <div class="card-header">
                            ⚠ 风险阻碍
                        </div>
                        """)

                        delay = gr.Radio(
                            ["是", "否"],
                            value="否",
                            label="是否延期"
                        )

                        risk_block = gr.Textbox(
                            lines=6,
                            label="风险说明"
                        )

            # =====================
            # 按钮
            # =====================

            with gr.Row():

                back_btn = gr.Button(
                    "返回工作台",
                    elem_classes=["back-btn"]
                )

                submit_btn = gr.Button(
                    "🚀 提交项目汇报",
                    variant="primary",
                    elem_classes=["submit-btn"]
                )

            # =====================
            # 提交包装函数
            # =====================

            def submit_project_wrapper(
                project_name,
                cycle_start,
                cycle_end,
                leader,
                participants,
                delay,
                risk_block,
                progress
            ):

                # 必填校验

                if not project_name:

                    raise gr.Error(
                        "请选择项目名称"
                    )

                if not leader.strip():

                    raise gr.Error(
                        "项目负责人不能为空"
                    )

                if not progress.strip():

                    raise gr.Error(
                        "项目进展不能为空"
                    )

                # 调用原接口

                submit_project(
                    project_name,
                    cycle_start,
                    cycle_end,
                    leader,
                    participants,
                    delay,
                    risk_block,
                    progress
                )

                # 成功提示

                gr.Info(
                    "项目汇报提交成功"
                )

                # 清空表单

                return (
                    None,
                    "",
                    TODAY,
                    "",
                    "",
                    "否",
                    "",
                    ""
                )

            submit_btn.click(
                submit_project_wrapper,
                [
                    project_name,
                    cycle_start,
                    cycle_end,
                    leader,
                    participants,
                    delay,
                    risk_block,
                    progress
                ],
                [
                    project_name,
                    leader,
                    cycle_start,
                    cycle_end,
                    participants,
                    delay,
                    risk_block,
                    progress
                ]
            )

    return (
        page,
        back_btn
    )

# project_page.py
def load_project_names():
    result = query_all_project()
    rows = result["raw_list"]
    names = []
    for row in rows:
        names.append(row[1])
    return sorted(list(set(names)))