import os
import sys
from decimal import Decimal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import AlgorithmEngine
import myAlgorithmEngine
from decimal import Decimal
import order
import computePath
import copy
def _init(): #初始化
    global _global_dict
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


def rainsert(idx1, idx2, driver, order1, instance, currentTimeOffset):
    # print(order1)
    # print(order1['startZoneID'])
    # print(instance['count'])
    # print(instance['NewMapData'])
    # print(instance['NewMapData'][order1['startZoneID']])
    # print(idx1, idx2)
    # print(driver['temp_route'])
    dis_ = computePath.dis(order1["startNodeID"], order1["endNodeID"], instance,
                                  instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                  instance['frequentPickup'], instance['frequentDrop'])
    # print("start")
    # print(instance['NewMapData'][order1['startZoneID']], instance['NewMapData'][order1['endZoneID']], dis_)
    requestTd = int(order1['startTime']) + int(instance['detour_factor']) * dis_
    # print("start")
    # print(requestTd)
    # print(driver['temp_route'])
    # print(driver['temp_route'])
    if idx1 == idx2:
        dis1 = computePath.dis(driver['temp_route'][idx1 - 1][0], order1["startNodeID"], instance,
                                  instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                  instance['frequentPickup'], instance['frequentDrop'])
        # print(driver['temp_route'][idx1 - 1][0], instance['NewMapData'][order1['startZoneID']], dis1)
        if len(driver['temp_route']) > idx1:
            dis2 = computePath.dis(order1["endNodeID"], driver['temp_route'][idx1][0], instance,
                                  instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                  instance['frequentPickup'], instance['frequentDrop'])
            # print(instance['NewMapData'][order1['endZoneID']], driver['temp_route'][idx1][0],dis2)
            detour = dis_ + dis2 + dis1 + driver['temp_route'][idx1 - 1][2] - driver['temp_route'][idx1][2]
            # print(detour)
            for num in range(idx1, len(driver['temp_route'])):
                driver['temp_route'][num][2] += detour
                driver['temp_route'][num][4] -= detour
            # print(driver['temp_route'])
        pick1 = driver['temp_route'][idx1 - 1][5]
        arr1 = driver['temp_route'][idx1 - 1][2]
        slack1 = requestTd - dis_ - arr1 - dis1
        # print(slack1)
        temp_route = {}
        temp0 = {}
        temp1 = {}
        temp0[0], temp0[1], temp0[2], temp0[3], temp0[4], temp0[5] = order1["startNodeID"], requestTd-dis_, arr1+dis1, order1['passengerCount'], slack1, pick1 + order1['passengerCount']
        temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5] = order1["endNodeID"], requestTd, arr1+dis1+dis_, order1['passengerCount'] * (-1), slack1, pick1
        t = 0
        for i in range(len(driver['temp_route'])):
            temp_route[t] = driver['temp_route'][i]
            t = t + 1
            if i+1 == idx1:
                temp_route[t] = temp0
                t = t + 1
                temp_route[t] = temp1
                t = t + 1

        driver['temp_route'] = temp_route
        # last_slack = driver['temp_route'][len(driver['temp_route'])-1][4]
        for num in range(len(driver['temp_route'])-2, 0, -1):
            last_slack = driver['temp_route'][len(driver['temp_route']) - 1][4]
            if last_slack > driver['temp_route'][num][4]:
                last_slack = driver['temp_route'][num][4]
            driver['temp_route'][num][4] = last_slack
        # print(driver['temp_route'])
    else:
        # instance['CHgraph'] = copy.deepcopy(instance['CHgraph1'])
        # if driver['temp_route'][idx1 - 1][0] in instance['cacheSD'] and \
        #         instance['NewMapData'][order1['startZoneID']] in instance['cacheSD'][driver['temp_route'][idx1 - 1][0]]:
        #     # cacheSD[l1][l2] = path
        #     instance['cacheSD'][driver['temp_route'][idx1 - 1][0]].pop(instance['NewMapData'][order1['startZoneID']])


        # result_dir = "../resources/raw_data/"
        # files = "ny_graph_h_j.json"
        # filePath = result_dir + files
        # with open(filePath, 'r', encoding='utf8') as fp:
        #     data['CHgraph'] = json.load(fp)
        #     if fp:
        #         fp.close()
        dis1 = computePath.dis(driver['temp_route'][idx1 - 1][0], order1["startNodeID"], instance,
                               instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                               instance['frequentPickup'], instance['frequentDrop'])
        # print(driver['temp_route'][idx1 - 1][0], instance['NewMapData'][order1['startZoneID']], dis1)
        dis2 = computePath.dis(order1["startNodeID"], driver['temp_route'][idx1][0], instance,
                               instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                               instance['frequentPickup'], instance['frequentDrop'])
        # print(instance['NewMapData'][order1['startZoneID']], driver['temp_route'][idx1][0], dis2)
        # dis1 = 50

        detour1 = dis2 + dis1 + driver['temp_route'][idx1 - 1][2] - driver['temp_route'][idx1][2]
        # print(detour1)
        for num in range(idx1, idx2, 1):
            # print(num)
            driver['temp_route'][num][2] += detour1
            driver['temp_route'][num][4] -= detour1
            driver['temp_route'][num][5] += order1['passengerCount']
        dis3 = computePath.dis(driver['temp_route'][idx2 - 1][0], order1["endNodeID"], instance,
                                  instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                  instance['frequentPickup'], instance['frequentDrop'])
        if len(driver['temp_route']) > idx2:
            dis4 = computePath.dis(order1["endNodeID"], driver['temp_route'][idx2][0], instance,
                                  instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                  instance['frequentPickup'], instance['frequentDrop'])
            detour2 = dis3 + dis4 + driver['temp_route'][idx2 - 1][2] - driver['temp_route'][idx2][2]
            for num in range(idx2, len(driver['temp_route']), 1):
                driver['temp_route'][num][2] += detour2
                driver['temp_route'][num][4] -= detour2
        arr1 = driver['temp_route'][idx1 - 1][2]
        pick1 = driver['temp_route'][idx1 - 1][5]
        arr2 = driver['temp_route'][idx2 - 1][2]
        pick2 = driver['temp_route'][idx2 - 1][5]
        slack2 = requestTd - arr2 - dis3

        temp_route = {}
        temp0 = {}
        temp1 = {}
        temp0[0], temp0[1], temp0[2], temp0[3], temp0[4], temp0[5] = order1["startNodeID"], requestTd - dis_, arr1 + dis1,\
                                                                     int(order1['passengerCount']), slack2, pick1 + order1['passengerCount']
        temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5] = order1["endNodeID"], requestTd, arr2 + dis3, \
                                                                     int(order1['passengerCount']) * (-1), slack2, pick2 - order1['passengerCount']
        t = 0
        for i in range(len(driver['temp_route'])):
            temp_route[t] = driver['temp_route'][i]
            t = t + 1
            if i+1 == idx1:
                temp_route[t] = temp0
                t = t + 1
            if i+1 == idx2:
                temp_route[t] = temp1
                t = t + 1
        driver['temp_route'] = temp_route
        # last_slack = driver['temp_route'][len(driver['temp_route']) - 1][4]
        for num in range(len(driver['temp_route']) - 2, 0, -1):
            last_slack = driver['temp_route'][len(driver['temp_route']) - 1][4]
            if last_slack > driver['temp_route'][num][4]:
                last_slack = driver['temp_route'][num][4]
            driver['temp_route'][num][4] = last_slack
    # print(driver['temp_route'])
    # print(driver['temp_route'])
    if idx1 == 1:
        if driver['temp_route'][0][0] == driver['temp_route'][1][0]:
            while driver['temp_route'][0][0] == driver['temp_route'][1][0]:
                for i in range(len(driver['temp_route'])-1):
                    driver['temp_route'][i] = driver['temp_route'][i+1]
                driver['temp_route'].pop(len(driver['temp_route'])-1)
                if len(driver['temp_route']) == 1:
                    if driver['temp_route'][0][2] < requestTd:
                        driver['temp_route'][0][1] = requestTd
                        driver['temp_route'][0][2] = requestTd
                    driver['temp_route'][0][4] = 6666
                    driver['temp_route'][0][5] = 0
                    driver['current_path'] = {}
                    return
        driver['current_path'] = {}
        current = computePath.current_loc(driver['temp_route'][0][0], driver['temp_route'][1][0], instance['cacheSP'], instance['graph'], instance['edges'],
                              instance['reverseGraph'], driver['temp_route'][0][2], currentTimeOffset,
                              driver['current_path'])
        # print(current)
        driver['temp_route'][0][0] = current[0]
        driver['temp_route'][0][1] = current[1]
        driver['temp_route'][0][2] = current[1]
        driver['temp_route'][0][3] = 0
        driver['temp_route'][0][4] = 6666
    for i in range(len(driver['temp_route'])):
        driver['temp_route'][i][4] = 6666
    # print(driver['temp_route'])


