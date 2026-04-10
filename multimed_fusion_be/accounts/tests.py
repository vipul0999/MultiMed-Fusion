from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


User = get_user_model()


class AccountSecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_hashes_password_and_response_is_sanitized(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "patient_a",
                "email": "patient@example.com",
                "password": "StrongPass@123",
                "role": "patient",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.data)

        user = User.objects.get(username="patient_a")
        self.assertNotEqual(user.password, "StrongPass@123")
        self.assertTrue(user.check_password("StrongPass@123"))

    def test_password_update_keeps_hashing(self):
        user = User.objects.create_user(
            username="patient_b",
            email="patientb@example.com",
            password="OldPass@123",
            role="patient",
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/api/auth/password/update/",
            {
                "old_password": "OldPass@123",
                "new_password": "NewPass@456",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertNotEqual(user.password, "NewPass@456")
        self.assertTrue(user.check_password("NewPass@456"))

    def test_login_response_never_exposes_plaintext_password(self):
        User.objects.create_user(
            username="doctor_login",
            email="doctor@example.com",
            password="Secure@789",
            role="doctor",
        )
        response = self.client.post(
            "/api/auth/login/",
            {"username": "doctor_login", "password": "Secure@789"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        payload = str(response.data)
        self.assertNotIn("Secure@789", payload)
        self.assertNotIn("password", response.data)
