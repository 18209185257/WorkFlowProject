import gradio as gr


def create_order_page():

    with gr.Column(
        visible=False,
        elem_classes=["leader-page"]
    ) as page:

        gr.HTML("""
        <div class="section-title">
        📦 订单管理
        </div>
        """)

        order_html = gr.HTML()

        add_btn = gr.Button(
            "➕ 新增订单"
        )

        back_btn = gr.Button(
            "返回管理后台"
        )

    return (
        page,
        order_html,
        add_btn,
        back_btn
    )