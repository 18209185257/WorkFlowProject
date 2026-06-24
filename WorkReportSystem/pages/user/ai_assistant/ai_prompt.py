def build_daily_prompt(
    reports,
    meetings,
    progresses
):

    txt = ""

    txt += "日报记录：\n"

    for d,c in reports:
        txt += f"{d}:{c}\n"

    txt += "\n会议记录：\n"

    for d,c in meetings:
        txt += f"{d}:{c}\n"

    txt += "\n项目进展：\n"

    for d,c in progresses:
        txt += f"{d}:{c}\n"

    prompt = f"""
你是企业工作助手。

根据以下内容生成规范工作日报。

输出格式：

【今日完成】
1.
2.
3.

【存在问题】
1.
2.

【明日计划】
1.
2.
3.

数据如下：

{txt}
"""

    return prompt

def build_weekly_prompt(
    reports,
    meetings,
    progresses
):

    txt = ""

    for d,c in reports:
        txt += f"{d}:{c}\n"

    prompt = f"""
根据以下工作内容生成周报。

输出：

一、本周完成工作

二、本周问题

三、下周计划

数据：

{txt}
"""

    return prompt

