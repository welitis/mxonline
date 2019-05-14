# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/13 21:01'

from django.conf.urls import url

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddUserFavView


urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="teacher"),

    # 机构收藏
    url(r'^add_fav/$', AddUserFavView.as_view(), name="add_fav"),
]