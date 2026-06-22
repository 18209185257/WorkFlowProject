import gradio as gr

def create_dashboard_page():

    with gr.Column(
        elem_classes=["dashboard-v14"]
    ) as dashboard_page:

        dashboard_html = gr.HTML(
            value="",
            visible=True
        )

    return (
        dashboard_page,
        dashboard_html
    )

