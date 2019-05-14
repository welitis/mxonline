# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/13 10:34'
import string
import random

from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "慕雪在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
            print("发送成功")

    elif send_type == "forget":
        email_title = "慕雪在线网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
            print("发送成功")


def generate_random_str(n=8):
    char = string.ascii_letters + string.digits
    return ''.join(random.sample(char, n))


