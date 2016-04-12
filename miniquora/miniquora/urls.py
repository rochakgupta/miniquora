from django.conf.urls import url, include, static
from django.contrib import admin
from account import views as accountviews
from qac import views as qacviews
from django.conf import settings

urlpatterns = [
    url(r'^$', qacviews.all_questions, name = 'all-questions'),
    url(r'^(?P<page_num>\d+)/$', qacviews.all_questions, name = 'all-questions-page'),
    url(r'^search/$', qacviews.search_questions, name = 'search-questions'),
    url(r'^admin/', admin.site.urls),
    url(r'^question/', include('qac.urls')),
    url(r'^account/', include('account.urls')),
] + static.static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
