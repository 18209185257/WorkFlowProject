from common.db import get_conn,get_project_conn

from .chart_renderer import (
    render_chart
)

#KPI
def build_employee_kpi_html():

    conn = get_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from users
        where role='user'
        """
    )

    employee_count = cur.fetchone()[0]

    conn.close()

    return f"""
    <div class='leader-kpi-container'>

        <div class='leader-kpi-card'>
            <div class='value'>
                {employee_count}
            </div>
            <div class='label'>
                员工总数
            </div>
        </div>

    </div>
    """

#工作负荷排行
def build_employee_workload_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            project_name,
            count(*)
        from project
        group by project_name
        order by count(*) desc
        limit 10
        """
    )

    rows = cur.fetchall()

    conn.close()

    names = []
    counts = []

    for n,c in rows:

        names.append(n)

        counts.append(c)

    option = {

        "title":{
            "text":"项目负责排行",
            "textStyle":{"color":"white"}
        },

        "backgroundColor":"#1e293b",

        "tooltip":{},

        "xAxis":{
            "type":"category",
            "data":names,
            "axisLabel":{"color":"white"}
        },

        "yAxis":{
            "type":"value",
            "axisLabel":{"color":"white"}
        },

        "series":[
            {
                "type":"bar",
                "data":counts
            }
        ]
    }

    return render_chart(
        "employee_workload_chart",
        option
    )

#日报提交排行
def build_employee_report_chart():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            reporter,
            count(*)
        from daily_report
        group by reporter
        order by count(*) desc
        limit 10
        """
    )

    rows = cur.fetchall()
    conn.close()

    names = []
    counts = []

    for n,c in rows:

        names.append(n)

        counts.append(c)

    option = {

        "title":{
            "text":"日报提交排行",
            "textStyle":{"color":"white"}
        },

        "backgroundColor":"#1e293b",

        "tooltip":{},

        "xAxis":{
            "type":"category",
            "data":names,
            "axisLabel":{"color":"white"}
        },

        "yAxis":{
            "type":"value",
            "axisLabel":{"color":"white"}
        },

        "series":[
            {
                "type":"bar",
                "data":counts
            }
        ]
    }

    return render_chart(
        "employee_report_chart",
        option
    )

#风险员工榜
def build_employee_risk_html():

    return """
    <div class='leader-card'>

        <h3>⚠ 风险员工榜</h3>
        <div 
        class='risk-content'>
            暂无数据
        </div>

    </div>
    """

#AI员工洞察
def build_employee_ai_insight():

    return """
    <div class='leader-card'>

        <h3>🤖 AI员工洞察</h3>
        <div class='ai-insight-content'>
            • 正在分析员工工作情况
        </div>

    </div>
    """