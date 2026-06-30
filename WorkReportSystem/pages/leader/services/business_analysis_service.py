from common.db import get_project_conn
from pages.leader.services.chart_renderer import render_chart


def build_business_kpi_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("select count(*) from project")
    project_count = cur.fetchone()[0]

    cur.execute("select count(*) from customer")
    customer_count = cur.fetchone()[0]

    cur.execute("select count(*) from daily_report")
    report_count = cur.fetchone()[0]

    cur.execute("select count(*) from users")
    employee_count = cur.fetchone()[0]

    conn.close()

    return f"""
    <div class='leader-kpi-container'>

        <div class='leader-kpi-card'>
            <div class='value'>{project_count}</div>
            <div class='label'>项目总数</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{customer_count}</div>
            <div class='label'>客户总数</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{employee_count}</div>
            <div class='label'>员工总数</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{report_count}</div>
            <div class='label'>日报总数</div>
        </div>

    </div>
    """

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

#项目增长趋势
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
        ],
        "color":["#3b82f6"],

    }
    return render_chart(
        "project_trend_chart",
        option
    )

#客户增长趋势
def build_customer_growth_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select create_time
        from customer
        """
    )

    rows = cur.fetchall()

    conn.close()

    date_map = {}

    for row in rows:

        if not row[0]:
            continue

        d = str(row[0])[:10]

        date_map[d] = date_map.get(d,0)+1

    dates = sorted(date_map.keys())

    values = [date_map[d] for d in dates]

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"客户增长趋势",
            "textStyle":{"color":"white"}
        },

        "xAxis":{
            "type":"category",
            "data":dates
        },

        "yAxis":{
            "type":"value"
        },

        "series":[
            {
                "type":"line",
                "smooth":True,
                "data":values
            }
        ]
    }

    return render_chart(
        "customer_growth_chart",
        option
    )

#风险趋势
def build_risk_trend_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            risk_level,
            count(*)
        from project
        group by risk_level
        """
    )

    rows = cur.fetchall()

    conn.close()

    data=[]

    for n,v in rows:

        data.append({

            "name":n or "正常",

            "value":v

        })

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"风险项目分布",
            "textStyle":{"color":"white"}
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
        "risk_distribution_chart",
        option
    )

#员工活跃趋势
#统计日报
def build_employee_activity_chart():

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

    names=[]
    values=[]

    for n,v in rows:

        names.append(n)

        values.append(v)

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"员工活跃排行",
            "textStyle":{"color":"white"}
        },

        "xAxis":{
            "type":"category",
            "data":names
        },

        "yAxis":{
            "type":"value"
        },

        "series":[
            {
                "type":"bar",
                "data":values
            }
        ]
    }

    return render_chart(
        "employee_active_chart",
        option
    )

#AI经营洞察
def build_business_ai_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from project
        """
    )

    project_count = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from customer
        """
    )

    customer_count = cur.fetchone()[0]

    conn.close()

    return f"""
    <div class='leader-card'>

        <h3>🤖 AI经营洞察</h3>

        • 当前累计项目 {project_count} 个

        • 当前客户 {customer_count} 家

        • 项目增长趋势稳定

        • 客户增长趋势稳定

        • 建议重点关注高风险项目

    </div>
    """

