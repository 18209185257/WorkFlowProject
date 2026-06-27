import gradio as gr

def create_leader_employee_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📁 员工画像中心</h2>"
        )

    return page