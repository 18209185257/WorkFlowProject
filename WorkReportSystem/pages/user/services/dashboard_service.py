from common.db import get_conn,get_project_conn,OLLAMA_URL,MODEL_NAME
from pages.user.services.my_project_service import get_user_project_dashboard
from .ai_service import ai_dashboard_analysis,ai_generate_weekly_report
import  requests
from pages.leader.services.ai_business_service import call_llm
from pages.user.dashboard.components.workbench import build_workbench_page
from pages.user.dashboard.components.project import build_project_page
from pages.user.dashboard.components.submit import build_submit_page
from pages.user.ai_assistant.ai_page import build_ai_page
from pages.user.dashboard.components.profile import build_profile_page

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


def get_dashboard_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()


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
        select id,
            project_name,
            main_leader,
            progress,
            risk_block,
            end_date
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
        select id,
            report_date,
            report_content
        from daily_report
        where reporter=?
        order by id desc
        limit 5
    """,
    (real_name,)
    )

    reports = []

    for r in cur.fetchall():
        reports.append({
            "id": r[0],
            "type": "daily",
            "date": r[1],
            "content": r[2]
        })

   #会议
    cur.execute("""
    select
        id,
        meet_date,
        meet_content
    from meeting
    where sponsor=?
    order by id desc
    limit 5
    """, (real_name,))

    for r in cur.fetchall():
        reports.append({
            "id": r[0],
            "type": "meeting",
            "date": r[1],
            "content": r[2]
        })

    #项目进展
    cur.execute("""
    select
        id,
        progress_date,
        progress_content
    from project_progress
    where reporter=?
    order by id desc
    limit 5
    """, (real_name,))

    for r in cur.fetchall():
        reports.append({
            "id": r[0],
            "type": "project",
            "date": r[1],
            "content": r[2]
        })
    reports = sorted(
        reports,
        key=lambda x: x["date"],
        reverse=True
    )[:10]

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

    line = {}
    cur.execute("""
    SELECT
        report_date,
        COUNT(*)
    FROM daily_report
    WHERE reporter=?
    GROUP BY report_date
    """, (real_name,))
    for d, c in cur.fetchall():
        line[d] = \
            line.get(d, 0) + c

    cur.execute("""
    SELECT
        meet_date,
        COUNT(*)
    FROM meeting
    WHERE sponsor=?
    GROUP BY meet_date
    """, (real_name,))

    for d, c in cur.fetchall():
        line[d] = \
            line.get(d, 0) + c

    cur.execute("""
    SELECT
        progress_date,
        COUNT(*)
    FROM project_progress
    WHERE reporter=?
    GROUP BY progress_date
    """, (real_name,))
    for d, c in cur.fetchall():
        line[d] = \
            line.get(d, 0) + c
    line_data = []
    for d in sorted(line.keys()):
        line_data.append(
            {
                "date": d,
                "count": line[d]
            }
        )

    conn.close()

    trend7 = get_submit_trend(
        real_name,
        7
    )

    trend15 = get_submit_trend(
        real_name,
        15
    )

    trend30 = get_submit_trend(
        real_name,
        30
    )

    ai_stats = {

        "report_count": report,

        "meeting_count": meeting,

        "project_count": project,

        "total_count":
            report + meeting + project

    }

    return {

        "total": report + meeting + project,

        "report": report,

        "meeting": meeting,

        "project": project,

        "pie": pie,

        "trend7": trend7,

        "trend15": trend15,

        "trend30": trend30,

        "projects": projects,

        "reports": reports,

        "ai_stats": ai_stats
    }

def build_dashboard_v14(username, real_name):
    data = get_dashboard_data(real_name)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    project_detail_map = {}
    for p in data["projects"]:
        project_detail_map[p[0]] = {
            "id": p[0],
            "name": p[1],
            "leader": p[2],
            "progress": p[3],
            "risk": p[4]
        }

    submit_detail_map = {}
    for r in data["reports"]:
        submit_detail_map[r["id"]] = {
            "id": r["id"],
            "type": r["type"],
            "date": r["date"],
            "content": r["content"]
        }

    project_json = json.dumps(project_detail_map, ensure_ascii=False)
    submit_json = json.dumps(submit_detail_map, ensure_ascii=False)

    pie_json = json.dumps(
        data["pie"],
        ensure_ascii=False
    )

    trend7_json = json.dumps(
        data["trend7"],
        ensure_ascii=False
    )

    trend15_json = json.dumps(
        data["trend15"],
        ensure_ascii=False
    )

    trend30_json = json.dumps(
        data["trend30"],
        ensure_ascii=False
    )

    project_html = ""

    colors = [
        "#1677ff",
        "#13c2c2",
        "#52c41a",
        "#722ed1",
        "#eb2f96",
        "#fa8c16"
    ]

    avatar_color = colors[
        hash(real_name) % len(colors)
    ]

    for idx, p in enumerate(data["projects"]):
        color = colors[idx % len(colors)]

        role = "负责人"

        project_html += f"""
        <div class="project-row">
            <div class="p-name">{p[1]}</div>
            <div class="p-progress-wrap" onclick="toggleProjectRow(this)">
                <!-- 完整文字包含所有换行，默认隐藏 -->
                <div class="full-text">{p[3]}</div>
            </div>
            <div class="p-role">{role}</div>
            <div class="p-end-date">{p[5]}</div>
        </div>
        """

    submit_html = ""
    for r in data["reports"]:
        submit_html += f"""
        <div class="submit-row">
            <div class="submit-dot">
                📄
            </div>
            <div class="submit-info">
                <div class="submit-title">
                    {r["date"]}
                </div>
                <!-- 点击绑定在描述文字上 -->
                <div
                    class="submit-desc"
                    onclick="toggleSubmitRow(this)"
                    data-full="{r['content']}"
                    data-opened="0">
                    {r['content']}
                </div>
            </div>
        </div>
        """
    workbench_page = build_workbench_page(
        real_name,
        now,
        data,
        pie_json,
        project_html,
        submit_html
    )

    project_page = build_project_page(
        project_html
    )

    submit_page = build_submit_page(
        submit_html
    )

    ai_page = build_ai_page(

    )

    profile_page = build_profile_page(
        username,
        real_name,
        avatar_color
    )


    return f"""
    <div
        id="projectData"
        data-json='{project_json}'
        style="display:none">
    </div>

    <div
        id="submitData"
        data-json='{submit_json}'
        style="display:none">
    </div>

    <input
    id="dashboard-user"
    type="hidden"
    value="{real_name}"
    >
    
        <input
        id="trend7Data"
        type="hidden"
        value='{trend7_json}'
        >
        
        <input
        id="trend15Data"
        type="hidden"
        value='{trend15_json}'
        >
        
        <input
        id="trend30Data"
        type="hidden"
        value='{trend30_json}'
        >
        <div class="v14-shell">
        
            <!-- 左侧菜单 -->
        
            <aside class="v14-sidebar">
        
                <div class="logo">
        
                    工作汇报平台
        
                </div>
        
                <div class="menu active"
                     onclick="showPage('workbench',this)">
                     <div style="display:flex;align-items:center;gap:8px;color:#ffffff">
                        <img src="/gradio_api/file=static/images/platform_menu.png" class="menu-icon">
                        工作台
                    </div>
                </div>
        
                <div class="menu"
                     onclick="showPage('project',this)">
                    <div style="display:flex;align-items:center;gap:8px;color:#ffffff">
                        <img src="/gradio_api/file=static/images/project_menu.png" class="menu-icon">
                        我的项目
                    </div>
        
                </div>
        
                <div class="menu"
                     onclick="showPage('submit',this)">
                    <div style="display:flex;align-items:center;gap:8px;color:#ffffff">
                        <img src="/gradio_api/file=static/images/submit_menu.png" class="menu-icon">
                        我的提交
                    </div>
        
                </div>
        
                <div class="menu"
                     onclick="showPage('ai',this)">
                   <div style="display:flex;align-items:center;gap:8px;color:#ffffff">
                        <img src="/gradio_api/file=static/images/ai_menu.png" class="menu-icon">
                        AI工作助手
                   </div>
                
                </div>
        
                <div class="menu"
                     onclick="showPage('profile',this)">
                   <div style="display:flex;align-items:center;gap:8px;color:#ffffff">
                        <img src="/gradio_api/file=static/images/profile_menu.png" class="menu-icon">
                        个人中心
                   </div>
        
                </div>
        
            </aside>

            <!-- 右侧内容 -->
        
            <main class="v14-content">
                
                {workbench_page}

                {project_page}
            
                {submit_page}
                
                {ai_page}
            
                {profile_page}

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

#趋势图日期刷选
def get_line_by_days(real_name, days=7):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            report_date,
            COUNT(*)
        FROM daily_report

        WHERE reporter=?

        GROUP BY report_date

        ORDER BY report_date DESC

        LIMIT ?
    """,(real_name,days))

    rows = cur.fetchall()

    conn.close()

    rows.reverse()

    return [

        {
            "date":r[0],
            "count":r[1]
        }

        for r in rows
    ]

def get_submit_trend(real_name, days):

    conn = get_project_conn()

    cur = conn.cursor()

    result = {}

    # 日报
    cur.execute(
        """
        select
            report_date,
            count(*)
        from daily_report
        where reporter=?
        and report_date>=date(
            'now',
            ?
        )
        group by report_date
        """,
        (
            real_name,
            f"-{days} day"
        )
    )

    for d,c in cur.fetchall():

        result[d] = result.get(d,0)+c

    # 会议

    cur.execute(f"""
    SELECT
        meet_date,
        COUNT(*)
    FROM meeting
    WHERE sponsor=?
    GROUP BY meet_date
    """,(real_name,))

    for d,c in cur.fetchall():

        result[d] = result.get(d,0)+c

    # 项目进展

    cur.execute(f"""
    SELECT
        progress_date,
        COUNT(*)
    FROM project_progress
    WHERE reporter=?
    GROUP BY progress_date
    """,(real_name,))

    for d,c in cur.fetchall():

        result[d] = result.get(d,0)+c

    conn.close()

    rows=[]

    for d in sorted(result.keys())[-days:]:

        rows.append({

            "date":d,

            "count":result[d]

        })

    return rows

def get_project_detail(project_id):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT project_name,
               progress,
               main_leader,
               developers,
               testers,
               risk_block,
               update_time
        FROM project
        WHERE id=?
    """, (project_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "name": row[0],
        "progress": row[1],
        "leader": row[2],
        "dev": row[3],
        "test": row[4],
        "risk": row[5],
        "time": row[6]
    }

