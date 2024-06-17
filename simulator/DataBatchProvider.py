from decimal import Decimal
import copy
import os
import sys
import json
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import computePath
import order

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


def dict_slice(adict, start, end):
    dict_slice = {}
    len = end-start
    for i in range(len):
        dict_slice[i] = adict[i+start]
    return dict_slice

def fetchCurrentRoundDrivers(drivers, currentTimeOffset, cacheSP, graph, reverseGraph, edges, instance):
    CurrentDrivers = {}
    j = 0
    # print(drivers[1]['nextFreeTimeOffset'])
    # print(currentTimeOffset)
    for i in range(len(drivers)):
        if(drivers[i]['nextFreeTimeOffset'] <= currentTimeOffset):
            updata(currentTimeOffset, drivers[i], False, cacheSP, graph, reverseGraph, edges, instance)
            drivers[i]['point'] = 0
            drivers[i]['used'] = 0
            CurrentDrivers[j] = drivers[i]
            j = j + 1
    return CurrentDrivers
# cacheSP, graph, reverseGraph, start_time, current_time
def updata(currentTimeOffset, driver, flag, cacheSP, graph, reverseGraph, edges, instance):
    # 没有乘客的时候，仅更新时间
    # passengerCount = 0
    if len(driver['temp_route']) == 1:
        if driver['temp_route'][0][2] < currentTimeOffset:
            driver['temp_route'][0][1] = currentTimeOffset
            driver['temp_route'][0][2] = currentTimeOffset
        driver['temp_route'][0][4] = 6666
        driver['temp_route'][0][5] = 0
    else:
        if driver['temp_route'][1][2] > currentTimeOffset and driver['temp_route'][0][0] != driver['temp_route'][1][0]:
            if driver['current_path'][len(driver['current_path'])-1][1] < currentTimeOffset:
                if len(driver['temp_route']) == 1:
                    driver['temp_route'].pop(0)
                else:
                    for i in range(len(driver['temp_route'])-1):
                        driver['temp_route'][i] = driver['temp_route'][i+1]
                    driver['temp_route'].pop(len(driver['temp_route'])-1)
                if len(driver['temp_route']) != 1:
                    # 下个点与当前点在同一个位置
                    while driver['temp_route'][0][0] == driver['temp_route'][1][0]:
                        passengerCount = driver['temp_route'][0][5]
                        if len(driver['temp_route']) == 1:
                            driver['temp_route'].pop(0)
                        else:
                            for i in range(len(driver['temp_route']) - 1):
                                driver['temp_route'][i] = driver['temp_route'][i + 1]
                            driver['temp_route'].pop(len(driver['temp_route'])-1)
                        if len(driver['temp_route']) == 1:
                            break
                if len(driver['temp_route']) == 1:
                    if driver['temp_route'][0][2] < currentTimeOffset:
                        driver['temp_route'][0][1] = currentTimeOffset
                        driver['temp_route'][0][2] = currentTimeOffset
                    driver['temp_route'][0][4] = 6666
                    driver['temp_route'][0][5] = 0
                    driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
                    return
                driver['current_path'] = {}
                current = computePath.current_loc(driver['temp_route'][0][0], driver['temp_route'][1][0], cacheSP, graph, edges, reverseGraph, driver['temp_route'][0][2], currentTimeOffset, driver['current_path'])
                driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
                return
            else:
                if driver['current_path'][0][1] < currentTimeOffset:
                    while driver['current_path'][0][1] < currentTimeOffset:
                        if len(driver['current_path']) == 1:
                            driver['current_path'].pop(0)
                        else:
                            for i in range(len(driver['current_path']) - 1):
                                driver['current_path'][i] = driver['current_path'][i + 1]
                            driver['current_path'].pop(len(driver['current_path'])-1)
                    driver['temp_route'][0][0] = driver['current_path'][0][0]
                    driver['temp_route'][0][1] = driver['current_path'][0][1]
                    driver['temp_route'][0][2] = driver['current_path'][0][1]
                    driver['temp_route'][0][3] = 0
                    driver['temp_route'][0][4] = 6666
                    # driver['temp_route'][0][5] = 0
                    driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
                    return
        while driver['temp_route'][1][2] <= currentTimeOffset:
            if len(driver['temp_route']) == 1:
                driver['temp_route'].pop(0)
            else:
                for i in range(len(driver['temp_route']) - 1):
                    driver['temp_route'][i] = driver['temp_route'][i + 1]
                driver['temp_route'].pop(len(driver['temp_route']) - 1)
            if len(driver['temp_route']) == 1:
                if driver['temp_route'][0][2] < currentTimeOffset:
                    driver['temp_route'][0][1] = currentTimeOffset
                    driver['temp_route'][0][2] = currentTimeOffset
                driver['temp_route'][0][3] = 0
                driver['temp_route'][0][4] = 6666
                driver['temp_route'][0][5] = 0
                driver['current_path'] = {}
                break
        if len(driver['temp_route']) != 1:
            while driver['temp_route'][0][0] == driver['temp_route'][1][0]:
                if len(driver['temp_route']) == 1:
                    driver['temp_route'].pop(0)
                else:
                    for i in range(len(driver['temp_route']) - 1):
                        driver['temp_route'][i] = driver['temp_route'][i + 1]
                    driver['temp_route'].pop(len(driver['temp_route']) - 1)
                if len(driver['temp_route']) == 1:
                    if driver['temp_route'][0][2] < currentTimeOffset:
                        driver['temp_route'][0][1] = currentTimeOffset
                        driver['temp_route'][0][2] = currentTimeOffset
                    driver['temp_route'][0][3] = 0
                    driver['temp_route'][0][4] = 6666
                    driver['temp_route'][0][5] = 0
                    driver['current_path'] = {}
                    driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
                    return
            driver['current_path'] = {}
            temp = {}
            temp = computePath.current_loc(driver['temp_route'][0][0], driver['temp_route'][1][0], cacheSP, graph, edges, reverseGraph, driver['temp_route'][0][2], currentTimeOffset, driver['current_path'])
            if temp!= None:
                driver['temp_route'][0][0] = temp[0]
                driver['temp_route'][0][1] = temp[1]
                driver['temp_route'][0][2] = temp[1]
                driver['temp_route'][0][3] = 0
                driver['temp_route'][0][4] = 6666
            else:
                if len(driver['temp_route']) == 1:
                    driver['temp_route'].pop(0)
                else:
                    for i in range(len(driver['temp_route']) - 1):
                        driver['temp_route'][i] = driver['temp_route'][i + 1]
                    driver['temp_route'].pop(len(driver['temp_route']) - 1)
                if len(driver['temp_route']) != 1:
                    while driver['temp_route'][0][0] == driver['temp_route'][1][0]:
                        if len(driver['temp_route']) == 1:
                            driver['temp_route'].pop(0)
                        else:
                            for i in range(len(driver['temp_route']) - 1):
                                driver['temp_route'][i] = driver['temp_route'][i + 1]
                            driver['temp_route'].pop(len(driver['temp_route']) - 1)
                        if len(driver['temp_route']) == 1:
                            break
                if len(driver['temp_route']) == 1:
                    if driver['temp_route'][0][2] < currentTimeOffset:
                        driver['temp_route'][0][1] = currentTimeOffset
                        driver['temp_route'][0][2] = currentTimeOffset
                    driver['temp_route'][0][4] = 6666
                    driver['temp_route'][0][5] = 0
                    driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
                    return
                driver['current_path'] = {}
                current = computePath.current_loc(driver['temp_route'][0][0], driver['temp_route'][1][0], cacheSP, graph, edges,
                                      reverseGraph, driver['temp_route'][0][2], currentTimeOffset,
                                      driver['current_path'])
        else:
            if driver['temp_route'][0][2] < currentTimeOffset:
                driver['temp_route'][0][1] = currentTimeOffset
                driver['temp_route'][0][2] = currentTimeOffset
            driver['temp_route'][0][3] = 0
            driver['temp_route'][0][4] = 6666
            driver['temp_route'][0][5] = 0
            driver['current_path'] = {}
    driver["currentZoneID"] = instance['node2region'][driver['temp_route'][0][0]]
    # print(driver["currentZoneID"])

