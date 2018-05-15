# -*- coding: utf-8 -*-
"""
File Name: controllers
Author: cl
Create Date: 23/03/2018
Change Date: 23/03/2018

Description:

Example:
    
"""

from run import controller
from magic_tower.models import *


@controller.load("up")
def move_up():
    battle_map_set.player.move_up()


@controller.load("down")
def move_down():
    battle_map_set.player.move_down()


@controller.load("left")
def move_left():
    battle_map_set.player.move_left()


@controller.load("right")
def move_right():
    battle_map_set.player.move_right()


@controller.load("p")
def display_hand_book():
    if status_map["p"] > 0:
        status_map["p"] = -2
    else:
        status_map["p"] = 2
