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
from magic_tower_2.base import Player, Tower, BattleMap
from magic_tower_2.items import init_map


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
