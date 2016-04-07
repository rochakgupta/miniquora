from django.conf.urls import url
from .views import add_question, show_question, edit_question, add_answer, edit_answer, add_comment, edit_comment

urlpatterns = [
    url(r'^(?P<id>\d+)/$', show_question, name="show-question"),
    url(r'^add/$', add_question, name="add-question"),
    url(r'^(?P<id>\d+)/edit/$', edit_question, name="edit-question"),
    url(r'^(?P<id>\d+)/add/$', add_answer, name="add-answer"),
    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/edit/$', edit_answer, name="edit-answer"),
    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/add/$', add_comment, name="add-comment"),
    url(r'^(?P<id>\d+)/(?P<a_id>\d+)/(?P<c_id>\d+)/edit/$', edit_comment, name="edit-comment")
]
