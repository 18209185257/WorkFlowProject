import gradio as gr


def create_my_profile_page():
    with gr.Column(
            visible=False
    ) as profile_page:
        profile_username = gr.Textbox(
            label="账号",
            interactive=False
        )

        profile_real_name = gr.Textbox(
            label="姓名",
            interactive=False
        )

        profile_role = gr.Textbox(
            label="角色",
            interactive=False
        )

        gr.Markdown("### 修改密码")

        new_pwd = gr.Textbox(
            type="password"
        )

        save_pwd_btn = gr.Button(
            "保存密码"
        )

        pwd_result = gr.Textbox()

        back_btn = gr.Button(
            "返回工作台"
        )

    return (

        profile_page,

        profile_username,

        profile_real_name,

        profile_role,

        new_pwd,

        save_pwd_btn,

        pwd_result,

        back_btn

    )