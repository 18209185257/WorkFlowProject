from common.db import get_project_conn
from .ollama_client import call_ollama


def run_employee_agent(question):

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute(
        """
        select
            reporter,
            count(*)
        from daily_report
        group by reporter
        """
    )

    rows = cur.fetchall()

    conn.close()

    txt = "\n".join([
        f"{r[0]}: {r[1]}"
        for r in rows
    ])

    prompt = f"""
员工数据：

{txt}

问题：

{question}
"""

    return call_ollama(prompt)