def serveOrder(driver, order1, currentTimeOffset, velocity, instance):

    if order.isAssigned(order1):
        print("Double Assign!")
    order.assignDriver(order1, driver)
    # print(driver['temp_route'])
    startTime = driver['temp_route'][len(driver['temp_route']) - 1][2]
    rainsert(1, 1, driver, order1, instance, currentTimeOffset)
    # print(driver['temp_route'])
    driver['currentZoneID'] = order1['endZoneID']
    driver['usedPassengerCount'] = order1['passengerCount']
    WaitTime = 0
    for i in range(len(driver['temp_route'])):
        if order1["startNodeID"] == driver['temp_route'][i][0]:
            WaitTime = driver['temp_route'][i][2] - order1['startTime']
            break
    set_value('TotalWaitTime', get_value('TotalWaitTime', 0) + WaitTime)
    driver['servingOrder'] = order1
    driver['orders'][len(driver['orders'])] = order1
    if len(driver['temp_route']) > 1:
        # print(driver['temp_route'][1][2] - driver['temp_route'][0][2])
        driver["serveTime"] = driver["serveTime"] + driver['temp_route'][len(driver['temp_route'])-1][2] - startTime
    else:
        driver["serveTime"] = driver["serveTime"] + order1['endTime'] - order1['startTime']
    driver["predictTimes"][len(driver["predictTimes"])] = driver['servingOrder']['idletime']
    if (driver['idleTime'] != 0):
        driver["actualTimes"][len(driver["actualTimes"])] = (currentTimeOffset - driver['idleTime'])
    if len(driver['temp_route']) > 1:
        driver['nextFreeTimeOffset'] = driver['temp_route'][len(driver['temp_route'])-1][2]
    else:
        driver['nextFreeTimeOffset'] = currentTimeOffset + (order1['endTime'] - order1['startTime'])
    # print(driver['nextFreeTimeOffset'])
    driver['currentTimeOffset'] = currentTimeOffset
    driver['idleTime'] = driver['nextFreeTimeOffset']

