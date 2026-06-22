import requests
import re

from pages.leader.leader_config import (
    API_HOST,
    TOKEN,
    TODAY_STR
)

from pages.leader.utils.data_utils import deduplicate_data

# =====================================

# 工具

# =====================================

def extract_username(text):

    patterns = [
        r"([\u4e00-\u9fa5]{2,4})本周",
        r"([\u4e00-\u9fa5]{2,4})最近",
        r"([\u4e00-\u9fa5]{2,4})今日",
        r"([\u4e00-\u9fa5]{2,4})项目"
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)

    return ""

# =====================================

# 查询用户本周日报

# =====================================

def query_user_week_report(text):
    username = extract_username(text)

    url = (
        f"{API_HOST}/api/query_report"
        f"?token={TOKEN}"
        f"&user={username}"
        f"&week=now"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    if not rows:

        return {
            "raw_data":f"未找到【{username}】本周日报",
            "raw_list":[]
        }

    txt = f"========【{username}本周工作总结】========\n"

    for row in rows:
        txt += (
            f"\n【{row[3]}】\n"
            f"工作内容：{row[2]}\n"
            f"需协助：{row[4]}\n"
        )

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 查询最近日报

# =====================================

def query_user_recent_report(text):

    username = extract_username(text)

    url = (
        f"{API_HOST}/api/query_report"
        f"?token={TOKEN}"
        f"&user={username}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    rows = rows[:5]

    if not rows:

        return {
            "raw_data":f"未找到【{username}】日报",
            "raw_list":[]
        }

    txt = f"========【{username}最近日报】========\n"

    for row in rows:

        txt += f"""

    【{row[3]}】

    {row[2]}
    """

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 今日工作总结

# =====================================

def query_user_today_report(text):


    username = extract_username(text)

    url = (
        f"{API_HOST}/api/query_report"
        f"?token={TOKEN}"
        f"&user={username}"
        f"&date={TODAY_STR}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    if not rows:

        return {
            "raw_data":f"未找到【{username}】今日日报",
            "raw_list":[]
        }

    txt = f"========【{username}今日工作总结】========\n"

    for row in rows:

        txt += f"""

    工作内容：

    {row[2]}

    需协助：

    {row[4]}
    """

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 本周工作统计

# =====================================

def query_work_statistics():

    url = (
        f"{API_HOST}/api/query_report"
        f"?token={TOKEN}"
        f"&week=now"
    )

    try:

         js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    user_map = {}

    for row in rows:

        user = row[1]

        user_map[user] = (
            user_map.get(user, 0) + 1
        )

    txt = "========【本周工作统计】========\n"

    for user,count in sorted(
        user_map.items(),
        key=lambda x:x[1],
        reverse=True
    ):

        txt += f"{user}：{count}篇日报\n"

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 日报排行榜

# =====================================

def query_daily_rank():

    url = (
        f"{API_HOST}/api/query_report"
        f"?token={TOKEN}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    user_map = {}

    for row in rows:

        user = row[1]

        user_map[user] = (
            user_map.get(user, 0) + 1
        )

    txt = "========【日报排行榜】========\n"

    rank = 1

    for user,count in sorted(
        user_map.items(),
        key=lambda x:x[1],
        reverse=True
    ):

        txt += f"{rank}. {user}（{count}篇）\n"

        rank += 1

    return {
        "raw_data":txt,
        "raw_list":rows
    }
