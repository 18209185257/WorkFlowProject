def build_project_page(
    project_html
):
    return f"""
       <!-- 我的项目 -->

        <div id="page-project"
             class="page hidden">
        
            <div class="page-header-user">
        
                <h2>我的项目</h2>
        
                <p>
                    当前负责项目情况
                </p>
        
            </div>
        
           <div class="project-panel">

                    <div class="panel-header">
                
                        <h3>
                            我负责的项目
                        </h3>
                
                    </div>
                
                    <div class="project-table-header">
                
                        <span>项目名称</span>
                
                        <span>进度</span>
                
                        <span>角色</span>
                
                        <span>截止时间</span>
                
                    </div>
                
                    {project_html}
                
                </div>
        
        </div>
        <div
            id="page-project-detail"
            class="page hidden">
        
                    <div class="page-header">
                
                        <button
                            class="back-btn"
                            onclick="showPage('project')">
                
                            ← 返回项目列表
                
                        </button>
                
                        <h2>项目详情</h2>
                
                    </div>
                
                    <div
                        id="projectDetailContainer">
                
                    </div>
                
                </div>
        
    """