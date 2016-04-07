from django import forms
from .models import Question, Answer, Comment

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['title','text']


class AnswerCreateForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text']
        
class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']