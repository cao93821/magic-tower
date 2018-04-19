# -*- coding: utf-8 -*-
"""
File Name: util
Author: cl
Create Date: 18/03/2018
Change Date: 18/03/2018

Description:

Example:
    
"""


def to_coordinate(left, top, length):
    """
    从实体坐标转虚拟坐标
    :param left:
    :param top:
    :param length:
    :return:
    """
    if left % length == 0 and top % length == 0:
        return left / length + 1, top / length + 1
    else:
        raise ValueError


def to_real_coordinate(x, y, length):
    """
    从虚拟坐标转实体坐标
    :param x:
    :param y:
    :param length:
    :return:
    """
    return (x - 1) * length, (y - 1) * length


def is_in_rect(button_rect, pos):
    """
    判断坐标pos是否在一个rect内
    :param button_rect:
    :param pos:
    :return:
    """
    return button_rect[0] + button_rect[2] > pos[0] > button_rect[0] \
           and button_rect[1] + button_rect[3] > pos[1] > button_rect[1]

