import pytest

from apps.olympiad.models import (
    Participant,
    Problem,
)
from apps.olympiad.serializers import (
    ParticipantSerializer,
    SubmissionSerializer,
)


@pytest.fixture
def participant():
    return Participant.objects.create(
        full_name="John Doe",
        email="john@example.com",
        grade=10,
        city="Berlin",
    )


@pytest.fixture
def problem():
    return Problem.objects.create(
        title="Problem 1",
        score=100,
        difficulty="Easy",
    )


@pytest.mark.django_db
def test_participant_grade_validation():
    serializer = ParticipantSerializer(
        data={
            "full_name": "John",
            "email": "john@test.com",
            "grade": 5,
            "city": "Berlin",
        }
    )

    assert not serializer.is_valid()
    assert "grade" in serializer.errors


@pytest.mark.django_db
def test_participant_valid_grade():
    serializer = ParticipantSerializer(
        data={
            "full_name": "John",
            "email": "john@test.com",
            "grade": 10,
            "city": "Berlin",
        }
    )

    assert serializer.is_valid()


@pytest.mark.django_db
def test_submission_serializer_score_validation(
    participant,
    problem,
):
    serializer = SubmissionSerializer(
        data={
            "participant": participant.id,
            "problem": problem.id,
            "score_earned": 200,
        }
    )

    assert not serializer.is_valid()
    assert "score_earned" in serializer.errors
