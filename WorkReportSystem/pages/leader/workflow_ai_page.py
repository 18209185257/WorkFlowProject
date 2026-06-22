import gradio as gr
from pathlib import Path

from .ai.chat_service import (
    user_send_msg,
    ai_reply,
    init_welcome
)

BASE_DIR = Path(__file__).parent

USER_AVATAR = str(BASE_DIR / "static" / "user.png")
AI_AVATAR = str(BASE_DIR / "static" / "ai.png")

def create_workflow_ai_page():

    with gr.Column(
        visible=False,
        elem_classes=["ai-dashboard"]
    ) as workflow_ai_page:

        # 顶部Banner
        gr.HTML("""
        <div class='ai-header'>
            <div>
                <h1>🤖 华智瑞森特 AI 工作流中心</h1>
                <p>项目管理 · 日报分析 · 风险预警 · 会议助手</p>
            </div>
        </div>
        """)

        # KPI区
        with gr.Row(elem_classes=["kpi-row"]):

            kpi_project = gr.HTML("""
            <div class='kpi-card'>
                <span>项目总数</span>
                <h2 id='kpi_project'>0</h2>
            </div>
            """)

            kpi_daily = gr.HTML("""
            <div class='kpi-card'>
                <span>本周日报</span>
                <h2 id='kpi_daily'>0</h2>
            </div>
            """)

            kpi_risk = gr.HTML("""
            <div class='kpi-card'>
                <span>风险项目</span>
                <h2 id='kpi_risk'>0</h2>
            </div>
            """)

        # 快捷入口

        gr.HTML("""
        <div class='quick-title'>
            ⚡ 快捷查询
        </div>
        """)

        with gr.Row():

            btn_week = gr.Button(
                "📋 本周工作总结",
                elem_classes=["quick-card"]
            )

            btn_risk = gr.Button(
                "⚠ 项目风险分析",
                elem_classes=["quick-card"]
            )

            btn_daily = gr.Button(
                "📝 日报统计",
                elem_classes=["quick-card"]
            )

            btn_rank = gr.Button(
                "📈 项目进度排行",
                elem_classes=["quick-card"]
            )

        # 主体

        with gr.Row():

            # 左侧聊天

            with gr.Column(scale=6):

                chatbot = gr.Chatbot(
                    type="messages",
                    value=init_welcome(),
                    height=650,
                    elem_classes=["enterprise-chatbot"]
                )

                msg = gr.Textbox(
                    placeholder="请输入问题..."
                )

            # 右侧驾驶舱

            with gr.Column(scale=4):

                ai_summary = gr.HTML("""
                <div class='ai-panel'>
                    <h3>📋 AI日报总结</h3>
                    <div id='summary_content'>
                        等待分析...
                    </div>
                </div>
                """)

                ai_risk = gr.HTML("""
                <div class='ai-panel'>
                    <h3>⚠ AI风险分析</h3>
                    <div id='risk_content'>
                        等待分析...
                    </div>
                </div>
                """)

                project_rank = gr.HTML("""
                <div class='ai-panel'>
                    <h3>📈 项目进度排行榜</h3>
                    <div id='rank_content'>
                        等待分析...
                    </div>
                </div>
                """)

        back_ai = gr.Button(
            "返回工作台",
            elem_classes=["back-btn"]
        )

    return (
        workflow_ai_page,
        kpi_project,
        kpi_daily,
        kpi_risk,
        btn_week,
        btn_risk,
        btn_daily,
        btn_rank,
        chatbot,
        msg,
        ai_summary,
        ai_risk,
        project_rank,
        back_ai
    )