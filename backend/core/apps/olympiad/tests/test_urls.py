from django.urls import reverse, resolve

from apps.olympiad.views import (
    ParticipantListCreateView,
    ProblemListCreateView,
    SubmissionCreateView,
    LeaderboardView,
)


def test_participants_url():
    path = reverse("participants")
    assert resolve(path).func.view_class == ParticipantListCreateView


def test_problems_url():
    path = reverse("problems")
    assert resolve(path).func.view_class == ProblemListCreateView


def test_submissions_url():
    path = reverse("submissions")
    assert resolve(path).func.view_class == SubmissionCreateView


def test_leaderboard_url():
    path = reverse("leaderboard")
    assert resolve(path).func.view_class == LeaderboardView
