from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    # Extend base user with role field
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    medical_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Patient: {self.user.username}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Dr. {self.user.username}"
