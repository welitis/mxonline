# _*_ encoding: utf-8 _*_
__author__ = 'Welisit'
__date__ = '2019/5/12 12:57'


import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['address', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'city', 'add_time']
    search_fields = ['address', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'city']
    list_filter = ['address', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)