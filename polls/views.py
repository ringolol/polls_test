import datetime
from django.contrib.sessions.backends.db import SessionStore
import django

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets, serializers, status

from .models import *


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


@api_view(['POST'])
def login(request):
    if not request.session.session_key:
        request.session.save()

    try:
        current_user = User.objects.get(session=request.session.session_key)
    except User.DoesNotExist:
        current_user = None

    if not current_user:
        current_user = User(
            session=request.session.session_key
        )
        current_user.save()

    return Response({'id': current_user.id, 'session': request.session.session_key})
    # serializer = UserSerializer(current_user)
    # return Response(serializer.data)

@api_view(['GET'])
def active_polls(request):
    today = datetime.date.today()
    active_polls = Poll.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    )
    return Response(
        PollSerializer(active_polls, many=True).data
    )
    
@api_view(['POST'])
def completed_polls_by_user(request):
    requested_user_id = request.data.get('user_id', None)
    try:
        selected_user = User.objects.get(id=requested_user_id)
    except User.DoesNotExist:
        selected_user = None
    
    completed_polls = CompletedPoll.objects.filter(user=selected_user)
    return Response(
        CompletedPollSerializer(completed_polls, many=True).data
    )

@api_view(['POST'])
def questions_by_poll(request):
    requested_poll_id = request.data.get('poll_id', None)
    questions = Question.objects.select_related().filter(poll_id=requested_poll_id)
    
    return Response(QuestionSerializer(questions, many=True).data)
    # answers = Answer.objects.select_related('question__poll').filter(question__poll__id=requested_poll_id)
    # print(answers)
    # return Response(AnswerSerializer(answers, many=True).data)

@api_view(['POST'])
def answers_by_question(request):
    requested_question_id = request.data.get('question_id', None)
    answers = Answer.objects.filter(question_id=requested_question_id)

    return Response(AnswerSerializer(answers, many=True).data)

@api_view(['POST'])
def submit_answers(request):
    '''
    {
        "poll_id": 1,
        "answered_questions": [
            { 
                "question_id": 1, 
                "answers": [ 
                    {"answer_id": 1} 
                ]
            },
            {
                "question_id": 2, 
                "answers": [ 
                    {"answer_id": 4}, 
                    {"answer_id": 5} 
                ]
            }
        ]
    }
    '''
    poll_id = request.data.get('poll_id', None)
    answered_questions = request.data.get('answered_questions', [])
    
    try:
        poll = Poll.objects.get(id=poll_id)
    except Exception as ex:
        return Response(
            {
                "message": f"poll with id {poll_id} does not exist",
                "exception": str(ex)
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(session=request.session.session_key)
    except Exception as ex:
        return Response(
            {
                "message": f'user with session {request.session.session_key} does not exist',
                "exception": str(ex)
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

    completed_poll, _ = CompletedPoll.objects.filter(poll=poll, user=user).get_or_create(
        {
            'poll': poll, 
            'user': user
        }
    )

    for question_obj in answered_questions:
        try:
            question_id = question_obj['question_id']
            answers_objs = question_obj['answers']
        except Exception as ex:
            return Response(
                {
                    "message": f'bad question data: {question_obj}',
                    "exception": ex
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            question = Question.objects.get(id=question_id, poll=poll)
        except Exception as ex:
            return Response(
                {
                    "message": f'poll {poll_id} does not have question {question_id}',
                    "exception": str(ex)
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        for answer_obj in answers_objs:
            try:
                answer_id = answer_obj['answer_id']
            except Exception as ex:
                return Response(
                    {
                        "message": f'bad answer data: {answer_obj}',
                        "exception": str(ex)
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                answer = Answer.objects.get(id=answer_id, question=question)
            except Exception as ex:
                return Response(
                    {
                        "message": f'question {question_id} does not have answer {answer_id}',
                        "exception": str(ex)
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            AsweredQuestion.objects.filter(completed_poll=completed_poll, question=question).update_or_create(
                {
                    'completed_poll': completed_poll, 
                    'question': question,
                    'answer': answer
                }
            )

    return Response({})