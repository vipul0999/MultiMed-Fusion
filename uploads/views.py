from rest_framework import generics, permissions

from ingest.llm_aggregator import query_all_llms
from .models import PatientFile
from .serializers import PatientFileSerializer
from ingest.tasks import ingest_patient_file
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from .serializers import PatientFileSearchResultSerializer


# Connect Qdrant & model
qdrant_client = QdrantClient(url="http://qdrant:6333")
model = SentenceTransformer('all-MiniLM-L6-v2')
COLLECTION_NAME = "patient_files"

class PatientFileUploadView(generics.CreateAPIView):
    queryset = PatientFile.objects.all()
    serializer_class = PatientFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally assign a doctor based on business logic
        #doctor = self.request.user.doctor_profile.user if self.request.user.is_doctor() else None

        #pf = serializer.save(doctor=doctor)
        pf = serializer.save()
        return ingest_patient_file.delay(pf.id)

class PatientFileSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", None)
        patient_id = request.query_params.get("patient_id", None)
        doctor_id = request.query_params.get("doctor_id", None)

        if not query or not patient_id or not doctor_id:
            return Response(
                {"error": "Query parameters 'q', 'patient_id', and 'doctor_id' are required"},
                status=400
            )

        # Encode query
        vector = model.encode(query).tolist()

        # Search Qdrant
        search_result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            with_payload=True,
            query_filter={
                "must": [
                    {"key": "patient_id", "match": {"value": int(patient_id)}},
                    {"key": "doctor_id", "match": {"value": int(doctor_id)}}
                ]
            }
        )

        SIMILARITY_THRESHOLD = 0.1
        filtered_results = [p for p in search_result if p.score >= SIMILARITY_THRESHOLD]

        if not filtered_results:
            return Response({"message": "No relevant matches found."}, status=404)

        # For now, take the top 1 best match
        top_point = filtered_results[0]
        payload = top_point.payload
        chunk_text = payload.get("text")

        llm_responses = query_all_llms(chunk_text,query)

        result = {
            "query": query,
            "best_match": {
                "file_id": payload.get("file_id"),
                "patient_id": payload.get("patient_id"),
                "doctor_id": payload.get("doctor_id"),
                "chunk_index": payload.get("chunk_index"),
                "score": top_point.score,
                "text": chunk_text,
            },
            "llm_responses": llm_responses,
        }

        return Response(result)

#
# class PatientFileSearchView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         query = request.query_params.get("q", None)
#         patient_id = request.query_params.get("patient_id", None)
#         doctor_id = request.query_params.get("doctor_id", None)
#
#         if not query or not patient_id or not doctor_id:
#             return Response(
#                 {"error": "Query parameters 'q', 'patient_id', and 'doctor_id' are required"},
#                 status=400
#             )
#
#         # Encode query
#         vector = model.encode(query).tolist()
#
#         # Search Qdrant
#         search_result = qdrant_client.search(
#             collection_name=COLLECTION_NAME,
#             query_vector=vector,
#             with_payload=True,
#             query_filter={
#                 "must": [
#                     {"key": "patient_id", "match": {"value": int(patient_id)}},
#                     {"key": "doctor_id", "match": {"value": int(doctor_id)}}
#                 ]
#             }
#         )
#         SIMILARITY_THRESHOLD = 0.0 # cosine similarity ranges from 0 (orthogonal) to 1 (same)
#         filtered_results = [p for p in search_result if p.score >= SIMILARITY_THRESHOLD]
#         # Prepare response
#         results = []
#         for point in filtered_results :
#             payload = point.payload
#             results.append({
#                 "file_id": payload.get("file_id"),
#                 "patient_id": payload.get("patient_id"),
#                 "doctor_id": payload.get("doctor_id"),
#                 "text": payload.get("text"),
#                 "chunk_index": payload.get("chunk_index"),
#                 "score":point.score
#             })
#
#         serializer = PatientFileSearchResultSerializer(results, many=True)
#         return Response(serializer.data)
