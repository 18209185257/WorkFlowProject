import chromadb
from sentence_transformers import SentenceTransformer
from common.db import get_project_conn


client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="work_report"
)

embedding_model = SentenceTransformer(
     "./models/bge-small-zh-v1.5"
)

model = SentenceTransformer("./models/all-MiniLM-L6-v2")

def add_document(
        doc_id,
        text,
        doc_type
):

    try:

        vector = embedding_model.encode(
            text
        ).tolist()

        collection.add(
            ids=[str(doc_id)],
            embeddings=[vector],
            metadatas=[
                {
                    "type": doc_type
                }
            ]
        )

    except Exception as e:

        print(
            "向量导入失败",
            doc_id,
            e
        )

def search_documents(
        question,
        top_k=5
):

    vector = embedding_model.encode(
        question
    ).tolist()

    result = collection.query(
        query_embeddings=[vector],
        n_results=top_k
    )

    docs = result.get(
        "documents",
        [[]]
    )[0]

    return docs
def rebuild_vector_db():

    conn = get_project_conn()

    cur = conn.cursor()

    try:

        old = collection.get()

        if old and old.get("ids"):

            collection.delete(
                ids=old["ids"]
            )

    except Exception:
        pass

    total = 0

    # =====================
    # 日报
    # =====================

    cur.execute("""
    select
        id,
        reporter,
        report_date,
        report_content
    from daily_report
    """)

    for row in cur.fetchall():

        doc_id = row[0]

        text = f"""
        日报

        提交人：
        {row[1]}

        日期：
        {row[2]}

        内容：
        {row[3]}
        """

        add_document(
            f"daily_{doc_id}",
            text,
            "daily"
        )

        total += 1

    # =====================
    # 会议
    # =====================

    cur.execute("""
    select
        id,
        sponsor,
        meet_date,
        meet_content
    from meeting
    """)

    for row in cur.fetchall():

        doc_id = row[0]

        text = f"""
        会议记录

        发起人：
        {row[1]}

        日期：
        {row[2]}

        内容：
        {row[3]}
        """

        add_document(
            f"meeting_{doc_id}",
            text,
            "meeting"
        )

        total += 1

    # =====================
    # 项目进展
    # =====================

    cur.execute("""
    select
        id,
        reporter,
        progress_date,
        progress_content
    from project_progress
    """)

    for row in cur.fetchall():

        doc_id = row[0]

        text = f"""
        项目进展

        提交人：
        {row[1]}

        日期：
        {row[2]}

        内容：
        {row[3]}
        """

        add_document(
            f"project_progress_{doc_id}",
            text,
            "project_progress"
        )

        total += 1

    # =====================
    # 项目
    # =====================

    cur.execute("""
    select
        id,
        project_name,
        main_leader,
        progress,
        risk_block,
        start_date,
        end_date
    from project
    """)

    for row in cur.fetchall():

        doc_id = row[0]

        text = f"""
        项目资料

        项目名称：
        {row[1]}

        项目负责人：
        {row[2]}

        项目进度：
        {row[3]}

        风险阻塞：
        {row[4]}

        开始时间：
        {row[5]}

        结束时间：
        {row[6]}
        """

        add_document(
            f"project_{doc_id}",
            text,
            "project"
        )

        total += 1

    # =====================
    # 风险
    # =====================

    try:

        cur.execute("""
        select
            id,
            project_name,
            risk_desc,
            solution
        from project_risk
        """)

        for row in cur.fetchall():

            doc_id = row[0]

            text = f"""
            项目风险

            项目：
            {row[1]}

            风险描述：
            {row[2]}

            解决方案：
            {row[3]}
            """

            add_document(
                f"risk_{doc_id}",
                text,
                "risk"
            )

            total += 1

    except Exception:

        pass

    conn.close()

    return f"""
    向量库重建完成

    共导入：

    {total}

    条知识
    """