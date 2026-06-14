import math

from django.db.models.functions import Coalesce
from django.db.models import (
    Avg,
    Count,
    Max,
    Min,
    Q,
    Sum,
    When,
)

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.olympiad.models import Participant, Problem, Submission
from apps.olympiad.serializers import (
    ParticipantForLeaderboardSerializer,
    ParticipantSerializer,
    SubmissionSerializer,
    ProblemSerializer,
    LeaderboardStatsSerializer,
)
from apps.olympiad.pagination import LeaderBoardPagination


class ParticipantListCreateView(generics.ListCreateAPIView):

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ProblemListCreateView(generics.ListCreateAPIView):

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class SubmissionCreateView(generics.CreateAPIView):

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class LeaderboardView(generics.ListAPIView):
    serializer_class = ParticipantForLeaderboardSerializer
    pagination_class = LeaderBoardPagination

    def get_queryset(self):

        city = self.request.query_params.get("city")

        qs = Participant.objects.all()

        if city:
            qs = qs.filter(city__icontains=city)

        return qs.annotate(
            total_score=Coalesce(
                Sum("submissions__score_earned", filter=Q(submissions__is_final=True)),
                0,
            )
        ).order_by("-total_score")


class LeaderboardStatsAPIView(APIView):

    BUCKET_SIZE = 100

    def get(self, request):

        leaderboard = Participant.objects.annotate(
            total_score=Coalesce(
                Sum(
                    "submissions__score_earned",
                    filter=Q(submissions__is_final=True),
                ),
                0,
            )
        )

        stats = leaderboard.aggregate(
            participant_count=Count("id"),
            average_score=Avg("total_score"),
            max_score=Max("total_score"),
            min_score=Min("total_score"),
        )

        # handle empty dataset safely
        max_score = stats["max_score"] or 0

        if stats["participant_count"] == 0:
            return Response(
                {
                    "participant_count": 0,
                    "average_score": 0,
                    "max_score": 0,
                    "min_score": 0,
                    "distribution": [],
                }
            )

        bucket_count = math.ceil(max_score / self.BUCKET_SIZE) or 1

        distribution = []

        for i in range(bucket_count):
            start = i * self.BUCKET_SIZE
            end = (i + 1) * self.BUCKET_SIZE

            count = leaderboard.filter(
                total_score__gte=start,
                total_score__lt=end,
            ).count()

            distribution.append(
                {
                    "range": f"{start}-{end}",
                    "count": count,
                }
            )

        response_data = {
            "participant_count": stats["participant_count"],
            "average_score": stats["average_score"] or 0,
            "max_score": stats["max_score"] or 0,
            "min_score": stats["min_score"] or 0,
            "distribution": distribution,
        }

        serializer = LeaderboardStatsSerializer(response_data)
        return Response(serializer.data)
