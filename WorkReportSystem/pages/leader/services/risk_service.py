from common.db import get_project_conn


def build_warning_html():

    conn = get_project_conn()
    cur = conn.cursor()

    warnings = []

    cur.execute("""
    select project_name
    from project
    where is_delay='是'
    """)

    for row in cur.fetchall():

        warnings.append(
            f"🚨 项目延期：{row[0]}"
        )

    cur.execute("""
    select customer_name
    from customer_follow
    where next_follow_date <> ''
    """)

    for row in cur.fetchall():

        pass

    conn.close()

    if not warnings:

        return """
        <div class='warning-card'>
            暂无重大风险
        </div>
        """

    html = "<div class='warning-card'>"

    for item in warnings:

        html += f"<p>{item}</p>"

    html += "</div>"

    return html