from common.db import get_conn,get_project_conn,OLLAMA_URL,MODEL_NAME
from pages.user.services.my_project_service import get_user_project_dashboard
import json
from .ai_service import ai_dashboard_analysis,ai_generate_weekly_report
from datetime import datetime
import  requests

# 提交类型统计
import json

def ollama_chat(prompt):

    try:

        r = requests.post(

            OLLAMA_URL,

            json={

                "model":MODEL_NAME,

                "prompt":prompt,

                "stream":False

            },

            timeout=120

        )

        return r.json()["response"]

    except Exception as e:

        return f"Ollama异常: {e}"

#项目健康度排行
def build_project_rank_dashboard(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        project_name,
        progress
    from project

    where

        main_leader=?

        or developers like ?

        or testers like ?

        or designer like ?

        or structure_engineer like ?

    limit 10
    """,
    (
        real_name,
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    rows = cur.fetchall()

    conn.close()

    names = []
    values = []

    for row in rows:

        names.append(row[0])

        try:
            values.append(int(row[1]))
        except:
            values.append(0)

    return f"""
    <div id="projectRankChart"
         style="height:320px">
    </div>

    <script>

    setTimeout(()=>{{

        let chart=echarts.init(
            document.getElementById(
                "projectRankChart"
            )
        );

        chart.setOption({{

            title:{{
                text:"项目健康度排行"
            }},

            xAxis:{{
                type:"value"
            }},

            yAxis:{{
                type:"category",
                data:{names}
            }},

            series:[{{

                type:"bar",

                data:{values}

            }}]

        }});

    }},300);

    </script>
    """

#AI工作分析
def build_ai_analysis_card(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select count(*)
    from daily_report
    where reporter=?
    """,
    (real_name,)
    )

    report_count = cur.fetchone()[0]

    conn.close()

    level = "优秀"

    if report_count < 5:
        level = "待提升"

    elif report_count < 15:
        level = "良好"

    return f"""
    <div class="dashboard-chart-card">

        <h3>
            🤖 AI工作分析
        </h3>

        <div style="padding:20px">

            <p>
                当前活跃度：
                <b>{level}</b>
            </p>

            <p>
                已提交日报：
                <b>{report_count}</b>
            </p>

            <p>
                建议：
                保持日报和项目汇报同步更新。
            </p>

        </div>

    </div>
    """

def build_submit_pie_chart_html(data):
    return f"""
    <div id="submitPie" style="width:100%;height:320px;"></div>

    <script>
    setTimeout(function(){{
        var chart = echarts.init(document.getElementById('submitPie'));

        var option = {{
            tooltip: {{
                trigger: 'item'
            }},
            legend: {{
                bottom: 0
            }},
            series: [{{
                type: 'pie',
                radius: '65%',
                data: {data}
            }}]
        }};

        chart.setOption(option);
    }}, 300);
    </script>
    """

def build_submit_line_chart_html(x_data, y_data):
    return f"""
    <div id="submitLine" style="width:100%;height:320px;"></div>

    <script>
    setTimeout(function(){{
        var chart = echarts.init(document.getElementById('submitLine'));

        var option = {{
            tooltip: {{
                trigger: 'axis'
            }},
            xAxis: {{
                type: 'category',
                data: {x_data}
            }},
            yAxis: {{
                type: 'value'
            }},
            series: [{{
                data: {y_data},
                type: 'line',
                smooth: true,
                areaStyle: {{}}
            }}]
        }};

        chart.setOption(option);
    }}, 300);
    </script>
    """

#ECharts KPI数据接口
def get_dashboard_kpi_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    # 日报
    cur.execute("select count(*) from daily_report where reporter=?", (real_name,))
    report = cur.fetchone()[0]

    # 会议
    cur.execute("select count(*) from meeting where sponsor=?", (real_name,))
    meeting = cur.fetchone()[0]

    # 项目
    cur.execute("""
        select count(*)
        from project
        where main_leader like ?
           or developers like ?
           or testers like ?
           or designer like ?
           or structure_engineer like ?
    """, (f"%{real_name}%",)*5)

    project = cur.fetchone()[0]

    conn.close()

    return {
        "report": report,
        "meeting": meeting,
        "project": project,
        "total": report + meeting + project
    }

