from services.user_db import register_user


def do_register(
    name,
    phone,
    username,
    password
):

    if not all([
        name,
        phone,
        username,
        password
    ]):
        return "请填写完整信息"

    return register_user(
        username,
        password,
        name,
        phone
    )