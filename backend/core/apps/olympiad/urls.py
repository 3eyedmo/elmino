from django.urls import path
from . import views

urlpatterns = [
    path(
        "participants/", views.ParticipantListCreateView.as_view(), name="participants"
    ),
    path("problems/", views.ProblemListCreateView.as_view(), name="problems"),
    path("submissions/", views.SubmissionCreateView.as_view(), name="submissions"),
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),
    path(
        "leaderboard/stats/",
        views.LeaderboardStatsAPIView.as_view(),
        name="leaderboard-stats",
    ),
]
