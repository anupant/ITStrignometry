__author__ = 'Anna'
from django.conf.urls import url
from . import views
from django.contrib import admin

app_name = 'learning'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^index_page/$', views.index_page, name='index_page'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/$', views.content_display, name='content_display'),
    #url(r'^(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/(?P<quiz_id>[0-9]+)/$', views.content_display, name='content_display'),
    url(r'^(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/(?P<quiz_id>[0-9]+)/$', views.start_quiz, name='start_quiz'),

    url(r'^(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/(?P<quiz_id>[0-9]+)/(?P<question1_id>[0-9]+)/$', views.start_quiz1, name='start_quiz1'),
    #url(r'^alternate_quiz/$', views.alternate_quiz, name='feedback_quiz_ind'),
    url(r'^alternate_quiz/(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/(?P<quiz_id>[0-9]+)/$',views.alternate_quiz, name='alternate_quiz')

    #url(r'^(?P<course_id>[0-9]+)/(?P<course_content_id>[0-9]+)/(?P<quiz_id>[0-9]+)/(?P<coursePerformance_id>[0-9]+)/$', views.feedback_quiz, name='feedback_quiz'),

]


