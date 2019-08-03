# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/3/16 17:57"


from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView
from .views import UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MymessageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 用户个人中心修改邮箱发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 用户个人中心修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 用户个人中心——我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 用户个人中心——我的收藏——收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 用户个人中心——我的收藏——收藏教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 用户个人中心——我的收藏——收藏课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 用户个人中心——我的消息
    url(r'^mymessage/$', MymessageView.as_view(), name='mymessage'),
]