import gradio as gr


def create_ai_floating_panel_page():
    panel = gr.HTML("""
    <div class="ai-float-btn"
         onclick="openAIPanel()">

        🤖

    </div>

    <div id="ai-panel"
         class="ai-panel hidden">

        <div class="ai-header">

            AI助手

            <span onclick="closeAIPanel()">
                ✖
            </span>

        </div>

        <div class="ai-body">

            AI内容区域

        </div>

    </div>
    """)

    return panel