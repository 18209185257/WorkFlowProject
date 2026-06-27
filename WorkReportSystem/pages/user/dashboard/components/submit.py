def build_submit_page(
    submit_html
):
    return f"""
       <!-- 我的提交 -->
        <div id="page-submit"
             class="page hidden">
            <div class="page-header-user">
                <h2>📤 我的提交</h2>
                <p>
                    最近工作记录
                </p>
            </div>
            <div class="submit-list">
                {submit_html}
            </div>
        </div>
        <div
            id="page-submit-detail"
            class="page hidden">
        
                    <div class="page-header">
                
                        <button
                            class="back-btn"
                            onclick="showPage('submit')">
                
                            ← 返回提交记录
                
                        </button>
                
                        <h2>提交详情</h2>
                
                    </div>
                
                    <div
                        id="submitDetailContainer">
                
                    </div>
                
        </div>
    """