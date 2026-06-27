import gradio as gr

def create_leader_customer_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📁 客户管理中心</h2>"
        )

    return page