from .chroma_service import collection
from .embedding_service import embedding

def upsert_vector(
        doc_id,
        content,
        metadata
):

    if not content:
        return

    collection.upsert(

        ids=[
            str(doc_id)
        ],

        documents=[
            content
        ],

        embeddings=[
            embedding(content)
        ],

        metadatas=[
            metadata
        ]

    )