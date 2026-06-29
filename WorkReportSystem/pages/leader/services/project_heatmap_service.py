from common.db import get_project_conn


def build_project_heatmap_html():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""

    select

        project_name,

        progress,

        is_delay,

        risk_block

    from project

    order by id desc

    """)

    rows = cur.fetchall()

    conn.close()

    html = """

    <div class="heatmap-panel">

        <div class="heatmap-title">

            🔥 项目热力图

        </div>

    """

    for row in rows:

        project_name = row[0]

        progress = row[1]

        is_delay = row[2]

        risk_block = row[3]

        # 风险等级

        if is_delay == "是":

            risk_icon = "🔴"

            risk_text = "高风险"

        elif risk_block:

            risk_icon = "🟡"

            risk_text = "中风险"

        else:

            risk_icon = "🟢"

            risk_text = "正常"

        html += f"""

        <div class="heatmap-row">

            <div class="heatmap-name">

                {project_name}

            </div>

            <div class="heatmap-risk">

                {risk_icon}
                {risk_text}

            </div>

            <div class="heatmap-progress">

                {progress}

            </div>

        </div>

        """

    html += "</div>"

    return html