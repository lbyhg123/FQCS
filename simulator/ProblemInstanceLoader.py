import sys
import os
import numpy as np
import json
from decimal import Decimal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import TxtParser
import TaxiDemandSupplyOracle
import time


def dict_slice(adict, start, end):
    dict_slice = {}
    len = end-start
    for i in range(len):
        dict_slice[i] = adict[i+start]
    # keys = adict.keys()
    # dict_slice = {}
    # for k in list(keys)[start:end]:
    #     dict_slice[k] = adict[k]
    # print(dict_slice[0])
    return dict_slice

def calOrder(orders):
    fileName4 = '../resources/result3/zoneToZone.txt'
    file4 = open(fileName4, "r", encoding='utf-8')
    file4lines = file4.readlines()
    zoneToZone = {}
    for i in range(1, 268):
        zoneToZone[i] = {}
        for j in range(1, 267):
            zoneToZone[i][j] = {}
    for i in range(len(file4lines)):
        t = file4lines[i].split(',')
        x = {}
        x['time'] = Decimal(t[2])
        x['tripLength'] = Decimal(t[3])
        x['cost'] = Decimal(t[4])
        x['number'] = Decimal(t[5])
        zoneToZone[int(t[0])][int(t[1])] = x

    return zoneToZone, 4.444335233880015


def order_fromString(id, x):
    order = {}
    x_list = x.split("]")[0].split(',')
    # print(x_list)
    if len(x_list) <= 1:
        return null
    order["id"] = id
    order["startZoneID"] = int(x_list[5])
    order["endZoneID"] = int(x_list[6])
    order["startNodeID"] = int(x_list[1])
    order["endNodeID"] = int(x_list[2])
    order['passengerCount'] = 1
    order["startTime"] = int(x_list[0])
    order["endTime"] = int(x_list[7])
    order["maxWaitTime"] = int(x_list[4])
    order["driver"] = {}
    order["insert_idx"] = {}
    order["idletime"] = 0
    order["dist"] = -1
    order["idleRatio"] = 0
    # print(order)
    return order

def loadBaseOrdersByDay(day):
    objectClass = "order"
    result_dir = "../resources2/raw_data/"
    # result_dir = "../resources/raw_data/"
    filePath = result_dir + "ny_Task" + str(day) + ".json"

    NewMapData = {}
    # orders = TxtParser.readFromFile(objectClass, filePath, NewMapData)
    file = open(filePath, "r", encoding='utf-8')
    # r = file.readline()
    # 读取多行
    r = file.readlines()
    r = r[0].split('[')
    print(r[2])
    print(r[3])
    xs = {}
    for i in range(2, len(r)):
        x = order_fromString(i, r[i])
        if x != {}:
            xs[len(xs)] = x
    print(len(xs))
    return xs

def loadBaseDriversByCount(driverCount, orders):
    np.random.seed()
    # start = np.random.randint(0, len(orders)-driverCount)
    start = 100000
    # np.random.seed(seed)
    print(start)
    drivers = {}
    for i in range(start, start+driverCount):
        driver = {}
        driver["id"] = i - start
        driver["curPos_lng"] = Decimal(0)
        driver["curPos_lat"] = Decimal(0)
        driver["curPos_time"] = Decimal(0)
        driver["nextFreeTimeOffset"] = Decimal(0)
        driver["currentZoneID"] = int(orders[i]['startZoneID'])
        driver["RealCurrentZoneID"] = {}
        driver["CurrentZoneIdToDestinationInstance"] = {}
        driver['point'] = int(0)
        driver["RealTime"] = Decimal(0)
        driver['crossZone'] = {}
        temp_loc = {}
        temp_loc[0] = int(orders[i]['startNodeID'])
        temp_loc[1] = Decimal(-10)
        temp_loc[2] = -10
        temp_loc[3] = 0
        temp_loc[4] = 6666
        temp_loc[5] = 0
        driver['temp_route'] = {}
        driver['temp_route'][len(driver['temp_route'])] = temp_loc
        driver['current_path'] = {}
        driver['passengerCount'] = 3
        driver['usedPassengerCount'] = 0

        if driver["currentZoneID"] >= 400:
            driver["currentZoneID"] = 41
        driver["servingOrder"] = {}
        driver['usedPassengerMessage'] = {}
        driver["orders"] = {}
        driver["predictTimes"] = {}
        driver["actualTimes"] = {}
        # driver["actualTimes"] = {}
        driver["idleTime"] = Decimal(0)
        driver["serveTime"] = Decimal(0)
        drivers[len(drivers)] = driver
    # t = drivers[1]
    # drivers[1] = drivers[0]
    # drivers[0] = t
    # t= {}
    # for i in range(len(drivers)):
    #     j = np.random.randint(0, len(drivers), size=1)
    #     j = int(j)
    #     t[i] = j
    #     driver = drivers[i]
    #     drivers[i] = drivers[j]
    #     drivers[j] = driver
    print(drivers[0])
    print(len(drivers))
    return drivers

