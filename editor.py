import sys

from pygame.constants import *

from configure import *
from magic_tower.util import to_real_coordinate
from magic_tower.modules import View, Button, message_manager, Mouse, EditorItem
from magic_tower.events import to_display_map, save_map, pop_load_panel


# 用于存储map数据，与configure中的格式一致，可以尝试一下使用default_dict
class Editor:
    def __init__(self, tower_map):
        self.tower_map = tower_map
        self.display_map = to_display_map(self.tower_map)


editor = Editor(default_tower_map)
mouse = Mouse()

pygame.init()
screen = View(32 * (16 + 7), 32 * 16, is_base=True)
controller_panel = View(32 * 7, 32 * 16, color=gray)
editor_panel = View(32 * 16, 32 * 16)
save_button = Button(save_map, 80, 40, params=(editor.display_map,), text="保存", color=white)
load_button = Button(pop_load_panel, 80, 40, text="加载", params=(screen, editor), color=white)

controller_panel.locate(0, 0, screen)
editor_panel.locate(32 * 7, 0, screen)


# 从配置当中读取可供添加的item
controller_map = {}
i = 1
j = 1
for key, value in item_dict.items():
    for item_number in value:
        controller_map[(i, j)] = EditorItem(key[0:-5], item_number, value)
        if i < 7:
            i += 1
        else:
            j += 1
            i = 1


if __name__ == '__main__':

    while True:
        save_button.locate(20, 32 * 14, controller_panel)
        load_button.locate(120, 32 * 14, controller_panel)

        # 绘制editor_panel上的元素
        for i in range(1, 17):
            for j in range(1, 17):
                editor_panel.blit(ground_image, to_real_coordinate(i, j, 32))
                if (i, j) in editor.display_map.keys():
                    value = editor.display_map[(i, j)]
                    button = Button(mouse.put, 32, 32, params=(editor.display_map, (i, j)), image=value.image)
                    button.locate(*to_real_coordinate(i, j, 32), editor_panel)
                else:
                    button = Button(mouse.put, 32, 32, params=(editor.display_map, (i, j)))
                    button.locate(*to_real_coordinate(i, j, 32), editor_panel)

        # 绘制controller_panel上的元素
        for key, value in controller_map.items():
            button = Button(mouse.load, 32, 32, (value,), image=value.image, color=gray)
            button.locate(*to_real_coordinate(*key, 32), controller_panel)

        # 所有的元素都统一渲染
        screen.render()

        # 绘制鼠标上的元素
        if mouse.is_on_mouse:
            print(pygame.mouse.get_pos())
            # 这个解包用得真pythonic
            screen.blit(mouse.item.image, (*pygame.mouse.get_pos(), 32, 32))

        # 打印消息
        if message_manager.message is not None:
            screen.blit(font_title.render(message_manager.message, 1, white), (300, 150))

        # 更新主界面
        pygame.display.update()

        # 事件触发器
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w and event.mod & KMOD_META:
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                screen.click(event.pos)
