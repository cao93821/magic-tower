import sys

from pygame.constants import *

from magic_tower.base import Controller, BattleMap, Tower, Player
from magic_tower.items import *
from magic_tower.util import to_real_coordinate
from tower_config import map1


pygame.init()
screen = pygame.display.set_mode((length * (number + 7), length * number))
controller_panel = screen.subsurface(0, 0, length * 7, length * number)
battle_panel = screen.subsurface(length * 7, 0, length * number, length * number)

name_panel = controller_panel.subsurface(0, 0, length * 7, length * 2)
display_panel = controller_panel.subsurface(0, length * 2, length * 7, length * 5)
player_panel = controller_panel.subsurface(0, length * 7, length * 7, length * 9)

font_description = pygame.font.Font(os.path.join(path, 'resource/Fonts/PingFang.ttc'), 13)
font_title = pygame.font.Font(os.path.join(path, 'resource/Fonts/PingFang.ttc'), 20)


# 初始化主角
player = Player()


# 初始化其他元素
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


all_map = [init_map(tower_map) for tower_map in [map1]]


# 加载所有元素
controller = Controller()

tower = Tower()

for tower_map in all_map:
    battle_map = BattleMap()
    tower.load_map(battle_map)
    for items in tower_map:
        for item in items:
            battle_map.load(item)
            controller.load(item)

tower.load(player, 'up')

# 图鉴控制
is_reading_book = False

# 开发模式
is_develop = False


def move(direction):
    if direction == "left":
        move_thread = threading.Thread(target=player.move_left)
    elif direction == 'right':
        move_thread = threading.Thread(target=player.move_right)
    elif direction == 'up':
        move_thread = threading.Thread(target=player.move_up)
    else:
        move_thread = threading.Thread(target=player.move_down)
    move_thread.start()


last_action = None


if __name__ == '__main__':

    while True:
        if not is_reading_book:
            # 绘制地板
            for i in range(16):
                for j in range(16):
                    battle_panel.blit(ground_image, to_real_coordinate(i + 1, j + 1, length))

            # 绘制元素
            render_lock.acquire()
            for coordinate, something in tower.battle_maps[tower.current_floor - 1].map.items():
                if not isinstance(something, Player):
                    battle_panel.blit(something.image, to_real_coordinate(coordinate[0], coordinate[1], length))
            render_lock.release()

            # 绘制人物
            battle_panel.blit(player.image, player.rect)

            if is_develop:
                for i in range(16):
                    for j in range(16):
                        battle_panel.blit(font_description.render('({},{})'.format(i + 1, j + 1), 1, white),
                                          to_real_coordinate(i + 1, j + 1, length))
        else:
            # 绘制图鉴
            battle_panel.fill(gray)
            battle_panel.blit(font_description.render('名称', 1, white), (80, 30))
            battle_panel.blit(font_description.render('生命值', 1, white), (140, 30))
            battle_panel.blit(font_description.render('攻击力', 1, white), (200, 30))
            battle_panel.blit(font_description.render('防御力', 1, white), (260, 30))
            battle_panel.blit(font_description.render('速度', 1, white), (320, 30))
            battle_panel.blit(font_description.render('预计损耗', 1, white), (380, 30))
            index = 1
            for key, value in monster_dict.items():
                battle_panel.blit(value['image'], (30, 30 + index * 50))
                battle_panel.blit(font_description.render('{}'.format(value['name']), 1, white),
                                  (80, 30 + index * 50))
                battle_panel.blit(font_description.render('{}'.format(value['life']), 1, white),
                                  (140, 30 + index * 50))
                battle_panel.blit(font_description.render('{}'.format(value['attack']), 1, white),
                                  (200, 30 + index * 50))
                battle_panel.blit(font_description.render('{}'.format(value['defend']), 1, white),
                                  (260, 30 + index * 50))
                battle_panel.blit(font_description.render('{}'.format(value['defend']), 1, white),
                                  (320, 30 + index * 50))
                loss = player.life - Monster(0, 0, key).fight(player)
                if loss < 0:
                    loss = '???'
                battle_panel.blit(font_description.render('{}'.format(loss), 1, white),
                                  (380, 30 + index * 50))
                index += 1

        # 绘制控制面板
        controller_panel.fill(white)
        display_panel.fill(gray)

        name_panel.blit(font_title.render('魔塔第{}层'.format(tower.current_floor), 1, gray), (10, 10))
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

        for i in range(len(controller.string_deque)):
            text = font_description.render(controller.string_deque[i], 1, white)
            display_panel.blit(text, (10, 10 + i * 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYUP:
                last_action = None
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w and event.mod & KMOD_META:
                    sys.exit()
                if event.key == K_p:
                    is_reading_book = not is_reading_book
                if not is_reading_book:
                    if event.key == K_UP:
                        move('up')
                        last_action = 'up'
                    if event.key == K_DOWN:
                        move('down')
                        last_action = 'down'
                    if event.key == K_RIGHT:
                        move('right')
                        last_action = 'right'
                    if event.key == K_LEFT:
                        move('left')
                        last_action = 'left'

        if last_action is not None:
            move(last_action)



