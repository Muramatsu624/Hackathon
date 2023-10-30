import random
import math
import time

def make_theme():
    # お題のリストを読み込み
    data_file = "theme_list.txt"
    f = open(data_file, 'r')
    theme_list = []
    for line in open(data_file, 'r', encoding="utf-8"):
        theme_list.append(line.strip("\n"))    

    # print(theme_list)

    # お題の中からランダムな要素を抽出
    ut = time.time()
    random.seed(int(ut))
    random_index = math.floor(random.random() * len(theme_list))

    # print(random_index)
    # print(theme_list[random_index])
    return theme_list[random_index]
    
#print(make_theme())


