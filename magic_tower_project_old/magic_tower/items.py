import time
import threading

from configure import *


# 全局锁，在渲染时使用
render_lock = threading.Lock()


class Item:
    """
    所有item的基类
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.battle_map = None
        self.controller = None
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
        self.controller.display('这是一堵墙')
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
            self.controller.display('怪物太强大了，回去再练练吧')
            return False
        else:
            self.pop_item()
            self.controller.display('你击败了{}，损失{}生命'.format(self.name, player.life - left_life))
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
            self.controller.display('你没有可以打开这扇门的钥匙')
            return False
        self.action()
        self.pop_item()
        self.controller.display('你打开了一扇门')
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
        self.controller.display('喝下了{}，回复{}生命值'.format(self.name, self.heal))
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
        self.controller.display('捡到一块{}，{}提升{}点'.format(self.name, param, self.number))
        return True


class Key(Item):
    def __init__(self, x, y, key_number):
        super().__init__(x, y)
        data = key_dict[key_number]
        self.name = data['name']
        self.image = data['image']

    def be_interacted(self, player):
        self.pop_item()
        self.controller.display('你捡到了一把{}'.format(self.name))
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
        self.controller.display('你来到了{}楼'.format(self.battle_map.tower.current_floor))
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
        self.controller.display('你得到了一把宝剑，攻击力提升{}'.format(self.attack))
        return True
