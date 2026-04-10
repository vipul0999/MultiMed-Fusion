from fastembed import TextEmbedding

# Create once (module-level singleton)
_MODEL_NAME = "BAAI/bge-small-en-v1.5"
_embedder = TextEmbedding(model_name=_MODEL_NAME)

def embedding_model_name() -> str:
    return _MODEL_NAME

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Returns normalized vectors by default (fastembed models are typically normalized).
    """
    vectors = []
    for vec in _embedder.embed(texts):
        vectors.append([float(x) for x in vec])
    return vectors

def embed_query(text: str) -> list[float]:
    return embed_texts([text.strip()])[0]