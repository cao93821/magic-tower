# -*- coding: utf-8 -*-
"""
File Name: views
Author: cl
Create Date: 07/04/2018
Change Date: 07/04/2018

Description:

Example:
    
"""

from configure import *
from magic_tower.models import player, tower, message_controller
from magic_tower.base_models import Player
from magic_tower.util import to_real_coordinate
from magic_tower.items import render_lock, Monster


def draw_battle(battle_panel):
    for i in range(16):
        for j in range(16):
            battle_panel.blit(ground_image, to_real_coordinate(i + 1, j + 1, 32))
    # 绘制元素
    render_lock.acquire()
    for coordinate, something in tower.battle_maps[tower.current_floor - 1].map.items():
        if not isinstance(something, Player):
            battle_panel.blit(something.image, to_real_coordinate(coordinate[0], coordinate[1], length))
    render_lock.release()

    # 绘制人物
    battle_panel.blit(player.image, player.rect)


def draw_player_panel(player_panel):
    player_panel.blit(font_title.render('生命值            {}'.format(player.life), 1, gray), (30, 10))
    player_panel.blit(font_title.render('攻击力            {}'.format(player.attack), 1, gray), (30, 40))
    player_panel.blit(font_title.render('防御力            {}'.format(player.defend), 1, gray), (30, 70))
    player_panel.blit(font_title.render('速度值            {}'.format(player.speed), 1, gray), (30, 100))

    player_panel.blit(yellow_key_image, (30, 140))
    player_panel.blit(blue_key_image, (90, 140))
    player_panel.blit(red_key_image, (150, 140))
    player_panel.blit(font_title.render('x {}'.format(player.yellow_key), 1, gray), (30, 170))
    player_panel.blit(font_title.render('x {}'.format(player.blue_key), 1, gray), (90, 170))
    player_panel.blit(font_title.render('x {}'.format(player.red_key), 1, gray), (150, 170))

    player_panel.blit(player.weapon_image, (30, 210))
    player_panel.blit(player.shield_image, (90, 210))
    player_panel.blit(player.shoes_image, (150, 210))


def draw_name_panel(name_panel):
    name_panel.blit(font_title.render('魔塔第{}层'.format(tower.current_floor), 1, gray), (10, 10))


def draw_display_panel(display_panel):
    for i in range(len(message_controller.string_deque)):
        display_panel.blit(font_description.render(message_controller.string_deque[i], 1, white), (10, 10 + i * 20))


def draw_hand_book_panel(hand_book_panel):
    hand_book_panel.fill(gray)
    hand_book_panel.blit(font_description.render('名称', 1, white), (80, 30))
    hand_book_panel.blit(font_description.render('生命值', 1, white), (140, 30))
    hand_book_panel.blit(font_description.render('攻击力', 1, white), (200, 30))
    hand_book_panel.blit(font_description.render('防御力', 1, white), (260, 30))
    hand_book_panel.blit(font_description.render('速度', 1, white), (320, 30))
    hand_book_panel.blit(font_description.render('预计损耗', 1, white), (380, 30))
    index = 1
    for key, value in monster_dict.items():
        hand_book_panel.blit(value['image'], (30, 30 + index * 50))
        hand_book_panel.blit(font_description.render('{}'.format(value['name']), 1, white),
                          (80, 30 + index * 50))
        hand_book_panel.blit(font_description.render('{}'.format(value['life']), 1, white),
                          (140, 30 + index * 50))
        hand_book_panel.blit(font_description.render('{}'.format(value['attack']), 1, white),
                          (200, 30 + index * 50))
        hand_book_panel.blit(font_description.render('{}'.format(value['defend']), 1, white),
                          (260, 30 + index * 50))
        hand_book_panel.blit(font_description.render('{}'.format(value['defend']), 1, white),
                          (320, 30 + index * 50))
        loss = player.life - Monster(0, 0, key).fight(player)
        if loss < 0:
            loss = '???'
        hand_book_panel.blit(font_description.render('{}'.format(loss), 1, white),
                          (380, 30 + index * 50))
        index += 1
