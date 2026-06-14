from django.db import models
from django.db.models import Q


class Participant(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    grade = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Problem(models.Model):
    class DifficultyLevel(models.TextChoices):
        EASY = "Easy", "Easy"
        MEDIUM = "Medium", "Medium"
        HARD = "Hard", "Hard"

    title = models.CharField(max_length=255)
    score = models.IntegerField()
    difficulty = models.CharField(max_length=50, choices=DifficultyLevel.choices)


class Submission(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name="submissions"
    )

    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="submissions"
    )

    score_earned = models.PositiveIntegerField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    is_final = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(score_earned__gte=0),
                name="score_positive",
            ),
            models.UniqueConstraint(
                fields=["participant", "problem"],
                condition=Q(is_final=True),
                name="unique_final_submission",
            ),
        ]

    def clean(self):
        if self.score_earned > self.problem.score:
            from django.core.exceptions import ValidationError

            raise ValidationError("Score cannot exceed problem maximum score.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
