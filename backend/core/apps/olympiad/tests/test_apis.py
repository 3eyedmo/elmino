import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from apps.olympiad.models import (
    Participant,
    Problem,
    Submission,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client):
    user = User.objects.create_user(
        username="tester",
        password="pass12345",
        is_staff=True,
    )

    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def participant():
    return Participant.objects.create(
        full_name="John",
        email="john@test.com",
        grade=10,
        city="Berlin",
    )


@pytest.fixture
def problem():
    return Problem.objects.create(
        title="Problem",
        score=100,
        difficulty="Easy",
    )


@pytest.mark.django_db
def test_participant_list_requires_auth(api_client):
    response = api_client.get(reverse("participants"))

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_create_participant(auth_client):
    response = auth_client.post(
        reverse("participants"),
        {
            "full_name": "Jane",
            "email": "jane@test.com",
            "grade": 9,
            "city": "Munich",
        },
        format="json",
    )

    assert response.status_code == 201

    assert Participant.objects.filter(email="jane@test.com").exists()


@pytest.mark.django_db
def test_create_submission(
    auth_client,
    participant,
    problem,
):
    response = auth_client.post(
        reverse("submissions"),
        {
            "participant": participant.id,
            "problem": problem.id,
            "score_earned": 80,
        },
        format="json",
    )

    assert response.status_code == 201

    assert Submission.objects.count() == 1


@pytest.mark.django_db
def test_leaderboard_ordering(auth_client):
    p1 = Participant.objects.create(
        full_name="A",
        email="a@test.com",
        grade=10,
        city="Berlin",
    )

    p2 = Participant.objects.create(
        full_name="B",
        email="b@test.com",
        grade=10,
        city="Berlin",
    )

    problem = Problem.objects.create(
        title="Problem",
        score=100,
        difficulty="Easy",
    )

    Submission.objects.create(
        participant=p1,
        problem=problem,
        score_earned=20,
    )

    Submission.objects.create(
        participant=p2,
        problem=problem,
        score_earned=90,
    )

    response = auth_client.get(reverse("leaderboard"))

    assert response.status_code == 200

    data = response.json()["results"]

    assert data[0]["id"] == p2.id
    assert data[1]["id"] == p1.id


@pytest.mark.django_db
def test_leaderboard_city_filter(auth_client):
    berlin = Participant.objects.create(
        full_name="Berlin User",
        email="berlin@test.com",
        grade=10,
        city="Berlin",
    )

    Participant.objects.create(
        full_name="Munich User",
        email="munich@test.com",
        grade=10,
        city="Munich",
    )

    response = auth_client.get(
        reverse("leaderboard"),
        {"city": "Berlin"},
    )

    assert response.status_code == 200

    data = response.json()["results"]

    assert len(data) == 1
    assert data[0]["id"] == berlin.id


@pytest.mark.django_db
def test_leaderboard_requires_authentication(api_client):
    response = api_client.get(reverse("leaderboard"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_leaderboard_returns_zero_for_participant_without_submission(
    auth_client,
):
    participant = Participant.objects.create(
        full_name="No Submission",
        email="nosub@test.com",
        grade=10,
        city="Berlin",
    )

    response = auth_client.get(reverse("leaderboard"))

    assert response.status_code == 200

    data = response.json()["results"]

    row = next(item for item in data if item["id"] == participant.id)

    assert row["total_score"] == 0


@pytest.mark.django_db
def test_leaderboard_pagination(
    auth_client,
):
    for i in range(15):
        Participant.objects.create(
            full_name=f"User {i}",
            email=f"user{i}@test.com",
            grade=10,
            city="Berlin",
        )

    response = auth_client.get(
        reverse("leaderboard"),
        {"page": 1, "page_size": 10},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 10
    assert data["count"] == 15
