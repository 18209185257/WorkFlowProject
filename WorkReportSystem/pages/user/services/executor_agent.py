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
