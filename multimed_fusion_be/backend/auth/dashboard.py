from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Patient
from .serializers import PatientSerializer
from django.db.models import Count

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        # Only show patients assigned to the logged-in doctor
        return Patient.objects.filter(doctor=self.request.user)

    # Dashboard endpoint
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        queryset = self.get_queryset()
        total_patients = queryset.count()
        age_groups = {
            '0-18': queryset.filter(age__lte=18).count(),
            '19-40': queryset.filter(age__gte=19, age__lte=40).count(),
            '41-60': queryset.filter(age__gte=41, age__lte=60).count(),
            '60+': queryset.filter(age__gt=60).count(),
        }

        data = {
            'total_patients': total_patients,
            'age_groups': age_groups,
            'patients': PatientSerializer(queryset, many=True).data
        }
        return Response(data)
