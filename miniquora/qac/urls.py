from django.conf.urls import url
from .views import add_question, show_question, edit_question, add_answer, edit_answer, add_question_comment, edit_question_comment, add_answer_comment, edit_answer_comment

#urlpatterns = [
#    url(r'^(?P<id>\d+)/$', show_question, name="show-question"),
#    url(r'^add/$', add_question, name="add-question"),
#    url(r'^(?P<id>\d+)/edit/$', edit_question, name="edit-question"),
#    url(r'^(?P<id>\d+)/add/$', add_answer, name="add-answer"),
#    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/edit/$', edit_answer, name="edit-answer"),
#    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/add/$', add_comment, name="add-comment"),
#    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/(?P<c_id>\d+)/edit/$', edit_comment, name="edit-comment")
#]

urlpatterns = [
    url(r'^(?P<id>\d+)/$', show_question, name="show-question"),
    url(r'^add/$', add_question, name="add-question"),
    url(r'^(?P<id>\d+)/edit/$', edit_question, name="edit-question"),
    url(r'^(?P<id>\d+)/comment/add/$', add_question_comment, name="add-question-comment"),
    url(r'^(?P<id>\d+)/comment/(?P<c_id>\d+)/edit/$', edit_question_comment, name="edit-question-comment"),
    url(r'^(?P<id>\d+)/answer/add/$', add_answer, name="add-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/edit/$', edit_answer, name="edit-answer"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/comment/add/$', add_answer_comment, name="add-answer-comment"),
    url(r'^(?P<id>\d+)/answer/(?P<a_id>\d+)/comment/(?P<c_id>\d+)/edit/$', edit_answer_comment, name="edit-answer-comment")
]