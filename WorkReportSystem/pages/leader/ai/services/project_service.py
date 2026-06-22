import requests

from common.config import (
    API_HOST,
    TOKEN
)

# =====================================

# 单项目查询

# =====================================

def query_single_project(project_name):

    url = (
        f"{API_HOST}/api/query_project"
        f"?token={TOKEN}"
        f"&name={project_name}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
           "raw_data":"项目接口调用失败",
            "raw_list":[]
        }

    rows = js.get(
        "data",
        []
    )

    if not rows:

        return {
            "raw_data":
                f"未找到【{project_name}】项目",
            "raw_list":[]
        }

    txt = f"========【{project_name}项目详情】========\n"

    for row in rows:

        txt += f"""

项目名称：
{row[1]}

负责人：
{row[3]}

项目进度：
{row[7]}

延期：
{row[5]}

风险：
{row[6]}

更新时间：
{row[8]}
"""

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 本周项目

# =====================================

def query_week_project():

    url = (
        f"{API_HOST}/api/query_project"
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
            "raw_data":"项目接口调用失败",
            "raw_list":[]
        }

    rows = js.get(
        "data",
        []
    )

    if not rows:

        return {
            "raw_data":"本周暂无项目更新",
            "raw_list":[]
        }

    txt = "========【本周项目更新】========\n"

    for row in rows:

        txt += f"""

项目：
{row[1]}

负责人：
{row[3]}

进度：
{row[7]}

风险：
{row[6]}
"""

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 全部项目

# =====================================

def query_all_project():

    url = (
        f"{API_HOST}/api/query_project"
        f"?token={TOKEN}"
   )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"项目接口调用失败",
            "raw_list":[]
        }

    rows = js.get(
        "data",
        []
    )

    if not rows:

        return {
            "raw_data":"暂无项目",
            "raw_list":[]
        }

    txt = "========【全部项目】========\n"

    for row in rows:

        txt += (
            f"{row[1]} ｜ "
            f"{row[3]} ｜ "
            f"{row[7]}\n"
        )

    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 项目统计

# =====================================

def query_project_statistics():

    url = (
        f"{API_HOST}/api/query_project"
        f"?token={TOKEN}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"项目接口调用失败",
            "raw_list":[]
        }

    rows = js.get(
        "data",
        []
    )

    total = len(rows)

    delay = 0

    risk = 0

    for row in rows:

        if str(row[5]) == "是":

            delay += 1

        if row[6]:

            risk += 1

    txt = f"""

========【项目统计】========

    项目总数：
    {total}

    延期项目：
    {delay}

    存在风险项目：
    {risk}
    """
    return {
        "raw_data":txt,
        "raw_list":rows
    }

# =====================================

# 项目排行

# =====================================

def query_project_rank():
    url = (
        f"{API_HOST}/api/query_project"
        f"?token={TOKEN}"
    )

    try:

        js = requests.get(
            url,
            timeout=5
        ).json()

    except Exception:

        return {
            "raw_data":"项目接口调用失败",
            "raw_list":[]
        }

    rows = js.get(
        "data",
        []
    )

    rows = sorted(
        rows,
        key=lambda x:
        len(str(x[7])),
        reverse=True
    )

    txt = "========【项目进度排行】========\n"

    rank = 1

    for row in rows:

        txt += (
            f"{rank}. "
            f"{row[1]}"
            f"（负责人：{row[3]}）\n"
        )

        rank += 1

    return {
        "raw_data":txt,
        "raw_list":rows
    }

