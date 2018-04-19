# -*- coding: utf-8 -*-
"""
File Name: controllers
Author: cl
Create Date: 23/03/2018
Change Date: 23/03/2018

Description:

Example:
    
"""

from run2 import controller
from magic_tower_2.models import *


@controller.load("up")
def move_up():
    tower.player.move_up()


@controller.load("down")
def move_down():
    tower.player.move_down()


@controller.load("left")
def move_left():
    tower.player.move_left()


@controller.load("right")
def move_right():
    tower.player.move_right()
