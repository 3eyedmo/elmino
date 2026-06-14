from django.db import transaction

from rest_framework import serializers
from .models import Participant, Problem, Submission


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ("id", "full_name", "email", "grade", "city", "registered_at")

    def validate_grade(self, value):

        if not 7 <= value <= 12:
            raise serializers.ValidationError("Grade must be between 7 and 12.")

        return value


class ParticipantForLeaderboardSerializer(ParticipantSerializer):
    total_score = serializers.IntegerField()

    class Meta(ParticipantSerializer.Meta):
        fields = ParticipantSerializer.Meta.fields + ("total_score",)


class ProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = "__all__"

    def validate(self, attrs):

        problem = attrs["problem"]

        if attrs["score_earned"] > problem.score:
            raise serializers.ValidationError(
                {"score_earned": "Score exceeds problem max score."}
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        participant = validated_data["participant"]
        problem = validated_data["problem"]

        Submission.objects.filter(
            participant=participant, problem=problem, is_final=True
        ).update(is_final=False)

        return super().create(validated_data)


class LeaderboardDistributionSerializer(serializers.Serializer):
    range = serializers.CharField()
    count = serializers.IntegerField()


class LeaderboardStatsSerializer(serializers.Serializer):
    participant_count = serializers.IntegerField()
    average_score = serializers.FloatField()
    max_score = serializers.IntegerField()
    min_score = serializers.IntegerField()
    distribution = LeaderboardDistributionSerializer(many=True)
