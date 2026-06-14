import pytest
from django.core.exceptions import ValidationError

from apps.olympiad.models import (
    Participant,
    Problem,
    Submission,
)


@pytest.fixture
def participant():
    return Participant.objects.create(
        full_name="John Doe", email="john@example.com", grade=10, city="Berlin"
    )


@pytest.fixture
def problem():
    return Problem.objects.create(title="Math Problem", score=100, difficulty="Easy")


@pytest.mark.django_db
def test_participant_created(participant):
    assert participant.id is not None
    assert participant.full_name == "John Doe"


@pytest.mark.django_db
def test_submission_score_cannot_exceed_problem_score(
    participant,
    problem,
):
    submission = Submission(
        participant=participant,
        problem=problem,
        score_earned=150,
    )

    with pytest.raises(ValidationError):
        submission.full_clean()


@pytest.mark.django_db
def test_submission_save_runs_validation(
    participant,
    problem,
):
    submission = Submission(
        participant=participant,
        problem=problem,
        score_earned=150,
    )

    with pytest.raises(ValidationError):
        submission.save()


@pytest.mark.django_db
def test_unique_final_submission_constraint(
    participant,
    problem,
):
    Submission.objects.create(
        participant=participant,
        problem=problem,
        score_earned=50,
        is_final=True,
    )

    with pytest.raises(ValidationError):
        Submission.objects.create(
            participant=participant,
            problem=problem,
            score_earned=60,
            is_final=True,
        )


@pytest.mark.django_db
def test_non_final_submissions_allowed(
    participant,
    problem,
):
    Submission.objects.create(
        participant=participant,
        problem=problem,
        score_earned=50,
        is_final=False,
    )

    Submission.objects.create(
        participant=participant,
        problem=problem,
        score_earned=60,
        is_final=False,
    )

    assert Submission.objects.count() == 2
