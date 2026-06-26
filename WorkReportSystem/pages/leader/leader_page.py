import gradio as gr
from datetime import datetime
from .services.user_service import get_user_list
from .services.dashboard_service import get_dashboard_stats

def build_overview_html(range_type="all"):

    stats = get_dashboard_stats(range_type)

    return f"""
    <div class="overview-board">
        <div class="overview-item">
            <div class="overview-value">
                {stats["project_count"]}
            </div>
            <div class="overview-label">
                项目总数
            </div>
        </div>
        
        <div class="overview-item">
            <div class="overview-value">
                {stats["meeting_count"]}
            </div>
            <div class="overview-label">
                会议总数
            </div>
        </div>

        <div class="overview-item">
            <div class="overview-value">
                {stats["report_count"]}
            </div>
            <div class="overview-label">
                日报总数
            </div>
        </div>
        
        <div class="overview-item">
            <div class="overview-value">
                {stats["user_count"]}
            </div>
            <div class="overview-label">
                员工总数
            </div>
        </div>

    </div>
    """

def create_leader_page():
    now = datetime.now()

    week_map = {
        0: "星期一",
        1: "星期二",
        2: "星期三",
        3: "星期四",
        4: "星期五",
        5: "星期六",
        6: "星期日"
    }

    today_str = now.strftime("%Y年%m月%d日")
    week_str = week_map[now.weekday()]

    with gr.Column(
            visible=False,
            elem_classes=["leader-page"]
    ) as page:
        gr.HTML("""
<style>

body,
.gradio-container{

    background:#f4f8fc !important;
}

.leader-page{
    max-width:1400px;
    margin:auto;

    padding:10px;
}

.hero-card{
    background:linear-gradient(
        135deg,
        #2563eb,
        #60a5fa
    );
    padding:15px 40px;
    border-radius:24px;
    box-shadow:0 6px 10px rgba(37,99,235,.25);
    margin-bottom:20px;
}

.hero-card h1{
    color:white !important;
    font-size:30px;
    margin:0;
}

.hero-card p{
    color:white !important;
    margin-top:6px;
    font-size:15px;
}

.section-title{
    font-size:28px;
    font-weight:700;
    margin-top:30px;
    margin-bottom:20px;
}

.stat-card{
    background:white;
    border-radius:18px;
    padding:28px;
    text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,.06);
}

.dashboard-bar{
    display:flex;
    gap:24px;

    background:white;

    border-radius:20px;

    padding:24px;

    box-shadow:0 6px 18px rgba(0,0,0,.06);

    margin-bottom:20px;
}

.dashboard-item{
    flex:1;
    text-align:center;
}

.dashboard-value{
    font-size:34px;
    font-weight:700;
    color:#2563eb;
}

.dashboard-label{
    margin-top:8px;
    color:#666;
}

.stat-value{
    font-size:34px;
    font-weight:700;
    color:#2563eb;
}

.stat-label{
    margin-top:8px;
    color:#666;
}

.notice-card{
    background:white;
    border-radius:18px;
    padding:24px;
    box-shadow:0 6px 18px rgba(0,0,0,.06);
}

.rank-wrap{

    display:flex;

    gap:20px;

    margin-top:10px;
}

.rank-card{

    flex:1;

    background:white;

    border-radius:18px;

    padding:20px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.06);
}

.rank-title{

    font-size:18px;

    font-weight:700;

    margin-bottom:12px;
}

.rank-row{

    display:flex;

    justify-content:space-between;

    padding:10px 0;

    border-bottom:
        1px solid #f0f0f0;
}

.overview-board{

    width:100%;

    display:flex;

    justify-content:space-evenly;

    align-items:center;

    background:white;

    border-radius:20px;

    padding:20px;

    box-sizing:border-box;

    box-shadow:
        0 8px 20px rgba(0,0,0,.05);
}

.overview-item{

    text-align:center;
}

.overview-value{
    font-size:42px;
    font-weight:700;
    color:#2563eb;
}

.overview-label{
    margin-top:4px;
    color:#64748b;
    font-size:14px;
}

.workbench-card button{

    width:240px !important;
    height:180px !important;

    background:white !important;

    border:none !important;

    border-radius:20px !important;

    box-shadow:
        0 8px 20px rgba(0,0,0,.08) !important;

    white-space:pre-line !important;

    font-size:18px !important;

    line-height:1.8 !important;
}

.workbench-card button:hover{

    transform:translateY(-5px);

    box-shadow:
        0 18px 40px rgba(37,99,235,.18) !important;

    border:1px solid #2563eb !important;
}

#card-ai,
#card-user{

    width:220px !important;
    height:220px !important;

    background:#ffffff !important;

    border:none !important;

    border-radius:20px !important;

    box-shadow:
        0 8px 24px rgba(0,0,0,.08) !important;

    white-space:pre-line !important;

    font-size:18px !important;

    font-weight:600 !important;

    transition:.25s !important;
}

#card-ai:hover,
#card-user:hover{

    transform:translateY(-5px);

    box-shadow:
        0 15px 35px rgba(37,99,235,.18) !important;
}

.leader-func-card button{

    width:320px !important;
    height:280px !important;

    background:#fff !important;

    border:none !important;
    border-radius:18px !important;

    box-shadow:
        0 8px 20px rgba(0,0,0,.08) !important;

    font-size:18px !important;
    line-height:1.8 !important;

    white-space:pre-line !important;

    transition:.25s !important;
}

.leader-func-card button:hover{

    transform:translateY(-4px);

    box-shadow:
        0 16px 30px rgba(37,99,235,.15) !important;
}

.kpi-card{

    background:white;

    border-radius:20px;

    padding:25px;

    text-align:center;

    box-shadow:
        0 8px 20px rgba(0,0,0,.06);
}

.kpi-value{

    font-size:40px;

    font-weight:700;

    color:#2563eb;
}

.kpi-label{

    margin-top:8px;

    color:#64748b;
}

.warning-card{

    background:#fff7e6;

    border-left:6px solid #faad14;

    padding:16px;

    margin-bottom:10px;

    border-radius:12px;
}

.ai-analysis-card{

    background:white;

    padding:25px;

    border-radius:18px;

    line-height:34px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.06);
}
</style>
""")

        # 欢迎区
        gr.HTML(f"""
        <div class="hero-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div>
                    <div class="section-title" style="display:flex;align-items:center;gap:8px;">
                        <img src="/gradio_api/file=static/images/leader_platform.png" style="width:60px;height:60px;vertical-align:middle;margin-right:8px;">
                        <h1>管理员控制台</h1>
                    </div>
                    <p>
                        AI工作流查询 · 用户管理 · 企业数据中心
                    </p>
                </div>

                <div style="
                    text-align:right;
                    color:white;
                ">
                    <div style="font-size:22px;font-weight:700;color:#ffffff;">
                        {today_str}
                    </div>

                    <div style="
                        margin-top:4px;
                        opacity:.9;
                        font-size:15px;
                        color:white;
                    ">
                        {week_str}
                    </div>
                </div>

            </div>

        </div>
        """)

        # 数据概览
        gr.HTML("""
        <div class="section-title">
        📊 数据概览
        </div>
        """)
        with gr.Row(elem_classes=["top-count"]):
            gr.Markdown("####   统计范围")

            stat_range = gr.Dropdown(
                choices=[
                    ("全部数据", "all"),
                    ("今天", "today"),
                    ("本周", "week"),
                    ("本月", "month")
                ],
                value="all",
                container=False,
                scale=0,
                min_width=180
            )
        overview_html = gr.HTML(
            value=build_overview_html("all")
        )

        gr.HTML("""
        <div class="section-title">
        🚀 功能中心
        </div>
        <style>

        .func-wrap{

            display:flex;
            gap:24px;

            margin-top:10px;
        }

        .func-card{
            width:100%;
            height:230px;
            background:white;
            border-radius:24px;
            padding:24px;
            box-sizing:border-box;
            box-shadow:0 10px 30px rgba(37,99,235,.08);
            transition:.25s;
            cursor:pointer;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            text-align:center;
        }

        .func-card:hover{
            transform:translateY(-8px);
            box-shadow:0 20px 40px rgba(37,99,235,.18);
            border:1px solid #3b82f6;
        }

        .func-icon{
             font-size:52px;
             margin-bottom:16px;
        }

        .func-title{
            font-size:22px;
            font-weight:700;
            color:#0f172a;
        }

        .func-desc{
            margin-top:12px;
            color:#64748b;
            line-height:30px;
            font-size:15px;
        }

        .hidden-btn{
            display:none !important;
        }
        
        .top-count{
            padding-left:20px;
            padding-right:20px;
        }

        </style>
        """)

        with gr.Row():
            with gr.Column(scale=0, min_width=260):
                gr.HTML("""
                <div class="func-card"
                     onclick="document.querySelector('#ai_hidden_btn').click();">
                    <div class="func-icon">
                        <img src="/gradio_api/file=static/images/ai_workflow.png">
                    </div>

                    <div class="func-title">
                        AI工作流
                    </div>

                    <div class="func-desc">
                        项目分析<br>
                        日报分析<br>
                        会议纪要
                    </div>

                </div>
                """)

                btn_ai_query = gr.Button(
                    "",
                    elem_id="ai_hidden_btn",
                    elem_classes=["hidden-btn"]
                )

            with gr.Column(scale=0, min_width=260):
                gr.HTML("""
                <div class="func-card"
                onclick="document.querySelector('#cockpit_hidden_btn').click();">

                    <div class="func-icon">
                        <img src="/gradio_api/file=static/images/ai_dashboard.png">
                    </div>
                    <div class="func-title">
                        经营驾驶舱
                    </div>
                    <div class="func-desc">
                        经营指标<br>
                        AI经营分析<br>
                        风险预警
                    </div>
                </div>
                """)

                btn_cockpit = gr.Button(
                    "",
                    elem_id="cockpit_hidden_btn",
                    elem_classes=["hidden-btn"]
                )

            with gr.Column(scale=0, min_width=260):
                gr.HTML("""

                <div class="func-card"
                onclick="document.querySelector('#project_center_btn').click();">

                    <div class="func-icon">
                        <img src="/gradio_api/file=static/images/ai_project.png">
                    </div>

                    <div class="func-title">
                        项目管理
                    </div>

                    <div class="func-desc">
                        项目列表<br>
                        项目进度<br>
                        风险项目
                    </div>

                </div>

                """)
                btn_project_center = gr.Button(
                    "",
                    elem_id="project_center_btn",
                    elem_classes=["hidden-btn"]
                )

            with gr.Column(scale=0, min_width=260):
                gr.HTML("""

                <div class="func-card"
                onclick="document.querySelector('#customer_hidden_btn').click();">
                    <div class="func-icon">
                       <img src="/gradio_api/file=static/images/ai_crm.png">
                    </div>
                    <div class="func-title">
                        客户管理
                    </div>

                    <div class="func-desc">
                        客户跟进<br>
                        销售机会<br>
                        商机管理
                    </div>

                </div>

                """)

                btn_customer = gr.Button(

                    "",

                    elem_id="customer_hidden_btn",

                    elem_classes=["hidden-btn"]

                )

            with gr.Column(scale=0, min_width=260):
                gr.HTML("""
                <div class="func-card"
                     onclick="document.querySelector('#user_hidden_btn').click();">
                    <div class="func-icon">
                        <img src="/gradio_api/file=static/images/ai_employee.png">
                    </div>

                    <div class="func-title">
                        员工管理
                    </div>
                    <div class="func-desc">
                        新增员工<br>
                        修改员工<br>
                        删除员工
                    </div>

                </div>
                """)

                btn_user_manager = gr.Button(
                    "",
                    elem_id="user_hidden_btn",
                    elem_classes=["hidden-btn"]
                )

        def refresh_overview(range_type):
            return build_overview_html(range_type)

        stat_range.change(
            fn=refresh_overview,
            inputs=stat_range,
            outputs=overview_html
        )

    return (
        page,

        overview_html,

        stat_range,

        btn_ai_query,
        btn_user_manager,
        btn_cockpit,
        btn_customer,
        btn_project_center
    )