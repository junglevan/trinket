'''
创建游戏核心类GameCoreController，将核心算法作为实例成员
1测试上下左右移动是否正常
2计算所有空位置 随机产生数字 90% 2 10% 4
3结束除非有空位置或者能merge不能结束
'''
import random

from model import Location


class GameCoreController:
    def __init__(self, list_zero=[]):
        self.__map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]  # 分装起来，只读
        self.__list_merge = None
        self.__list_zero = list_zero  # 减少产生，建议做成实例变量

    @property
    def map(self):
        return self.__map

    def display(self):
        for item in self.__map:
            print(item)

    # 2020->2200
    def move_zero_left(self):
        for i in range(len(self.__list_merge) - 1, -1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    # 0422->4400
    def __merge(self):
        self.move_zero_left()
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] *= 2
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)

    def square_merge_left(self):
        map2 = eval(self.__map.__repr__())
        for line in self.__map: #传入可变对象，可以修改 line和map都是可变对象
            self.__list_merge = line#a = 对象b c = a ->c = 对象b
            self.__merge()

        if map2 != self.__map:
            self.produce_random()
        return self.__map

    def produce_random(self):
        for r in range(4):
            for c in range(4):
                if self.__map[r][c] == 0:
                    self.__list_zero.append(Location(r, c))  # 分装数据 可读性强
        if len(self.__list_zero) == 0: return
        loc = random.choice(self.__list_zero)
        self.map[loc.r][loc.c] = self.create_random_number()
        self.__list_zero=[]

    def create_random_number(self):
        return 4 if random.randint(1, 10) == 10 else 2

    # right:map-convert-square-convert
    def square_merge_right(self):
        for items in self.__map:
            for c in range(2):
                items[c], items[3 - c] \
                    = items[3 - c], items[c]
        self.square_merge_left()
        for items in self.__map:
            for c in range(2):
                items[c], items[3 - c] \
                    = items[3 - c], items[c]
        return self.__map

    # up:map-convert-square-convert (\)
    def square_merge_up(self):
        for r in range(1, 4):
            for c in range(r):
                self.__map[r][c], self.__map[c][r] \
                    = self.__map[c][r], self.__map[r][c]
        self.square_merge_left()
        for r in range(1, 4):
            for c in range(r):
                self.__map[r][c], self.__map[c][r] \
                    = self.__map[c][r], self.__map[r][c]
        return self.__map

    # down:map-convert-square-convert (/)
    def square_merge_down(self):
        for r in range(3):
            for c in range(4 - r):
                self.__map[r][c], self.__map[3 - c][3 - r] \
                    = self.__map[3 - c][3 - r], self.__map[r][c]
        self.square_merge_left()
        for r in range(3):
            for c in range(4 - r):
                self.__map[r][c], self.__map[3 - c][3 - r] \
                    = self.__map[3 - c][3 - r], self.__map[r][c]
        return self.__map

    def dead(self):
        map1 = eval(self.__map.__repr__())
        if \
                self.square_merge_down() == map1 and \
                        self.square_merge_up() == map1 and \
                        self.square_merge_right() == map1 and \
                        self.square_merge_left() == map1:
            print("dead")
            self.__map = ["dead"]

        else:
            self.__map = map1



