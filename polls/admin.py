from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(CompletedPoll)
class CompletedPollAdmin(admin.ModelAdmin):
    pass

@admin.register(AsweredQuestion)
class AsweredQuestionAdmin(admin.ModelAdmin):
    pass