def loadTaxiDemandOracle(day, fileName):
    objectClass = "Oracle"
    result_dir = "../resources2/raw_data/"
    filePath = result_dir + fileName
    NewMapData = {}
    zoneDemandTables = TxtParser.readFromFile(objectClass, filePath, NewMapData)
    # print("test2")
    # print(zoneDemandTables[1][211])
    # print(zoneDemandTables[2][211])
    # print(zoneDemandTables[3][211])
    # print(zoneDemandTables[1][210])
    # print(zoneDemandTables[2][210])
    # print(zoneDemandTables[3][210])
    # print(zoneDemandTables[1][212])
    # print(zoneDemandTables[2][212])
    # print(zoneDemandTables[3][212])
    # print("start")
    # print(zoneDemandTables[0])
    frameTime = 30*60
    beginTimeOffset = (day-1)*24*60*60
    endTimeOffset = day * 24 * 60 * 60
    beginIndex = beginTimeOffset/frameTime
    endIndex = endTimeOffset/frameTime
    # print("endIndex")
    # print(endIndex-beginIndex)
    t = dict_slice(zoneDemandTables, int(beginIndex), int(endIndex))
    # print("test3")
    # print(t[1][210])
    # print(t[2][210])
    # print(t[3][210])
    oracle = {}
    oracle = t
    # oracle['frameTime'] = frameTime
    # print(oracle['zoneDemandTables'][0])
    # print(zxc)
    # print(oracle[0])
    return oracle

def loadgraph():
    result_dir = "../resources2/raw_data/"
    files = "ny_graph_o_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        graph = json.load(fp)
        print('这是文件中的json数据：', graph[1])
        print('这是读取到文件数据的数据类型：', type(graph))
    return graph




def loadreverseGraph():
    result_dir = "../resources2/raw_data/"
    files = "ny_graph_r_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        reverseGraph = json.load(fp)
        print('这是文件中的json数据：', reverseGraph[1])
        print('这是读取到文件数据的数据类型：', type(reverseGraph))
    return reverseGraph

def loadedges():
    result_dir = "../resources2/raw_data/"
    files = "ny_edges_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        edges = json.load(fp)
        print('这是文件中的json数据：', edges[str(1)])
        print('这是读取到文件数据的数据类型：', type(edges))
    return edges

def loaddistanceFrequentNodes():
    result_dir = "../resources2/raw_data/"
    files = "ny_fre_dis.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        distanceFrequentNodes = json.load(fp)
        print(len(distanceFrequentNodes))
        print('这是文件中的json数据：', distanceFrequentNodes[str(4097)])
        print('这是读取到文件数据的数据类型：', type(distanceFrequentNodes))
    return distanceFrequentNodes


def loadpathFrequentNodes():
    result_dir = "../resources2/raw_data/"
    files = "ny_fre_path.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        pathFrequentNodes = json.load(fp)
        print(len(pathFrequentNodes))
        print('这是文件中的json数据：', pathFrequentNodes[str(4097)])
        print('这是读取到文件数据的数据类型：', type(pathFrequentNodes))
    return pathFrequentNodes

def loadfrequentPickup():
    result_dir = "../resources2/raw_data/"
    files = "ny_fre_pick.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        frequentPickup = json.load(fp)
        print(len(frequentPickup))
        print('这是文件中的json数据：', frequentPickup[1])
        print('这是读取到文件数据的数据类型：', type(frequentPickup))
    return frequentPickup

def loadfrequentDrop():
    result_dir = "../resources2/raw_data/"
    files = "ny_fre_drop.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        frequentDrop = json.load(fp)
        print(len(frequentDrop))
        print('这是文件中的json数据：', frequentDrop[1])
        print('这是读取到文件数据的数据类型：', type(frequentDrop))
    return frequentDrop

def loadtime_list():
    result_dir = "../resources2/raw_data/"
    files = "ny_inter_region_cost_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        time_list = json.load(fp)
        print(len(time_list))
        print('这是文件中的json数据：', time_list["1"])
        print('这是读取到文件数据的数据类型：', type(time_list))
    return time_list

def loadNode2region():
    result_dir = "../resources2/raw_data/"
    files = "ny_node2region_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        Node2region = json.load(fp)
        print(len(Node2region))
        print('这是文件中的json数据：', Node2region[0])
        print('这是读取到文件数据的数据类型：', type(Node2region))
    return Node2region