def serve2Order(driver, order1, currentTimeOffset, velocity, instance):
    if order.isAssigned(order1):
        print("Double Assign!")
        return 0
    usedPassengerMessage = {}
    order.assignDriver(order1, driver)
    startTime = driver['temp_route'][len(driver['temp_route'])-1][2]
    # print(2)
    # print(driver['temp_route'])
    rainsert(order1['insert_idx'][0], order1['insert_idx'][1], driver, order1, instance, currentTimeOffset)
    # print(driver['temp_route'])
    driver['usedPassengerCount'] = driver['usedPassengerCount'] + order1['passengerCount']
    usedPassengerMessage['passengerCount'] = driver['servingOrder']['passengerCount']

    driver['usedPassengerMessage'][len(driver['usedPassengerMessage'])] = usedPassengerMessage
    driver['orders'][len(driver['orders'])] = order1
    if driver["RealTime"] < order1['startTime']:
        WaitTime = 0
    else:
        WaitTime = driver['temp_route'][order1['insert_idx'][0]] - order1['startTime']

    set_value('TotalWaitTime', get_value('TotalWaitTime', 0) + WaitTime)

    driver['servingOrder'] = order1

    if len(driver['temp_route']) > 1:
        driver["serveTime"] = driver["serveTime"] + driver['temp_route'][len(driver['temp_route'])-1][2] - startTime
    else:
        driver["serveTime"] = driver["serveTime"] + order1['endTime'] - order1['startTime']
    driver["predictTimes"][len(driver["predictTimes"])] = driver['servingOrder']['idletime']
    if (driver['idleTime'] != 0):
        driver["actualTimes"][len(driver["actualTimes"])] = (currentTimeOffset - driver['idleTime'])
    if len(driver['temp_route']) > 1:
        driver['nextFreeTimeOffset'] = driver['temp_route'][len(driver['temp_route']) - 1][2]
    else:
        driver['nextFreeTimeOffset'] = currentTimeOffset + (order1['endTime'] - order1['startTime'])

    driver['idleTime'] = driver['nextFreeTimeOffset']
    driver['servingOrder'] = order1
    driver['currentZoneID'] = order1['endZoneID']



