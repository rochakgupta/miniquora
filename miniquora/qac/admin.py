from django.contrib import admin
from .models import Question, Answer, Comment

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['title','created_by','created_on']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text','created_by']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text','created_by']

