import sqlite3

from common.config import DB_PATH

def build_weekly_report():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 项目总数
    cur.execute(
        "select count(*) from project"
    )
    project_count = cur.fetchone()[0]
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
        select project_name
        from project
        where risk_block!=''
        """
    )
    risk_projects = [
        x[0]
        for x in cur.fetchall()
    ]
    # 日报数
    cur.execute(
        """
        select count(*)
        from daily_report
        """
    )
    report_count = cur.fetchone()[0]
    conn.close()
    md = f"""
# 📄 本周工作周报

## 一、项目情况

- 项目总数：{project_count}
- 延期项目：{delay_count}

## 二、日报情况

- 累计日报：{report_count} 份

## 三、重点风险

"""

    for p in risk_projects:

        md += f"- {p}\n"

    md += """

## 四、建议

优先关注风险项目推进情况。

"""

    return md