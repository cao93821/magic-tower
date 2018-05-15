# -*- coding: utf-8 -*-
"""
File Name: editor_utils
Author: cl
Create Date: 01/05/2018
Change Date: 01/05/2018

Description:

Example:
    
"""

import datetime
import os
import pickle

from configure import path, default_tower_map, item_dict, white, gray


class MessageManager:
    """
    消息管理器类，用来发送全局消息
    """
    def __init__(self):
        self._message = None
        self.time = None

    @property
    def message(self):
        """
        从消息管理器中读取存储的消息
        :return:
        """
        if self.time is not None:
            if (datetime.datetime.now() - self.time).seconds > 1:
                self._message = None
        return self._message

    @message.setter
    def message(self, message):
        """
        向消息管理器发送一条消息
        :param message:
        :return:
        """
        self.time = datetime.datetime.now()
        self._message = message


class EditorItem:
    """
    编辑器实体对象
    """
    def __init__(self, item_type, item_number, data_dict):
        self.type = item_type
        self.number = item_number
        self.image = data_dict[item_number]['image']


class Mouse:
    """
    鼠标类，用来处理一些与鼠标拖动相关的操作
    """
    def __init__(self):
        self.is_on_mouse = False
        self.item = None

    def load(self, item):
        self.is_on_mouse = True
        self.item = item

    def put(self, display_map, coordinate):
        if self.is_on_mouse:
            display_map[coordinate] = self.item


message_manager = MessageManager()


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