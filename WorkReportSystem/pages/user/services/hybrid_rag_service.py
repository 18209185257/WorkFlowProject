from common.db import get_project_conn
from .rag_service import (
    search_documents
)

def keyword_search(
        question,
        limit=10
):

    conn = get_project_conn()

    cur = conn.cursor()

    docs = []
    cur.execute("""
    select
        project_name,
        progress,
        risk_block
    from project
    """)
    for row in cur.fetchall():

        text = f"""
        项目名称:
        {row[0]}

        项目进度:
        {row[1]}

        风险:
        {row[2]}
        """

        if question in text:
            docs.append(text)

    cur.execute("""
    select
        report_content
    from daily_report
    """)
    for row in cur.fetchall():

        if question in row[0]:
            docs.append(row[0])

    cur.execute("""
    select
        meet_content
    from meeting
    """)
    for row in cur.fetchall():

        if question in row[0]:
            docs.append(row[0])

    conn.close()

    return docs[:limit]

def hybrid_search(
        question,
        top_k=8
):
    keyword_docs = keyword_search(
        question,
        top_k
    )
    vector_docs = search_documents(
        question,
        top_k
    )
    all_docs = []

    seen = set()
    for d in keyword_docs:

        if d not in seen:
            all_docs.append(d)

            seen.add(d)
    for d in vector_docs:

        if d not in seen:
            all_docs.append(d)

            seen.add(d)
    return all_docs[:top_k]