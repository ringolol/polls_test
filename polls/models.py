from django.db import models


class User(models.Model):
    pass

class Poll(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=200)

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    many_answers = models.BooleanField()
    answers = models.CharField(max_length=500)

class CompletedPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['poll', 'user']]

class AsweredQuestion(models.Model):
    comp_poll = models.ForeignKey(CompletedPoll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)

    class Meta:
        unique_together = [['comp_poll', 'question']]