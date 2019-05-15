# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(u'城市名', max_length=20)
    desc = models.CharField(u'城市描述', max_length=200)
    add_time = models.DateTimeField(u'添加时间', auto_now_add=True)

    def __str__(self):
        return '<CityDict %s>' % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"城市"


class CourseOrg(models.Model):
    CATEGORY = (
        ('pxjg', u'培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
    )

    address = models.CharField(u'机构地址', max_length=150)
    name = models.CharField(u'机构名', max_length=50)
    category = models.CharField(u'机构类别', max_length=10, choices=CATEGORY, default='pxjg')
    desc = models.TextField(u'机构描述')
    click_nums = models.IntegerField(u'点击数', default=0)
    fav_nums = models.IntegerField(u'收藏数', default=0)
    students = models.IntegerField(u'学习人数', default=0)
    course_nums = models.IntegerField(u'课程数', default=0)
    image = models.ImageField(u'logo', upload_to='org/%Y/%m')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    add_time = models.DateTimeField(u'添加时间', auto_now_add=True)

    def __str__(self):
        return '<CourseOrg %s>' % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"课程机构"


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所在机构')
    name = models.CharField(u'教师名', max_length=50)
    age = models.IntegerField(u'年龄', default=25)
    work_years = models.IntegerField(u'工作年限', default=0)
    work_company = models.CharField(u'所在公司', max_length=50)
    work_position = models.CharField(u'工作职位', max_length=30)
    points = models.CharField(u'特点', max_length=50)
    click_nums = models.IntegerField(u'点击数', default=0)
    fav_nums = models.IntegerField(u'收藏数', default=0)
    image = models.ImageField(u'头像', upload_to="teacher/%Y/%m", default='')
    add_time = models.DateTimeField(u'添加时间', auto_now_add=True)

    def __str__(self):
        return '<Teacher %s>' % self.name

    class Meta:
        verbose_name = verbose_name_plural = u"教师"