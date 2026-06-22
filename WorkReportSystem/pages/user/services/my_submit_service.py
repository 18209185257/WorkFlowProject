from common.db import get_project_conn

def query_my_submit_history(
    real_name,
    start_date=None,
    end_date=None,
    submit_type="全部"
):

    conn = get_project_conn()

    cur = conn.cursor()

    result = []

    # 日报
    if submit_type in ["全部", "日报"]:

        sql = """
        select
            report_date,
            report_content
        from daily_report
        where reporter=?
        """

        params = [real_name]

        if start_date:
            sql += " and report_date>=?"
            params.append(start_date)

        if end_date:
            sql += " and report_date<=?"
            params.append(end_date)

        cur.execute(sql, params)

        for row in cur.fetchall():

            result.append({

                "type": "日报",

                "date": row[0],

                "content": row[1]

            })

    # 会议记录
    if submit_type in ["全部", "会议记录"]:

        sql = """
        select
            meet_date,
            meet_title,
            meet_content
        from meeting
        where sponsor=?
        """

        params = [real_name]

        if start_date:
            sql += " and meet_date>=?"
            params.append(start_date)

        if end_date:
            sql += " and meet_date<=?"
            params.append(end_date)

        cur.execute(sql, params)

        for row in cur.fetchall():

            result.append({

                "type": "会议记录",

                "date": row[0],

                "content": f"{row[1]}<br>{row[2]}"

            })

    # 项目汇报
    if submit_type in ["全部", "项目汇报"]:

        sql = """
        select
            create_time,
            progress
        from project
        where main_leader=?
        """

        params = [real_name]

        cur.execute(sql, params)

        for row in cur.fetchall():

            result.append({

                "type": "项目汇报",

                "date": row[0],

                "content": row[1]

            })

    conn.close()

    result.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return result


def build_my_submit_html(
    real_name,
    start_date=None,
    end_date=None,
    submit_type="全部"
):

    rows = query_my_submit_history(
        real_name,
        start_date,
        end_date,
        submit_type
    )

    if not rows:

        return """
        <div class="empty-card">
            暂无提交记录
        </div>
        """

    html = """
    <div class="submit-history-list">
    """

    for row in rows:

        html += f"""
        <div class="submit-card">

            <div class="submit-header">

                <span>
                    {row["type"]}
                </span>

                <span>
                    {row["date"]}
                </span>

            </div>

            <div class="submit-content">

                {row["content"]}

            </div>

        </div>
        """

    html += "</div>"

    return html