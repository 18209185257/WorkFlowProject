from common.db import get_project_conn


def get_user_daily_reports(real_name, limit=20):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        report_date,
        report_content
    from daily_report
    where reporter=?
    order by id desc
    limit ?
    """, (real_name, limit))

    rows = cur.fetchall()

    conn.close()

    return rows


def get_user_meetings(real_name, limit=20):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        meet_date,
        meet_content
    from meeting
    where sponsor=?
    order by id desc
    limit ?
    """, (real_name, limit))

    rows = cur.fetchall()

    conn.close()

    return rows


def get_user_project_progress(real_name):

    conn = get_project_conn()
    cur = conn.cursor()

    cur.execute("""
    select
        progress_date,
        progress_content
    from project_progress
    where reporter=?
    order by id desc
    limit 50
    """, (real_name,))

    rows = cur.fetchall()

    conn.close()

    return rows

#AI项目总结
def generate_project_summary(
    real_name
):

    progresses = \
        get_user_project_progress(
            real_name
        )

    txt = ""

    for d,c in progresses:

        txt += f"{d}:{c}\n"

    return f"""
请分析以下项目进展：

输出：

项目完成情况

当前风险

下一步建议

数据：

{txt}
"""