# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    DEGREE = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )

    course_org = models.ForeignKey(CourseOrg, null=True, blank=True)
    name = models.CharField(u"课程名", max_length=50)
    desc = models.CharField(u"课程描述", max_length=300)
    detail = models.TextField(u"课程详情", )
    teacher = models.ForeignKey(Teacher, verbose_name=u'教师', null=True, blank=True)
    degree = models.CharField(u"等级", choices=DEGREE, max_length=3)
    learn_times  = models.IntegerField(u"学习时长", default=0)
    category = models.CharField(u'课程类别', max_length=20, default=u"后端开发")
    students = models.IntegerField(u"学习人数", default=0)
    fav_nums = models.IntegerField(u"收藏人数", default=0)
    image = models.ImageField(u"图片", upload_to='courses/%Y/%m', max_length=100)
    click_nums = models.IntegerField(u"点击数", default=0)
    tag = models.CharField(u'课程标签', max_length=10, default='')
    youneed_know = models.CharField(u'你需要知道', max_length=300, default='')
    teacher_tell = models.CharField(u'学到什么', max_length=300, default='')
    add_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    def __str__(self):
        return "<course %s>" % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"课程"

    def get_learn_users(self):
        return self.usercourse_set.all()[:4]


class Lesson(models.Model): # 章节
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(u"章节名", max_length=100)
    add_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    def __str__(self):
        return "<Lesson %s>" % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"章节"


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(u"视频名称", max_length=100)
    url = models.CharField(u'访问地址', max_length=200, default='')
    video_times = models.IntegerField(u"视频时长(分钟数)", default=0)
    add_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    def __str__(self):
        return "<Video %s>" % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"视频"


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(u"课程资源名", max_length=100)
    download = models.FileField(u"保存路径", upload_to="course/resource/%Y/%m")
    add_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    def __str__(self):
        return "<CourseResource %s>" % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"课程资源"