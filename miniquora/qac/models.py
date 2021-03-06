from django.db import models
from account.models import MyUser


# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=100, default='')
    text = models.TextField(max_length=1000, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='questions_created')
    upvoted_by = models.ManyToManyField(MyUser, related_name='questions_upvoted', blank=True)
    downvoted_by = models.ManyToManyField(MyUser, related_name='questions_downvoted', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Answer(models.Model):
    text = models.TextField(max_length=1000, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='answers_created')
    upvoted_by = models.ManyToManyField(MyUser, related_name='answers_upvoted', blank=True)
    downvoted_by = models.ManyToManyField(MyUser, related_name='answers_downvoted', blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created_on']


class Comment(models.Model):
    text = models.TextField(max_length=1000, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments_created')
    upvoted_by = models.ManyToManyField(MyUser, related_name='comments_upvoted', blank=True)
    downvoted_by = models.ManyToManyField(MyUser, related_name='comments_downvoted', blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments', null=True, default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments', null=True, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created_on']
