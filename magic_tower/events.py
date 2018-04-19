# -*- coding: utf-8 -*-
"""
File Name: events
Author: cl
Create Date: 28/01/2018
Change Date: 28/01/2018

Description:

Example:
    
"""

import os
import pickle

from configure import path, default_tower_map, item_dict, white, gray
from magic_tower.modules import message_manager, EditorItem, View, Button


def save_map(display_map):
    """
    保存tower_map
    :param display_map:
    :return:
    """
    # 先将display_map转化成editor_map
    with open(os.path.join(path, 'save1'), 'bw') as f:
        maps = {1: to_tower_map(display_map)}
        pickle.dump(maps, f)
        message_manager.message = '保存成功'


def check_maps():
    with open(os.path.join(path, 'save1'), 'br') as f:
        maps = pickle.load(f)
    return maps


def load_map(editor, num, view):
    """
    加载保存的tower_map
    :param num
    :param editor:
    :param view
    :return:
    """
    with open(os.path.join(path, 'save1'), 'br') as f:
        editor.tower_map = pickle.load(f)[num]
        editor.display_map = to_display_map(editor.tower_map)
        view.delete()
        message_manager.message = '加载成功'


def load_map_for_run():
    with open(os.path.join(path, 'save1'), 'br') as f:
        return pickle.load(f)


def to_display_map(tower_map):
    """
    tower_map转display_map
    :param tower_map:
    :return:
    """
    display_map = {}
    for key, value in tower_map.items():
        for item_number, pos_set in value.items():
            for pos in pos_set:
                display_map[pos] = EditorItem(key[0:-1], item_number, item_dict[key[0:-1] + '_dict'])
    return display_map


def to_tower_map(display_map):
    """
    display_map转tower_map
    :param display_map:
    :return:
    """
    tower_map = default_tower_map
    for pos, editor_item in display_map.items():
        tower_map[editor_item.type + 's'][editor_item.number].add(pos)
    return tower_map


def pop_load_panel(screen, editor):
    """
    弹出加载弹窗
    :param screen:
    :param editor:
    :return:
    """
    load_panel = View(32 * 8, 32 * 4, color=gray)
    load_panel.locate(40, 40, screen)
    maps = check_maps()
    for number in maps.keys():
        button = Button(load_map, 80, 40, text="第{}层".format(number), color=white, params=(editor, number, load_panel))
        button.locate(10, 10, load_panel)

