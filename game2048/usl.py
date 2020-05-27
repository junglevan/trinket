import os

from bll import GameCoreController


class GameView:
    def __init__(self):
        self.__manager = GameCoreController()


    def main(self):
        self.__manager.produce_random()
        self.__manager.produce_random()
        while True:

            self.__manager.display()
            item = input("[po] 上下左右，q退出")
            if item == "[":
                self.__up()
            elif item == "p":
                self.__down()
            elif item == "o":
                self.__left()
            elif item == "]":
                self.__right()
            elif item == "q":
                break
            else:
                pass

            if self.__manager.map == ["dead"]:
                break
            os.system("clear")

    def __up(self):
        self.__manager.square_merge_up()
        self.__manager.dead()

    def __down(self):
        self.__manager.square_merge_down()
        self.__manager.dead()
    def __left(self):
        self.__manager.square_merge_left()
        self.__manager.dead()
    def __right(self):
        self.__manager.square_merge_right()
        self.__manager.dead()

