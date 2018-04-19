# -*- coding: utf-8 -*-
"""
File Name: run2.py
Author: cl
Create Date: 18/03/2018
Change Date: 18/03/2018

Description:

Example:
    
"""

import sys
from threading import Thread

from pygame.constants import *

from configure import *
from magic_tower_2.base_view import BaseView
from magic_tower_2.modules import View
from magic_tower_2.base import Controller

pygame.init()


# 初始化controller
controller = Controller()

# 装配controllers，附带model层的初始化
# 不能使用import magic_tower_2.controllers执行其中的代码，可能是因为懒加载之类的东西
from magic_tower_2.controllers import *
from magic_tower_2.views import draw_battle, draw_player_panel, draw_name_panel


# 装配view层
screen = View(32 * (16 + 7), 32 * 16, is_base=True)
base_view = BaseView(screen)
controller_panel = View(32 * 7, 32 * 16, color=gray)
battle_panel = View(32 * 16, 32 * 16)
name_panel = View(32 * 7, 32 * 2, color=white)
display_panel = View(32 * 7, 32 * 5)
player_panel = View(32 * 7, 32 * 9, color=white)

controller_panel.locate(0, 0, screen)
battle_panel.locate(32 * 7, 0, screen)
name_panel.locate(0, 0, controller_panel)
display_panel.locate(0, 32 * 2, controller_panel)
player_panel.locate(0, 32 * 7, controller_panel)

battle_panel.load(draw_battle)
player_panel.load(draw_player_panel)
name_panel.load(draw_name_panel)
base_view.load_controller(controller)


flag = 1


def render():
    while flag:
        base_view.draw()
        pygame.display.update()


if __name__ == '__main__':

    thread_render = Thread(target=render)
    thread_render.start()
    while True:
        # 事件触发器
        for event in pygame.event.get():
            if event.type == QUIT:
                flag = 0
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_w and event.mod & KMOD_META:
                    flag = 0
                    sys.exit()
                if event.key == K_UP:
                    base_view.key_press('up')
                if event.key == K_DOWN:
                    base_view.key_press('down')
                if event.key == K_RIGHT:
                    base_view.key_press('right')
                if event.key == K_LEFT:
                    base_view.key_press("left")

            if event.type == MOUSEBUTTONDOWN:
                base_view.click(event.pos)


