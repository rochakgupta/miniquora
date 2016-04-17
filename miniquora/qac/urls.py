from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<id>\d+)/$', show_question, name="show-question"),
    url(r'^add/$', add_question, name="add-question"),
    url(r'^(?P<id>\d+)/edit/$', edit_question, name="edit-question"),
    url(r'^(?P<id>\d+)/edit/$', delete_question, name="delete-question"),
    url(r'^(?P<id>\d+)/load_vote/$', load_vote_question, name = 'load-vote-question'),
    url(r'^(?P<id>\d+)/vote/$', vote_question, name = 'vote-question'),
    url(r'^(?P<id>\d+)/comment/add/$', add_question_comment, name="add-question-comment"),
    url(r'^(?P<id>\d+)/comment/(?P<c_id>\d+)/edit/$', edit_question_comment, name="edit-question-comment"),
    url(r'^(?P<id>\d+)/comment/(?P<c_id>\d+)/delete/$', delete_question_comment, name="delete-question-comment"),
    url(r'^(?P<id>\d+)/answer/add/$', add_answer, name="add-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/edit/$', edit_answer, name="edit-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/delete/$', delete_answer, name="delete-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/load_vote/$', load_vote_answer, name="load-vote-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/vote/$', vote_answer, name="vote-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/comment/add/$', add_answer_comment, name="add-answer-comment"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/comment/(?P<c_id>\d+)/edit/$', edit_answer_comment, name="edit-answer-comment"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/comment/(?P<c_id>\d+)/delete/$', delete_answer_comment, name="delete-answer-comment")
]