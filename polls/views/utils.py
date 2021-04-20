from rest_framework.response import Response
from rest_framework import status

from polls.models import *


def login_decorator(fun):
    def dec_fun(request, *args, **kwargs):
        try:
            _current_user = User.objects.get(session=request.session.session_key)
        except User.DoesNotExist:
            _current_user = User(
                session=request.session.session_key
            )
            _current_user.save()
        return fun(request, *args, **kwargs)
    return dec_fun

def exception_response(ex, message):
    return Response(
        {
            "message": message,
            "exception": str(ex)
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )


# def str2date(string):
#     return datetime.datetime.strptime(string, "%m-%d-%Y").date()