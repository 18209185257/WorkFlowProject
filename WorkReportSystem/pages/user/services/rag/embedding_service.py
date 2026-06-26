from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "./models/bge-small-zh-v1.5"
)

def embedding(text):

    return model.encode(
        text
    ).tolist()