# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/2/20 22:39"

import xadmin

from .models import CourseOrg, City, Teacher


class CourseOrgAdmin(object):
    list_display = ['name', 'courses', 'click_nums', 'fav_nums', 'address', 'city']
    search_fields = ['name', 'click_nums', 'fav_nums', 'address', 'city__name']
    list_filter = ['name', 'click_nums', 'fav_nums', 'address', 'city']
    relfield_style = 'fk-ajax'


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
