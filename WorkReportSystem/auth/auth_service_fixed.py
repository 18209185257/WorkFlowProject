import sqlite3
from datetime import datetime
from common.config import DB_USER_PATH


def get_conn():
    return sqlite3.connect(DB_USER_PATH)


def init_db():

    conn = get_conn()
    cur = conn.cursor()

    # 创建表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        real_name TEXT,
        phone TEXT,
        create_time TEXT
    )
    """)

    # 检查是否已存在用户，如果不存在才插入默认用户
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]

    if user_count == 0:  # 只有当表为空时才插入默认用户
        users = [
            (
                "admin",
                "123456",
                "leader",
                "系统管理员",
                "13800000000"
            ),
            (
                "leader",
                "123456",
                "leader",
                "项目经理",
                "13800000001"
            ),
            (
                "zhangsan",
                "123456",
                "user",
                "张三",
                "13800000002"
            ),
            (
                "lisi",
                "123456",
                "user",
                "李四",
                "13800000003"
            )
        ]

        for user in users:
            try:
                cur.execute(
                    """
                    INSERT INTO users(
                        username,
                        password,
                        role,
                        real_name,
                        phone,
                        create_time
                    )
                    VALUES(?,?,?,?,?,?)
                    """,
                    (
                        user[0],
                        user[1],
                        user[2],
                        user[3],
                        user[4],
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                )
                print(f"✅ 成功插入用户: {user[0]}")
            except Exception as e:
                print(f"❌ 插入用户失败 {user[0]}:", e)

    conn.commit()
    conn.close()


def login_check(username, password):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT role,real_name
        FROM users
        WHERE username=?
        AND password=?
    """, (username, password))

    row = cur.fetchone()

    conn.close()

    return row

def change_password(
        username,
        old_pwd,
        new_pwd,
        confirm_pwd):

    if new_pwd != confirm_pwd:
        return "❌ 两次密码输入不一致"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            old_pwd
        )
    )

    user = cur.fetchone()

    if not user:
        conn.close()
        return "❌ 原密码错误"

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            new_pwd,
            username
        )
    )

    conn.commit()
    conn.close()

    return "✅ 密码修改成功"

def register_user(
        username,
        password,
        real_name,
        phone
):

    if not username:
        return "❌ 账号不能为空"

    if not password:
        return "❌ 密码不能为空"

    if not real_name:
        return "❌ 姓名不能为空"

    if not phone:
        return "❌ 手机号不能为空"

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    if cur.fetchone():
        conn.close()
        return "❌ 账号已存在"

    cur.execute(
        """
        INSERT INTO users(
            username,
            password,
            role,
            real_name,
            phone,
            create_time
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            username,
            password,
            "user",
            real_name,
            phone,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return "✅ 注册成功"

#修改用户
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

#删除用户
def delete_user(username):

    conn = sqlite3.connect(DB_USER_PATH)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()