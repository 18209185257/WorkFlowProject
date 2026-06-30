from common.db import get_project_conn,get_conn
from datetime import datetime,timedelta


def get_warning_items():

    warnings = []

    conn = get_project_conn()
    conn_user = get_conn()

    cur = conn.cursor()
    cur_user = conn_user.cursor()

    # ==================================
    # 1 项目延期
    # ==================================

    cur.execute("""
    select

        project_name,

        end_date

    from project

    where is_delay='是'
    """)

    for row in cur.fetchall():

        warnings.append(

            f"⚠ 项目延期：{row[0]}"

        )

    # ==================================
    # 2 日报缺失
    # ==================================

    cur_user.execute("""
    select real_name

    from users

    where role='user'
    """)

    users = [
        x[0]
        for x in cur_user.fetchall()
    ]

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    cur.execute("""
    select reporter

    from daily_report

    where report_date=?
    """,(today,))

    submit_users = {
        x[0]
        for x in cur.fetchall()
    }

    for user in users:

        if user not in submit_users:

            warnings.append(

                f"⚠ 未提交日报：{user}"

            )

    # ==================================
    # 3 项目风险
    # ==================================

    cur.execute("""
    select

        project_name,

        risk_block

    from project

    where risk_block<>''
    """)

    for row in cur.fetchall():

        warnings.append(

            f"⚠ 项目风险：{row[0]}"

        )

    conn.close()

    return warnings

def build_warning_html():

    warnings = get_warning_items()

    if not warnings:

        return """
        <div class='warning-empty'>

            ✅ 当前无风险预警

        </div>
        """

    html = """

    <div class='warning-center'>

        <div class='warning-title'>

            🚨 AI预警中心

        </div>

    """

    for item in warnings:

        html += f"""

        <div class='warning-item'>

            {item}

        </div>

        """

    html += "</div>"

    return html

