CURRENT_USER = {}


def set_current_user(user_info):
    global CURRENT_USER
    CURRENT_USER = user_info


def get_current_user():
    return CURRENT_USER