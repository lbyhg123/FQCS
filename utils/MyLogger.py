import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))
import ProblemInstance
import driver
# print(str(int(time.time())))
#
# print(time.localtime())
#
# print(time.strftime('%Y-%m-%d %H:%M:%S'))
#
result_dir = "../resources2/result/"
# s = 1
# filename = "data.txt"
# file = str(int(time.time())) + "_" + str(s) + "_" + filename
# # -*- coding: utf-8 -*-
# # 方法一：
# # "w"是写的权限，下文"r"是读的权限，"encoding"是写入或读取文档的编码方式
# file = open(result_dir + file, "w", encoding='utf-8')
# file.write('练习文本')
# file.close()
# # 方法二：
# with open(r"D:\python\test1\练习.txt", "w", encoding='utf-8')as f:
#     f.write('练习文本')
# # 方法一：
# file = open(r"D:\python\test1\练习.txt", "r", encoding='utf-8')
# text = file.readline()
# print(text)
# file.close()
# # 方法二：
# with open(r"D:\python\test1\练习.txt", "r", encoding='utf-8')as f:
#     text = f.readline()
#     print(text)

def MyLogger(filename, seed, day):
    files = str(int(time.time())) + "_" + str(seed) + "_" + str(day) + "_" + filename
    _init()
    set_value(0, files)
    # print(get_value(0))
    file = open(result_dir + files, "w", encoding='utf-8')
    # print(1)
    # file = open(r"../resources/result/练习.txt", "w", encoding='utf-8')
    # file.write('练习文本\n')
    # file.write('练习文本\n')
    file.close()
    # file = open(result_dir + files, "a", encoding='utf-8')
    # file.write(str(day) + "\n")
    # file.close()


def _init(): #初始化
    global  _global_dict
    _global_dict = {}
def set_value(key, value):
    #定义一个全局变量
    _global_dict[key] = value
def get_value(key, defValue=None):
    #获得全局变量，不存在则返回默认值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


def logResult(instance, algorithm):
    files = get_value(0)
    file = open(result_dir + files, "a", encoding='utf-8')
    # file = open(result_dir + files, "w", encoding='utf-8')
    servingTime = ProblemInstance.calculateTotalServingTime(instance['drivers1'])
    orderCount = ProblemInstance.calculateTotalAssignedOrderCount(instance['drivers1'])
    # TotalDistance = ProblemInstance.calculateTotalDistance(instance['drivers'])
    TotalDistance = 0
    template = str(instance['info']) + ",RunningTime:" + str(instance['endRunningMillis']-instance['startRunningMillis']) \
               + ",servingTime:" + str(servingTime) + ",orderCount:" + str(orderCount) + ",TotalDistance:" + str(TotalDistance) + "\n"
    file.write(template)
    print(template)
    template = "RealTotalDistance:" + str(driver.get_value('RealTotalDistance'))\
               + ",OracleTotalDistance:" + str(driver.get_value('OracleTotalDistance')) + \
               ",TotalWaitTime:" + str(driver.get_value('TotalWaitTime')) + "\n"
    # else:
    #     template = "RealTotalDistance:" + str(AlgorithmEngine.get_value(RealTotalDistance)) \
    #                + ",OracleTotalDistance:" + str(AlgorithmEngine.get_value(OracleTotalDistance)) + \
    #                ",TotalDistance:" + str(AlgorithmEngine.get_value(TotalDistance)) + "\n"

    file.write(template)
    print(template)
    # file.write('练习文本\n')
    # file.flush()
    # print(template)
    file.close()
if __name__ == '__main__':
    MyLogger("file.txt", 1)
    instance = 1
    algorithm = 2
    logResult(instance , algorithm)
    logResult(instance, algorithm)
    logResult(instance, algorithm)