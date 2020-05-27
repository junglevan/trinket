'''
正整数的拆分 顺序无意义 默认数值从大到小 如5拆成 4-1 3-2 3-1-1 2-2-1 2-1-1-1 1-1-1-1-1
'''
import copy
from tkinter import _flatten
import sys

def Integersplit(interger):
    matri = [interger]
    egg = [matri]
    target_matrix=copy.deepcopy(matri)
    target_egg = [target_matrix]
    splity(matri,egg, target_egg)
    print(target_egg)
    print('总计数:',len(target_egg))


def splity(matri,egg, target_egg):
    integer = matri[0]
    if integer <= 1:
        return
    if integer > 1:
        for baby_integer in range(1, integer):
            matri.clear()
            matri.append(integer - baby_integer)
            matri.append([baby_integer]) # matri:[4]->[3,[1]] egg:[[4]]->[[3,[1]]]
            flat_egg = list(_flatten(egg)) #->[3,1]
            signal = True
            for index in range(len(flat_egg) - 1):
                if flat_egg[index] < flat_egg[index + 1]:
                    signal = False
                    break
            if signal:
                target_egg.append(flat_egg) #[[4],[3,1]]
            matri_to_right=matri[-1]
            splity(matri_to_right,egg, target_egg) #...
while True:
    try:
        n=int(sys.stdin.readline())
        Integersplit(n)
    except:
        break