import chromadb

from .embedding_service import (
    embedding
)

client = chromadb.PersistentClient(
    path="./database/chroma"
)

collection = client.get_or_create_collection(
    name="workflow_rag"
)

def search_docs(
        question,
        top_k=5
):

    result = collection.query(

        query_embeddings=[
            embedding(question)
        ],

        n_results=top_k

    )

    return result["documents"][0]