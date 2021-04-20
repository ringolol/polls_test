"""polls_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

from polls.views import login, active_polls, completed_polls_by_user, \
        questions_by_poll, answers_by_question, submit_answers


api_urlpatterns = [
    # path('accounts/', include('rest_registration.api.urls')),
    path('login/', login),
    path('active_polls/', active_polls),
    path('completed_polls_by_user/', completed_polls_by_user),
    path('questions_by_poll/', questions_by_poll),
    path('answers_by_question/', answers_by_question),
    path('submit_answers/', submit_answers),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('docs/', include_docs_urls(title='API Documentation')),
]
