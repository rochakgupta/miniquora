from django.conf.urls import url
from .views import login, logout, signup, forgot_password, reset_password, activate, home, edit_profile, search_my_questions

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name ="logout" ),
    url(r'^signup/$', signup, name ="signup" ),
    url(r'^forgot-password/$', forgot_password, name ="forgot-password" ),
    url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name="reset-password"),
    url(r'^activate/(?P<id>\d+)/(?P<otp>\d{4})/$', activate, name="activate-account"),
    url(r'^(?P<id>\d+)/home/$', home, name = "home"),
    url(r'^(?P<id>\d+)/home/(?P<page_num>\d+)/$', home, name = "home-page"),
    url(r'^(?P<id>\d+)/home/search/$', search_my_questions, name = "search-my-questions"),
    url(r'^(?P<id>\d+)/edit/$', edit_profile, name = "edit-profile"),
]