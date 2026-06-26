from common.db import get_project_conn

from .chroma_service import (
    collection
)

from .embedding_service import (
    embedding
)

def sync_daily_reports():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            id,
            reporter,
            report_content
        from daily_report
    """)

    rows = cur.fetchall()

    conn.close()

    for row in rows:

        doc_id = f"daily_{row[0]}"

        text = row[2]

        collection.upsert(

            ids=[
                doc_id
            ],

            documents=[
                text
            ],

            embeddings=[
                embedding(text)
            ],

            metadatas=[
                {
                    "type":"daily",
                    "user":row[1]
                }
            ]

        )

def sync_project_reports():

    conn = get_project_conn()

    cur = conn.cursor()

    cur.execute("""
        select
            id,
            project_name,
            progress
        from project
    """)

    rows = cur.fetchall()

    conn.close()

    for row in rows:

        collection.upsert(

            ids=[
                f"project_{row[0]}"
            ],

            documents=[
                row[2]
            ],

            embeddings=[
                embedding(row[2])
            ],

            metadatas=[
                {
                    "type":"project",
                    "project":row[1]
                }
            ]

        )

