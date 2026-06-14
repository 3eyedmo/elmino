from random import randint, sample

from django.core.management.base import BaseCommand

from faker import Faker

from apps.olympiad.models import (
    Participant,
    Problem,
    Submission,
)


class Command(BaseCommand):
    help = "Seed olympiad demo data"

    def handle(self, *args, **options):
        fake = Faker()
        if Participant.objects.count() > 50:
            self.stdout.write(
                self.style.WARNING("Participants already exist. Skipping seed.")
            )
            return

        participants = []

        for i in range(1, 80):
            participant = Participant.objects.create(
                full_name=fake.name(),
                email=fake.unique.email(),
                grade=randint(7, 12),
                city=fake.city(),
            )

            participants.append(participant)

        problems = [
            Problem.objects.create(
                title="Math Basics",
                score=100,
                difficulty="Easy",
            ),
            Problem.objects.create(
                title="Geometry",
                score=100,
                difficulty="Easy",
            ),
            Problem.objects.create(
                title="Algebra",
                score=150,
                difficulty="Medium",
            ),
            Problem.objects.create(
                title="Number Theory",
                score=150,
                difficulty="Medium",
            ),
            Problem.objects.create(
                title="Combinatorics",
                score=200,
                difficulty="Hard",
            ),
            Problem.objects.create(
                title="Graph Theory",
                score=200,
                difficulty="Hard",
            ),
            Problem.objects.create(
                title="Dynamic Programming",
                score=250,
                difficulty="Hard",
            ),
            Problem.objects.create(
                title="Probability",
                score=120,
                difficulty="Medium",
            ),
            Problem.objects.create(
                title="Logic",
                score=80,
                difficulty="Easy",
            ),
            Problem.objects.create(
                title="Advanced Math",
                score=300,
                difficulty="Hard",
            ),
        ]

        for participant in participants:

            solved = sample(problems, randint(3, len(problems)))

            for problem in solved:

                Submission.objects.create(
                    participant=participant,
                    problem=problem,
                    score_earned=randint(0, problem.score),
                )

        self.stdout.write(
            self.style.SUCCESS("Olympiad demo data created successfully.")
        )
