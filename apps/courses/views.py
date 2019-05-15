# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Course, Video
from operation.models import UserFavorite, CourseComments, UserCourse


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

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'courses/course-detail.html', {
            'course': course,
            'crt_page': crt_page,
            'course_fav': course_fav,
            'org_fav': org_fav,
            'relate_courses': relate_courses
        })


class CourseVedioView(LoginRequiredMixin, View):
    """课程章节信息"""

    login_url = '/login/'

    def get(self, request, course_id):
        crt_page = 'course_page'
        course = Course.objects.get(pk=course_id)
        all_resource = course.courseresource_set.all()

        # 添加用户课程
        if not UserCourse.objects.filter(user=request.user, course=course).exists():
            usercourse = UserCourse(user=request.user, course=course)
            usercourse.save()

        # 学过该课的人还学过什么
        all_usercourse = UserCourse.objects.filter(course=course)
        all_user_ids = [usercourse.user.id for usercourse in all_usercourse]
        all_user_courses = UserCourse.objects.filter(user_id__in=all_user_ids).all()
        course_ids = [usercourse.course_id for usercourse in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:3]

        return render(request, 'courses/course-video.html', {
            'course': course,
            'crt_page': crt_page,
            'relate_courses': relate_courses,
            'all_resource': all_resource
        })


class CourseCommentView(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request, course_id):
        crt_page = 'course_page'
        course = Course.objects.get(pk=course_id)
        all_resource = course.courseresource_set.all()
        all_comments = course.coursecomments_set.order_by('-add_time')

        # 添加用户课程
        if not UserCourse.objects.filter(user=request.user, course=course).exists():
            usercourse = UserCourse(user=request.user, course=course)
            usercourse.save()

        # 学过该课的人还学过什么
        all_usercourse = UserCourse.objects.filter(course=course)
        all_user_ids = [usercourse.user.id for usercourse in all_usercourse]
        all_user_courses = UserCourse.objects.filter(user_id__in=all_user_ids).all()
        course_ids = [usercourse.course_id for usercourse in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:3]

        return render(request, 'courses/course-comment.html', {
            'course': course,
            'crt_page': crt_page,
            'relate_courses': relate_courses,
            'all_resource': all_resource,
            'all_comments': all_comments,
        })


class CourseAddCommentView(View):
    """添加评论"""
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id and comments.strip():
            try:
                course = Course.objects.get(pk=course_id)
                coursecomments = CourseComments(user=request.user, comments=comments, course=course)
                coursecomments.save()
                return JsonResponse({'status': 'success', 'msg': '评论成功'})
            except:
                return JsonResponse({'status': 'fail', 'msg': '信息不正确'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '信息不正确'})


class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, video_id):
        crt_page = 'course_page'
        crt_video = Video.objects.get(pk=video_id)
        course = crt_video.lesson.course
        all_resource = course.courseresource_set.all()

        # 添加用户课程
        if not UserCourse.objects.filter(user=request.user, course=course).exists():
            usercourse = UserCourse(user=request.user, course=course)
            usercourse.save()

        # 学过该课的人还学过什么
        all_usercourse = UserCourse.objects.filter(course=course)
        all_user_ids = [usercourse.user.id for usercourse in all_usercourse]
        all_user_courses = UserCourse.objects.filter(user_id__in=all_user_ids).all()
        course_ids = [usercourse.course_id for usercourse in all_user_courses]
        relate_courses = Course.objects.filter(pk__in=course_ids).order_by('-click_nums')[:3]

        return render(request, 'courses/course-play.html', {
            'course': course,
            'crt_page': crt_page,
            'relate_courses': relate_courses,
            'all_resource': all_resource,
            'crt_video':crt_video,
        })