def fetchSecondDrivers(drivers, currentTimeOffset, lastTimeOffset, cacheSP, graph, reverseGraph, edges, instance):
    CurrentDrivers = {}
    j = 0
    for i in range(len(drivers)):
        if drivers[i]['nextFreeTimeOffset'] > currentTimeOffset:
            # print(drivers[i]['temp_route'])
            updata(currentTimeOffset, drivers[i], False, cacheSP, graph, reverseGraph, edges, instance)
            # print(drivers[i]['temp_route'])
            if len(drivers[i]['temp_route']) > 1:
                drivers[i]['used'] = 0
                CurrentDrivers[j] = drivers[i]
                j = j+1
    return CurrentDrivers

def fetchCurrentRoundOrders(orders, currentTimeOffset, currentOrderIndex):
    CurrentOrders = {}
    j = 0
    t = dict_slice(orders, currentOrderIndex, len(orders))
    # print(t[0]['id'])
    # print(t[0]['startTime'])
    for i in range(len(t)):
        if order.isAssigned(t[i]):
            continue
        if t[i]['startTime'] <= currentTimeOffset and currentTimeOffset-15 <= t[i]['startTime']:
        # if t[i]['startTime'] <= currentTimeOffset:
            CurrentOrders[j] = t[i]
            j = j + 1
            currentOrderIndex = currentOrderIndex + 1
            currentOrderIndexSum('currentOrderIndex', 1)
    # print("currentOrderIndex:")
    # print(get_value('currentOrderIndex'))
    # print(len(CurrentOrders))
    return CurrentOrders

