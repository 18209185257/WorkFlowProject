import gradio as gr
from .services.cockpit_service import (
    build_cockpit_html,
    build_rank_html
)


def create_cockpit_page():

    with gr.Column(
        visible=False,
        elem_classes=["cockpit-page"]
    ) as page:

        # ==========================
        # 标题
        # ==========================

        gr.HTML("""
        <div class="section-title">
            📈 企业经营驾驶舱
        </div>
        """)

        # ==========================
        # 经营数据大屏
        # ==========================

        cockpit_html = gr.HTML(
            value="""
            <div class="notice-card">
                经营数据加载中...
            </div>
            """
        )

        # ==========================
        # 项目排行榜
        # ==========================
        gr.HTML("""
        <div class="section-title">
            📊 项目排行榜
        </div>
        """)

        rank_html = gr.HTML(
            value=build_rank_html()
        )

        # ==========================
        # AI经营分析
        # ==========================

        gr.HTML("""
        <div class="section-title">
            🤖 AI经营分析
        </div>
        """)

        ai_analysis_html = gr.HTML(
            value="""
            <div class="ai-analysis-card">
            点击下方按钮生成经营日报
            </div>
            """
        )

        # ==========================
        # 风险预警
        # ==========================

        gr.HTML("""
        <div class="section-title">
            🚨 风险预警
        </div>
        """)

        warning_html = gr.HTML(
            value="""
            <div class="notice-card">
                暂无风险数据
            </div>
            """
        )

        # ==========================
        # 返回按钮
        # ==========================
        with gr.Row():
            generate_ai_btn = gr.Button(
                "🤖 一键生成经营日报",
                elem_classes=["ai-generate-btn"]
            )

            back_btn = gr.Button(
                "返回管理后台",
                variant="secondary"
            )

    return (
        page,
        cockpit_html,
        rank_html,
        ai_analysis_html,
        warning_html,
        generate_ai_btn,
        back_btn
    )