"""
菜单和权限管理
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rbac import models
from rbac.forms.menu import MenuModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()

    menu_id = request.GET.get('mid')  # 在前端应将数字转成字符串：{{ row.id|safe }}

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'menu_id': menu_id,
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