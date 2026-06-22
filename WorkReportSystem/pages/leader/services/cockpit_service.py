from common.db import get_project_conn


def build_cockpit_html():

    conn = get_project_conn()
    cur = conn.cursor()

    # 项目数
    cur.execute(
        "select count(*) from project"
    )
    project_count = cur.fetchone()[0]

    # 延期项目
    cur.execute("""
    select count(*)
    from project
    where is_delay='是'
    """)
    delay_count = cur.fetchone()[0]

    # 客户数
    cur.execute("""
    select count(*)
    from customer_follow
    """)
    customer_count = cur.fetchone()[0]

    # 跟进客户
    cur.execute("""
    select count(*)
    from customer_follow
    where follow_stage <> ''
    """)
    follow_count = cur.fetchone()[0]

    # 订单数
    cur.execute("""
    select count(*)
    from sales_order
    """)
    order_count = cur.fetchone()[0]

    # 订单金额
    cur.execute("""
    select ifnull(sum(order_amount),0)
    from sales_order
    """)
    order_amount = cur.fetchone()[0]

    # 回款
    cur.execute("""
    select ifnull(sum(payment_amount),0)
    from payment_record
    """)
    payment_amount = cur.fetchone()[0]

    # 日报数
    cur.execute("""
    select count(*)
    from daily_report
    """)
    report_count = cur.fetchone()[0]

    conn.close()

    return f"""
    <div class="cockpit-board">

        <div class="cockpit-card">
            <div class="title">项目总数</div>
            <div class="value">{project_count}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">延期项目</div>
            <div class="value danger">{delay_count}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">客户总数</div>
            <div class="value">{customer_count}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">跟进客户</div>
            <div class="value">{follow_count}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">订单数量</div>
            <div class="value">{order_count}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">订单金额</div>
            <div class="value">¥{order_amount}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">累计回款</div>
            <div class="value success">¥{payment_amount}</div>
        </div>

        <div class="cockpit-card">
            <div class="title">日报总数</div>
            <div class="value">{report_count}</div>
        </div>

    </div>
    """

def build_rank_html():

    conn = get_project_conn()

    cur = conn.cursor()

    # =====================
    # 项目负责人排行
    # =====================

    cur.execute("""
    SELECT

        main_leader,
        COUNT(*)

    FROM project

    GROUP BY main_leader

    ORDER BY COUNT(*) DESC

    LIMIT 10
    """)

    project_rank = cur.fetchall()

    # =====================
    # 延期排行
    # =====================

    cur.execute("""
    SELECT

        main_leader,
        COUNT(*)

    FROM project

    WHERE is_delay='是'

    GROUP BY main_leader

    ORDER BY COUNT(*) DESC

    LIMIT 10
    """)

    delay_rank = cur.fetchall()

    # =====================
    # 风险排行
    # =====================

    cur.execute("""
    SELECT

        main_leader,
        COUNT(*)

    FROM project

    WHERE risk_block IS NOT NULL
    AND trim(risk_block)!=''

    GROUP BY main_leader

    ORDER BY COUNT(*) DESC

    LIMIT 10
    """)

    risk_rank = cur.fetchall()

    conn.close()

    html = """
    <div class="rank-wrap">
    """

    # =====================
    # 项目排行
    # =====================

    html += """
    <div class="rank-card">

        <div class="rank-title">

        🏆 项目负责人排行

        </div>
    """

    for i, row in enumerate(project_rank, start=1):

        html += f"""
        <div class="rank-row">

            <span>{i}. {row[0]}</span>

            <span>{row[1]}个项目</span>

        </div>
        """

    html += "</div>"

    # =====================
    # 延期排行
    # =====================

    html += """
    <div class="rank-card">

        <div class="rank-title">

        🚨 延期负责人排行

        </div>
    """

    for i, row in enumerate(delay_rank, start=1):

        html += f"""
        <div class="rank-row">

            <span>{i}. {row[0]}</span>

            <span>{row[1]}个延期</span>

        </div>
        """

    html += "</div>"

    # =====================
    # 风险排行
    # =====================

    html += """
    <div class="rank-card">

        <div class="rank-title">

        ⚠ 风险负责人排行

        </div>
    """

    for i, row in enumerate(risk_rank, start=1):

        html += f"""
        <div class="rank-row">

            <span>{i}. {row[0]}</span>

            <span>{row[1]}个风险</span>

        </div>
        """

    html += "</div>"

    html += "</div>"

    return html