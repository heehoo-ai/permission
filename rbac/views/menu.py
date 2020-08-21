"""
菜单和权限管理
"""
from collections import OrderedDict
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, MultiAddPermissionForm, \
    MultiEditPermissionForm
from rbac.service.urls import memory_reverse
from rbac.service.routers import get_all_url_dict

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


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    generate_formset = None
    update_formset = None
    if request.method == 'POST' and post_type == 'generate':
        # pass # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # pass  # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    # 1. 获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    """
    {
        'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
        ....
    }
    """
    router_name_set = set(all_url_dict.keys())

    # 2. 获取数据库中所有的URL
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])
    """
    {
        'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
        'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
        ...
    }
    """

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3. 应该添加、删除、修改的权限有哪些？
    # 3.1 计算出应该增加的name
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name
    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': update_formset,
        }
    )


def multi_permissions_del(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
