# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    GENDER = (
        ('male', u'男'),
        ('female', u'女'),
    )

    nick_name = models.CharField(u'昵称', max_length=50, default='')
    birthday = models.DateField(u'生日', null=True, blank=True)
    gender = models.CharField(u'性别', max_length=6, choices=GENDER, default='male')
    address = models.CharField(u"地址", max_length=100, default=u'')
    mobile = models.CharField(u"手机", max_length=11, null=True, blank=True)
    image = models.ImageField(u"头像", upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    def __str__(self):
        return "<user %s>" % self.username

    class Meta:
        verbose_name = verbose_name_plural = u"用户信息"


class EmailVerifyRecord(models.Model):
    SEND_TYPE = (
        ('register', u'注册'),
        ('forget', u'找回密码'),
    )
    code = models.CharField(u"验证码", max_length=20)
    email = models.EmailField(u"邮箱", max_length=50)
    send_type = models.CharField(u"验证码类型", choices=SEND_TYPE, max_length=10)
    send_time = models.DateTimeField(u"发送时间", auto_now_add=True)

    def __str__(self):
        return "<EmailVerifyRecord %s>" % self.email

    class Meta:
        verbose_name = verbose_name_plural = u"邮箱验证码"


class Banner(models.Model):
    title = models.CharField(u"标题", max_length=100)
    image = models.ImageField(u"图片", upload_to="banner/%Y/%m", max_length=100)
    url = models.URLField(u"访问地址", max_length=200)
    index = models.IntegerField(u"顺序", default=100)
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True)

    def __str__(self):
        return "<Banner %s>" % self.title

    class Meta:
        verbose_name = verbose_name_plural = u"轮播图"

