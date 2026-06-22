from common.db import get_project_conn,OLLAMA_URL

import requests
import json


MODEL_NAME = "qwen2.5:7b"


def call_llm(prompt):

    payload = {

        "model": MODEL_NAME,

        "prompt": prompt,

        "stream": False,

        "temperature": 0.2
    }

    try:

        r = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )

        return r.json()["response"]

    except Exception as e:

        return f"AI分析失败：{str(e)}"


def build_business_analysis_html():

    conn = get_project_conn()

    cur = conn.cursor()

    # =====================
    # 项目
    # =====================

    cur.execute("""
    select

        project_name,
        main_leader,
        is_delay,
        risk_block,
        progress

    from project
    """)

    projects = cur.fetchall()

    # =====================
    # 客户
    # =====================

    cur.execute("""
    select

        customer_name,
        sales_name,
        customer_level,
        customer_status,
        follow_stage,
        next_follow_date

    from customer_follow
    """)

    customers = cur.fetchall()

    # =====================
    # 日报
    # =====================

    cur.execute("""
    select

        reporter,
        report_content,
        help_item

    from daily_report
    order by id desc
    limit 50
    """)

    reports = cur.fetchall()

    conn.close()

    prompt = f"""
    你是企业CEO经营顾问。

    请根据经营数据输出日报。

    要求：

    不要超过600字。

    必须输出：

    【经营评分】

    【经营概况】

    【销售情况】

    【项目情况】

    【风险预警】

    【重点员工】

    【经营建议】

    重点指出：

    1 延期项目

    2 高风险项目

    3 超期未跟进客户

    4 未回款订单

    5 活跃员工

    项目数据：
    {projects}

    客户数据：
    {customers}

    订单数据：
    {0}

    回款数据：
    {0}

    日报数据：
    {reports}
    """
    return call_llm(prompt)

def wrap_analysis(text):

    return f"""
    <div class="ai-analysis-card">

    {text.replace(chr(10),'<br>')}

    </div>
    """

# 驾驶舱大屏HTML
def build_cockpit_html(stats):
    return f"""
    <div class="cockpit-board">

        <div class="cockpit-card">
            <h3>客户总数</h3>
            <div class="cockpit-value">
                {stats["customer_count"]}
            </div>
        </div>

        <div class="cockpit-card">
            <h3>项目总数</h3>
            <div class="cockpit-value">
                {stats["project_count"]}
            </div>
        </div>

        <div class="cockpit-card">
            <h3>订单总金额</h3>
            <div class="cockpit-value">
                ¥{stats["order_amount"]}
            </div>
        </div>

        <div class="cockpit-card">
            <h3>累计回款</h3>
            <div class="cockpit-value">
                ¥{stats["payment_amount"]}
            </div>
        </div>

    </div>
    """