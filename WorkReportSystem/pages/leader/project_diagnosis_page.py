import gradio as gr


def create_project_diagnosis_page():

    with gr.Column(
        visible=False,
        elem_id="page-project_diagnosis",
        elem_classes=["page"]
    ) as page:

        gr.HTML(
            "<h2>🩺 AI项目诊断中心</h2>"
        )

        project_name = gr.Textbox(
            label="项目名称"
        )

        diagnosis_btn = gr.Button(
            "开始诊断"
        )

        diagnosis_result = gr.Markdown()

    return (
        page,
        project_name,
        diagnosis_btn,
        diagnosis_result
    )