def loadCHgraph():
    result_dir = "../resources2/raw_data/"
    files = "ny_graph_h_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        CHgraph = json.load(fp)
        print(len(CHgraph))
        print('这是文件中的json数据：', CHgraph[1])
        print('这是读取到文件数据的数据类型：', type(CHgraph))
    return CHgraph

def loadNewMapData():
    fileName4 = '../resources/result3/TestMap.txt'
    file4 = open(fileName4, "r", encoding='utf-8')
    file4lines = file4.readlines()
    NewMapData = {}
    NewMapData2 = {}
    for i in range(len(file4lines)):
        zoneMessage = {}
        zoneMessage['LocationID'] = int(file4lines[i].split(',')[0].split(':')[1])
        zoneMessage['NodeId'] = int(file4lines[i].split(',')[5].split(':')[1].split('\n')[0])
        NewMapData[zoneMessage['LocationID']] = zoneMessage['NodeId']
        NewMapData2[i] = zoneMessage
    print(NewMapData)
    return NewMapData, NewMapData2

def loadNy_location():
    fileName2 = '../resources2/raw_data/ny_location'
    file2 = open(fileName2, "r", encoding='utf-8')
    file2lines = file2.readlines()
    ny_location = {}
    for i in range(len(file2lines)):
        point = {}
        npLocation = file2lines[i].split('\n')[0].split(',')
        point['longitude'] = float(npLocation[1])
        point['latitude'] = float(npLocation[2])
        ny_location[i] = point
    print(ny_location[0])
    return ny_location


def loadNodeRange():
    result_dir = "../resources2/dataDeal/"
    files = "nodeRange.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        graph = json.load(fp)
        print('这是文件中的json数据：', graph["1"])
        print('这是读取到文件数据的数据类型：', type(graph))
    return graph

def loadNodeRangeNode():
    result_dir = "../resources2/dataDeal/"
    files = "ny_fre_dis12.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        graph = json.load(fp)
        print('这是文件中的json数据：', graph["1"])
        print('这是读取到文件数据的数据类型：', type(graph))
    return graph

def loadProblemInstance(orderDate , driverCount, seed, need):
    data = {}
    data['orders'] = loadBaseOrdersByDay(orderDate)
    # print(data['orders'][1])
    # data['drivers'] = loadBaseDriversByCount(driverCount, seed)
    data['driverCount'] = driverCount
    # data['mapZone'] = TxtParser.run_map()
    data['velocity'] = 4.444335233880015
    # data['zoneToZone'], data['velocity'] = calOrder(data['orders'])
    # print(len(data['mapZone']))
    # print(data['drivers'][1])
    data['orderOracle'] = loadTaxiDemandOracle(1, "deepst_gc.txt")
    data['orderReal'] = loadTaxiDemandOracle(1, "deepst_gc.txt_real")
    data['count'] = 0
    data['cacheSD'] = {}
    data['cacheSP'] = {}
    data['graph'] = loadgraph()
    data['reverseGraph'] = loadreverseGraph()
    data['edges'] = loadedges()
    data['ny_location'] = loadNy_location()
    data['distanceFrequentNodes'] = loaddistanceFrequentNodes()
    data['pathFrequentNodes'] = loadpathFrequentNodes()
    data['frequentPickup'] = loadfrequentPickup()
    data['frequentDrop'] = loadfrequentDrop()
    data['time_list'] = loadtime_list()
    data['node2region'] = loadNode2region()
    data['CHgraph'] = loadCHgraph()
    data['CHgraph1'] = loadCHgraph()
    if need == 1:
        data['NodeRangeNode'] = loadNodeRangeNode()
        data['NodeRange'] = loadNodeRange()
    # data['NewMapData'], data['NewMapData2'] = loadNewMapData()
    data['drivers'] = loadBaseDriversByCount(driverCount, data['orders'])
    # print(len(data['orderOracle']))
    # print(len(data['orderReal']))
    frameTime = 30 * 60
    data['taxiWatchdog'] = TaxiDemandSupplyOracle.initialTimeFrames(frameTime)
    # print(data['taxiWatchdog'][0])
    # print(len(data['taxiWatchdog']))
    # print(len(data['taxiWatchdog'][0]))

    # a = "Fri Jun 01 00:00:00 2018"
    # basetime = time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")) + (orderDate-1)*24*60*60
    # basetime = int(basetime)
    # print(len(data['orders']))
    # for i in range(len(data['orders'])):
    #     data['orders'][i]['startTime'] = data['orders'][i]['startTime'] - basetime
    #     data['orders'][i]['endTime'] = data['orders'][i]['endTime'] - basetime
    return data

