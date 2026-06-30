from pages.leader.services.project_manager.ai_task_service import (
    get_ai_tasks
)

from pages.leader.services.project_manager.ai_task_service import (
    auto_create_tasks
)

from .ollama_client import (
    call_ollama
)


def ai_project_manager():

    tasks = get_ai_tasks()

    prompt = f"""
你是资深项目经理。

当前任务：

{tasks}

请输出：

1.风险分析

2.整改建议

3.任务安排

4.项目健康总结
"""

    return call_ollama(
        prompt
    )