from decimal import Decimal
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import ZoneDemandTable
def order_fromString(x):
    # print(x)
    order = {}
    x_list = x.split(",")
    # print(x_list)
    if len(x_list) <= 1:
        return null
    # print(x_list)
    order["id"] = int(x_list[0])
    order["startZoneID"] = int(x_list[1])
    order["endZoneID"] = int(x_list[2])

    # order['passengerCount'] = int(x_list[3])
    order['passengerCount'] = 1
    order["startPoint_lng"] = Decimal(x_list[4])
    order["startPoint_lat"] = Decimal(x_list[5])
    order["endPoint_lng"] = Decimal(x_list[6])
    order["endPoint_lat"] = Decimal(x_list[7])
    order["startTime"] = Decimal(x_list[8])
    order["endTime"] = Decimal(x_list[9])
    order["cost"] = Decimal(x_list[10])
    order["tripLength"] = Decimal(x_list[11])
    order["maxWaitTime"] = Decimal(x_list[12])
    order["driver"] = {}
    order["insert_idx"] = {}
    order["idletime"] = 0
    order["idleRatio"] = 0
    # order['people_number']
    # for i in x_list:
    #     print(i)
    return order

def driver_fromString(x, NewMapData):
    driver = {}
    x_list = x.split(",")
    if len(x_list) <= 1:
        return null
    driver["id"] = int(x_list[0])
    driver["curPos_lng"] = Decimal(x_list[1])
    driver["curPos_lat"] = Decimal(x_list[2])
    driver["curPos_time"] = Decimal(x_list[3])
    driver["nextFreeTimeOffset"] = Decimal(x_list[4])
    driver["currentZoneID"] = int(x_list[5])
    driver["RealCurrentZoneID"] = {}
    driver["CurrentZoneIdToDestinationInstance"] = {}
    driver['point'] = int(0)
    driver["RealTime"] = Decimal(0)
    driver['crossZone'] = {}
    temp_loc = {}
    temp_loc[0] = NewMapData[int(x_list[5])]
    temp_loc[1] = Decimal(-10)
    temp_loc[2] = -10
    temp_loc[3] = 0
    temp_loc[4] = 6666
    temp_loc[5] = 0
    driver['temp_route'] = {}
    driver['temp_route'][len(driver['temp_route'])] = temp_loc
    driver['current_path'] = {}
    # t = random.random()
    # # sum1: 6368275,sum2: 1253893,sum3: 354435,sum4: 168946,sum5: 389838,sum6: 240598,sum7: 10,sum8: 3,sum9: 9,sum10: 0
    # numbers1 = [0.9281611785405368, 0.9725820638019091, 0.999997493165172, 0.9999986326355484, 0.9999989744766614, 1.0000000000000002]
    # for i in range(6):
    #     if t < numbers1[i]:
    #         passengerCount = i + 4
    #         break
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
    return driver

def oracle_fromString(x):
    oracle = {}
    x_list = x.split(",")
    demandTable = ZoneDemandTable.ZoneDemandTable()
    if len(x_list) <= 1:
        return null
    offset = 256 - len(x_list)
    print(offset)
    for i in range(offset, 256):
        demandTable[i] = demandTable[i] + Decimal(x_list[i-offset])
    # print(x)
    # print(demandTable)
    return demandTable

def readFromFile(objectClass , filePath, NewMapData):
    xs = {}
    file = open(filePath, "r", encoding='utf-8')
    # r = file.readline()
    # 读取多行
    r = file.readlines()
    print(r[1])
    # for order in r:
    for i in range(len(r)):
        if objectClass == "order":
            x = order_fromString(r[i])
        elif objectClass == "driver":
            x = driver_fromString(r[i], NewMapData)
            x['id'] = i
        elif objectClass == "Oracle":
            x = oracle_fromString(r[i])
        if x != {}:
            xs[i] = x
    # orders[1]['driver']=1
    # print(orders[1])
    # print(orders[1]['cost'])
    file.close()
    return xs

