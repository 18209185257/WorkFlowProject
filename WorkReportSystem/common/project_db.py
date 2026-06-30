import sqlite3
from common.db import get_project_conn

def get_all_project():
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            project_name,
            main_leader,
            progress_rate,
            status

        from project
        """
    )
    rows = cur.fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({

            "project_name": row[0],

            "main_leader": row[1],

            "progress": int(row[2]),

            "status": row[3]

        })

    return result

def get_project_owner(
        project_name
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select project_manager

        from project

        where project_name=?
        """,
        (
            project_name,
        )
    )

    row = cur.fetchone()

    conn.close()

    if row:

        return row[0]

    return None