if __name__ == '__main__':
    # loadProblemInstance(4, 1000, 1)
    data = {}
    data['NodeRangeNode'] = loadNodeRangeNode()
    data['NodeRange'] = loadNodeRange()


    # day = 30
    # loadProblemInstance(30, 1000, 1)
    # orders = loadBaseOrdersByDay(day)
    # # orderOracle = loadTaxiDemandOracle(2, "new_deepst_gc.txt")
    # orderOracle = loadTaxiDemandOracle(1, "new_deepst_gc.txt_real")
    # print(len(orderOracle))
    # 计算预测的人数
    # x = {}
    # print(orders[0])
    # for i in range(48):
    #     x[i] = {}
    #     for j in range(1, 16 * 16 + 1):
    #         x[i][j] = 0
    # for i in range(len(orders)):
    #     x[int(orders[i]['startTime']/30/60)][orders[i]['startZoneID']] = x[int(orders[i]['startTime']/30/60)][orders[i]['startZoneID']] + 1
    # sum2 = 0
    # for i in range(len(x)):
    #     for j in range(len(x[i])):
    #         sum2 = sum2 + x[i][j + 1]
    # print(sum2)
    # result_dir = "../resources2/raw_data/"
    #
    # # files = "new_deepst_gc.txt"
    # files = "new_deepst_gc.txt_real"
    # file = open(result_dir + files, "a", encoding='utf-8')
    # sum2 = 0
    # for i in range(len(x)):
    #     template = ""
    #     template = str(x[i][1])
    #     sum2 = sum2 + x[i][1]
    #     for j in range(1, len(x[i])):
    #         template = template + "," + str(x[i][j + 1])
    #         sum2 = sum2 + x[i][j + 1]
    #     template = template + "\n"
    #     file.write(template)
    #     # file.write('练习文本\n')
    #     file.flush()
    # print(sum2)




    # fileName4 = '../resources/result3/TestMap.txt'
    # file4 = open(fileName4, "r", encoding='utf-8')
    # file4lines = file4.readlines()
    # NewMapData = {}
    # for i in range(len(file4lines)):
    #     zoneMessage = {}
    #     zoneMessage['LocationID'] = int(file4lines[i].split(',')[0].split(':')[1])
    #     zoneMessage['NodeId'] = int(file4lines[i].split(',')[5].split(':')[1].split('\n')[0])
    #     NewMapData[zoneMessage['LocationID']] = zoneMessage['NodeId']
    # print(NewMapData)
    # print(file4lines[0])
    # mapZone = TxtParser.run_map()
    # print(mapZone[60][201])
    # for i in range(1, 31):
    #     print(i)
    #     orders = loadBaseOrdersByDay(i)
    #     print(len(orders))
    #     sum1 = 0
    #     sum2 = 0
    #     print(orders[0])
    #     result_dir = "../resources/result7/"
    #     files10 = str(i) + "_" + "orders_basic.txt"
    #     file = open(result_dir + files10, "a", encoding='utf-8')
    #     for j in range(len(orders)):
    #         if not np.isinf(float(mapZone[orders[j]['startZoneID']][orders[j]['endZoneID']]['cross_id'][len(mapZone[orders[j]['startZoneID']][orders[j]['endZoneID']]['cross_id'])-1]['cost'])):
    #         # if mapZone[orders['start_id']][orders['end_id']]['cross_id'][len(mapZone[orders['start_id']][orders['end_id']]['cross_id'])-1]['cost']
    #     # 2764898, 148, 148, 1, 0.0, 0.0, 0.0, 0.0, 1528588800, 1528589374, 8.3, 0.96, 129.3601365056359
    #             template = str(orders[j]['id']) + "," + str(orders[j]['startZoneID'])\
    #                        + "," + str(orders[j]['endZoneID']) + "," + str(orders[j]['passengerCount'])\
    #                        + "," + str(orders[j]['startPoint_lng']) + "," + str(orders[j]['startPoint_lat'])\
    #                        + "," + str(orders[j]['endPoint_lng']) + "," + str(orders[j]['endPoint_lat'])\
    #                        + "," + str(orders[j]['startTime']) + "," + str(orders[j]['endTime'])\
    #                        + "," + str(orders[j]['cost']) + "," + str(orders[j]['tripLength']) \
    #                        + "," + str(orders[j]['maxWaitTime'])\
    #                        + "\n"
    #             # print(template)
    #             file.write(template)
    #         else:
    #             print(mapZone[orders[j]['startZoneID']][orders[j]['endZoneID']])


    # loadBaseDriversByCount(1000, 1)

