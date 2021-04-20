from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    session = models.CharField(max_length=200, unique=True)

class Poll(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200)

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    many_answers = models.BooleanField()

class CompletedPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['poll', 'user']]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class AsweredQuestion(models.Model):
    completed_poll = models.ForeignKey(CompletedPoll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['completed_poll', 'question', 'answer']]