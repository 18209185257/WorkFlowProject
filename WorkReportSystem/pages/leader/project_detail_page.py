import gradio as gr


def create_project_detail_page():

    with gr.Column(
        visible=False
    ) as page:

        detail_html = gr.HTML()
        modal_html = gr.HTML("""

        <div
            id="progressEditModal"
            class="custom-modal"
            style="display:none"
        >

            <div class="custom-modal-content">

                <h3>编辑项目进展</h3>
                <div
                    style="
                        margin-top:20px;
                        display:flex;
                        gap:10px;
                    "
                >

                    <button
                        onclick="saveProgress()"
                        class="blue-btn"
                    >
                        保存
                    </button>

                    <button
                        onclick="closeProgressModal()"
                    >
                        取消
                    </button>

                </div>

            </div>

        </div>

        """)
        gr.HTML("<h3>新增项目进展</h3>")
        progress_content = gr.Textbox(
            label="项目进展",
            lines=4
        )
        risk_content = gr.Textbox(
            label="当前风险",
            lines=2
        )

        next_plan = gr.Textbox(
            label="下一步计划",
            lines=2
        )

        add_progress_btn = gr.Button(
            "保存进展"
        )

        gr.HTML("<hr>")
        gr.HTML("<h3>项目成员管理</h3>")

        member_username = gr.Textbox(
            label="员工账号"
        )

        member_name = gr.Textbox(
            label="姓名"
        )

        member_role = gr.Textbox(
            label="项目角色"
        )

        add_member_btn = gr.Button(
            "添加成员"
        )

        delete_member_id = gr.Textbox(
            visible=False,
            elem_id="delete_member_id"
        )

        delete_member_btn = gr.Button(
            "",
            visible=False,
            elem_id="delete_member_btn"
        )

        gr.HTML("<hr>")
        gr.HTML("<h3>项目风险管理</h3>")
        risk_level = gr.Dropdown(
            ["低", "中", "高"],
            value="中",
            label="风险等级"
        )

        risk_desc = gr.Textbox(
            label="风险内容",
            lines=3
        )

        risk_solution = gr.Textbox(
            label="解决方案",
            lines=3
        )

        add_risk_btn = gr.Button(
            "新增风险"
        )

        delete_risk_id = gr.Textbox(
            visible=False,
            elem_id="delete_risk_id"
        )

        delete_risk_btn = gr.Button(
            "",
            visible=False,
            elem_id="delete_risk_btn"
        )

        edit_risk_id = gr.Textbox(
            visible=False,
            elem_id="edit_risk_id"
        )

        ai_project_btn = gr.Button(
            "🤖 AI分析项目",
            variant="primary"
        )

        ai_project_html = gr.HTML()

        back_btn = gr.Button(
            "返回项目中心"
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

        edit_progress_id = gr.Textbox(
            visible=False,
            elem_id="edit_progress_id"
        )

        load_progress_btn = gr.Button(
            "",
            visible=False,
            elem_id="load_progress_btn"
        )

        edit_progress_content = gr.Textbox(
            visible=False
        )

        edit_risk_content = gr.Textbox(
            visible=False
        )

        edit_next_plan = gr.Textbox(
            visible=False
        )

        ai_result = gr.Textbox(
            label="AI项目分析",
            lines=20,
            visible=False
        )

    return (
        page,
        detail_html,
        modal_html,
        progress_content,
        risk_content,
        next_plan,
        add_progress_btn,
        member_name,
        member_role,
        add_member_btn,
        ai_project_btn,
        ai_project_html,
        back_btn,
        delete_member_id,
        delete_member_btn,
        risk_level,
        risk_desc,
        risk_solution,
        add_risk_btn,

        delete_risk_id,
        delete_risk_btn,
        edit_risk_id,
        delete_progress_id,
        delete_progress_btn,
        edit_progress_id,
        load_progress_btn,
        edit_progress_content,
        edit_risk_content,
        edit_next_plan,
        ai_result
    )