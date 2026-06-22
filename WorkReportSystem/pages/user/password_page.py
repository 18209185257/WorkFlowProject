import gradio as gr


def create_password_page():

    with gr.Column(
        visible=False,
        elem_classes=["page-container"]
    ) as page:
        gr.HTML("""
        <div class="breadcrumb">
            工作台 &gt; 修改密码
        </div>
        """)

        with gr.Column(
            elem_classes=["form-card"]
        ):

            gr.Markdown("## 🔐 修改密码")

            old_pwd = gr.Textbox(
                label="当前密码",
                type="password"
            )

            new_pwd = gr.Textbox(
                label="新密码",
                type="password"
            )

            confirm_pwd = gr.Textbox(
                label="确认新密码",
                type="password"
            )

            result = gr.Markdown()

            # 底部按钮区域
            with gr.Row(
                elem_classes=["action-row"]
            ):

                back_password = gr.Button(
                    "返回工作台",
                    elem_classes=["back-btn"]
                )

                submit_btn = gr.Button(
                    "💾 保存修改",
                    variant="primary",
                    elem_classes=["submit-btn"]
                )

    return (
        page,
        back_password,
        old_pwd,
        new_pwd,
        confirm_pwd,
        submit_btn,
        result
    )