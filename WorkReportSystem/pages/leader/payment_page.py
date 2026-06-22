import gradio as gr


def create_payment_page():

    with gr.Column(
        visible=False,
        elem_classes=["leader-page"]
    ) as page:

        gr.HTML("""
        <div class="section-title">
        💰 回款管理
        </div>
        """)

        payment_html = gr.HTML()

        add_btn = gr.Button(
            "➕ 新增回款"
        )

        back_btn = gr.Button(
            "返回管理后台"
        )

    return (
        page,
        payment_html,
        add_btn,
        back_btn
    )