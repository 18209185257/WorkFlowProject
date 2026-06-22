import gradio as gr


def create_my_project_page():

    with gr.Column(
        visible=False,
        elem_classes=["dashboard-container"]
    ) as page:

        with gr.Column(
            elem_classes=["page-content"]
        ):

            # ===================================
            # 面包屑
            # ===================================
            gr.HTML("""
            <div class="breadcrumb">
                工作台 > 我的项目
            </div>
            """)

            # ===================================
            # 项目列表
            # ===================================
            with gr.Group(
                elem_classes=["section-card"]
            ):

                gr.HTML("""
                <div class="card-header">
                    📜 我的项目
                </div>
                """)

                project_summary_html = gr.HTML()

                project_html = gr.HTML()

            # ===================================
            # 项目概览
            # ===================================
            project_summary_html = gr.HTML()

            # ===================================
            # 项目KPI
            # ===================================
            project_kpi_html = gr.HTML()

            refresh_project_kpi_btn = gr.Button(
                "",
                visible=False,
                elem_id="refresh_project_kpi_btn"
            )

            # ===================================
            # 当前项目ID
            # ===================================
            current_project_id = gr.Textbox(
                visible=False,
                elem_id="current_project_id"
            )

            # ===================================
            # 编辑项目进展弹框
            # ===================================
            modal_html = gr.HTML("""
            <div id="myProgressModal"
                 class="custom-modal"
                 style="display:none">

                <div class="custom-modal-content">

                    <h3>
                        编辑项目进展
                    </h3>

                    <textarea
                        id="mp_progress"
                        rows="6"
                        placeholder="项目进展">
                    </textarea>

                    <textarea
                        id="mp_risk"
                        rows="3"
                        placeholder="风险">
                    </textarea>

                    <textarea
                        id="mp_next"
                        rows="3"
                        placeholder="下一步计划">
                    </textarea>

                    <div style="
                        display:flex;
                        gap:12px;
                        margin-top:20px;
                    ">

                        <button
                            class="blue-btn"
                            onclick="saveMyProgress()">
                            保存
                        </button>

                        <button
                            onclick="closeMyProgressModal()">
                            取消
                        </button>

                    </div>

                </div>

            </div>

            <div id="myProgressDeleteModal"
                 class="custom-modal"
                 style="display:none">

                <div class="custom-modal-content">

                    <h3>
                        删除项目进展
                    </h3>

                    <p>
                        确定删除这条项目进展？
                    </p>

                    <div style="
                        display:flex;
                        gap:12px;
                        margin-top:20px;
                    ">

                        <button
                            class="delete-btn"
                            onclick="confirmDeleteMyProgress()">
                            删除
                        </button>

                        <button
                            onclick="closeDeleteMyProgressModal()">
                            取消
                        </button>

                    </div>

                </div>

            </div>
            """)

            # ===================================
            # 项目进展填写
            # ===================================
            with gr.Group(
                elem_classes=["section-card"]
            ):

                gr.HTML("""
                <div class="card-header">
                    📈 项目进展汇报
                </div>
                """)

                with gr.Row():

                    with gr.Column(scale=3):

                        progress_content = gr.Textbox(
                            label="项目进展",
                            lines=8
                        )

                    with gr.Column(scale=2):

                        risk_content = gr.Textbox(
                            label="当前风险",
                            lines=4
                        )

                        next_plan = gr.Textbox(
                            label="下一步计划",
                            lines=3
                        )

                result_msg = gr.Textbox(
                    label="提交结果",
                    interactive=False
                )

                with gr.Row():

                    submit_progress_btn = gr.Button(
                        "🚀 提交项目进展",
                        variant="primary"
                    )

            # ===================================
            # AI项目分析
            # ===================================
            with gr.Group(
                elem_classes=["section-card"]
            ):

                gr.HTML("""
                <div class="card-header">
                    🤖 AI项目分析
                </div>
                """)

                ai_btn = gr.Button(
                    "生成分析报告",
                    variant="secondary"
                )

                ai_html = gr.HTML()

            # ===================================
            # 历史项目进展
            # ===================================
            with gr.Group(
                elem_classes=["section-card"]
            ):

                gr.HTML("""
                <div class="card-header">
                    🕒 历史项目进展记录
                </div>
                """)

                progress_history_html = gr.HTML()

            # ===================================
            # 隐藏事件组件
            # ===================================
            edit_progress_id = gr.Textbox(
                visible=False,
                elem_id="edit_progress_id"
            )

            load_progress_btn = gr.Button(
                "",
                visible=False,
                elem_id="load_progress_btn"
            )

            save_edit_progress_btn = gr.Button(
                "",
                visible=False,
                elem_id="save_edit_progress_btn"
            )

            edit_progress_content = gr.Textbox(
                visible=False,
                elem_id="edit_progress_content"
            )

            edit_risk_content = gr.Textbox(
                visible=False,
                elem_id="edit_risk_content"
            )

            edit_next_plan = gr.Textbox(
                visible=False,
                elem_id="edit_next_plan"
            )

            load_project_btn = gr.Button(
                "",
                visible=False,
                elem_id="load_project_btn"
            )

            refresh_progress_btn = gr.Button(
                "",
                visible=False,
                elem_id="refresh_progress_btn"
            )

            delete_progress_id = gr.Textbox(
                visible=False,
                elem_id="delete_progress_id"
            )

            delete_progress_btn = gr.Button(
                "",
                visible=False,
                elem_id="delete_progress_btn"
            )

            # ===================================
            # 返回
            # ===================================
            with gr.Row():

                back_btn = gr.Button(
                    "← 返回工作台",
                    elem_classes=["back-btn"]
                )

    return (
        page,
        project_summary_html,
        project_html,
        modal_html,
        project_summary_html,
        project_kpi_html,
        refresh_project_kpi_btn,
        current_project_id,
        edit_progress_id,
        load_progress_btn,
        save_edit_progress_btn,
        edit_progress_content,
        edit_risk_content,
        edit_next_plan,
        load_project_btn,
        progress_content,
        risk_content,
        next_plan,
        submit_progress_btn,
        result_msg,
        ai_btn,
        ai_html,
        progress_history_html,
        refresh_progress_btn,
        delete_progress_id,
        delete_progress_btn,
        back_btn
    )