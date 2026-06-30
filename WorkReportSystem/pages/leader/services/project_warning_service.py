from datetime import datetime
import sqlite3
from common.config import DB_PATH

def build_project_warning_html():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    warnings = []
    today = datetime.now()
    # ==========================
    # 延期项目
    # ==========================
    cur.execute("""
        select project_name
        from project
        where is_delay='是'
    """)
    for row in cur.fetchall():
        warnings.append(
            (
                "red",
                f"项目延期：{row['project_name']}"
            )
        )

    # ==========================
    # 风险阻塞
    # ==========================

    cur.execute("""
        select
            project_name,
            risk_block
        from project
        where risk_block is not null
          and risk_block!=''
    """)

    for row in cur.fetchall():
        warnings.append(
            (
                "orange",
                f"{row['project_name']} 存在风险阻塞"
            )
        )

    # ==========================
    # 超过7天未更新
    # ==========================
    cur.execute("""
        select
            project_name,
            update_time
        from project
    """)

    for row in cur.fetchall():
        try:
            update_time = datetime.strptime(
                row["update_time"],
                "%Y-%m-%d"
            )
            days = (
                today - update_time
            ).days
            if days >= 7:
                warnings.append(
                    (
                        "red",
                        f"{row['project_name']} 已 {days} 天未更新"
                    )
                )
        except:
            pass
    conn.close()
    if not warnings:
        return """
        <div class='warning-green'>
            ✅ 当前无预警项目
        </div>
        """
    html = ""
    for level, msg in warnings:
        html += f"""
        <div class='warning-{level}'>
            {msg}
        </div>
        """
    return html