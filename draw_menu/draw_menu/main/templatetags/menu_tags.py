from typing import Dict, List
from django.db import models
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import resolve

from ..models import MenuItem, Menu

register = template.Library()


def build_struct(menu_items: List) -> List:
    """
    Функция строит древовидную структуру в виде списка словарей, где у каждого item есть список наследников children.
    Если наследников нет, то список пуст.
    :param menu_items: Список объектов модели MenuItem
    :return: Древовидную структуру в виде списка словарей
    """
    items: Dict = {item: {'item': item, 'children': []} for item in menu_items}
    struct: List = list()
    for item in menu_items:
        if item.parent is None:
            struct.append(items[item])
        else:
            items[item.parent]['children'].append(items[item])
    return struct


def set_parent_active(parent: MenuItem, menu_structure: List, base: List) -> None:
    """
    Функция рекурсивно устанавливает атрибут is_active как True для каждого родителя, у которого наследник child
    имеет атрибут is_active как True
    :param parent: родительский элемент активного наследника child
    :param menu_structure: текущий список наследников
    :param base: базовая древовидная структура
    :return: None
    """
    if parent is None:
        return
    for item in menu_structure:
        if item['item'] == parent:
            item['item'].is_active = True
            set_parent_active(item['item'].parent, base, base)
            return
        set_parent_active(parent, item['children'], base)


def set_active(menu_structure: List, current_url: str, base: List) -> None:
    """
    Функция рекурсивно ищет объект модели MenuItem, для которого атрибут url равен текущему адресу страницы current_url
    :param menu_structure: Текущий список наследников
    :param current_url: URL текущей страницы
    :param base: Исходная древовидная структура
    :return: None
    """
    for item in menu_structure:
        if item['item'].url == current_url:
            item['item'].is_active = True
            set_parent_active(item['item'].parent, base, base)
        children = item['children']
        if len(children) != 0:
            set_active(children, current_url, base)


def get_object_or_false(model, **kwargs) -> models.Model | bool:
    """
    Функция возвращает объект модели, если таковая найдется. В противном случае вернут False
    :param model: Модель бд
    :param kwargs: именованные аргументы модели
    :return: Объект модели либо None
    """
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return False


@register.inclusion_tag('main/menu.html', takes_context=True)
def draw_menu(context, menu_name) -> Dict | None:
    request = context['request']
    current_url = request.path

    menu = get_object_or_false(Menu, name=menu_name)
    if not menu:
        return None

    menu_items = MenuItem.objects.filter(menu_name=menu).prefetch_related('child')
    struct = build_struct(menu_items)
    set_active(struct, current_url[1::], struct)
    return {'struct': struct}
