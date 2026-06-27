import gradio as gr

def create_leader_ai_page():

    with gr.Column(
        visible=False
    ) as page:

        gr.HTML(
            "<h2>🤖 AI领导助手</h2>"
        )

        gr.HTML("""
        <div class="leader-ai-tip">

        <h3>💡 AI可直接完成</h3>

        <ul>

        <li>生成本周领导周报</li>

        <li>分析项目情况</li>

        <li>分析项目风险</li>

        <li>谁没交日报</li>

        <li>朱涛最近工作总结</li>

        </ul>

        </div>
        """)

        question = gr.Textbox(
            label="请输入问题"
        )

        answer = gr.Markdown()

        ask_btn = gr.Button(
            "分析"
        )

    return (
        page,
        question,
        answer,
        ask_btn
    )