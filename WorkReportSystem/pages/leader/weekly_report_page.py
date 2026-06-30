import gradio as gr

def create_weekly_report_page():
    with gr.Column(
        visible=False,
        elem_id="page-weekly_report",
        elem_classes=["page"]
    ) as page:

        gr.HTML(
            """
            <h2>📄 AI周报生成中心</h2>
            <p>在这里生成和管理您的AI周报</p>
            """
        )

        generate_btn = gr.Button(
            "生成AI周报"
        )

        report_md = gr.Markdown()

    return (
        page,
        generate_btn,
        report_md
    )