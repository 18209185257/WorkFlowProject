from common.db import get_conn

from project_manager.ai_task_service import (
    create_ai_task
)


def auto_check_daily_report():

    conn = get_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select username
        from users
        where role='user'
        """
    )

    users = cur.fetchall()

    conn.close()

    count = 0

    for u in users:

        create_ai_task(

            project_name="日报",

            title="日报补交",

            desc="系统检测日报缺失",

            assignee=u[0],

            priority="中",

            deadline="今日18点"

        )

        count += 1

    return count