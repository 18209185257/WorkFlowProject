from common.db import get_project_conn,get_conn
import json
from pages.user.services.ai_chat_service import (
    generate_ai_chat
)
from pages.leader.services.chart_renderer import (
    render_chart
)

def get_leader_kpi():

    conn = get_project_conn()
    user_conn = get_conn()

    cur = conn.cursor()
    user_cur = user_conn.cursor()

    result = {}

    # 项目数
    cur.execute(
        """
        select count(*)
        from project
        """
    )

    result["project_count"] = cur.fetchone()[0]

    # 员工数
    user_cur.execute(
        """
        select count(*)
        from users
        where role='user'
        """
    )

    result["employee_count"] = user_cur.fetchone()[0]

    # 客户数
    cur.execute(
        """
        select count(*)
        from customer
        """
    )

    result["customer_count"] = cur.fetchone()[0]

    # 风险数
    cur.execute(
        """
        select count(*)
        from project
        where risk_block is not null
        and risk_block <> ''
        """
    )

    result["risk_count"] = cur.fetchone()[0]

    # 日报数
    cur.execute(
        """
        select count(*)
        from daily_report
        """
    )

    result["daily_count"] = cur.fetchone()[0]

    # 会议数
    cur.execute(
        """
        select count(*)
        from meeting
        """
    )

    result["meeting_count"] = cur.fetchone()[0]

    conn.close()

    return result

def build_kpi_html():

    data = get_leader_kpi()
    return f"""
    <div class="leader-kpi-grid">

        <div class="leader-kpi-card">
            <div class="kpi-title">项目总数</div>
            <div class="kpi-value">
                {data["project_count"]}
            </div>
        </div>

        <div class="leader-kpi-card">
            <div class="kpi-title">员工总数</div>
            <div class="kpi-value">
                {data["employee_count"]}
            </div>
        </div>

        <div class="leader-kpi-card">
            <div class="kpi-title">客户总数</div>
            <div class="kpi-value">
                {data["customer_count"]}
            </div>
        </div>

        <div class="leader-kpi-card">
            <div class="kpi-title">风险数量</div>
            <div class="kpi-value risk">
                {data["risk_count"]}
            </div>
        </div>

        <div class="leader-kpi-card">
            <div class="kpi-title">日报总数</div>
            <div class="kpi-value">
                {data["daily_count"]}
            </div>
        </div>

        <div class="leader-kpi-card">
            <div class="kpi-title">会议总数</div>
            <div class="kpi-value">
                {data["meeting_count"]}
            </div>
        </div>

    </div>
    """

def get_project_status_data():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select
        is_delay,
        count(*)
    from project
    group by is_delay
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_project_status_chart():

    rows = get_project_status_data()
    print("项目状态数据：", rows)

    data = []

    for name,count in rows:

        if not name:
            name = "正常"

        data.append({
            "value":count,
            "name":name
        })

    option = {
        "backgroundColor":"#1e293b",

        "tooltip":{
            "trigger":"item"
        },

        "legend":{
            "textStyle":{
                "color":"white"
            }
        },

        "series":[
            {
                "type":"pie",

                "radius":"65%",

                "data":data
            }
        ]
    }

    return render_chart(
        "project_status_chart",
        option
    )

def get_project_trend():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select
        update_time,
        count(*)
    from project
    group by update_time
    order by update_time
    limit 30
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_project_trend_chart():
    print(
        "build_project_trend_chart()"
    )

    rows = get_project_trend()
    print("项目趋势数据：", rows)

    dates = []
    counts = []

    for d,c in rows:

        dates.append(d)

        counts.append(c)

    option = {

        "backgroundColor":"#1e293b",

        "tooltip":{},

        "xAxis":{
            "type":"category",
            "data":dates,
            "axisLabel":{
                "color":"white"
            }
        },

        "yAxis":{
            "type":"value",
            "axisLabel":{
                "color":"white"
            }
        },

        "series":[
            {
                "type":"line",
                "smooth":True,
                "data":counts
            }
        ]
    }
    return render_chart(
        "project_trend_chart",
        option
    )

