from datetime import datetime

from common.db import get_project_conn

from pages.leader.services.ai_decision_service import (
    build_ai_decision
)

#自动生成报告
def generate_daily_business_report():

    report = build_ai_decision("system")

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        insert into ai_business_report
        (
            report_date,
            report_content,
            create_time
        )
        values
        (
            ?,
            ?,
            ?
        )
        """,
        (
            datetime.now().strftime("%Y-%m-%d"),
            report,
            str(datetime.now())
        )
    )

    conn.commit()

    conn.close()

    return report

#查询历史报告
def get_business_reports():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            report_date,
            report_content
        from ai_business_report
        order by id desc
        limit 30
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows
