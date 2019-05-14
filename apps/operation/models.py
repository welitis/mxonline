# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from courses.models import Course
from users.models import UserProfile
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(u"用户名", max_length=20)
    mobile = models.CharField(u"手机", max_length=11)
    course_name = models.CharField(u"课程名", max_length=50)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<UserAsk %s>" % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"用户咨询"


class CourseComments(models.Model):
    """课程评论"""
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    comments = models.CharField(u"评论", max_length=200)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<CourseComments %s>" % self.comments

    class Meta:
        verbose_name = verbose_name_plural = u"课程评论"


class UserFavorite(models.Model):
    FAV_TYPE = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '教师'),
    )
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(u"收藏id", default=0)
    fav_type = models.IntegerField(u"收藏类型", choices=FAV_TYPE, default=1)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<UserFavorite %s:%s>" % (self.user, self.fav_type)

    class Meta:
        verbose_name = verbose_name_plural = u"用户收藏"


class UserMessage(models.Model):
    user = models.IntegerField(u"用户id", default=0)
    message = models.CharField(u"信息", max_length=500)
    has_read = models.BooleanField(u"是否已读", default=False)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<UserMessage %s>" % self.message

    class Meta:
        verbose_name = verbose_name_plural = u"消息"


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程名")
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<UserCourse %s>" % self.course

    class Meta:
        verbose_name = verbose_name_plural = u"用户课程"