"""
菜单和权限管理
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')  # 在前端应将数字转成字符串：{{ row.id|safe }}
    second_menu_id = request.GET.get('sid')  # 用户选择的二级

    # 防止地址栏伪装menu_id打开新建功能
    menu_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menu_exists:
        menu_id = None

    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menus': second_menus,
            'menu_id': menu_id,
            'second_menu_id': second_menu_id,
            'permissions': permissions,
        }
    )


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(memory_reverse(request, 'rbac:menu_list'))

        return render(request, 'rbac/update.html', {'form': form}) # 错误信息保存在form中


def menu_edit(request, pk):
    """
    修改一级菜单
    :param request:
    :param pk:要修改的菜单id
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = MenuModelForm(instance=obj)   # instance=obj : 使編輯框内帶默認值
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = MenuModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(memory_reverse(request, 'rbac:menu_list'))

        return render(request, 'rbac/update.html', {'form': form})  # 错误信息保存在form中


def menu_del(request, pk):
    """
    删除菜单
    :param request:
    :param pk:
    :return:
    """
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    if request.method == 'POST':
        models.Menu.objects.filter(id=pk).delete()
        return redirect(origin_url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_obj})
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = SecondMenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(memory_reverse(request, 'rbac:menu_list'))

        return render(request, 'rbac/update.html', {'form': form}) # 错误信息保存在form中


def second_menu_edit(request, pk):
    """
    修改二级菜单
    :param request:
    :param pk:要修改的菜单id
    :return:
    """
    permission_object = models.Permission.objects.filter(id=pk).first()
    if not permission_object:
        return HttpResponse('二级菜单不存在')

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)   # instance=obj : 使編輯框内帶默認值
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = SecondMenuModelForm(instance=permission_object, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(memory_reverse(request, 'rbac:menu_list'))

        return render(request, 'rbac/update.html', {'form': form})  # 错误信息保存在form中


def second_menu_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限信息
    :param request:
    :param second_menu_id: 已选择的二级菜单ID（用于设置默认值）
    :return:
    """

    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = PermissionModelForm(data=request.POST)
        if form.is_valid():
            second_menu_obj = models.Permission.objects.filter(id=second_menu_id).first()
            if not second_menu_obj:
                return HttpResponse('二级菜单不存在，请重新选择！')
            form.instance.pid = second_menu_obj
            form.save()
            return redirect(memory_reverse(request, 'rbac:menu_list'))

        return render(request, 'rbac/update.html', {'form': form}) # 错误信息保存在form中


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 当前要编辑的权限ID
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/update.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/update.html', {'form': form})


def permission_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
