from common.db import get_project_conn

from pages.leader.services.chart_renderer import (
    render_chart
)

#API
def build_customer_kpi_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from customer
        """
    )

    total_customer = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from customer
        where date(create_time)=date('now')
        """
    )

    new_customer = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from customer
        where status='流失'
        """
    )

    lost_customer = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from project
        """
    )

    project_count = cur.fetchone()[0]

    conn.close()

    return f"""
    <div class='leader-kpi-container'>

        <div class='leader-kpi-card'>
            <div class='value'>{total_customer}</div>
            <div class='label'>客户总数</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{new_customer}</div>
            <div class='label'>新增客户</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{lost_customer}</div>
            <div class='label'>流失客户</div>
        </div>

        <div class='leader-kpi-card'>
            <div class='value'>{project_count}</div>
            <div class='label'>合作项目数</div>
        </div>

    </div>
    """

#客户贡献排行
def build_customer_amount_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            customer_name,
            amount
        from customer
        order by amount desc
        limit 10
        """
    )

    rows = cur.fetchall()

    conn.close()

    names = []
    values = []

    for n,v in rows:

        names.append(n)

        values.append(v)

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"客户项目金额排行",
            "textStyle":{"color":"white"}
        },

        "tooltip":{},

        "xAxis":{
            "type":"value",
            "axisLabel":{"color":"white"}
        },

        "yAxis":{
            "type":"category",
            "data":names,
            "axisLabel":{"color":"white"}
        },

        "series":[
            {
                "type":"bar",
                "data":values,
                "itemStyle":{
                    "color":"#3b82f6"
                }
            }
        ]
    }

    return render_chart(
        "customer_amount_chart",
        option
    )

#客户项目排行榜
def build_customer_project_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            customer_name,
            count(*)
        from project
        group by customer_name
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
            "text":"客户项目数量排行",
            "textStyle":{"color":"white"}
        },

        "tooltip":{},

        "xAxis":{
            "type":"category",
            "data":names,
            "axisLabel":{
                "color":"white",
                "rotate":30
            }
        },

        "yAxis":{
            "type":"value",
            "axisLabel":{"color":"white"}
        },

        "series":[
            {
                "type":"bar",
                "data":values,
                "itemStyle":{
                    "color":"#06b6d4"
                }
            }
        ]
    }

    return render_chart(
        "customer_project_chart",
        option
    )

#行业分布
def build_customer_industry_chart():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            industry,
            count(*)
        from customer
        group by industry
        """
    )

    rows = cur.fetchall()

    conn.close()

    data=[]

    for n,v in rows:

        data.append({

            "name":n,

            "value":v

        })

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"客户行业分布",
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
        "customer_industry_chart",
        option
    )

#客户活跃度
def build_customer_active_chart():

    option = {

        "backgroundColor":"#1e293b",

        "title":{
            "text":"客户活跃度",
            "textStyle":{"color":"white"}
        },

        "series":[
            {
                "type":"pie",

                "radius":"65%",

                "data":[

                    {
                        "name":"活跃客户",
                        "value":80
                    },

                    {
                        "name":"沉默客户",
                        "value":20
                    }

                ]
            }
        ]
    }

    return render_chart(
        "customer_active_chart",
        option
    )

#风险客户榜
def build_customer_risk_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            customer_name,
            status
        from customer
        where status!='正常'
        limit 10
        """
    )

    rows = cur.fetchall()

    conn.close()

    html = """
    <div class='leader-card'>

    <h3>⚠ 风险客户榜</h3>

    <table class='leader-table'>
    """

    for name,status in rows:

        html += f"""
        <tr>

            <td>{name}</td>

            <td>{status}</td>

        </tr>
        """

    html += "</table></div>"

    return html

#AI客户洞察
def build_customer_ai_insight():

    return """
    <div class='leader-card'>

    <h3>🤖 AI客户洞察</h3>

    • 本月新增客户 5 家

    • 华为项目金额最高

    • 腾讯30天未联系

    • 制造业客户占比最高

    • 建议重点维护高价值客户

    </div>
    """