def get_submit_detail(submit_id):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT reporter,
               report_content,
               report_date,
               help_item
        FROM daily_report
        WHERE id=?
    """, (submit_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "user": row[0],
        "content": row[1],
        "date": row[2],
        "help": row[3]
    }

def generate_dashboard_ai(real_name):

    data = get_dashboard_data(real_name)

    total = data["total"]

    report = data["report"]

    meeting = data["meeting"]

    project = data["project"]

    return f"""
本周累计提交 {total} 次。

日报提交 {report} 次，
会议记录 {meeting} 次，
项目进展 {project} 次。

整体工作活跃度良好。

建议：

1. 保持日报连续性；
2. 加强项目风险记录；
3. 重点关注延期项目。
"""

def generate_weekly_report(real_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select report_content
        from daily_report
        where reporter=?
        order by id desc
        limit 20
    """,(real_name,))

    texts = []

    for row in cur.fetchall():

        texts.append(row[0])

    return "\n".join(texts)

def generate_daily_report(task_text):

    prompt = f"""
根据以下工作内容，
生成规范日报：

{task_text}
"""

    return call_llm(prompt)

#AI项目分析
def generate_project_analysis(project_name):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select progress,
               risk_block
        from project
        where project_name=?
    """,(project_name,))

    row = cur.fetchone()

    if not row:

        return "项目不存在"

    progress = row[0]

    risk = row[1]

    return f"""
项目：{project_name}

当前进度：

{progress}

风险：

{risk}

AI建议：

1. 持续跟踪关键节点
2. 每周同步风险状态
3. 增加里程碑检查
"""

