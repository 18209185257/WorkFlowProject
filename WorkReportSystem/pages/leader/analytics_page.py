import gradio as gr

def create_leader_analytics_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📁 数据分析中心</h2>"
        )

    return page