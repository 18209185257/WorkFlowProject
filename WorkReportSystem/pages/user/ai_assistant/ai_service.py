def ai_daily(text):

    return f"""
【AI生成日报】

今日工作：

{text}

明日计划：

1、继续推进当前任务
2、完成测试验证
3、同步项目进展
"""


def ai_meeting(text):

    return f"""
【AI会议纪要】

会议内容：

{text}

待办事项：

1、任务分配
2、进度跟踪
3、风险处理
"""


def ai_weekly(real_name):

    return f"""
【{real_name} 周报】

本周工作完成情况：

日报：
会议：
项目：

AI分析：

整体工作推进正常。
"""


def ai_project(project_name):

    return f"""
项目：

{project_name}

AI分析：

1、项目状态正常

2、建议持续跟踪关键节点

3、定期同步风险
"""