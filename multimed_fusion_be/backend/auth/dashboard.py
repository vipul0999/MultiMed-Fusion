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


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        # Only admin or staff can view doctors, modify logic if needed
        user = self.request.user
        if user.is_staff:
            return Doctor.objects.all()

        # Otherwise return only the logged-in doctor's record
        return Doctor.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        queryset = self.get_queryset()
        total_doctors = queryset.count()

        # Example: group doctors by specialty
        specialties = queryset.values('specialty').annotate(
            count=Count('specialty')
        )

        # Optional: doctor experience buckets
        exp_groups = {
            '0-5 yrs': queryset.filter(experience__lte=5).count(),
            '6-15 yrs': queryset.filter(experience__gte=6, experience__lte=15).count(),
            '15+ yrs': queryset.filter(experience__gt=15).count(),
        }

        data = {
            'total_doctors': total_doctors,
            'specialties': specialties,
            'experience_groups': exp_groups,
            'doctors': DoctorSerializer(queryset, many=True).data
        }
        return Response(data)


        data = {
            'total_patients': total_patients,
            'age_groups': age_groups,
            'patients': PatientSerializer(queryset, many=True).data
        }
        return Response(data)
