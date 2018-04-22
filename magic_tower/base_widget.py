from collections import deque


# 控制器
class Controller:

    def __init__(self):
        self.route_map = {}

    def key_press(self, key):
        self.route_map[key]()

    def load(self, key):
        def decorator(f):
            self.route_map[key] = f
            return f
        return decorator


# 消息中心
class MessageCenter:

    def __init__(self):
        self.subscribe_list = []

    def publish(self, message):
        for subscriber in self.subscribe_list:
            subscriber.notify(message)

    def add_subscriber(self, subscriber):
        """

        :param subscriber: 订阅者需要实现notify方法
        :return:
        """
        self.subscribe_list.append(subscriber)

    def register(self, promulgator):
        """

        :param promulgator: 发布者
        :return:
        """
        promulgator.message_center = self


# 消息管理器
class MessageController:
    def __init__(self):
        self.string_deque = deque(('game start',), 7)

    def notify(self, string):
        self.string_deque.append(string)