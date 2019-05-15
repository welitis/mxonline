# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings

from .models import CourseOrg, CityDict, Teacher
from courses.models import Course
from .forms import UserAskForm
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    """课程机构列表功能"""
    def get(self, request):
        page_num = request.GET.get('page', 1)
        city_id = request.GET.get('city_id', "")
        category = request.GET.get('category', "")
        sort_type = request.GET.get('sort_type', "")

        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 按城市进行分类
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id).all()

        # 对机构类别进行分类
        if category:
            all_orgs = all_orgs.filter(category=category)
        org_nums = all_orgs.count()
        all_category = CourseOrg.CATEGORY

        # 按学习人数排序
        if sort_type == "students":
            all_orgs = all_orgs.order_by('-students')

        # 按课程数进行排序
        if sort_type == "course":
            all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页
        paginator = Paginator(all_orgs, settings.EACH_PAGE_NUMS)    # 拿到分页器对象
        try:
            page_of_org = paginator.page(page_num)
        except EmptyPage:
            page_of_org = paginator.page(1)
        current_page_num = page_of_org.number
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

        return render(request, "org-list.html", {
            'all_citys': all_citys,
            'org_nums': org_nums,
            'page_of_org': page_of_org,
            'page_range': page_range,
            'city_id': city_id,
            'category': category,
            'all_category': all_category,
            'hot_orgs': hot_orgs,
            'sort_type': sort_type,
            'crt_page': 'org_page',
        })


class AddUserAskView(View):
    """用户添加咨询"""
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class OrgHomeView(View):
    """机构首页"""
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(pk=org_id)
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2).exists():
                has_fav = True
        return render(request, 'organization/org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """机构课程列表页"""
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(pk=org_id)
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2).exists():
                has_fav = True

        return render(request, 'organization/org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(pk=org_id)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2).exists():
                has_fav = True

        return render(request, 'organization/org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(pk=org_id)
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2).exists():
                has_fav = True

        return render(request, 'organization/org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddUserFavView(View):
    """用户添加收藏"""
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        exists_record = UserFavorite.objects.filter(fav_id=int(fav_id), fav_type=int(fav_type), user=request.user)
        try:
            if fav_type == '1':
                fav_obj = Course.objects.get(pk=fav_id)
                    # 添加course收藏数+1
            elif fav_type == '2':
                fav_obj = CourseOrg.objects.get(pk=fav_id)
                    # 添加course_org收藏数+1
            elif fav_type == '3':
                fav_obj = Teacher.objects.get(pk=fav_id)
                    # 添加teacher收藏数+1
            else:
                return JsonResponse({'status': 'fail', 'msg': 'fav_type error'})
        except:
            return JsonResponse({'status': 'fail', 'msg': 'fav_id error'})
        if exists_record:
            exists_record.delete()      # 如果记录已存在说明用户已收藏，这次请求是要取消收藏
            fav_obj.fav_nums -= 1
            fav_obj.save()
            return JsonResponse({'status': 'success', 'msg': '收藏'})
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_type = fav_type
                user_fav.fav_id = fav_id
                user_fav.save()
                fav_obj.fav_nums += 1
                fav_obj.save()
                return JsonResponse({'status': 'success', 'msg': '已收藏'})
            else:
                return JsonResponse({'status': 'failt', 'msg': '收藏出错'})


class TeacherListView(View):
    def get(self, request):
        page_num = request.GET.get('page', 1)
        sort_type = request.GET.get('sort_type', "time")

        all_teacher = Teacher.objects.all()
        hot_teacher = all_teacher.order_by("-click_nums")[:3]

        # 按点击量进行排序
        if sort_type == 'click_nums':
            all_teacher = all_teacher.order_by('-click_nums')

        teacher_nums = all_teacher.count()

        # 对课程机构进行分页
        paginator = Paginator(all_teacher, settings.EACH_PAGE_NUMS)    # 拿到分页器对象
        try:
            page_of_teacher = paginator.page(page_num)
        except EmptyPage:
            page_of_teacher = paginator.page(1)
        current_page_num = page_of_teacher.number
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

        return render(request, "organization/teachers-list.html", {
            'teacher_nums': teacher_nums,
            'page_of_teacher': page_of_teacher,
            'page_range': page_range,
            'hot_teacher': hot_teacher,
            'sort_type': sort_type,
            'crt_page': 'teacher_page',
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        crt_page = 'teacher_page'
        teacher = Teacher.objects.get(pk=teacher_id)
        hot_teacher = Teacher.objects.order_by("-click_nums")[:3]
        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3).exists():
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.pk, fav_type=2).exists():
                org_fav = True

        teacher.click_nums += 1
        teacher.save()

        return render(request, 'organization/teacher-detail.html', {
            'teacher': teacher,
            'crt_page': crt_page,
            'teacher_fav': teacher_fav,
            'org_fav': org_fav,
            'hot_teacher': hot_teacher
        })
