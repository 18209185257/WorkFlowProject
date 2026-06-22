from common.db import get_project_conn
import json

# KPI
def dashboard_kpi_api(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM daily_report WHERE reporter=?
    """, (real_name,))
    report = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM meeting WHERE sponsor=?
    """, (real_name,))
    meeting = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM project
        WHERE main_leader LIKE ?
           OR developers LIKE ?
           OR testers LIKE ?
           OR designer LIKE ?
    """, tuple([f"%{real_name}%"]*4))

    project = cur.fetchone()[0]

    conn.close()

    return {
        "report": report,
        "meeting": meeting,
        "project": project
    }

def api_submit_pie(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        (SELECT COUNT(*) FROM daily_report WHERE reporter=?),
        (SELECT COUNT(*) FROM meeting WHERE sponsor=?),
        (SELECT COUNT(*) FROM project WHERE main_leader LIKE ?)
    """, (
        real_name,
        real_name,
        f"%{real_name}%"
    ))

    r = cur.fetchone()
    conn.close()

    return {
        "report": r[0],
        "meeting": r[1],
        "project": r[2]
    }

def api_submit_line(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT date(create_time) as d, COUNT(*)
        FROM daily_report
        WHERE reporter=?
        GROUP BY d
        ORDER BY d
    """, (real_name,))

    rows = cur.fetchall()
    conn.close()

    return rows


def get_dashboard_data(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute(
        """
        select count(*)
        from daily_report
        where reporter=?
        """,
        (real_name,)
    )
    report_count = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from meeting
        where sponsor=?
        """,
        (real_name,)
    )
    meeting_count = cur.fetchone()[0]

    cur.execute(
        """
        select count(*)
        from project
        where main_leader like ?
        """,
        (f"%{real_name}%",)
    )
    project_count = cur.fetchone()[0]

    conn.close()

    return json.dumps(
        {
            "report": report_count,
            "meeting": meeting_count,
            "project": project_count
        }
    )

def dashboard_line_api(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
        select substr(report_date,1,10), count(*)
        from daily_report
        where reporter=?
        group by substr(report_date,1,10)
        order by report_date asc
    """, (real_name,))

    rows = cur.fetchall()

    conn.close()

    return [
        [r[0], r[1]]
        for r in rows
    ]