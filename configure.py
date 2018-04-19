import pygame
import os

# 用于精准定位，避免由于打开位置的关系寻错路径
path = os.path.dirname(__file__)

pygame.init()

length = 32
number = 16
white = 255, 255, 255  # 白色
gray = 96, 96, 96  # 灰色
player_image_list = pygame.image.load(os.path.join(path, 'resource/Characters/Actor01-Braver01.png'))
wall_image_list = pygame.image.load(os.path.join(path, 'resource/Characters/Event01-Wall01.png'))
door_image_list = pygame.image.load(os.path.join(path, 'resource/Characters/Event01-Door01.png'))
downstairs_image = pygame.image.load(os.path.join(path, 'resource/down_floor.png'))
upstairs_image = pygame.image.load(os.path.join(path, 'resource/up_floor.png'))
yellow_key_image = pygame.image.load(os.path.join(path, 'resource/Icons/Item01-01_1_1.png'))
blue_key_image = pygame.image.load(os.path.join(path, 'resource/Icons/Item01-01_1_2.png'))
red_key_image = pygame.image.load(os.path.join(path, 'resource/Icons/Item01-01_1_3.png'))
weapon_image_list = pygame.image.load(os.path.join(path, 'resource/Characters/Item01-08.png'))
shoes_image = pygame.image.load(os.path.join(path, 'resource/Item02-04_4_1.png'))
monster_image1 = pygame.image.load(os.path.join(path, 'resource/Battlers/Actor02-Monster01_1_1.png'))
monster_image2 = pygame.image.load(os.path.join(path, 'resource/Battlers/Monster03-01_1_1.png'))
monster_image3 = pygame.image.load(os.path.join(path, 'resource/Battlers/Monster02-01_1_1.png'))
font_title = pygame.font.Font(os.path.join(path, 'resource/Fonts/PingFang.ttc'), 20)


def load_image(image_path):
    return pygame.image.load(os.path.join(path, image_path))


player_downs = [player_image_list.subsurface((0, 0, 32, 32)),
                player_image_list.subsurface((32, 0, 32, 32)),
                player_image_list.subsurface((64, 0, 32, 32)),
                player_image_list.subsurface((96, 0, 32, 32))]
player_lefts = [player_image_list.subsurface((0, 32, 32, 32)),
                player_image_list.subsurface((32, 32, 32, 32)),
                player_image_list.subsurface((64, 32, 32, 32)),
                player_image_list.subsurface((96, 32, 32, 32))]
player_rights = [player_image_list.subsurface((0, 64, 32, 32)),
                 player_image_list.subsurface((32, 64, 32, 32)),
                 player_image_list.subsurface((64, 64, 32, 32)),
                 player_image_list.subsurface((96, 64, 32, 32))]
player_ups = [player_image_list.subsurface((0, 96, 32, 32)),
              player_image_list.subsurface((32, 96, 32, 32)),
              player_image_list.subsurface((64, 96, 32, 32)),
              player_image_list.subsurface((96, 96, 32, 32))]
ground_image = wall_image_list.subsurface((64, 0, 32, 32))
wall_images = [wall_image_list.subsurface((32, 0, 32, 32)),
               wall_image_list.subsurface((32, 32, 32, 32)),
               wall_image_list.subsurface((32, 64, 32, 32)),
               wall_image_list.subsurface((32, 96, 32, 32))]
yellow_door_images = [door_image_list.subsurface((0, 0, 32, 32)),
                      door_image_list.subsurface((0, 32, 32, 32)),
                      door_image_list.subsurface((0, 64, 32, 32)),
                      door_image_list.subsurface((0, 96, 32, 32))]
blue_door_images = [door_image_list.subsurface((32, 0, 32, 32)),
                    door_image_list.subsurface((32, 32, 32, 32)),
                    door_image_list.subsurface((32, 64, 32, 32)),
                    door_image_list.subsurface((32, 96, 32, 32))]
red_door_images = [door_image_list.subsurface((64, 0, 32, 32)),
                   door_image_list.subsurface((64, 32, 32, 32)),
                   door_image_list.subsurface((64, 64, 32, 32)),
                   door_image_list.subsurface((64, 96, 32, 32))]
