from .tool_registry import TOOLS

def execute_plans(
        username,
        question,
        plans
):
    results = {}
    for task in plans:
        tool = TOOLS.get(task)

        if not tool:
            continue
        func = tool["func"]
        if task == "chat":

            result = func(
                username,
                question
            )

        else:

            result = func(
                username
            )
        results[task] = result
    return results

def execute_tool(
        task,
        username,
        question
):

    print(
        "执行工具:",
        task
    )

    tool = TOOLS.get(task)

    if not tool:

        return "未找到工具"

    func = tool["func"]

    if task == "chat":

        return func(
            username,
            question
        )

    result = func(
        username
    )

    print(
        f"{task}结果:",
        result[:200]
        if isinstance(result,str)
        else result
    )

    return result