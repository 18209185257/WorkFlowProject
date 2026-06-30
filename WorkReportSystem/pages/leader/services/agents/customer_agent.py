from common.db import get_project_conn
from .ollama_client import call_ollama


def run_customer_agent(question):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            customer_name,
            company_name
        from customer
        """
    )

    rows = cur.fetchall()

    conn.close()

    txt = "\n".join([
        f"{r[0]} | {r[1]}"
        for r in rows
    ])

    prompt = f"""
客户数据：

{txt}

问题：

{question}
"""

    return call_ollama(prompt)