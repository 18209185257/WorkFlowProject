import gradio as gr

def build_ai_page():
    return """
    <div id="page-ai"
     class="page hidden">
       <div class="ai-container">

           <!-- 顶部AI控制台 -->
           <div class="ai-hero">

               <div class="ai-title">
                   🤖 AI工作中枢
               </div>

               <div class="ai-subtitle">
                   Copilot 企业智能办公系统
               </div>

               <div class="status-items">
                    <span class="ai-suggest">Qwen ✔</span>
                    <span  class="ai-suggest">DeepSeek ✔</span>
                    <span  class="ai-suggest">RAG ✔</span>
                    <span  class="ai-suggest">Memory ✔</span>
    
                </div>

           </div>
           
           <div class="ai-grid">

                <div class="ai-card" onclick="runAI('daily')">
                    📄 AI日报
                </div>
    
                <div class="ai-card" onclick="runAI('weekly')">
                    📝 AI周报
                </div>
    
                <div class="ai-card" onclick="runAI('project')">
                    📊 项目分析
                </div>
    
                <div class="ai-card" onclick="runAI('risk')">
                    ⚠️ 风险预警
                </div>
    
                <div class="ai-card" onclick="runAI('meeting')">
                    📅 会议纪要
                </div>
    
                <div class="ai-card" onclick="runAI('chat')">
                    💬 AI问答
                </div>

           </div>
           
           <div class="ai-chat-panel">

                <div id="ai-result"
                     class="ai-result-box">
    
                    请输入问题或点击功能开始分析...
    
                </div>
    
                <div class="ai-input-box">
    
                    <textarea id="ai-question"
                              placeholder="请输入你的问题...">
                    </textarea>
    
                    <button onclick="askAI()">
                        发送
                    </button>
    
                </div>

           </div>
           
            
            <div class="ai-history">

                <div class="history-title">
                    📚 最近AI记录
                </div>
    
                <div id="ai-history-list">
    
                </div>

            </div>

       </div>
    </div>
    """
