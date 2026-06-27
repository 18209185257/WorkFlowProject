import gradio as gr

def create_leader_risk_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>📁 风险预警中心</h2>"
        )

    return page