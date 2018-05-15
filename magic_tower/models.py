# -*- coding: utf-8 -*-
"""
File Name: models
Author: cl
Create Date: 23/03/2018
Change Date: 23/03/2018

Description:

Example:
    
"""


from tower_config import map1
from magic_tower.base.base_models import Player, Tower, MessageController
from magic_tower.items import init_map, message_center, BattleMap


# 装配model层
player = Player()
all_map = [init_map(tower_map) for tower_map in (map1,)]
tower = Tower()

for tower_map in all_map:
    battle_map = BattleMap()
    tower.load_map(battle_map)
    for items in tower_map:
        for item in items:
            battle_map.load(item)

tower.load(player, 'up')
message_controller = MessageController()
message_center.add_subscriber(message_controller)

status_map = {"p": 0}  # 2表示等待开启，1表示开启，0表示初始状态，-2表示等待关闭，-1表示关闭
