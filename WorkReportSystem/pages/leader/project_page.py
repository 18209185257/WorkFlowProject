import gradio as gr

def create_leader_project_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📁 项目管理中心</h2>"
        )

    return page