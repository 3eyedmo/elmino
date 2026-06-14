from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default admin user if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists."))
            return

        User.objects.create_superuser(
            username="admin",
            password="admin",
            is_staff=True,
        )

        self.stdout.write(self.style.SUCCESS("Admin user created successfully."))
