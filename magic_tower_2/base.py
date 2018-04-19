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
from magic_tower.items import Stairs


class Tower:
    def __init__(self):
        self.battle_maps = []
        self.current_floor = 1
        self.player = None

    def load_map(self, battle_map):
        self.battle_maps.append(battle_map)
        battle_map.tower = self

    def load(self, player, load_type, floor=1):
        self.player = player
        self.current_floor = floor
        if load_type == 'up':
            x = self.battle_maps[self.current_floor - 1].entrance[0]
            y = self.battle_maps[self.current_floor - 1].entrance[1]
        else:
            x = self.battle_maps[self.current_floor - 1].exit[0]
            y = self.battle_maps[self.current_floor - 1].exit[1]
        player.locate(x, y)
        player.battle_map = self.battle_maps[self.current_floor - 1]


class BattleMap:
    def __init__(self):
        self.x_max = 16
        self.y_max = 16
        self.map = {}
        self.tower = None
        self.entrance = (8, 16)
        self.exit = None

    def load(self, something):
        if isinstance(something, Stairs):
            if something.name == 'down':
                self.entrance = (something.x, something.y)
            else:
                self.exit = (something.x, something.y)
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
