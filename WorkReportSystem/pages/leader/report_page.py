import gradio as gr

def create_leader_report_page():

    with gr.Column(
        visible=False,
        elem_id="page-weekly_report",
        elem_classes=["page"]
    ) as page:

        gr.HTML(
            "<h2>📁 周报/月报中心</h2>"
        )

    return page