import sqlite3
from common.config import DB_PATH


def build_auto_ai_insight():

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    # =====================
    # 项目总数
    # =====================

    cur.execute(
        "select count(*) from project"
    )

    project_count = cur.fetchone()[0]

    # =====================
    # 延期项目
    # =====================

    cur.execute(
        """
        select count(*)
        from project
        where is_delay='是'
        """
    )

    delay_count = cur.fetchone()[0]

    # =====================
    # 风险项目
    # =====================

    cur.execute(
        """
        select project_name
        from project
        where risk_block is not null
          and risk_block!=''
        limit 3
        """
    )

    risk_projects = [
        row[0]
        for row in cur.fetchall()
    ]

    # =====================
    # 今日日报数
    # =====================

    cur.execute(
        """
        select count(*)
        from daily_report
        where report_date=date('now')
        """
    )

    report_count = cur.fetchone()[0]

    conn.close()

    html = f"""

    <div class='leader-auto-ai'>

        <div class='ai-title'>
            🤖 AI自动洞察
        </div>

        <div class='ai-subtitle'>
            <b>{project_count}</b>
            个项目
        </div>

        <div class='ai-suggest'>
            ⚠️ 延期项目
            <b>{delay_count}</b>
            个
        </div>

        <div class='ai-suggest'>
            📋 今日日报
            <b>{report_count}</b>
            份
        </div>

        <hr>

        <div class='ai-subtitle'>
            🔥 风险项目：
        </div>

        <ul>

            {''.join(
                [f"<li>{p}</li>"
                 for p in risk_projects]
            )}

        </ul>

        <hr>

        <div class='ai-subtitle'>

        💡 建议优先关注：

        </div>

        <div class='ai-suggest'>

        {risk_projects[0]
        if risk_projects
        else "暂无高风险项目"}

        </div>

    </div>

    """

    return html