from common.db import user_db_query
from auth.auth_service import get_conn
import sqlite3
from common.config import DB_USER_PATH


import pandas as pd

def get_user_list():

    sql = """
    SELECT
        username,
        role,
        real_name,
        phone,
        create_time
    FROM users
    ORDER BY id DESC
    """

    return user_db_query(sql)

def get_user_detail(username):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            username,
            real_name,
            phone,
            role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    return row

def update_user(
        username,
        real_name,
        phone,
        role
):

    conn = sqlite3.connect(DB_USER_PATH)
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET
        real_name=?,
        phone=?,
        role=?
    WHERE username=?
    """, (
        real_name,
        phone,
        role,
        username
    ))

    conn.commit()
    conn.close()

def delete_user(username):

    conn = sqlite3.connect(DB_USER_PATH)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

def build_user_html():

    users = get_user_list()

    html = """
    <div class="user-table">

        <div class="user-manage-row header">
            <div>用户名</div>
            <div>姓名</div>
            <div>手机号</div>
            <div>角色</div>
            <div>创建时间</div>
            <div>操作</div>
        </div>
    """

    for row in users:

        username = row[0]
        role = row[1]
        real_name = row[2]
        phone = row[3]
        create_time = row[4]

        if role == "user":
            action = f"""
            <button
                class="edit-btn"
                onclick="editUser(
        '{username}',
        '{real_name}',
        '{phone}',
        '{role}'
    )"
            >
            编辑
            </button>

            <button
                class="delete-btn"
                onclick="deleteUser('{username}')"
            >
            删除
            </button>
            """
        else:

            action = "-"

        html += f"""
        <div class="user-manage-row">
            <div>{username}</div>
            <div>{real_name}</div>
            <div>{phone}</div>
            <div>{role}</div>
            <div>{create_time}</div>
            <div>{action}</div>
        </div>
        """

    html += "</div>"

    return html

def delete_user_by_name(username):

    conn = sqlite3.connect(DB_USER_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()

    conn.close()

    return True