#日报提交趋势图
def get_daily_report_trend():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select
        report_date,
        count(*)
    from daily_report
    group by report_date
    order by report_date
    limit 30
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_daily_report_chart():

    rows = get_daily_report_trend()
    print("日报趋势数据：", rows)

    dates = []
    counts = []

    for d,c in rows:

        dates.append(d)

        counts.append(c)

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"日报提交趋势",
            "textStyle":{
                "color":"white"
            }
        },

        "tooltip":{},

        "xAxis":{
            "type":"category",
            "data":dates,
            "axisLabel":{
                "color":"white"
            }
        },

        "yAxis":{
            "type":"value",
            "axisLabel":{
                "color":"white"
            }
        },

        "series":[
            {
                "type":"bar",
                "data":counts
            }
        ]
    }

    return render_chart(
        "daily_report_chart",
         option
    )

#风险排行榜
def get_risk_rank():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select
        project_name,
        risk_block
    from project
    where risk_block is not null
    and risk_block <> ''
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def build_risk_rank_html():

    rows = get_risk_rank()

    html = """
    <div class="leader-risk-panel">

        <div class="risk-title">
            ⚠ 风险排行榜
        </div>
    """

    for project,risk in rows[:10]:

        html += f"""
        <div class="risk-item">

            <div class="risk-project">
                {project}
            </div>

            <div class="risk-content">
                {risk}
            </div>

        </div>
        """

    html += "</div>"

    return html

def get_dashboard_ai_insight():

    conn = get_project_conn()
    conn_user = get_conn()

    cur = conn.cursor()
    cur_user = conn_user.cursor()

    # 风险项目

    cur.execute("""
    select count(*)
    from project
    where risk_block<>''
    """)

    risk_count = cur.fetchone()[0]

    # 延期项目

    cur.execute("""
    select count(*)
    from project
    where is_delay='是'
    """)

    delay_count = cur.fetchone()[0]

    # 未提交日报

    from datetime import datetime

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn_user.execute("""
    select real_name
    from users
    where role='user'
    """)

    all_users = {
        x[0]
        for x in cur_user.fetchall()
    }

    cur.execute("""
    select reporter
    from daily_report
    where report_date=?
    """,(today,))

    submit_users = {
        x[0]
        for x in cur.fetchall()
    }

    not_submit = len(
        all_users - submit_users
    )

    # 高风险项目

    cur.execute("""
    select
        project_name
    from project
    where risk_block<>''
    limit 5
    """)

    projects = [
        x[0]
        for x in cur.fetchall()
    ]

    conn.close()

    return {

        "risk":risk_count,

        "delay":delay_count,

        "not_submit":not_submit,

        "projects":projects

    }

def build_ai_insight_html():

    data = get_dashboard_ai_insight()

    html = f"""

    <div class="leader-ai-insight">

        <div class="insight-title">

            🤖 AI洞察

        </div>

        <div class="insight-item">

            ⚠ 高风险项目：
            {data["risk"]} 个

        </div>

        <div class="insight-item">

            🚨 延期项目：
            {data["delay"]} 个

        </div>

        <div class="insight-item">

            📅 未提交日报：
            {data["not_submit"]} 人

        </div>

        <div class="insight-item">

            📈 本周重点关注：

            <br>

            {"<br>".join(data["projects"])}

        </div>

    </div>

    """

    return html

def build_auto_ai_insight():

    data = get_dashboard_ai_insight()

    prompt = f"""
你是企业管理驾驶舱AI。

当前数据：

高风险项目：

{data['risk']}

延期项目：

{data['delay']}

未提交日报：

{data['not_submit']}

重点项目：

{','.join(data['projects'])}

请输出：

1、当前经营状态

2、风险等级

3、建议优先关注内容

控制在200字以内。
"""

    return generate_ai_chat(
        "leader",
        prompt
    )




