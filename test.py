import gradio as gr
from .services.user_service import get_user_list

def create_user_manager_page():

    with gr.Column(
        visible=False,
        elem_classes=["page-container"]
    ) as page:

        gr.HTML("""
        <div class="breadcrumb">
            管理后台 > 用户管理
        </div>
        """)

        # 用户表格
        user_html = gr.HTML()

        # 当前选中用户
        selected_username = gr.State("")

        edit_event = gr.Textbox(
            visible=False,
            elem_id="edit_event"
        )

        delete_event = gr.Textbox(
            visible=False,
            elem_id="delete_event"
        )

        # ==========================
        # 编辑弹窗
        # ==========================
        with gr.Dialog(
            visible=False
        ) as edit_dialog:

            gr.Markdown("## 编辑用户")

            with gr.Row():
                edit_username = gr.Textbox(
                    label="用户名",
                    interactive=False
                )

                edit_name = gr.Textbox(
                    label="姓名"
                )



            with gr.Row():
                edit_phone = gr.Textbox(
                    label="手机号"
                )

                edit_role = gr.Dropdown(
                    choices=["user", "leader"],
                    label="角色"
                )

            with gr.Row():

                save_btn = gr.Button(
                    "保存修改",
                    variant="primary"
                )

                delete_btn = gr.Button(
                    "删除用户",
                    variant="stop"
                )

                cancel_btn = gr.Button(
                    "取消"
                )

        # ==========================
        # 删除确认弹窗
        # ==========================
        with gr.Dialog(
                visible=False
        ) as delete_dialog:
            delete_text = gr.Markdown()

            confirm_delete_btn = gr.Button(
                "确认删除",
                variant="stop"
            )

            cancel_delete_btn = gr.Button("取消")

        back_btn = gr.Button(
            "返回管理后台"
        )

    return (

        page,

        user_html,

        selected_username,

        edit_event,
        delete_event,

        # 编辑弹窗
        edit_dialog,
        edit_username,
        edit_name,
        edit_phone,
        edit_role,

        save_btn,
        delete_btn,
        cancel_btn,

        # 删除弹窗
        delete_dialog,
        delete_text,
        confirm_delete_btn,
        cancel_delete_btn,

        # 返回
        back_btn
    )

