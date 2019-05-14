# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings

# Create your views here.
from .models import Course
from operation.models import UserFavorite


class CourseListView(View):
    def get(self, request):
        page_num = request.GET.get('page', 1)
        sort_type = request.GET.get('sort_type', "time")

        all_course = Course.objects.all()
        hot_course = all_course.order_by("-click_nums")[:3]

        # 按时间进行排序
        if sort_type == 'time':
            all_course = all_course.order_by('-add_time')

        # 按点击量进行排序
        elif sort_type == 'click_nums':
            all_course = all_course.order_by('-click_nums')

        # 按学习人数排序
        elif sort_type == "learn_nums":
            all_course = all_course.order_by('-students')

        course_nums = all_course.count()

        # 对课程机构进行分页
        paginator = Paginator(all_course, settings.EACH_PAGE_NUMS)    # 拿到分页器对象
        try:
            page_of_course = paginator.page(page_num)
        except EmptyPage:
            page_of_course = paginator.page(1)
        current_page_num = page_of_course.number
        # 获取当前页面的相邻页码列表，如果当前是7， 则获得列表为[5,6,7,8,9]
        page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages+1)))
        # 添加上首尾页码，形成 [1, '...', 5,6,7,8,9, '...', 19]
        if page_range[0] != 1:
            if page_range[0] == 2:              # page_range = [2,3,4,5,6] ==> [1,2,3,4,5,6]
                page_range.insert(0, 1)
            else:                               # page_range = [5,6,7,8,9] ==> [1,'...', 5,6,7,8,9]
                page_range[:0] = [1, '...']
        if page_range[-1] != paginator.num_pages:
            if page_range[-1] == paginator.num_pages - 1:
                page_range.append(paginator.num_pages)
            else:
                page_range.extend(['...', paginator.num_pages])

        return render(request, "courses/course-list.html", {
            'course_nums': course_nums,
            'page_of_course': page_of_course,
            'page_range': page_range,
            'hot_course': hot_course,
            'sort_type': sort_type,
            'crt_page': 'course_page',
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        crt_page = 'course_page'
        course = Course.objects.get(pk=course_id)
        course_fav = False
        org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1).exists():
                course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.pk, fav_type=2).exists():
                org_fav = True

        course.click_nums += 1
        course.save()
        return render(request, 'courses/course-detail.html', {
            'course': course,
            'crt_page': crt_page,
            'course_fav': course_fav,
            'org_fav': org_fav
        })