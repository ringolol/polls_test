from rest_framework import serializers

from polls.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'session']

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'name', 'start_date', 'end_date', 'description']

class CompletedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedPoll
        poll = PollSerializer
        user = UserSerializer
        fields = ['poll_id', 'user_id']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'poll_id', 'text', 'many_answers']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        question = QuestionSerializer
        fields = ['id', 'question_id', 'text']