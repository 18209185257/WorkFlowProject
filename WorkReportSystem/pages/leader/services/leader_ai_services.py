from common.db import get_project_conn,get_conn

from datetime import datetime

#今日未交日报
def get_not_submit_report_users():

    conn = get_project_conn()
    user_conn = get_conn()

    cur = conn.cursor()
    user_cur = user_conn.cursor()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    user_cur.execute("""
    select real_name
    from users
    where role='user'
    """)

    all_users = {
        x[0]
        for x in user_cur.fetchall()
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

    conn.close()

    return list(
        all_users - submit_users
    )

#风险项目
def get_high_risk_projects():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select
        project_name,
        risk_block
    from project
    where risk_block<>''
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

#员工最近工作
def get_employee_recent_work(
        real_name
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select report_content
    from daily_report
    where reporter=?
    order by id desc
    limit 10
    """,(real_name,))

    rows = cur.fetchall()

    conn.close()

    return "\n".join(
        x[0]
        for x in rows
    )

