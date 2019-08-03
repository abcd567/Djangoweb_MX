# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequireMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):

        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,

        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #课程点击数+1
        course.click_nums += 1
        course.save()

        had_fav_course = False
        had_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                had_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                had_fav_org = True

        #标签
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
            # if relate_courses[0].id == course.id:
            #     relate_course = relate_courses[1]
            # else:
            #     relate_course = relate_courses[0]
        else:
            relate_course = []
        return render(request, "course-detail.html", {
            'course': course,
            'relate_course': relate_course,
            'had_fav_course': had_fav_course,
            'had_fav_org': had_fav_org,
        })


class CourseInfoView(LoginRequireMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students = course.get_learn_user_nums()
        course.save()
        #查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        #学过该课程的用户还学过
        #过滤出学过该课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        #选出id
        user_ids = [user_course.user.id for user_course in user_courses]
        #通过id选出学过该课程的用户
        # user是UserCourse的外键，所以加下划线,两个下划线是传递list类型，只要id在user_ids这个list里面都满足过滤条件
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resource = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            'course': course,
            'course_resource': course_resource,
            'relate_courses': relate_courses,

        })


class CommentView(LoginRequireMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 学过该课程的用户还学过
        # 过滤出学过该课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 选出id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 通过id选出学过该课程的用户
        # user是UserCourse的外键，所以加下划线,两个下划线是传递list类型，只要id在user_ids这个list里面都满足过滤条件
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resource = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            'course': course,
            'course_resource': course_resource,
            'all_comment': all_comment,
            'relate_courses': relate_courses,
        })


class AddCommentsView(View):
    """
    用户添加评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断登陆状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):

        video = Video.objects.get(id=int(video_id))
        # 查询用户是否已经关联该课程
        course = video.lesson.course
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过该课程的用户还学过
        # 过滤出学过该课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 选出id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 通过id选出学过该课程的用户
        # user是UserCourse的外键，所以加下划线,两个下划线是传递list类型，只要id在user_ids这个list里面都满足过滤条件
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        course_resource = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            'course': course,
            'course_resource': course_resource,
            'relate_courses': relate_courses,
            'video': video,

        })