weapon_images = [weapon_image_list.subsurface((0, 0, 32, 32)),
                 weapon_image_list.subsurface((32, 0, 32, 32)),
                 weapon_image_list.subsurface((64, 0, 32, 32)),
                 weapon_image_list.subsurface((96, 0, 32, 32)),
                 weapon_image_list.subsurface((0, 32, 32, 32))]
shield_images = [weapon_image_list.subsurface((0, 64, 32, 32)),
                 weapon_image_list.subsurface((32, 64, 32, 32)),
                 weapon_image_list.subsurface((64, 64, 32, 32)),
                 weapon_image_list.subsurface((96, 64, 32, 32)),
                 weapon_image_list.subsurface((0, 96, 32, 32))]

stairs_dict = {
    '001': {
        'name': 'up',
        'image': upstairs_image,
    },
    '002': {
        'name': 'down',
        'image': downstairs_image,
    }
}

weapon_dict = {
    '001': {
        'name': '宝剑',
        'image': weapon_images[0],
        'attack': 10
    },
    '002': {
        'name': '大宝剑',
        'image': weapon_images[1],
        'attack': 20
    },
    '003': {
        'name': '炒鸡宝剑',
        'image': weapon_images[2],
        'attack': 30
    }
}


key_dict = {
    '001': {
        'name': '黄钥匙',
        'image': yellow_key_image,
    },
    '002': {
        'name': '蓝钥匙',
        'image': blue_key_image,
    },
    '003': {
        'name': '红钥匙',
        'image': red_key_image,
    }
}

door_dict = {
    '001': {
        'name': '黄门',
        'image': yellow_door_images[0],
        'images': yellow_door_images
    },
    '002': {
        'name': '蓝门',
        'image': blue_door_images[0],
        'images': blue_door_images
    },
    '003': {
        'name': '红门',
        'image': red_door_images[0],
        'images': red_door_images
    }
}

wall_dict = {
    '001': {
        'name': '普通墙',
        'image': wall_images[0],
        'images': wall_images
    }
}

monster_dict = {
    '001': {
        'name': '绿色史莱姆',
        'life': 20,
        'attack': 12,
        'defend': 0,
        'speed': 5,
        'image': monster_image1},
    '002': {
        'name': '小蝙蝠',
        'life': 30,
        'attack': 15,
        'defend': 2,
        'speed': 14,
        'image': monster_image2},
    '003': {
        'name': '骷髅怪',
        'life': 80,
        'attack': 20,
        'defend': 5,
        'speed': 8,
        'image': monster_image3}}

drug_dict = {
    '001': {
        'name': '生命药水',
        'heal': 50,
        'image': load_image('resource/Icons/Item01-02_1_1.png')},
    '002': {
        'name': '高级生命药水',
        'heal': 200,
        'image': load_image('resource/Icons/Item01-02_1_2.png')}}


gem_dict = {
    '001': {
        'name': '红宝石',
        'type': 'attack',
        'number': 2,
        'image': load_image('resource/Characters/Item01-Gem01.png').subsurface(0, 0, 32, 32)},
    '002': {
        'name': '蓝宝石',
        'type': 'defend',
        'number': 2,
        'image': load_image('resource/Characters/Item01-Gem01.png').subsurface(32, 0, 32, 32)}}

none_surface = pygame.Surface((32, 32))
none_surface.fill(white)

none_dict = {
    '001': {
        'name': '清除',
        'image': none_surface},
    }

item_dict = {
    'none_dict': none_dict,
    'wall_dict': wall_dict,
    'door_dict': door_dict,
    'stairs_dict': stairs_dict,
    'gem_dict': gem_dict,
    'drug_dict': drug_dict,
    'monster_dict': monster_dict,
    'key_dict': key_dict,
    'weapon_dict': weapon_dict
}

default_tower_map = {
    'walls': {
        '001': set()
    },
    'doors': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'keys': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'stairss': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'weapons': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'monsters': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'drugs': {
        '001': set(),
        '002': set(),
        '003': set()
    },
    'gems': {
        '001': set(),
        '002': set(),
        '003': set()
    }
    }