def map_fromString(map):
    zone = {}
    # print(map)
    x_list = map.split("cross_id:")
    # print(x_list[1])
    x_list_1 = x_list[0].split(':')
    zone["start_id"] = int(x_list_1[1].split(',')[0][1:])
    zone["end_id"] = int(x_list_1[2].split(',')[0][1:])
    # print(zone)
    x_list1 = x_list_1[3].split('[')[1].split(']')[0].split(', ')
    x_list2 = x_list_1[4].split('[')[1].split(']')[0].split(', ')
    zone["destination_list"] = {}
    zone["cost_list"] = {}

    # for i in range(len(x_list1)):
    #     zone["destination_list"][len(zone["destination_list"])] = x_list1[len(x_list1) - i - 1]
    #     zone["cost_list"][len(zone["cost_list"])] = x_list2[len(x_list2) - i - 1]


    # print(zone)
    # zone["destination_list"] = {}
    # zone["cost_list"] = {}

    # zone["sum_instance"] = float(x_list[0].split(',')[2][10:])
    # print(zone)
    zone["cross_id"] = {}
    x_list_2 = x_list[1].split('Adjacent_nodes1')
    # print(x_list[1])
    # print(x_list_2[0])
    # print(x_list_2[1])
    for i in range(1, len(x_list_2)):
        # print(x_list_2[i])
        x_data1 = x_list_2[i].split('},')[0].split('{')[1].split(', ')
        x_data2 = x_list_2[i].split('},')[1].split('{')[1].split(', ')
        x_data3 = x_list_2[i].split('},')[2].split(', ')
        # print(x_list_2[i].split('},')[0].split('{')[1].split(', '))
        # # print(x_list_2[i])
        # # print(x_list_2[i].split('},'))
        # print(x_list_2[i].split('},')[1].split('{')[1].split(', '))
        # print(x_data3)
        zone["cross_id"][i-1] = {}
        zone["cross_id"][i - 1]['longitude'] = float(x_data3[0].split(': ')[1])
        zone["cross_id"][i - 1]['latitude'] = float(x_data3[1].split(': ')[1])
        zone["cross_id"][i - 1]['cost'] = float(x_data3[2].split(': ')[1])
        zone["cross_id"][i - 1]['time'] = float(x_data3[3].split(': ')[1].split('}')[0])
        zone["cross_id"][i - 1]['Adjacent_nodes1'] = {}
        zone["cross_id"][i - 1]['Adjacent_nodes_distance'] = {}
        # print(zone["cross_id"][i - 1])
        # print(x_data1)
        # print(x_data2)
        if x_data1 != ['']:
            for j in range(len(x_data1)):
                # print(x_data1[j].split(': '))
                # print(x_data2[j].split(': '))
                zone["cross_id"][i - 1]['Adjacent_nodes1'][j] = int(x_data1[j].split(': ')[1])
                zone["cross_id"][i - 1]['Adjacent_nodes_distance'][j] = float(x_data2[j].split(': ')[1])
        # print(zone["cross_id"][i - 1])
    points_data = {}

    # if x_list[1] != " {}\n":
    #     data = x_list[1].split('time')
    #     for t in range(1, len(data), 1):
    #         points_data[t] = {}
    #         points_data[t]['time'] = Decimal(data[t].split('{')[0].split(',')[0][3:])
    #         points_data[t]['all_instance'] = Decimal(data[t].split('{')[0].split(',')[1][17:])
    #         points_data[t]['zone'] = {}
    #         points_data[t]['instance'] = {}
    #         if data[t].split('{')[1].split('}')[0] != '':
    #             for i in range(len(data[t].split('{')[1].split('}')[0].split(','))):
    #                 points_data[t]['zone'][i] = int(data[t].split('{')[1].split('}')[0].split(',')[i].split(': ')[1])
    #                 points_data[t]['instance'][i] = Decimal(data[t].split('{')[2].split('}')[0].split(',')[i].split(': ')[1])
    # zone['cross_id'] = points_data
    # print(zone)
    return zone

def readmapFile(filePath):
    xs = {}
    file = open(filePath, "r", encoding='utf-8')
    # r = file.readline()
    # 读取多行
    r = file.readlines()
    print(r[0])
    print(r[1])
    # print(r[2])
    # print(r[3])
    c = {}
    for i in range(len(r)):
        # x['strat_id'] = r[i][0:10]
        # x['end_id'] = r[i][9:10]
        x = map_fromString(r[i])
        # print(x)
        if x != {}:
            c[x['end_id']] = x
        if x['end_id'] == 262:
            xs[x['start_id']] = c
            c = {}
    file.close()
    return xs

def writeTofile(recordObjects , filePath):
    file = open(filePath, "w", encoding='utf-8')
    # file.write('练习文本')
    file.close()

def run_map():
    result_dir = "../resources/result/"
    files = "new_map_data3.txt"
    filePath = result_dir + files
    t = readmapFile(filePath)
    # files = "map_data2.txt"
    # filePath = result_dir + files
    # t1 = readmapFile(filePath)
    print("start")
    print(len(t))
    print(len(t[2]))
    sum = 0
    # print(len(t[205]))
    # for i in range(len(t)):
    #     sum = sum + len(t[i])
    #     # print(i,len(t[i]))
    for key in t:
        sum = sum + len(t[key])
    print(sum)
    # print(len(t1))
    # print(len(t1[206]))
    # for i in range(len(t),263):
    #     t[len(t)] = t1[i]
    # print(t[0][4])
    # print(len(t))
    # print(len(t[206]))
    # print(len(t[207]))
    return t

if __name__ == '__main__':
    run_map()