def build_workbench_page(
    real_name,
    now,
    data,
    todo_html,
    pie_json,
    project_html,
    submit_html
):
    return f"""
      <!-- 工作台 -->
        <div id="page-workbench"
             class="page">

            <div class="welcome-bar">

                <div>

                    <div class="welcome-title">
                        欢迎回来，{real_name}
                    </div>

                    <div class="welcome-desc">
                        今日工作状态总览
                    </div>

                </div>

                <div class="welcome-date">
                    {now}
                </div>

            </div>

            <div class="kpi-row">

                <div class="kpi-card">

                    <div class="num">

                        {data["total"]}

                    </div>

                    <div>总提交</div>

                </div>

                <div class="kpi-card">

                    <div class="num">

                        {data["report"]}

                    </div>

                    <div>日报</div>

                </div>

                <div class="kpi-card">

                    <div class="num">

                        {data["meeting"]}

                    </div>

                    <div>会议</div>

                </div>

                <div class="kpi-card">

                    <div class="num">

                        {data["project"]}

                    </div>

                    <div>项目</div>

                </div>

            </div>
            
            <div class="todo-panel">
                <h3>
                    📌 我的待办
                </h3>
                {todo_html}
            </div>

            <div class="chart-row">

                <div class="chart-card">
                    <div class="chart-title">
                        提交类型分布
                    </div>

                    <div id="pieChart"
                         data-chart='{pie_json}'>

                    </div>

                </div>

                <div class="chart-card">
                    <div class="chart-header">

                        <div class="chart-title">
                            近7天提交趋势
                        </div>
            
                        <select id="trendDays"
                                onchange="reloadTrend(this.value)">
            
                            <option value="7">近7天</option>
                            <option value="15">近15天</option>
                            <option value="30">近30天</option>
            
                        </select>
            
                    </div>
                    <div id="lineChart">
                    </div>

                </div>

            </div>

            <div class="quick-row">

                <div
                    class="quick-card"
                    onclick="
                    document
                    .getElementById(
                        'daily_page_btn'
                    )
                    .click();
                    ">
                
                    📄 日报填报
                
                </div>
                
                <div
                    class="quick-card"
                    onclick="
                    document
                    .getElementById(
                        'meeting_page_btn'
                    )
                    .click();
                    ">
                
                    📅 会议记录
                
                </div>
                
                <div
                    class="quick-card"
                    onclick="
                    document
                    .getElementById(
                        'project_page_btn'
                    )
                    .click();
                    ">
                
                    📊 项目进展
                
                </div>

            </div>
            
            <div class="dashboard-bottom">

                <div class="project-panel">

                    <div class="panel-header">
                
                        <h3>
                            我负责的项目
                        </h3>
                
                        <div
                        class="panel-link"
                        onclick="showPage('project',this)">
                        
                        查看全部
                        
                        </div>
                
                    </div>
                
                    <div class="project-table-header">
                
                        <span>项目名称</span>
                
                        <span>进度</span>
                
                        <span>角色</span>
                
                        <span>截止时间</span>
                
                    </div>
                    <div class="project_list">
                       {project_html}
                    </div>
                
                </div>
            
                <div class="submit-panel">

                    <div class="panel-header">
                
                        <h3>
                            最近提交记录
                        </h3>
                
                        <div
                            class="panel-link"
                            onclick="showPage('submit',this)">
                            
                            查看全部
                            
                        </div>
                
                    </div>
                
                    <div class="submit-timeline">
                
                        {submit_html}
                
                    </div>
                
                </div>
                
            </div>

        </div>
    """