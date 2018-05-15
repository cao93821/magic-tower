# -*- coding: utf-8 -*-
"""
File Name: items
Author: cl
Create Date: 18/03/2018
Change Date: 18/03/2018

Description:

Example:
    
"""

import time
import threading

from configure import *
from magic_tower.base.base_frame import MessageCenter


# 全局锁，在渲染时使用
render_lock = threading.Lock()

# 消息中心
message_center = MessageCenter()


def init_map(map_dict):
    walls = [Wall(*wall, item_number) for item_number, wall_set in map_dict['walls'].items() for wall in wall_set]
    doors = [Door(*door, item_number) for item_number, door_set in map_dict['doors'].items() for door in door_set]
    keys = [Key(*key, item_number) for item_number, key_set in map_dict['keys'].items() for key in key_set]
    stairss = [Stairs(*stairs, item_number) for item_number, stairs_set in map_dict['stairss'].items() for stairs in stairs_set]
    weapons = [Weapon(*weapon, item_number) for item_number, weapon_set in map_dict['weapons'].items() for weapon in weapon_set]
    monsters = [Monster(*monster, item_number) for item_number, monster_set in map_dict['monsters'].items() for monster in monster_set]
    drugs = [Drug(*drug, item_number) for item_number, drug_set in map_dict['drugs'].items() for drug in drug_set]
    gems = [Gem(*gem, item_number) for item_number, gem_set in map_dict['gems'].items() for gem in gem_set]
    return [walls, doors, keys, stairss, weapons, monsters, drugs, gems]


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


class Item:
    """
    所有item的基类
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.battle_map = None
        self.message_center = message_center
        self.lock = render_lock

    def be_interacted(self, player):
        pass

    def pop_item(self):
        render_lock.acquire()
        self.battle_map.map.pop((self.x, self.y))
        render_lock.release()


class Wall(Item):
    def __init__(self, x, y, wall_number):
        super().__init__(x, y)
        data = wall_dict[wall_number]
        self.name = data['name']
        self.images = data['images']
        self.image = data['image']
        self.destroyable = False

    def be_interacted(self, player):
        if self.destroyable:
            self.action()
            self.pop_item()
            return True
        self.message_center.publish('这是一堵墙')
        return False

    def action(self):
        for i in [1, 2, 3]:
            time.sleep(0.08)
            self.image = self.images[i]


class Monster(Item):
    def __init__(self, x, y, monster_number):
        super().__init__(x, y)
        data = monster_dict[monster_number]
        self.name = data['name']
        self.life = data['life']
        self.attack = data['attack']
        self.defend = data['defend']
        self.speed = data['life']
        self.image = data['image']

    def be_interacted(self, player):
        left_life = self.fight(player)
        if left_life < 0:
            self.message_center.publish('怪物太强大了，回去再练练吧')
            return False
        else:
            self.pop_item()
            self.message_center.publish('你击败了{}，损失{}生命'.format(self.name, player.life - left_life))
            player.life = left_life
            return True

    def fight(self, player):
        monster_life = self.life
        player_life = player.life
        if self.speed > player.speed:
            while True:
                player_life -= (self.attack - player.defend)
                if player_life < 0:
                    break
                monster_life -= (player.attack - self.defend)
                if monster_life < 0:
                    break
        else:
            while True:
                monster_life -= (player.attack - self.defend)
                if monster_life < 0:
                    break
                player_life -= (self.attack - player.defend)
                if player_life < 0:
                    break
        return player_life


class Door(Item):
    def __init__(self, x, y, door_number):
        super().__init__(x, y)
        data = door_dict[door_number]
        self.name = data['name']
        self.images = data['images']
        self.image = data['image']

    def be_interacted(self, player):
        if self.name == '黄门' and player.yellow_key > 0:
            player.yellow_key -= 1
        elif self.name == '蓝门' and player.blue_key > 0:
            player.blue_key -= 1
        elif self.name == '红门' and player.red_key > 0:
            player.red_key -= 1
        else:
            self.message_center.publish('你没有可以打开这扇门的钥匙')
            return False
        self.action()
        self.pop_item()
        self.message_center.publish('你打开了一扇门')
        return True

    def action(self):
        for i in [1, 2, 3]:
            time.sleep(0.08)
            self.image = self.images[i]


class Drug(Item):
    def __init__(self, x, y, drug_number):
        super().__init__(x, y)
        data = drug_dict[drug_number]
        self.name = data['name']
        self.heal = data['heal']
        self.image = data['image']

    def be_interacted(self, player):
        player.life += self.heal
        self.pop_item()
        self.message_center.publish('喝下了{}，回复{}生命值'.format(self.name, self.heal))
        return True


class Gem(Item):
    def __init__(self, x, y, gem_number):
        super().__init__(x, y)
        data = gem_dict[gem_number]
        self.name = data['name']
        self.type = data['type']
        self.number = data['number']
        self.image = data['image']

    def be_interacted(self, player):
        if self.type == 'attack':
            player.attack += self.number
            param = '攻击力'
        elif self.type == 'defend':
            player.defend += self.number
            param = '防御力'
        else:
            player.speed += self.number
            param = '速度'
        self.pop_item()
        self.message_center.publish('捡到一块{}，{}提升{}点'.format(self.name, param, self.number))
        return True


class Key(Item):
    def __init__(self, x, y, key_number):
        super().__init__(x, y)
        data = key_dict[key_number]
        self.name = data['name']
        self.image = data['image']

    def be_interacted(self, player):
        self.pop_item()
        self.message_center.publish('你捡到了一把{}'.format(self.name))
        if self.name == '黄钥匙':
            player.yellow_key += 1
        elif self.name == '蓝钥匙':
            player.blue_key += 1
        else:
            player.red_key += 1
        return True


class Stairs(Item):
    def __init__(self, x, y, stairs_number):
        super().__init__(x, y)
        data = stairs_dict[stairs_number]
        self.name = data['name']
        self.image = data['image']

    def be_interacted(self, player):
        self.action()
        self.message_center.publish('你来到了{}楼'.format(self.battle_map.tower.current_floor))
        return False

    def action(self):
        if self.name == 'down':
            self.battle_map.tower.current_floor -= 1
        else:
            self.battle_map.tower.current_floor += 1
        self.battle_map.tower.load(self.battle_map.tower.player, self.name, self.battle_map.tower.current_floor)


class Weapon(Item):
    def __init__(self, x, y, weapon_number):
        super().__init__(x, y)
        data = weapon_dict[weapon_number]
        self.name = data['name']
        self.attack = data['attack']
        self.image = data['image']

    def be_interacted(self, player):
        player.attack += self.attack
        player.weapon_image = self.image
        self.pop_item()
        self.message_center.publish('你得到了一把宝剑，攻击力提升{}'.format(self.attack))
        return True


