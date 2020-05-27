#!/usr/bin/env python
#coding=utf-8

#from __future__ import print_function
import time
import os
import datetime

def chang_an_time():
    '''
    长安十二时辰
    '''
    h = int(time.strftime('%H'))  # hour
    # hour_chang_an 时辰
    str_hour = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥','子']
    quarter = ['--','[一刻]','[二刻]','[三刻]','[四刻]']
    hour_chang_an = str_hour[(h + 1) // 2]
    # cz 初）正）
    initial_exact = "正" if not h % 2 else "初"
    m = int(time.strftime('%M'))  # minute
    s = int(time.strftime('%S'))  # second
    a = 60.0 * float(m) + datetime.datetime.now().second   # 转换为秒
    c=time.time()-time.mktime(time.strptime(time.strftime('%Y %m %d %H:00:00'),'%Y %m %d %H:%M:%S'))
    # ke 刻 fe 分 ta 弹指
    # 1h = 4刻10分 = 250 分 = 3600s
    # 1分 = 40弹指 = 3600/250 s=14.4s
    # 1刻 = 60分 = 3600*60/250 s=864s=14.4m
    # 1弹指 = 3600/(250*40) s = 0.36s
    flip_chang_an = (c%14.4)/0.36 # 秒
    min_chang_an=int(c//14.4)  # 分
    q=min_chang_an//60
    print("%s%s%s%s分%f弹指" %(hour_chang_an, initial_exact,quarter[q], min_chang_an,flip_chang_an))
while True:
    chang_an_time()
    time.sleep(0.1)
    os.system('clear')
# print("haha")
# 1刻=60分;1分=40弹指
# 3600秒 = 250*40弹指; 1秒= 100/36弹指
# tips:
# print(int(100*a/36//40//60))
# 1刻=60分;1分=40弹指
# 3600秒 = 250*40弹指; 1秒= 100/36弹指
# print(int(100*a/36//40%60))
# print(int(100*a/36%60))
# 1刻=60分;1分=40弹指
# 1刻=60分;1分=40弹指
# 3600秒 = 250*40弹指; 1秒= 100/36弹指
# 1刻=60分;1分=40弹指
# 3600秒 = 250*40弹指; 1秒= 100/36弹指
# 3600秒 = 250*40弹指; 1秒= 100/36弹指
# 总弹指 = 总秒数*100/36
# "总弹指//40//60 刻
# "总弹指//40%60 分
# "总弹指%40 弹指
# float会造成弹指不标准;不可取
