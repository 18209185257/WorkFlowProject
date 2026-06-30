import sqlite3
from common.config import DB_PATH

from pages.leader.services.leader_agent import (
    leader_agent
)


def get_project_info(project_name):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        select *
        from project
        where project_name=?
        """,
        (project_name,)
    )

    row = cur.fetchone()

    conn.close()

    return row

def get_project_reports(project_name):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        select
            reporter,
            report_content,
            report_date
        from daily_report
        where report_content like ?
        order by report_date desc
        limit 20
        """,
        (f"%{project_name}%",)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def project_diagnosis(
        username,
        project_name
):

    project = get_project_info(
        project_name
    )

    if not project:

        return "未找到项目"

    reports = get_project_reports(
        project_name
    )

    report_text = ""

    for r in reports:

        report_text += f"""
汇报人：
{r['reporter']}

日期：
{r['report_date']}

内容：
{r['report_content']}
"""

    prompt = f"""
你是一名企业PMO总监。

请分析下面项目。

项目名称：
{project['project_name']}

负责人：
{project['main_leader']}

当前进度：
{project['progress']}

延期情况：
{project['is_delay']}

风险：
{project['risk_block']}

相关日报：

{report_text}

请输出：

# 当前状态

# 风险分析

# 延期概率

# 后续建议

要求专业、简洁。
"""

    result = leader_agent(
        username,
        prompt
    )

    return result
