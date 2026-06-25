from common.db import get_project_conn
from datetime import datetime

def save_conversation(
        username,
        role,
        content
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    insert into ai_conversation(
        username,
        role,
        content,
        create_time
    )
    values(?,?,?,?)
    """,(
        username,
        role,
        content,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()

def get_recent_context(
        username,
        limit=10
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    select role,content
    from ai_conversation
    where username=?
    order by id desc
    limit ?
    """,(username,limit))

    rows = cur.fetchall()

    conn.close()

    rows.reverse()

    return rows

def build_ai_context(
        username,
        limit=20
):

    rows = get_recent_context(
        username,
        limit
    )

    context = ""

    for role,content in rows:

        if role == "user":

            context += \
            f"用户：{content}\n"

        else:

            context += \
            f"助手：{content}\n"

    return context

def get_user_conversations(
        username,
        limit=50
):
    conn = get_project_conn()

    cur = conn.cursor()
    cur.execute("""
    select
        role,
        content,
        create_time
    from ai_conversation
    where username=?
    order by id desc
    limit ?
    """,
                (
                    username,
                    limit
                ))

def clean_old_conversation(
        username
):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
    delete from ai_conversation
    where id not in(
        select id
        from ai_conversation
        where username=?
        order by id desc
        limit 100
    )
    """,(username,))

    conn.commit()

    conn.close()
