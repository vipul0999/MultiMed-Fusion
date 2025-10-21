# backend/ingest/vectorize_google.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams
import uuid
import os
import math
import google.generativeai as genai

# Configure Google Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Connect to Qdrant
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://qdrant:6333"))

COLLECTION_NAME = "patient_files"
CHUNK_SIZE = 500  # approx words per chunk

# Create collection if it doesn't exist
try:
    qdrant_client.get_collection(COLLECTION_NAME)
except Exception:
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,  # Google embedding-gecko-001 vector size
            distance="Cosine"
        )
    )

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of roughly chunk_size words."""
    words = text.split()
    chunks = [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks

def get_google_embedding(text: str):
    """Return embedding vector from Google Generative AI."""
    response = genai.models.embed_text(
        model="embedding-gecko-001",
        text=text
    )
    return response.embeddings[0].value  # this is a list of floats


def store_text_in_qdrant(file_id, text, base_payload):
    """
    Store embeddings in Qdrant with patient/doctor context and chunking.
    """
    chunks = chunk_text(text)
    points = []

    for i, chunk in enumerate(chunks):
        vector = get_google_embedding(chunk)
        payload = base_payload.copy()
        payload.update({
            "chunk_index": i,
            "text": chunk,
            "file_id": file_id
        })
        point_id = str(uuid.uuid4())
        points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        ))

    # Upsert all chunks into Qdrant
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return points
