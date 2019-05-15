# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/13 21:01'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVedioView, CourseCommentView, CourseAddCommentView, VideoPlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^course_video/(?P<course_id>\d+)/$', CourseVedioView.as_view(), name="course_vedio"),
    url(r'^course_comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play"),
    url(r'^add_comment/$', CourseAddCommentView.as_view(), name="add_comment"),

]