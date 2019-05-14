# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/14 20:52'

from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'crt_page': 'home_page',
    })