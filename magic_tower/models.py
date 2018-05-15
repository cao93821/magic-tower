# -*- coding: utf-8 -*-
"""
File Name: models
Author: cl
Create Date: 23/03/2018
Change Date: 23/03/2018

Description:

Example:
    
"""


from magic_tower.base_widget import MessageController
from tower_config import map1, map2
from magic_tower.base_frame import Player, BattleMapSet, BattleMap
from magic_tower.items import init_map, message_center


# 装配model层
player = Player()
battle_map_set = BattleMapSet()

for tower_map in (map1, map2):
    battle_map = BattleMap("初始之地")
    battle_map_set.load_map(battle_map)
    battle_map.read_item_config(tower_map, init_map)

battle_map_set.load(player)
message_controller = MessageController()
message_center.add_subscriber(message_controller)

# 状态表
status_map = {"p": 0}  # 2表示等待开启，1表示开启，0表示初始状态，-2表示等待关闭，-1表示关闭