def serveOrder3(driver, order1, currentTimeOffset, velocity, instance):

    if order.isAssigned(order1):
        print("Double Assign!")
    usedPassengerMessage = {}
    order.assignDriver(order1, driver)

    startTime = driver['temp_route'][len(driver['temp_route']) - 1][2]
    # print(order1['insert_idx'][0], order1['insert_idx'][1])
    # print(driver['temp_route'])
    queryID = get_value('count', 0)
    # print(queryID)


    rainsert(order1['insert_idx'][0], order1['insert_idx'][1], driver, order1, instance, currentTimeOffset)
    # print(driver['temp_route'])
    driver['usedPassengerCount'] = order1['passengerCount'] + driver['usedPassengerCount']

    usedPassengerMessage['passengerCount'] = driver['servingOrder']['passengerCount']

    driver['usedPassengerMessage'][len(driver['usedPassengerMessage'])] = usedPassengerMessage
    #
    # print(order1['insert_idx'][0])
    # print(driver['temp_route'])
    # if driver["RealTime"] < order1['startTime']:
    #     WaitTime = 0
    # else:
    #     WaitTime = driver['temp_route'][order1['insert_idx'][0]] - order1['startTime']
    WaitTime = 0
    for i in range(len(driver['temp_route'])):
        if order1["startNodeID"] == driver['temp_route'][i][0]:
            WaitTime = driver['temp_route'][i][2] - order1['startTime']
            break

    set_value('TotalWaitTime', get_value('TotalWaitTime', 0) + WaitTime)

    driver['servingOrder'] = order1

    driver['orders'][len(driver['orders'])] = order1
    # if driver['temp_route'][len(driver['temp_route'])-1][2] - startTime < 0:
    #     print(driver['temp_route'][len(driver['temp_route'])-1][2], startTime)
    if len(driver['temp_route']) > 1:
        # if driver['temp_route'][len(driver['temp_route'])-1][2] - startTime < 0:
        #     driver["serveTime"] = driver["serveTime"] + 0
        # else:
        driver["serveTime"] = driver["serveTime"] + driver['temp_route'][len(driver['temp_route'])-1][2] - startTime
    else:
        driver["serveTime"] = driver["serveTime"] + order1['endTime'] - order1['startTime']


    driver["predictTimes"][len(driver["predictTimes"])] = driver['servingOrder']['idletime']
    if (driver['idleTime'] != 0):
        driver["actualTimes"][len(driver["actualTimes"])] = (currentTimeOffset - driver['idleTime'])


    if len(driver['temp_route']) > 1:
        driver['nextFreeTimeOffset'] = driver['temp_route'][len(driver['temp_route'])-1][2]
    else:
        driver['nextFreeTimeOffset'] = currentTimeOffset + (order1['endTime'] - order1['startTime'])


    driver['idleTime'] = driver['nextFreeTimeOffset']
    driver['servingOrder'] = order1
    driver['currentZoneID'] = order1['endZoneID']
