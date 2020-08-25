#!/usr/bin/env python
# -*- coding:utf-8 -*-


menu_list = [
    {'id': 1, 'title': '菜单1'},
    {'id': 2, 'title': '菜单2'},
    {'id': 3, 'title': '菜单3'},
]

menu_dict = {}
"""
{
    1:{'id': 1, 'title': '菜单1'},
    2:{'id': 2, 'title': '菜单2'},
    3:{'id': 3, 'title': '菜单3'},
}
"""
for item in menu_list:
    menu_dict[item['id']] = item

# menu_dict[2]['title'] = '666'

menu_dict[2]['children'] = [11,22]

print(menu_list)
