# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/13 21:01'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

]