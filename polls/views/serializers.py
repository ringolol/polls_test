from rest_framework import serializers

from polls.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'session']

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']

class CompletedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedPoll
        poll = PollSerializer
        user = UserSerializer
        fields = ['id', 'poll', 'user']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'many_answers']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        question = QuestionSerializer
        fields = ['id', 'question', 'text']