def build_dashboard_kpi_echarts(real_name):

    data = get_dashboard_kpi_data(real_name)

    return f"""
    <div id="kpiChart" style="width:100%;height:220px;"></div>

    <script>
    setTimeout(function(){{

        var chart = echarts.init(document.getElementById('kpiChart'));

        var option = {{
            title: {{
                text: '工作台统计',
                left: 'left'
            }},
            tooltip: {{
                trigger: 'item'
            }},
            series: [{{
                type: 'pie',
                radius: ['40%', '70%'],
                data: [
                    {{value: {data['report']}, name: '日报'}},
                    {{value: {data['meeting']}, name: '会议'}},
                    {{value: {data['project']}, name: '项目汇报'}}
                ]
            }}]
        }};

        chart.setOption(option);

    }}, 200);
    </script>
    """

def get_dashboard_kpi(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    # 日报
    cur.execute("""
    select count(*)
    from daily_report
    where reporter=?
    """,(real_name,))
    report_count = cur.fetchone()[0]

    # 会议
    cur.execute("""
    select count(*)
    from meeting
    where sponsor=?
    """,(real_name,))
    meeting_count = cur.fetchone()[0]

    # 项目
    cur.execute("""
    select count(*)
    from project
    where main_leader like ?
       or developers like ?
       or testers like ?
       or designer like ?
       or structure_engineer like ?
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    project_count = cur.fetchone()[0]

    conn.close()

    total = (
        report_count +
        meeting_count +
        project_count
    )

    return {

        "total": total,

        "report": report_count,

        "meeting": meeting_count,

        "project": project_count
    }


def build_project_rank_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            project_name,
            progress
        from project
        order by progress desc
        limit 5
    """)

    rows = cur.fetchall()

    conn.close()

    names = []
    values = []

    for row in rows:

        names.append(row[0])

        try:
            values.append(
                int(
                    str(row[1]).replace("%","")
                )
            )
        except:
            values.append(0)

    return f"""
    <div
        id="project_rank_chart"
        style="
            width:100%;
            height:350px;
            background:white;
            border-radius:16px;
        "
    ></div>

    <script>

    setTimeout(()=>{{

        var chart=
        echarts.init(
            document.getElementById(
                'project_rank_chart'
            )
        );

        chart.setOption({{

            title:{{
                text:'项目进度排行榜'
            }},

            tooltip:{{}},

            xAxis:{{
                type:'value',
                max:100
            }},

            yAxis:{{
                type:'category',
                data:{names}
            }},

            series:[{{

                type:'bar',

                data:{values}

            }}]

        }});

    }},200);

    </script>
    """

def get_report_count(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select count(*)
        from daily_report
        where reporter=?
    """,(real_name,))

    count = cur.fetchone()[0]

    conn.close()

    return count

def get_meeting_count(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select count(*)
        from meeting
        where sponsor=?
    """,(real_name,))

    count = cur.fetchone()[0]

    conn.close()

    return count

def get_project_count(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select count(*)
        from project
        where
            main_leader like ?
            or developers like ?
            or testers like ?
            or designer like ?
            or structure_engineer like ?
    """,(
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    count = cur.fetchone()[0]

    conn.close()

    return count


def build_ai_analysis_html(real_name):

    return f"""
    <div class="ai-panel">

        <div class="ai-title">
            AI工作分析
        </div>

        <div id="ai-result">
            正在分析 {real_name} 的工作数据...
        </div>

        <script>
        setTimeout(()=>{{
            fetch("/api/ai/dashboard?user={real_name}")
            .then(r=>r.json())
            .then(data=>{{
                document.getElementById("ai-result").innerText =
                    data.summary;
            }});
        }}, 500);
        </script>

    </div>
    """

def build_weekly_report_html(real_name):

    result = ai_generate_weekly_report(real_name)

    return f"""
    <div class="ai-weekly-report">

        <div class="ai-title">
            🧠 AI自动周报
        </div>

        <div class="ai-content">
            {result}
        </div>

    </div>
    """

def load_dashboard_ai(real_name):

    return (
        build_ai_analysis_html(
            real_name
        )
    )

def get_submit_pie_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute(
        "select count(*) from daily_report where reporter=?",
        (real_name,)
    )
    daily = cur.fetchone()[0]

    cur.execute(
        "select count(*) from meeting where sponsor=?",
        (real_name,)
    )
    meeting = cur.fetchone()[0]

    cur.execute("""
        select count(*)
        from project
        where main_leader like ?
           or developers like ?
           or testers like ?
           or designer like ?
           or structure_engineer like ?
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    project = cur.fetchone()[0]

    conn.close()

    return json.dumps({
        "日报": daily,
        "会议记录": meeting,
        "项目汇报": project
    })

def get_submit_line_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select report_date
        from daily_report
        where reporter=?
        order by report_date
    """,
    (real_name,)
    )

    rows = cur.fetchall()

    conn.close()

    stat = {}

    for row in rows:

        day = row[0]

        stat[day] = stat.get(day, 0) + 1

    return json.dumps(stat)


# =========================
# 饼图数据
# =========================
def get_dashboard_pie(real_name):

    data = get_dashboard_kpi(real_name)

    return {
        "日报": data["report"],
        "会议": data["meeting"],
        "项目": data["project"]
    }

# =========================
# 折线图（按日期统计）
# =========================
def get_dashboard_line(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select report_date, count(*)
        from daily_report
        where reporter=?
        group by report_date
        order by report_date asc
    """, (real_name,))

    rows = cur.fetchall()

    conn.close()

    return [
        {"date": r[0], "count": r[1]}
        for r in rows
    ]

# =========================
# TOP5项目
# =========================
def get_top_projects(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select project_name, progress
        from project
        where main_leader like ?
        order by id desc
        limit 5
    """, (f"%{real_name}%",))

    rows = cur.fetchall()

    conn.close()

    return rows

# =========================
# 最近提交
# =========================
def get_recent_submit(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select project_name, create_time
        from project
        where main_leader like ?
        order by create_time desc
        limit 10
    """, (f"%{real_name}%",))

    rows = cur.fetchall()

    conn.close()

    return rows

from datetime import datetime

def get_welcome_html(username):

    now = datetime.now()

    if now.hour < 12:
        greeting = "上午好"
    elif now.hour < 18:
        greeting = "下午好"
    else:
        greeting = "晚上好"

    return f"""
    <div class="welcome-card">

        <div>

            <div class="welcome-title">
                {greeting}，{username}
            </div>

            <div class="welcome-desc">
                欢迎使用工作汇报管理平台
            </div>

        </div>

        <div class="welcome-date">
            {now.strftime("%Y-%m-%d")}
        </div>

    </div>
    """

def build_project_progress_html(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select project_name
        from project
        where main_leader like ?
        limit 5
    """,(f"%{real_name}%",))

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class="dashboard-card">

        <div class="card-title">
            我负责的项目
        </div>

        <table class="project-table">

            <tr>
                <th>项目名称</th>
                <th>状态</th>
            </tr>
    """

    for r in rows:

        html += f"""
        <tr>
            <td>{r[0]}</td>
            <td>进行中</td>
        </tr>
        """

    html += "</table></div>"

    return html

def build_submit_timeline_html(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select report_date
        from daily_report
        where reporter=?
        order by report_date desc
        limit 5
    """,(real_name,))

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class="dashboard-card">

        <div class="card-title">
            最近提交记录
        </div>

        <div class="timeline">
    """

    for r in rows:

        html += f"""
        <div class="timeline-item">
            📄 日报提交
            <span>{r[0]}</span>
        </div>
        """

    html += "</div></div>"

    return html

def get_project_list(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select

        project_name,
        main_leader,
        progress,
        risk_block,
        update_time

    from project

    where

        main_leader like ?

        or developers like ?

        or testers like ?

        or designer like ?

        or structure_engineer like ?

    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    rows = cur.fetchall()

    conn.close()

    return rows

def get_submit_timeline(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    result = []

    cur.execute("""
    select

        report_date,
        report_content

    from daily_report

    where reporter=?

    order by report_date desc
    limit 20
    """,
    (real_name,)
    )

    for row in cur.fetchall():

        result.append({

            "type":"日报",

            "time":row[0],

            "content":row[1]

        })

    conn.close()

    return result

#AI分析
def generate_dashboard_ai(real_name):

    kpi = get_dashboard_kpi(real_name)

    projects = get_project_list(real_name)

    risk_count = 0

    delay_count = 0

    for p in projects:

        risk = str(p[3] or "")

        progress = str(p[2] or "")

        delay = ""

        if len(p) > 5:
            delay = str(p[5] or "")

        if risk.strip():
            risk_count += 1

        if delay == "是":
            delay_count += 1

    prompt = f"""
你是一名企业项目管理顾问。

员工：{real_name}

日报数量：{kpi['report']}
会议数量：{kpi['meeting']}
项目数量：{kpi['project']}

风险项目数：{risk_count}
延期项目数：{delay_count}

请生成：

1 工作活跃度分析

2 项目风险分析

3 下周建议

控制在300字以内。
"""

    try:

        result = ollama_chat(prompt)

        return result

    except Exception as e:

        return f"AI分析失败: {e}"

#自动周报
def generate_weekly_report(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        report_date,
        report_content

    from daily_report

    where reporter=?

    order by report_date desc

    limit 20
    """,
    (real_name,)
    )

    rows = cur.fetchall()

    conn.close()

    content = "\n".join(

        [
            f"{r[0]} {r[1]}"
            for r in rows
        ]

    )

    prompt = f"""
根据下面工作记录生成周报：

{content}

下周建议：

1. 持续推进项目任务
2. 定期更新日报
3. 提前识别项目风险
"""

    try:

        result = ollama_chat(prompt)

        return result

    except Exception as e:

        return f"周报生成失败: {e}"

def get_dashboard_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    # KPI

    cur.execute(
        "select count(*) from daily_report where reporter=?",
        (real_name,)
    )
    report = cur.fetchone()[0]

    cur.execute(
        "select count(*) from meeting where sponsor=?",
        (real_name,)
    )
    meeting = cur.fetchone()[0]

    cur.execute("""
        select count(*)
        from project
        where main_leader like ?
           or developers like ?
           or testers like ?
           or designer like ?
           or structure_engineer like ?
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    project = cur.fetchone()[0]

    # 项目

    cur.execute("""
        select
            project_name,
            progress
        from project
        where
            main_leader like ?
            or developers like ?
            or testers like ?
            or designer like ?
            or structure_engineer like ?
        limit 20
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    projects = cur.fetchall()

    # 最近日报

    cur.execute("""
        select
            report_date,
            report_content
        from daily_report
        where reporter=?
        order by id desc
        limit 10
    """,
    (real_name,)
    )

    reports = cur.fetchall()

    # 饼图

    pie = {
        "日报": report,
        "会议": meeting,
        "项目": project
    }

    # 趋势图

    cur.execute("""
        select
            report_date,
            count(*)
        from daily_report
        where reporter=?
        group by report_date
        order by report_date
    """,
    (real_name,)
    )

    line = []

    for row in cur.fetchall():

        line.append({
            "date": row[0],
            "count": row[1]
        })

    conn.close()

    return {

        "total": report + meeting + project,

        "report": report,

        "meeting": meeting,

        "project": project,

        "pie": pie,

        "line": line,

        "projects": projects,

        "reports": reports
    }

def build_dashboard_v14(username, real_name):

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    data = get_dashboard_data(real_name)

    pie_json = json.dumps(
        data["pie"],
        ensure_ascii=False
    )

    line_json = json.dumps(
        data["line"],
        ensure_ascii=False
    )

    project_html = ""

    for p in data["projects"]:

        project_html += f"""
        <div class="project-item">

            <span>{p[0]}</span>

            <span>{p[1]}%</span>

        </div>
        """

    submit_html = ""

    for r in data["reports"]:

        submit_html += f"""
        <div class="submit-item">

            <span>{r[0]}</span>

            <span>{r[1][:40]}</span>

        </div>
        """

    ai_html = f"""
    <div class="ai-analysis-card">

        <h4>🤖 AI工作分析</h4>

        <p>当前用户：{real_name}</p>

        <p>AI分析模块开发中...</p>

    </div>
    """

    return f"""

<input
id="dashboard-user"
type="hidden"
value="{real_name}"
>

<div class="v14-shell">

    <!-- 左侧菜单 -->

    <aside class="v14-sidebar">

        <div class="logo">

            🚀 工作汇报平台

        </div>

        <div class="menu active"
             onclick="showPage('workbench',this)">

            📊 工作台

        </div>

        <div class="menu"
             onclick="showPage('project',this)">

            📁 我的项目

        </div>

        <div class="menu"
             onclick="showPage('submit',this)">

            📤 我的提交

        </div>

        <div class="menu"
             onclick="showPage('ai',this)">

            🤖 AI分析

        </div>

        <div class="menu"
             onclick="showPage('profile',this)">

            👤 个人中心

        </div>

    </aside>

    <!-- 右侧内容 -->

    <main class="v14-content">

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

            <div class="chart-row">

                <div class="chart-card">

                    <div id="pieChart"
                         data-chart='{pie_json}'>

                    </div>

                </div>

                <div class="chart-card">

                    <div id="lineChart"
                         data-chart='{line_json}'>

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

        </div>

        <!-- 我的项目 -->

        <div id="page-project"
             class="page hidden">

            <h3>

                我的项目

            </h3>

            <div class="project-list">

                {project_html}

            </div>

        </div>

        <!-- 我的提交 -->

        <div id="page-submit"
             class="page hidden">

            <h3>

                最近提交

            </h3>

            <div class="submit-list">

                {submit_html}

            </div>

        </div>

        <!-- AI分析 -->

        <div id="page-ai"
             class="page hidden">

            <h3>

                AI分析

            </h3>

            <div class="ai-card">

                {ai_html}

            </div>

        </div>

        <!-- 个人中心 -->

        <div id="page-profile"
             class="page hidden">

            <h3>

                个人中心

            </h3>

            <div class="profile-card">

                <p>

                    姓名：{real_name}

                </p>

                <p>

                    账号：{username}

                </p>

                <hr>

                <h4>

                    修改密码

                </h4>

                <input
                id="oldPwd"
                type="password"
                placeholder="旧密码">

                <input
                id="newPwd"
                type="password"
                placeholder="新密码">

                <button
                onclick="changePassword()">

                    修改密码

                </button>

                <div id="pwdResult"></div>

            </div>

        </div>

    </main>

</div>
<script>

setTimeout(() => {{

    if(window.afterDashboardRender){{

        window.afterDashboardRender();

    }}

}},300);

</script>
"""

def get_user_profile(username):

    conn = get_conn()

    cur = conn.cursor()

    cur.execute("""
    select

        username,
        real_name,
        role

    from users

    where username=?
    """,(username,))

    row = cur.fetchone()

    conn.close()

    return row

def update_user_password(username,new_pwd):

    conn = get_conn()

    cur = conn.cursor()

    cur.execute("""
    update users

    set password=?

    where username=?
    """,
    (
        new_pwd,
        username
    ))

    conn.commit()

    conn.close()

    return "密码修改成功"

#项目健康度排行
def get_project_health_rank():

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        project_name,
        progress
    from project
    order by cast(
        replace(progress,'%','')
        as integer
    ) desc
    limit 10
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

#风险预警
def get_risk_projects(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        project_name,
        progress,
        risk_block

    from project

    where

        (
            main_leader like ?
            or developers like ?
            or testers like ?
            or designer like ?
            or structure_engineer like ?
        )

        and

        (
            is_delay='是'
            or risk_block!=''
        )

    limit 20
    """,
    (
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%",
        f"%{real_name}%"
    ))

    rows = cur.fetchall()

    conn.close()

    return rows


def get_notifications(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select

        id,
        title,
        content,
        create_time

    from notification

    where receiver=?

    order by id desc

    limit 20
    """,
    (real_name,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def generate_daily_report(task):

    return f"""
        今日完成：
        
        {task}
        
        存在问题：
        
        暂无
        
        明日计划：
        
        继续推进相关工作。
        """

def generate_meeting_summary(content):

    return f"""
        【会议纪要】
        
        会议内容：
        
        {content}
        
        行动项：
        
        1. 负责人跟进任务
        
        2. 风险持续跟踪
        
        3. 下周复盘
        """

#项目风险预测
def project_risk_predict(progress,is_delay,risk):

    score = 0

    try:

        score += int(
            str(progress)
            .replace("%","")
        )

    except:

        pass

    if is_delay=="是":

        score -= 40

    if risk:

        score -= 30

    if score < 40:

        return "高风险"

    if score < 70:

        return "中风险"

    return "低风险"

def get_notice_list(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select

        title,
        content,
        create_time

    from notification

    where receiver=?

    order by id desc

    limit 10
    """,
    (real_name,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows



