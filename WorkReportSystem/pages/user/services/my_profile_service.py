from common.db import get_project_conn


def get_my_profile(username):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            username,
            real_name,
            role
        from user
        where username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    return {

        "username": row[0],

        "real_name": row[1],

        "role": row[2]

    }


def build_my_profile_html(username):

    user = get_my_profile(username)

    if not user:

        return """
        <div class="empty-card">
            用户不存在
        </div>
        """

    return f"""
    <div class="profile-card">

        <div class="profile-row">

            <span class="profile-label">
                用户账号
            </span>

            <span>
                {user["username"]}
            </span>

        </div>

        <div class="profile-row">

            <span class="profile-label">
                姓名
            </span>

            <span>
                {user["real_name"]}
            </span>

        </div>

        <div class="profile-row">

            <span class="profile-label">
                角色
            </span>

            <span>
                {user["role"]}
            </span>

        </div>

    </div>
    """