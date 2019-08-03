# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/3/10 0:08"
"""
专门放非继承的View,通常习惯以Mixin命名
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequireMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)