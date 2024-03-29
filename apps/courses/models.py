# _*_ encoding: utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    # detail = models.TextField(verbose_name=u'课程详情')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/%(datetime)s",
                           filePath="courses/ueditor/%(datetime)s", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    degree = models.CharField(verbose_name=u'难度', choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(min)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'后端开发')
    tag = models.CharField(max_length=10, verbose_name=u'课程标签', default='')
    need_know = models.CharField(max_length=300, verbose_name=u'课程须知', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name=u'老师告诉你',default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def get_learn_user(self):
        #获取学生5名
        return self.usercourse_set.all()[:5]

    def get_learn_user_nums(self):
        # 获取学生人数
        return self.usercourse_set.all().count()

    def get_course_lesson(self):
        #获取课程章节
        return self.lesson_set.all()

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.projectedu.com'>跳转</>")
    go_to.short_decription = "跳转"

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  #不生成新的表 用于数据分类


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        #获取章节视频
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    video_time = models.IntegerField(default=0, verbose_name=u'学习时长(min)')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
