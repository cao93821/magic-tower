from configure import white, font_title, gray
from magic_tower.util import is_in_rect
import pygame
import datetime


class MessageManager:
    """
    消息管理器类，用来发送全局消息
    """
    def __init__(self):
        self._message = None
        self.time = None

    @property
    def message(self):
        """
        从消息管理器中读取存储的消息
        :return:
        """
        if self.time is not None:
            if (datetime.datetime.now() - self.time).seconds > 1:
                self._message = None
        return self._message

    @message.setter
    def message(self, message):
        """
        向消息管理器发送一条消息
        :param message:
        :return:
        """
        self.time = datetime.datetime.now()
        self._message = message


class EditorItem:
    """
    编辑器实体对象
    """
    def __init__(self, item_type, item_number, data_dict):
        self.type = item_type
        self.number = item_number
        self.image = data_dict[item_number]['image']


class Mouse:
    """
    鼠标类，用来处理一些与鼠标拖动相关的操作
    """
    def __init__(self):
        self.is_on_mouse = False
        self.item = None

    def load(self, item):
        self.is_on_mouse = True
        self.item = item

    def put(self, display_map, coordinate):
        if self.is_on_mouse:
            display_map[coordinate] = self.item


# 创建一个消息管理器实体
message_manager = MessageManager()


class View:
    """
    视图类
    """
    def __init__(self, width, height, is_base=False, color=None):
        if is_base:
            self.surface = pygame.display.set_mode((width, height))
        else:
            self.surface = None
        self.x = 0
        self.y = 0
        self.rect = None

        self.width = width
        self.height = height
        self.module_list = []
        self.color = color
        self.image = None
        self.font = None
        self.text = None
        self.upper_view = None
        self.render_func = None

    def locate(self, x, y, view):
        if self.surface is not None:
            print('已经有了')
        self.x = x
        self.y = y
        self.upper_view = view
        self.rect = (x, y, self.width, self.height)
        self.surface = view.surface.subsurface(self.rect)
        view.module_list.append(self)

    def fill(self, color=white):
        self.surface.fill(color)

    def blit(self, *args):
        self.surface.blit(*args)

    def click(self, pos):
        """
        寻址算法
        算法原理：遍历该view层的module_list，找到pos的落点，如果落点为button，则触发，如果落点为view，则进入下一层遍历，反之则break
        :param pos:
        :return:
        """
        module_list = self.module_list
        relative_pos = pos
        while module_list:
            # 导致module_list以实现覆盖
            for overridable_module in reversed(module_list):
                if is_in_rect(overridable_module.rect, relative_pos):
                    if isinstance(overridable_module, View):
                        # 如果是落点为View，则进行下一层遍历
                        module_list = overridable_module.module_list
                        relative_pos = (pos[0] - overridable_module.x, pos[1] - overridable_module.y)
                        break
                    if isinstance(overridable_module, Button):
                        # 如果落点为Button，则触发Button
                        overridable_module.press()
                        module_list = []
                        break
            else:
                break

    def load(self, render_func):
        """
        装载渲染函数
        :param render_func:
        :return:
        """
        self.render_func = render_func

    def render(self):
        """
        渲染算法
        :return:
        """
        if self.color:
            self.surface.fill(self.color)
        if self.image:
            self.surface.blit(self.image, (0, 0))
        if self.text:
            self.surface.blit(self.font.render(self.text, 1, gray), (20, 5))
        # self.render_func(self)
        module_list = self.module_list
        for overridable_module in module_list:
            overridable_module.render()

    def delete(self):
        self.upper_view.module_list.remove(self)


class Button:
    """
    按钮类
    """
    def __init__(self, task, width, height, params=(), color=None, font=font_title, text=None, image=None):
        self.x = 0
        self.y = 0
        self.cover = True
        self.task = task
        self.params = params
        self.text = text
        self.image = image
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.rect = None
        self.surface = None

    def locate(self, x, y, view):
        self.rect = (x, y, self.width, self.height)
        self.surface = view.surface.subsurface(self.rect)
        view.module_list.append(self)

    def render(self):
        if self.color:
            self.surface.fill(self.color)
        if self.image:
            self.surface.blit(self.image, (0, 0))
        if self.text:
            self.surface.blit(self.font.render(self.text, 1, gray), (20, 5))  # 怎么居中排放呢？

    def press(self):
        self.task(*self.params)


