import gradio as gr


def create_ai_floating_panel_page():

    panel = gr.HTML(
        """
        <div class='ai-float-btn'
             onclick='openAIPanel()'>

            🤖 AI

        </div>

        <div id='ai-panel'
             class='ai-panel hidden'>

            AI内容区域

        </div>
        """
    )

    return panel