from datetime import datetime, timedelta

from common.db import (
    get_conn,
    get_project_conn
)

from .project_detail_service import (
    get_project_health_rank,
    get_risk_warning_projects
)


def get_date_condition(range_type):
    today = datetime.now()
    if range_type == "today":
        start = today.strftime("%Y-%m-%d")
        end = start
    elif range_type == "week":
        monday = today - timedelta(days=today.weekday())
        start = monday.strftime("%Y-%m-%d")
        end = today.strftime("%Y-%m-%d")
    elif range_type == "month":
        start = today.strftime("%Y-%m-01")
        end = today.strftime("%Y-%m-%d")
    else:
        return None
    return start, end

def get_dashboard_stats(range_type="all"):
    conn = get_project_conn()
    cur = conn.cursor()

    user_conn = get_conn()
    user_cur = user_conn.cursor()

    user_cur.execute(
        "SELECT COUNT(*) FROM users"
    )
    user_count = user_cur.fetchone()[0]

    if range_type == "today":

        project_where = """
        date(update_time)=date('now')
        """

        report_where = """
        date(report_date)=date('now')
        """

        meeting_where = """
        date(meet_date)=date('now')
        """

    elif range_type == "week":

        project_where = """
        strftime('%Y-%W',update_time)=
        strftime('%Y-%W','now')
        """

        report_where = """
        strftime('%Y-%W',report_date)=
        strftime('%Y-%W','now')
        """

        meeting_where = """
        strftime('%Y-%W',meet_date)=
        strftime('%Y-%W','now')
        """

    elif range_type == "month":

        project_where = """
        strftime('%Y-%m',update_time)=
        strftime('%Y-%m','now')
        """

        report_where = """
        strftime('%Y-%m',report_date)=
        strftime('%Y-%m','now')
        """

        meeting_where = """
        strftime('%Y-%m',meet_date)=
        strftime('%Y-%m','now')
        """

    else:

        project_where = "1=1"
        report_where = "1=1"
        meeting_where = "1=1"

    cur.execute(
        f"SELECT COUNT(*) FROM project WHERE {project_where}"
    )
    project_count = cur.fetchone()[0]

    cur.execute(
        f"SELECT COUNT(*) FROM daily_report WHERE {report_where}"
    )
    report_count = cur.fetchone()[0]

    cur.execute(
        f"SELECT COUNT(*) FROM meeting WHERE {meeting_where}"
    )
    meeting_count = cur.fetchone()[0]

    conn.close()
    user_conn.close()

    return {
        "user_count": user_count,
        "project_count": project_count,
        "report_count": report_count,
        "meeting_count": meeting_count
    }

def get_cockpit_stats():
    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select count(*)
    from customer_follow
    """)

    # 客户数
    customer_count = cur.fetchone()[0]

    cur.execute("""
    select count(*)
    from project
    """)

    #项目数
    project_count = cur.fetchone()[0]

    cur.execute("""
    select ifnull(sum(order_amount),0)
    from sales_order
    """)

    #订单金额
    order_amount = cur.fetchone()[0]

    cur.execute("""
    select ifnull(sum(payment_amount),0)
    from payment_record
    """)

    # 回款金额
    payment_amount = cur.fetchone()[0]

    return {

        "customer_count": customer_count,

        "project_count": project_count,

        "order_amount": round(order_amount, 2),

        "payment_amount": round(payment_amount, 2)
    }


def get_dashboard_project_stat():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        "select count(*) from project"
    )
    total = cur.fetchone()[0]
    cur.execute("""
    select count(*)
    from project
    where is_delay='是'
    """)
    delay = cur.fetchone()[0]
    conn.close()
    warning = len(
        get_risk_warning_projects()
    )
    healthy = len([
        x
        for x in get_project_health_rank()
        if x[1] >= 80
    ])
    return {
        "total": total,
        "delay": delay,
        "warning": warning,
        "healthy": healthy
    }

def build_project_dashboard_html():
    stat = get_dashboard_project_stat()
    return f"""
    <div class='dashboard-kpi-wrap'>
        <div class='kpi-card'>
            <div>{stat["total"]}</div>
            <span>项目总数</span>
        </div>
        <div class='kpi-card'>
            <div>{stat["delay"]}</div>
            <span>延期项目</span>
        </div>
        <div class='kpi-card'>
            <div>{stat["warning"]}</div>
            <span>风险项目</span>
        </div>
        <div class='kpi-card'>
            <div>{stat["healthy"]}</div>
            <span>健康项目</span>
        </div>
    </div>
    """