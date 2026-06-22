from common.db import get_project_conn


def build_warning_html():

    conn = get_project_conn()

    cur = conn.cursor()

    warnings = []

    cur.execute("""
    select
        project_name,
        risk_block
    from project
    where risk_block <> ''
    """)

    for row in cur.fetchall():

        warnings.append(
            f"⚠ 项目【{row[0]}】存在风险：{row[1]}"
        )

    cur.execute("""
    select
        customer_name,
        next_follow_date
    from customer_follow
    """)

    for row in cur.fetchall():

        warnings.append(
            f"📞 客户【{row[0]}】待跟进"
        )

    conn.close()

    if not warnings:

        return """
        <div class='warning-card'>
        当前无风险
        </div>
        """

    html = "<div class='warning-card'>"

    for item in warnings:

        html += f"<p>{item}</p>"

    html += "</div>"

    return html