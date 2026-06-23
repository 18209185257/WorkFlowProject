import gradio as gr


def create_ai_assistant_page():

    with gr.Column(
        visible=False
    ) as ai_page:

        gr.HTML("""
        <h2>🤖 AI工作助手</h2>
        <p>
        日报、会议纪要、周报、项目分析
        </p>
        """)

        with gr.Tabs():

            with gr.Tab("AI日报助手"):

                daily_input = gr.Textbox(
                    lines=8,
                    label="输入今日工作内容"
                )

                daily_btn = gr.Button(
                    "生成日报"
                )

                daily_output = gr.Textbox(
                    lines=12
                )

            with gr.Tab("AI会议纪要"):

                meeting_input = gr.Textbox(
                    lines=10,
                    label="会议内容"
                )

                meeting_btn = gr.Button(
                    "生成纪要"
                )

                meeting_output = gr.Textbox(
                    lines=12
                )

            with gr.Tab("AI周报"):

                weekly_btn = gr.Button(
                    "生成周报"
                )

                weekly_output = gr.Textbox(
                    lines=15
                )

            with gr.Tab("项目分析"):

                project_name = gr.Textbox(
                    label="项目名称"
                )

                project_btn = gr.Button(
                    "分析项目"
                )

                project_output = gr.Textbox(
                    lines=15
                )

    return (
        ai_page,

        daily_input,
        daily_btn,
        daily_output,

        meeting_input,
        meeting_btn,
        meeting_output,

        weekly_btn,
        weekly_output,

        project_name,
        project_btn,
        project_output
    )