#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    """
    # 2. 权限信息初始化
    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session。
    # 当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__is_menu",
                                                                                      "permissions__icon",
                                                                                      "permissions__url").distinct()
    # 3. 获取权限+菜单
    permission_list = []
    menu_list = []
    for item in permission_queryset:
        permission_list.append(item['permissions__url'])
        if item['permissions__is_menu']:
            menu_list.append({
                'title': item['permissions__title'],
                'icon': item['permissions__icon'],
                'url': item['permissions__url'],
            })

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_list
