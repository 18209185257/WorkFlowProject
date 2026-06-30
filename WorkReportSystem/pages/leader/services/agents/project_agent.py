from common.db import get_project_conn

from .ollama_client import (
    call_ollama
)

from pages.leader.services.knowledge.knowledge_service import (
    search_knowledge
)

def run_project_agent(question):
    conn = get_project_conn()
    cur = conn.cursor()
    cur.execute(
        """
        select
            project_name,
            risk_level,
            project_status
        from project
        limit 30
        """
    )

    rows = cur.fetchall()

    conn.close()

    project_text = "\n".join([
        f"{r[0]} | {r[1]} | {r[2]}"
        for r in rows
    ])

    knowledge = search_knowledge(
        question
    )

    prompt = f"""
    你是企业项目管理专家。

    公司知识：

    {knowledge}

    项目数据：

    {project_text}

    问题：

    {question}

    请结合公司规范回答。
    """

    return call_ollama(prompt)