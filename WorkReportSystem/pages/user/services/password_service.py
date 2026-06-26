from common.db import get_conn
import gradio as gr

def change_password(
        username,
        old_pwd,
        new_pwd
):

    if not old_pwd:
        raise gr.Error("请输入原密码")

    if not new_pwd:
        raise gr.Error("请输入新密码")

    conn = get_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select password
        from users
        where username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    if not row:

        conn.close()
        raise gr.Error("用户不存在")

    if row[0] != old_pwd:

        conn.close()
        raise gr.Error("原密码错误")

    cur.execute(
        """
        update users
        set password=?
        where username=?
        """,
        (
            new_pwd,
            username
        )
    )

    conn.commit()

    conn.close()
    raise gr.Info("密码修改成功")