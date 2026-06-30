import sqlite3
from common.config import DB_PATH
from pages.leader.services.leader_agent import (
    leader_agent
)

def load_project_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        select
            project_name,
            progress,
            is_delay,
            risk_block
        from project
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def load_report_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        select
            reporter,
            report_content
        from daily_report
        order by id desc
        limit 100
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def build_weekly_context():
    projects = load_project_data()

    reports = load_report_data()
    context = "项目情况：\n"

    for p in projects:
        context += f"""
    项目:
    {p[0]}

    进度:
    {p[1]}

    延期:
    {p[2]}

    风险:
    {p[3]}
    """
    context += "\n日报情况：\n"

    for r in reports:
        context += f"""
    人员:
    {r[0]}

    内容:
    {r[1]}
    """
    return context

def build_ai_weekly_report():
    context = build_weekly_context()
    prompt = f"""
    你是企业总经理助理。

    请根据以下数据生成领导周报。

    要求：

    1 项目总体情况

    2 风险情况

    3 员工工作情况

    4 需要重点关注的问题

    5 下周建议

    数据：

    {context}
    """

    report = leader_agent(
        "系统",
        prompt
    )
    return report