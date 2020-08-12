"""
角色管理
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

        return render(request, 'rbac/update.html', {'form': form}) # 错误信息保存在form中


def role_edit(request, pk):
    """
    修改角色
    :param request:
    :param pk:要修改的角色id
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = RoleModelForm(instance=obj)   # instance=obj : 使編輯框内帶默認值
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = RoleModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))

        return render(request, 'rbac/update.html', {'form': form})  # 错误信息保存在form中


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    if request.method == 'POST':
        models.Role.objects.filter(id=pk).delete()
        return redirect(origin_url)
