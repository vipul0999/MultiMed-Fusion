from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with 5 doctors, 5 patients, and 1 admin"

    def handle(self, *args, **kwargs):
        created_count = 0

        # Create 5 Doctors
        for i in range(10, 20):
            username = f"doctor{i}"
            email = f"{username}@test.com"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="password",
                    role="doctor",
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"{username} already exists"))

        # Create 5 Patients
        for i in range(10, 20):
            username = f"patient{i}"
            email = f"{username}@test.com"

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="password",
                    role="patient",
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"{username} already exists"))

        # Create 1 Admin
        if not User.objects.filter(username="admin1").exists():
            admin = User.objects.create_user(
                username="admin1",
                email="admin1@test.com",
                password="password",
                role="admin",
                is_staff=True,
                is_superuser=True,
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS("Created admin1"))
        else:
            self.stdout.write(self.style.WARNING("admin1 already exists"))

        self.stdout.write(self.style.SUCCESS(f"\nSeeding complete. Created {created_count} users.\n"))