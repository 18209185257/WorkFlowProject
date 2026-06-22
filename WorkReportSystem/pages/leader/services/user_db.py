import sqlite3
from datetime import datetime

DB_PATH = "user.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,

        role TEXT NOT NULL DEFAULT 'user',

        real_name TEXT,
        phone TEXT,

        create_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def register_user(
    username,
    password,
    real_name,
    phone
):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(
        "select id from users where username=?",
        (username,)
    )

    if cur.fetchone():
        conn.close()
        return "账号已存在"

    cur.execute("""
    INSERT INTO users(
        username,
        password,
        role,
        real_name,
        phone,
        create_time
    )
    VALUES(?,?,?,?,?,?)
    """, (
        username,
        password,
        "user",
        real_name,
        phone,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return "注册成功"