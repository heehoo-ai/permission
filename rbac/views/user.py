"""
用户管理
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm
from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetPasswordUserModelForm


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    user_queryset = models.UserInfo.objects.all()

    return render(request, 'rbac/user_list.html', {'users': user_queryset})


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))

        return render(request, 'rbac/update.html', {'form': form}) # 错误信息保存在form中


def user_del(request, pk):
    """
    删除用户
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})

    if request.method == 'POST':
        models.UserInfo.objects.filter(id=pk).delete()
        return redirect(origin_url)


def user_edit(request, pk):
    """
    修改用户
    :param request:
    :param pk:要修改的用户id
    :return:
    """
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')

    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)   # instance=obj : 使編輯框内帶默認值
        return render(request, 'rbac/update.html', {'form': form})

    if request.method == 'POST':
        form = UpdateUserModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))

        return render(request, 'rbac/update.html', {'form': form})  # 错误信息保存在form中


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/update.html', {'form': form})

    form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/update.html', {'form': form})
