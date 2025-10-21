from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import openai  # or local LLM
from qdrant_client.http.models import ScoredPoint

# Connect to Qdrant
qdrant_client = QdrantClient(url="http://qdrant:6333")
COLLECTION_NAME = "patient_files"

# Load same embedding model used for ingestion
model = SentenceTransformer('all-MiniLM-L6-v2')


def query_patient_vectors(question, top_k=5):
    """
    1. Embed the question
    2. Query Qdrant for most similar text chunks
    3. Return the retrieved text
    """
    q_vector = model.encode(question).tolist()

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=q_vector,
        limit=top_k,
        with_payload=True
    )

    retrieved_texts = [pt.payload['text'] for pt in search_result]
    return retrieved_texts


def generate_answer(question, context_texts):
    """
    Generate a response from retrieved text
    """
    context = "\n".join(context_texts)
    prompt = f"Patient data:\n{context}\n\nDoctor question: {question}\nAnswer concisely:"

    # Using OpenAI API (replace with local LLM if desired)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()
