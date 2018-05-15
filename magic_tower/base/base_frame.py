# -*- coding: utf-8 -*-
"""
File Name: model
Author: cl
Create Date: 18/03/2018
Change Date: 18/03/2018

Description:

Example:
    
"""


import time

from configure import *


class BattleMapSet:
    def __init__(self):
        self.battle_maps = {}
        self.current_map = None
        self.player = None

    def load_map(self, battle_map):
        self.battle_maps[battle_map.name] = battle_map
        battle_map.tower = self

    def set_current_map(self, map_name):
        self.current_map = self.battle_maps[map_name]

    def load(self, player, map_name="初始之地"):
        self.set_current_map(map_name)
        self.player = player
        entrance_coordinate = self.current_map.find_entrance("起始点")
        player.locate(entrance_coordinate[0], entrance_coordinate[1])
        player.battle_map = self.current_map


class BattleMap:
    def __init__(self, name):
        self.x_max = 16
        self.y_max = 16
        self.map = {}
        self.tower = None
        self.entrance = {(8, 16): "起始点"}
        self.exit = None
        self.name = name

    def read_item_config(self, item_config_dict, read_func):
        self.name = item_config_dict['name']
        item_list = read_func(item_config_dict['item_list'])
        for items in item_list:
            for item in items:
                self._load(item)

    def set_entrance(self, coordinate, map_name):
        self.entrance[coordinate] = map_name

    def find_entrance(self, map_name):
        for key, value in self.entrance.items():
            if value == map_name:
                return key

    def _load(self, something):
        if something.x < 1 or something.x > 16:
            raise ValueError('参数错误')
        if something.y < 1 or something.y > 16:
            raise ValueError('参数错误')
        value = self.map.get((something.x, something.y))
        if value is not None:
            raise ValueError('这个位置已经有东西了')
        self.map[(something.x, something.y)] = something
        something.battle_map = self


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.life = 100
        self.attack = 10
        self.defend = 10
        self.speed = 10
        self.yellow_key = 1
        self.blue_key = 1
        self.red_key = 1
        self.weapon_image = weapon_images[0]
        self.shield_image = shield_images[0]
        self.shoes_image = shoes_image
        self.range = number
        self.rect = None
        self.images = [player_downs, player_lefts, player_rights, player_ups]
        self.image = self.images[0][0]
        self.battle_map = None
        self.running = False

    def locate(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x - 1) * length, (self.y - 1) * length, length, length)

    def move_up(self):
        if not self.running:
            self.running = not self.running
            self.image = self.images[3][0]
            if self.y > 1:
                something = self.battle_map.map.get((self.x, self.y - 1))
                if something is None or something.be_interacted(self):
                    self.y -= 1
                    self.action(self.rect.width, 'up')
            self.running = not self.running

    def move_down(self):
        if not self.running:
            self.running = not self.running
            self.image = self.images[0][0]
            if self.y < self.range:
                something = self.battle_map.map.get((self.x, self.y + 1))
                if something is None or something.be_interacted(self):
                    self.y += 1
                    self.action(self.rect.width, 'down')
            self.running = not self.running

    def move_left(self):
        if not self.running:
            self.running = not self.running
            self.image = self.images[1][0]
            if self.x > 1:
                something = self.battle_map.map.get((self.x - 1, self.y))
                if something is None or something.be_interacted(self):
                    self.x -= 1
                    self.action(self.rect.width, 'left')
            self.running = not self.running

    def move_right(self):
        if not self.running:
            self.running = not self.running
            self.image = self.images[2][0]
            if self.x < self.range:
                something = self.battle_map.map.get((self.x + 1, self.y))
                if something is None or something.be_interacted(self):
                    self.x += 1
                    self.action(self.rect.width, 'right')
            self.running = not self.running

    def action(self, distance, direction):
        for i in [1, 2, 3, 0]:
            time.sleep(0.05)
            if direction == 'up':
                self.rect.top -= distance / 4
                self.image = self.images[3][i]
            elif direction == 'down':
                self.rect.top += distance / 4
                self.image = self.images[0][i]
            elif direction == 'left':
                self.rect.left -= distance / 4
                self.image = self.images[1][i]
            else:
                self.rect.left += distance / 4
                self.image = self.images[2][i]


from collections import deque


# 控制器
class Controller:

    def __init__(self):
        self.route_map = {}

    def key_press(self, key):
        self.route_map[key]()

    def load(self, key):
        def decorator(f):
            self.route_map[key] = f
            return f
        return decorator


# 消息中心
class MessageCenter:

    def __init__(self):
        self.subscribe_list = []

    def publish(self, message):
        for subscriber in self.subscribe_list:
            subscriber.notify(message)

    def add_subscriber(self, subscriber):
        """

        :param subscriber: 订阅者需要实现notify方法
        :return:
        """
        self.subscribe_list.append(subscriber)

    def register(self, promulgator):
        """

        :param promulgator: 发布者
        :return:
        """
        promulgator.message_center = self


# 消息管理器
class MessageController:
    def __init__(self):
        self.string_deque = deque(('game start',), 7)

    def notify(self, string):
        self.string_deque.append(string)

