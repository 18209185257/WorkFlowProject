from common.db import get_project_conn


def get_business_stats():
    conn = get_project_conn()
    cur = conn.cursor()
    # 项目总数
    cur.execute(
        "select count(*) from project"
    )
    project_total = cur.fetchone()[0]
    # 延期项目
    cur.execute(
        """
        select count(*)
        from project
        where is_delay='是'
        """
    )
    delay_count = cur.fetchone()[0]
    # 风险项目
    cur.execute(
        """
        select count(*)
        from project
        where risk_block is not null
        and trim(risk_block)!=''
        """
    )
    risk_count = cur.fetchone()[0]
    # 日报数量
    cur.execute(
        """
        select count(*)
        from daily_report
        """
    )
    report_count = cur.fetchone()[0]
    conn.close()
    return {
        "project_total": project_total,
        "delay_count": delay_count,
        "risk_count": risk_count,
        "report_count": report_count
    }


def get_risk_projects():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            project_name,
            main_leader,
            risk_block
        from project
        where risk_block is not null
        and trim(risk_block)!=''
        order by update_time desc
        limit 10
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def get_delay_projects():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            project_name,
            main_leader
        from project
        where is_delay='是'
        order by update_time desc
        limit 10
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows
