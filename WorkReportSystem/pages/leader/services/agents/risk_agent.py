from common.db import get_project_conn

from .ollama_client import (
    call_ollama
)

from pages.leader.services.knowledge.knowledge_service import (
    search_knowledge
)

def run_risk_agent(question):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            project_name,
            risk_level
        from project
        where risk_level is not null
        """
    )

    rows = cur.fetchall()

    conn.close()

    risk_text = "\n".join([
        f"{r[0]} | {r[1]}"
        for r in rows
    ])

    knowledge = search_knowledge(
        question
    )

    prompt = f"""
    公司风险管理规范：

    {knowledge}

    风险数据：

    {risk_text}

    问题：

    {question}
    """

    return call_ollama(prompt)