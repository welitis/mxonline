# -*- coding:utf-8 -*-

"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetUserView, ModifyPwdView
from .views import index

import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url('^$', index, name="index"),
    # url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetUserView.as_view(), name='reset'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),

    # 课程机构首页
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程列表首页
    url(r'^courses/', include('courses.urls', namespace="courses")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

]