def currentOrderIndexSum(key, value):
    _global_dict[key] += value

def slideToNextRound(key, frameLength):
    _global_dict[key] += frameLength
    # currentTimeOffset + frameLength

def fetchCurrentProblemInstance(tmp_data, frameLength, need):
    # print(get_value('currentTimeOffset'))
    # print(len(tmp_data['orders']))
    # print(tmp_data['orders'][len(tmp_data['orders'])-1]['startTime'])
    if get_value('currentTimeOffset') > tmp_data['orders'][len(tmp_data['orders'])-1]['startTime']:
        return {}

    # if get_value('currentTimeOffset') < 24000:
    #     slideToNextRound('currentTimeOffset', 1000)
    # # print(get_value('currentOrderIndex'))
    data = {}

    # print("starts:" , len(tmp_data['drivers']))



    if get_value('currentTimeOffset') < 20000:
        slideToNextRound('currentTimeOffset', 20000)

    if get_value('currentTimeOffset') > 20000 and get_value('currentTimeOffset') < 25000:
        slideToNextRound('currentTimeOffset', 1000)

    if get_value('currentTimeOffset') > 25000 and get_value('currentTimeOffset') < 25200:
        slideToNextRound('currentTimeOffset', 100)
    # print(get_value('currentOrderIndex'))

    data['orders'] = fetchCurrentRoundOrders(tmp_data['orders'], get_value('currentTimeOffset'),
                                             get_value('currentOrderIndex'))
    # print(len(data['orders']))
    data['drivers1'] = tmp_data['drivers1']
    if data['orders'] == {}:
        data['secondDrivers'] = {}
        data['drivers'] = {}
    else:
        if get_value('currentTimeOffset') != 0:
            data['secondDrivers'] = fetchSecondDrivers(tmp_data['drivers1'], get_value('currentTimeOffset'), tmp_data['currentTimeOffset'], tmp_data['cacheSP'], tmp_data['graph'], tmp_data['reverseGraph'], tmp_data['edges'], tmp_data)
        else:
            data['secondDrivers'] = {}
        # print(len(data['secondDrivers']))
        data['drivers'] = fetchCurrentRoundDrivers(tmp_data['drivers1'], get_value('currentTimeOffset'), tmp_data['cacheSP'], tmp_data['graph'], tmp_data['reverseGraph'], tmp_data['edges'], tmp_data)
    # print(len(data['drivers1']))
    # print(len())
    # print(data['drivers1'][0]['temp_route'])
    # print(data['drivers'][0]['temp_route'])
    # data['orders'] = fetchCurrentRoundOrders(tmp_data['orders'], get_value('currentTimeOffset'), get_value('currentOrderIndex'))
    data['currentTimeOffset'] = get_value('currentTimeOffset')
    data['taxiWatchdog'] = tmp_data['taxiWatchdog']
    data['orderOracle'] = tmp_data['orderOracle']
    data['orderReal'] = tmp_data['orderReal']
    # data['mapZone'] = tmp_data['mapZone']
    # data['zoneToZone'] = tmp_data['zoneToZone']
    data['velocity'] = tmp_data['velocity']

    data['cacheSD'] = tmp_data['cacheSD']
    data['cacheSP'] = tmp_data['cacheSP']
    data['graph'] = tmp_data['graph']
    data['reverseGraph'] = tmp_data['reverseGraph']
    data['edges'] = tmp_data['edges']
    data['ny_location'] = tmp_data['ny_location']
    data['distanceFrequentNodes'] = tmp_data['distanceFrequentNodes']
    data['frequentPickup'] = tmp_data['frequentPickup']
    data['frequentDrop'] = tmp_data['frequentDrop']
    data['CHgraph1'] = tmp_data['CHgraph1']
    # data['NewMapData'] = tmp_data['NewMapData']
    # data['NewMapData2'] = tmp_data['NewMapData2']
    data['count'] = tmp_data['count']
    data['node2region'] = tmp_data['node2region']
    data['time_list'] = tmp_data['time_list']
    data['CHgraph'] = tmp_data['CHgraph']
    if need == 1:
        data['NodeRange'] = tmp_data['NodeRange']
        data['NodeRangeNode'] = tmp_data['NodeRangeNode']
    # result_dir = "../resources/raw_data/"
    # files = "ny_graph_h_j.json"
    # filePath = result_dir + files
    # with open(filePath, 'r', encoding='utf8') as fp:
    #     data['CHgraph'] = json.load(fp)
    #     if fp:
    #         fp.close()

    slideToNextRound('currentTimeOffset', frameLength)
    # print("---------------------")
    return data