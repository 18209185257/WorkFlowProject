import gradio as gr

def build_ai_page():

    return """
    <button
        id="ai_daily_btn"
        style="display:none">
    </button>

    <button
        id="ai_weekly_btn"
        style="display:none">
    </button>

    <button
        id="ai_project_btn"
        style="display:none">
    </button>

    <button
        id="ai_risk_btn"
        style="display:none">
    </button>

    <button
        id="ai_meeting_btn"
        style="display:none">
    </button>

    <button
        id="ai_chat_btn"
        style="display:none">
    </button>
    <div id="page-ai" class="page hidden">

        <div class="page-header">

            <h2>🤖 AI工作助手</h2>

            <p>智能生成日报、周报、项目分析与风险预警</p>

        </div>

        <div class="ai-grid">

            <div class="ai-card"
                 onclick="runAI('daily')">

                <div class="ai-icon">📄</div>

                <div class="ai-title">
                    AI日报生成
                </div>

            </div>

            <div class="ai-card"
                 onclick="runAI('weekly')">

                <div class="ai-icon">📝</div>

                <div class="ai-title">
                    AI周报生成
                </div>

            </div>

            <div class="ai-card"
                 onclick="runAI('project')">

                <div class="ai-icon">📊</div>

                <div class="ai-title">
                    AI项目分析
                </div>

            </div>

            <div class="ai-card"
                 onclick="runAI('risk')">

                <div class="ai-icon">⚠️</div>

                <div class="ai-title">
                    AI风险预警
                </div>

            </div>

            <div class="ai-card"
                 onclick="runAI('meeting')">

                <div class="ai-icon">📅</div>

                <div class="ai-title">
                    AI会议纪要
                </div>

            </div>

            <div class="ai-card"
                 onclick="runAI('chat')">

                <div class="ai-icon">💬</div>

                <div class="ai-title">
                    AI问答
                </div>

            </div>

        </div>

        <div id="ai-result"
             class="ai-result">

            点击功能开始分析...

        </div>
        
        <div class="ai-chat-box">

            <textarea
                id="ai-question"
                placeholder="请输入问题">
            </textarea>
        
            <button
                onclick="askAI()">
        
                提问
        
            </button>

        </div>

    </div>
    """