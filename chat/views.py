from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import query_patient_vectors, generate_answer


class DoctorChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question')
        patient_id = request.data.get('patient_id')

        if not question or not patient_id:
            return Response({"error": "question and patient_id required"}, status=400)

        # Retrieve top relevant chunks
        retrieved_texts = query_patient_vectors(question, top_k=5)

        # Generate answer from retrieved chunks
        answer = generate_answer(question, retrieved_texts)
        return Response({"answer": answer})
