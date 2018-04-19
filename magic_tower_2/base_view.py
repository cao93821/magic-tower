# -*- coding: utf-8 -*-
"""
File Name: base
Author: cl
Create Date: 18/03/2018
Change Date: 18/03/2018

Description:

Example:
    
"""


class BaseView:

    def __init__(self, view):
        self.view = view
        self.controller = None

    def load_controller(self, controller):
        self.controller = controller

    def key_press(self, key):
        self.controller.key_press(key)

    def click(self, pos):
        self.view.click(pos)

    def draw(self):
        self.view.render()


