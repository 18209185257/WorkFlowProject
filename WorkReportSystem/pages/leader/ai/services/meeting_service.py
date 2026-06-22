import re
import requests

from common.config  import (
    API_HOST,
    TOKEN,
    CURR_YEAR
)

from ...utils.data_utils import deduplicate_data

# =====================================

# 本周全部会议

# =====================================

def query_week_meeting():

    url = (
        f"{API_HOST}/api/query_meeting"
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
            "raw_data":"会议接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    if not rows:

        return {
            "raw_data":"本周暂无会议",
            "raw_list":[]
        }

    txt = "========【本周会议记录】========\n"

    for row in rows:

        txt += f"""

    会议日期：
    {row[3]}

    参会人：
    {row[1]}

    主题：
    {row[2]}

    纪要：
    {row[4]}
    """

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 某人本周参会

# =====================================

def query_user_week_meeting(text):

    match = re.search(
        r"([\u4e00-\u9fa5]+)本周参会记录",
        text
    )

    if not match:

        return {
            "raw_data":"无法识别姓名",
            "raw_list":[]
        }

    username = match.group(1)

    url = (
        f"{API_HOST}/api/query_meeting"
        f"?token={TOKEN}"
        f"&week=now"
        f"&name={username}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

         return {
            "raw_data":"会议接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    if not rows:

       return {
            "raw_data":
                f"未查到【{username}】本周会议",
            "raw_list":[]
        }

    txt = f"========【{username}本周会议】========\n"

    for row in rows:

        txt += (
            f"{row[3]} ｜ "
            f"{row[2]}\n"
        )

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 某日会议

# =====================================

def query_meeting_by_date(text):


    match = re.search(
        r"(\d{1,2})月(\d{1,2})[日号]会议记录",
        text
    )

    if not match:

        return {
            "raw_data":"无法识别日期",
            "raw_list":[]
        }

    month = int(match.group(1))
    day = int(match.group(2))

    target = (
        f"{CURR_YEAR}-"
        f"{month:02d}-"
        f"{day:02d}"
    )

    url = (
        f"{API_HOST}/api/getMeetByDate"
        f"?token={TOKEN}"
        f"&meet_date={target}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"会议接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    if not rows:

        return {
            "raw_data":
                f"{target}暂无会议",
            "raw_list":[]
        }

    txt = f"========【{target}会议】========\n"

    for row in rows:

        txt += f"""
    
    
    主题：
    {row[2]}
    
    参会人：
    {row[1]}
    
    纪要：
    {row[4]}
    """

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 会议统计

# =====================================

def query_meeting_statistics():


    url = (
        f"{API_HOST}/api/query_meeting"
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
            "raw_data":"会议接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    total = len(rows)

    users = set()

    for row in rows:

        users.add(
            row[1]
        )

    txt = f"""

========【会议统计】========

    本周会议数：
    {total}
    
    参会人数：
    {len(users)}
    """

    return {
        "raw_data":txt,
        "raw_list":rows
    }


# =====================================

# 会议排行榜

# =====================================

def query_meeting_rank():


    url = (
        f"{API_HOST}/api/query_meeting"
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
            "raw_data":"会议接口调用失败",
            "raw_list":[]
        }

    rows = deduplicate_data(
        js.get("data", [])
    )

    counter = {}

    for row in rows:

        user = row[1]

        counter[user] = (
            counter.get(user,0)+1
        )

    rank = sorted(
        counter.items(),
        key=lambda x:x[1],
        reverse=True
    )

    txt = "========【参会排行榜】========\n"

    idx = 1

    for user,count in rank:

        txt += (
            f"{idx}. "
            f"{user}"
            f"（{count}次）\n"
        )

        idx += 1

    return {
        "raw_data":txt,
        "raw_list":rows
    }
