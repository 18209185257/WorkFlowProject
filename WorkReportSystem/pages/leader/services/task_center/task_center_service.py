from common.db import get_project_conn


def get_user_tasks(username):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select

            id,
            task_title,
            priority,
            deadline,
            status

        from ai_task

        where assignee=?

        order by id desc
        """,
        (
            username,
        )
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def finish_task(task_id):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        update ai_task

        set status='已完成'

        where id=?
        """,
        (
            task_id,
        )
    )

    conn.commit()

    conn.close()