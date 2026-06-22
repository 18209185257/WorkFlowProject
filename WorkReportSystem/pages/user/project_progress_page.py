import gradio as gr

def create_project_progress_page():
    with gr.Column(
        visible=False
    ) as page:
        gr.HTML("""
        <h2>项目进展</h2>
        """)
        progress_history_html = gr.HTML()
        progress_content = gr.Textbox(
            label="今日完成",
            lines=4
        )
        risk_content = gr.Textbox(
            label="风险",
            lines=2
        )
        next_plan = gr.Textbox(
            label="下一步计划",
            lines=2
        )
        save_btn = gr.Button(
            "保存进展",
            variant="primary"
        )

        ai_btn = gr.Button(
            "🤖 AI生成项目周报"
        )

        ai_result = gr.Textbox(
            lines=20,
            label="AI分析结果"
        )

        result_msg = gr.Textbox()
        back_btn = gr.Button(
            "返回我的项目"
        )
    return (
        page,
        progress_history_html,
        progress_content,
        risk_content,
        next_plan,
        save_btn,
        result_msg,
        ai_btn,
        ai_result,
        back_btn
    )