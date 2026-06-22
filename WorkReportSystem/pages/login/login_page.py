import gradio as gr
def create_login_page():

    with gr.Column(
        visible=True,
        elem_classes=["login-page"]
    ) as page:

        with gr.Row(elem_classes=["login-wrapper"]):

            # 左侧宣传
            with gr.Column(
                scale=1,
                elem_classes=["login-left"]
            ):

                gr.HTML("""
                <div class="brand-panel">

                    <div class="brand-logo">
                        📊
                    </div>

                    <div class="brand-title">
                        华智瑞森特工作汇报系统
                    </div>

                    <div class="brand-subtitle">
                        AI驱动企业经营管理平台
                    </div>

                    <div class="brand-desc">
                        项目汇报 · 会议记录 · 日报上传 · 数据归档
                    </div>

                </div>
                """)

            # 右侧
            with gr.Column(
                scale=1,
                elem_classes=["login-right"]
            ):

                # ======================
                # 登录面板
                # ======================
                with gr.Column(
                    elem_classes=["login-card"],
                    visible=True
                ) as login_panel:

                    gr.Markdown("## 用户登录")

                    username = gr.Textbox(
                        label="账号",
                        placeholder="请输入账号",
                        lines=1
                    )

                    password = gr.Textbox(
                        label="密码",
                        type="password",
                        placeholder="请输入密码",
                        lines=1
                    )

                    with gr.Row():
                        gr.HTML("<div></div>")

                        register_btn = gr.HTML("""
                        <div class="register-link-text">
                            员工注册
                        </div>
                        """)

                    btn = gr.Button(
                        "登录系统",
                        variant="primary",
                        elem_classes="no-flash-btn"
                    )

                    msg = gr.Markdown("")

                # ======================
                # 注册面板
                # ======================
                with gr.Column(
                    elem_classes=["login-card"],
                    visible=False
                ) as register_panel:

                    gr.Markdown("## 员工注册")

                    reg_name = gr.Textbox(
                        label="姓名"
                    )

                    reg_phone = gr.Textbox(
                        label="手机号"
                    )

                    reg_user = gr.Textbox(
                        label="账号"
                    )

                    reg_pwd = gr.Textbox(
                        label="密码",
                        type="password"
                    )

                    reg_msg = gr.Markdown()

                    reg_msg = gr.Markdown()

                    with gr.Row():
                        back_login_btn = gr.Button(
                            "返回登录",
                            elem_id="back_login_btn",
                            scale=1
                        )

                        reg_submit = gr.Button(
                            "确认注册",
                            elem_id="reg_submit_btn",
                            scale=1
                        )

        gr.HTML("""
        <div class="copyright">
            © 2026 华智瑞森特工作汇报系统 版权所有
        </div>
        """)

    return (

        page,

        # 登录
        username,
        password,
        btn,
        msg,

        # 面板
        login_panel,
        register_panel,

        # 注册入口
        register_btn,

        # 注册信息
        reg_name,
        reg_phone,
        reg_user,
        reg_pwd,

        back_login_btn,
        reg_submit,
        reg_msg
    )