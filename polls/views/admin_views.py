from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from polls.models import *
from .serializers import *
from .utils import exception_response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_poll(request):
    try:
        name = request.data['poll_name']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        description = request.data['description']
        poll = Poll(name=name, start_date=start_date, end_date=end_date, \
                description=description)
        poll.save()
    except Exception as ex:
        return exception_response(ex, f'bad poll data: {request.data}')

    return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_poll(request):
    try:
        poll_id = request.data['poll_id']
        updated_pars = request.data['updated_pars']
        
    except Exception as ex:
        return exception_response(ex, f'bad poll data: {request.data}')

    if 'start_date' in updated_pars:
        return Response({"message": "start_date cannot be changed after creation"})

    try:
        poll = Poll.objects.get(id=poll_id).update(**updated_pars)
    except Exception as ex:
        return exception_response(ex, f'incorrect parameters in updated_pars: {updated_pars}')

    return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_poll(request):
    try:
        poll_id = request.data['poll_id']
    except Exception as ex:
        return exception_response(ex, f'bad poll data: {request.data}')

    try:
        poll = Poll.objects.get(id=poll_id).delete()
    except Exception as ex:
        return exception_response(ex, f'poll {poll_id} does not exist')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request):
    try:
        poll_id = request.data['poll_id']
        text = request.data['text']
        answers = request.data['answers']
        many_answers = request.data['many_answers']
        poll = Poll.objects.get(id=poll_id)
        question = Question(poll=poll, text=text, many_answers=many_answers)
        question.save()

        for answer in answers:
            Answer(question, answer['text']).save()
        
    except Exception as ex:
        return exception_response(ex, f'bad question data: {request.data}')

    return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_question(request):
    try:
        question_id = request.data['question_id']
        updated_pars = request.data['updated_pars']
        
    except Exception as ex:
        return exception_response(ex, f'bad question data: {request.data}')

    try:
        question = Question.objects.get(id=question_id).update(**updated_pars)
    except Exception as ex:
        return exception_response(ex, f'incorrect parameters in updated_pars: {updated_pars}')

    return Response({})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_question(request):
    try:
        question_id = request.data['question_id']
    except Exception as ex:
        return exception_response(ex, f'bad question data: {request.data}')

    try:
        question = Question.objects.get(id=question_id).delete()
    except Exception as ex:
        return exception_response(ex, f'question {question} does not exist')