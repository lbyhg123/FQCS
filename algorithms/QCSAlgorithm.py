import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))

import BaseAlgorithm
import driver
import TaxiDemandSupplyOracle
import myAlgorithmEngine
import order
import computePath
import math
import json
def run(instance, isRealDemand, info, f):
    detour_factor = 1.4

    instance['detour_factor'] = detour_factor
    if instance['orders'] == {}:
        return
    orderIndex, driverIndex = BaseAlgorithm.buildIndex(instance)

    currentTimeOffset = instance['currentTimeOffset']
    zoneIdleTimeMap = {}
    zoneDriverCount = {}
    oracle = {}


    sum = 0
    for i in range(len(orderIndex)):
        # print(orderIndex[i])
        sum = sum + len(orderIndex[i])
    # print("***********************************",  sum, len(instance['drivers']), len(instance['secondDrivers']))


    for i in range(800):
        zoneDriverCount[i] = len(driverIndex[i])
    if isRealDemand:
        oracle = instance['orderReal']
    else:
        oracle = instance['orderOracle']
    sum = 0

    for k in range(len(instance['drivers'])):
        zoneOrders = {}
        selectedOrder = {}
        for j in range(len(instance['orders'])):
            if order.isAssigned(instance['orders'][j]):
                continue
            if instance['orders'][j]["dist"] == -1:
                instance['orders'][j]["dist"] = computePath.dis(instance['orders'][j]["startNodeID"], instance['orders'][j]["endNodeID"], instance,
                           instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                           instance['frequentPickup'], instance['frequentDrop'])
            if reachable(instance['orders'][j]["dist"], instance['orders'][j], instance['drivers'][k], instance, detour_factor) == False:
                continue
            # print(str(instance['node2region'][instance['drivers'][k]['temp_route'][0][0]]), str(instance['orders'][j]["startZoneID"]))
            if instance['node2region'][instance['drivers'][k]['temp_route'][0][0]] != instance['orders'][j]["startZoneID"]:
                if instance['time_list'][str(instance['node2region'][instance['drivers'][k]['temp_route'][0][0]])][
                                str(instance['orders'][j]["startZoneID"])] <= instance['orders'][j]["startTime"] + instance['orders'][j]["maxWaitTime"] - instance['drivers'][k]['temp_route'][0][2]:
                                continue
            zoneOrders[len(zoneOrders)] = instance['orders'][j]
        if zoneOrders == {}:
            continue
        # print(k, len(zoneOrders))
        selectedOrder= BaseAlgorithm.ITGfindBestOrders(instance['drivers'][k], zoneOrders, zoneIdleTimeMap, oracle,
                                                    instance['taxiWatchdog'],
                                          currentTimeOffset, zoneDriverCount, 100000000000000000000000000000000, instance,0)
        # print(selectedOrder)
        if instance['drivers'][k] != {} and selectedOrder != {}:
            # TaxiDemandSupplyOracle.addTimeRecord(instance['taxiWatchdog'], instance['drivers'][k]['temp_route'][len(instance['drivers'][k]['temp_route'])-1][0],
            #                                      currentTimeOffset + instance['drivers'][k]['temp_route'][len(instance['drivers'][k]['temp_route'])-1][2], 1)
            driver.serveOrder(instance['drivers'][k], selectedOrder, currentTimeOffset,
                            instance['velocity'], instance)
            # zoneOrders.pop(j)
            # assignedDrivers[len(assignedDrivers)] = instance['drivers'][k]
            TaxiDemandSupplyOracle.addTimeRecord(instance['taxiWatchdog'], instance['node2region'][instance['drivers'][k]['temp_route'][len(instance['drivers'][k]['temp_route'])-1][0]],
                                                 instance['drivers'][k]['temp_route'][len(instance['drivers'][k]['temp_route'])-1][2], 1)
            # zoneIdleTimeMap.pop(selectedOrder['endZoneID'])
            zoneDriverCount[instance['node2region'][instance['drivers'][k]['temp_route'][0][0]]] = zoneDriverCount[instance['node2region'][instance['drivers'][k]['temp_route'][0][0]]] - 1
            sum = sum + 1
    # print(sum)





def getDistance(x, y):
    t1 = (float(x['longitude'])-float(y['longitude'])) ** 2
    t2 = (float(x['latitude'])-float(y['latitude']))**2
    # print(t1,t2)
    sum = t1+t2
    # print(sum)
    sqrt = math.sqrt(sum)
    # print(sqrt)
    return sqrt*10000


def reachable(dist, order, driver, instance, detour_factor):
    # print(driver['temp_route'])
    # print(driver['passengerCount'], driver['temp_route'][0][5], order['passengerCount'])

    # for i in range(len(driver['temp_route'])):
    #     if driver['passengerCount'] < (driver['temp_route'][i][5] + order['passengerCount']):
    #         # print(driver['passengerCount'], driver['temp_route'][0][5], order['passengerCount'])
    #         return False
    if instance['node2region'][driver['temp_route'][0][0]] == order["startZoneID"]:
        return True
    else:
        try:
            time_left = order['startTime'] + dist * detour_factor
            # print(instance['node2region'][driver['temp_route'][0][0]])
            # print(order["startZoneID"])
            # print(len(instance['time_list']))
            # print(instance['time_list'][str(instance['node2region'][driver['temp_route'][0][0]])][str(order["startZoneID"])], time_left - dist - driver['temp_route'][0][2])
            if instance['time_list'][str(instance['node2region'][driver['temp_route'][0][0]])][str(order["startZoneID"])] <= time_left - dist - driver['temp_route'][0][2]:
                return True
            else:
                return False
        except IndexError:
            return False


def rabound(used_driver, order, instance):
    idx_ = {}
    idx_[0] = -1
    idx_[1] = -1
    cost_ = 2147483647
    dist = getDistance(instance['ny_location'][order["startNodeID"]],
                           instance['ny_location'][order["endNodeID"]])
    for i in range(1, len(used_driver['temp_route'])+1):
        # if feasible1(i, len(used_driver['temp_route']), order, used_driver, instance):
            # print("start")
        cost_t = racost1(i, len(used_driver['temp_route']), order, used_driver, instance, dist)
        # print(cost_t)
        if cost_t < cost_:
            cost_ = cost_t
            idx_[0] = i
            idx_[1] = len(used_driver['temp_route'])
        if i == len(used_driver['temp_route'])-1:
            break
    return cost_







def Leinsertion2(order, used_driver, instance):
    idx_ = {}
    idx_[0] = -1
    idx_[1] = -1
    dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
                           instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                           instance['frequentPickup'], instance['frequentDrop'])
    # dist = getDistance(instance['ny_location'][order["startNodeID"]],
    #                    instance['ny_location'][order["endNodeID"]])
    # print("start")
    # print(dist)
    cost_ = 2147483647
    Dio = {}
    Pic = {}
    Dio[len(Dio)] = 2147483647
    Dio[len(Dio)] = 2147483647
    Pic[len(Pic)] = -1
    Pic[len(Pic)] = -1
    for i in range(1, len(used_driver['temp_route'])+1):
        # print(i, i)
        if feasible(i, i, order, used_driver, instance):
            # print("start")
            cost_t = racost(i, i, order, used_driver, instance, dist)
            # print(cost_t)
            if cost_t < cost_:
                cost_ = cost_t
                idx_[0] = i
                idx_[1] = i
        if i > 1 and Dio[i] != 2147483647:
            dis1 = computePath.dis(used_driver['temp_route'][i - 1][0], order["endNodeID"], instance,
                                   instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                   instance['frequentPickup'], instance['frequentDrop'])
            # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][i - 1][0]], instance['ny_location'][order["endNodeID"]])
            if dis1 != -1:
                if i == len(used_driver['temp_route'])-1:
                    cost_i = dis1 + Dio.get(i)
                    if cost_i + used_driver['temp_route'][i - 1][2] > int(order["startTime"] + dist * instance['detour_factor']):
                        cost_i = 2147483647
                else:
                    dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][i][0], instance,
                                           instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                           instance['frequentPickup'], instance['frequentDrop'])
                    # dis2 = getDistance(instance['ny_location'][order["endNodeID"]], instance['ny_location'][used_driver['temp_route'][i][0]])
                    if dis2 != 1:
                        arr = dis1 + used_driver['temp_route'][i - 1][2] + Dio[i]
                        cost_i = dis2 - used_driver['temp_route'][i][2] + arr
                        if cost_i > used_driver['temp_route'][i][4] or arr > int(order["startTime"] + dist * instance['detour_factor']):
                            cost_i = 2147483647
                    else:
                        cost_i = 2147483647
                if cost_i < cost_:
                    cost_ = cost_i
                    idx_[0] = Pic[i]
                    idx_[1] = i
        if i == len(used_driver['temp_route'])-1:
            break
        if used_driver['temp_route'][i][2] > dist * instance['detour_factor']:
            break
        if used_driver['temp_route'][i][5] + order['passengerCount'] > used_driver['passengerCount']:
            Dio[len(Dio)] = 2147483647
            Pic[len(Pic)] = -1
        else:
            dis1 = computePath.dis(used_driver['temp_route'][i - 1][0], order["startNodeID"], instance,
                                   instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                   instance['frequentPickup'], instance['frequentDrop'])
            # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][i - 1][0]], instance['ny_location'][order["startNodeID"]])
            dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][i][0], instance,
                                   instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                                   instance['frequentPickup'], instance['frequentDrop'])
            # dis2 = getDistance(instance['ny_location'][order["startNodeID"]], instance['ny_location'][used_driver['temp_route'][i][0]])
            if dis1 != -1 and dis2 != -1:
                det = dis1 + dis2 + used_driver['temp_route'][i - 1][2] + used_driver['temp_route'][i][2]
                if det > used_driver['temp_route'][i][4] or det > Dio[i]:
                    Dio[len(Dio)] = Dio[i]
                    Pic[len(Pic)] = Pic[i]
                else:
                    Dio[len(Dio)] = det
                    Pic[len(Pic)] = i
            else:
                Dio[len(Dio)] = Dio[i]
                Pic[len(Pic)] = Pic[i]
    if idx_[0]!=-1:
        if feasible(idx_[0], idx_[1], order, used_driver, instance):
            return idx_[0], idx_[1], cost_, dist
        else:
            return -1, -1, 2147483647, dist
    return idx_[0], idx_[1], cost_, dist

def Leinsertion1(order, used_driver, instance):
    idx_ = {}
    idx_[0] = -1
    idx_[1] = -1
    cost_ = 2147483647
    dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
                           instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                           instance['frequentPickup'], instance['frequentDrop'])
    # dist = getDistance(instance['ny_location'][order["startNodeID"]],
    #                        instance['ny_location'][order["endNodeID"]])
    for i in range(1, 2):
        if feasible(1, 1, order, used_driver, instance):
            # print("start")
            cost_t = racost(1, 1, order, used_driver, instance, dist)
            if cost_t < cost_:
                cost_ = cost_t
                idx_[0] = 1
                idx_[1] = 1
        # if i == len(used_driver['temp_route'])-1:
        #     # print(1)
        #     break
    return idx_[0], idx_[1], cost_, dist

def Leinsertion(order, used_driver, instance):
    idx_ = {}
    idx_[0] = -1
    idx_[1] = -1
    cost_ = 2147483647
    dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
                           instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                           instance['frequentPickup'], instance['frequentDrop'])
    # dist = getDistance(instance['ny_location'][order["startNodeID"]],
    #                    instance['ny_location'][order["endNodeID"]])
    for i in range(1, len(used_driver['temp_route'])+1):
        if feasible(i, len(used_driver['temp_route']), order, used_driver, instance):
            # print("start")
            cost_t = racost(i, len(used_driver['temp_route']), order, used_driver, instance, dist)
            if cost_t < cost_:
                cost_ = cost_t
                idx_[0] = i
                idx_[1] = len(used_driver['temp_route'])
        if i == len(used_driver['temp_route'])-1:
            break
    return idx_[0], idx_[1], cost_, dist


def feasible(idx1, idx2, order, used_driver, instance):
    # print("good",idx1, idx2)

    # dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
    dist = getDistance(instance['ny_location'][order["startNodeID"]],
                           instance['ny_location'][order["endNodeID"]])
    # print(used_driver['temp_route'])
    EndIndex = instance['detour_factor']
    # print(EndIndex)
    # print(dist)
    if len(used_driver['temp_route']) > 6 and idx1 == 1:
        return False
    if idx1 == idx2:
        if used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] > used_driver['passengerCount']:
            return False
        arr1 = used_driver['temp_route'][idx1 - 1][2]
        # print(arr1)
        # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                               instance['ny_location'][order["startNodeID"]])
        # print(dis1)
        if dis1 == -1:
            return False
        # print(int(order["startTime"] + order["maxWaitTime"]))
        # print(arr1, dis1, dist, float(order["startTime"]), arr1 + dis1 + dist, float(order["startTime"]) + dist * EndIndex)
        # print(arr1 + dis1 + dist, float(order["startTime"]) + dist * EndIndex)
        if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
            return False
        # print(len(used_driver['temp_route']), idx1)
        if len(used_driver['temp_route']) > idx1:
            # dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            dis2 = getDistance(instance['ny_location'][order["endNodeID"]],
                                   instance['ny_location'][used_driver['temp_route'][idx1][0]])
            # print(dis2)
            if dis2 == -1:
                return False
            detour = dist + dis1 + dis2 + used_driver['temp_route'][idx1 - 1][2] - used_driver['temp_route'][idx1][2]
            # print(detour, used_driver['temp_route'][idx1][4])
            if detour > used_driver['temp_route'][idx1][4]:
                return False
        # print(used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] <= used_driver['passengerCount'])
        return used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] <= used_driver['passengerCount']
    else:
        # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'],
        #                        instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
        #                        instance['frequentDrop'])
        # print(dis1)
        for i in range(idx1-1, idx2, 1):
            if used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] > used_driver['passengerCount']:
                return False
        dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                               instance['ny_location'][order["startNodeID"]])
        # print("good1")
        # print(dis1)
        if dis1 == -1:
            return False
        # dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'],
        #                        instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
        #                        instance['frequentDrop'])
        dis2 = getDistance(instance['ny_location'][order["startNodeID"]],
                               instance['ny_location'][used_driver['temp_route'][idx1][0]])
        # print(dis2)
        if dis2 == -1:
            return False
        arr1 = used_driver['temp_route'][idx1 - 1][2]
        # print(arr1)
        detour1 = dis1 + dis2 + used_driver['temp_route'][idx1 - 1][2] - used_driver['temp_route'][idx1][2]
        # print(detour1)
        # print(dis1, dis2, arr1, detour1, int(order["startTime"] + order["maxWaitTime"]), used_driver['temp_route'][idx1][4])
        if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
            # arr2 + detour1 + dis3 > float(order["startTime"]) + dist * 1.3
            return False
        # print("good1111")
        if detour1 > used_driver['temp_route'][idx1][4]:
            return False
        # for i in range(idx1-1, idx2, 1):
        #     if used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] > used_driver['passengerCount']:
        #         return False
        # dis3 = computePath.dis(used_driver['temp_route'][idx2 - 1][0], order["endNodeID"], instance, instance['CHgraph'],
        #                        instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
        #                        instance['frequentDrop'])
        # print(dis1, dis2, dis3, arr1, detour1, int(order["startTime"] + order["maxWaitTime"]),
        #       used_driver['temp_route'][idx1][4])
        dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][idx2 - 1][0]],
                               instance['ny_location'][order["endNodeID"]])
        if dis3 == -1:
            return False
        arr2 = used_driver['temp_route'][idx2 - 1][2]
        # print(arr2 + detour1 + dis3, int(order["startTime"] + dist * 1.3))
        if arr2 + detour1 + dis3 > float(order["startTime"]) + dist * EndIndex:
            return False
        # print(dis1, dis2, dis3, arr1, arr2, detour1, int(order["startTime"] + order["maxWaitTime"]),
        #       used_driver['temp_route'][idx1][4])
        if len(used_driver['temp_route']) > idx2:
            # dis4 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx2][0], instance, instance['CHgraph'],
            #                    instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
            #                    instance['frequentDrop'])
            dis4 = getDistance(instance['ny_location'][order["endNodeID"]],
                                   instance['ny_location'][used_driver['temp_route'][idx2][0]])
            if dis4 == -1:
                return False
            detour2 = dis3 + dis4 + detour1 + used_driver['temp_route'][idx2-1][2] - used_driver['temp_route'][idx2][0]
            return detour2 <= used_driver['temp_route'][idx2][4]
    return True



def racost(idx1, idx2, order, used_driver, instance, dist):
    # print(idx1, idx2)

    if idx1 == idx2:
        # print(len(used_driver['temp_route']))
        if len(used_driver['temp_route']) == 1:
            # print(dist)
            # print(computePath.dis(used_driver['temp_route'][0][0], instance['NewMapData'][order["startZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop']))
            return dist + computePath.dis(used_driver['temp_route'][0][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            # return dist + getDistance(instance['ny_location'][used_driver['temp_route'][0][0]],
            #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
        elif idx1 == len(used_driver['temp_route']):
            return dist + computePath.dis(used_driver['temp_route'][len(used_driver['temp_route'])-1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            # return dist + getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route'])-1][0]],
            #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
        else:
            dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
            #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
            dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["endZoneID"]]],
            #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
            return dist + dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
    elif idx2 == len(used_driver['temp_route']):
        dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
        #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
        # print(used_driver['temp_route'][idx1 - 1][0], instance['NewMapData'][order["startZoneID"]], dis1)
        dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
        #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
        # print(instance['NewMapData'][order["startZoneID"]], used_driver['temp_route'][idx1][0], dis2)
        cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
        # print(used_driver['temp_route'])
        # print(cost_d1)
        dis3 = computePath.dis(used_driver['temp_route'][len(used_driver['temp_route']) - 1][0], order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route']) - 1][0]],
        #                    instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
        return cost_d1 + dis3
    else:
        dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance,
                               instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                               instance['frequentPickup'], instance['frequentDrop'])
        # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
        #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
        dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance,
                               instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
                               instance['frequentPickup'], instance['frequentDrop'])
        # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
        #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
        cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
        dis3 = computePath.dis(used_driver['temp_route'][idx2 - 1][0],
                               order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'],
                               instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][idx2 - 1][0]],
        #                    instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
        dis4 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx2][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis4 = getDistance(instance['ny_location'][instance['NewMapData'][order["endZoneID"]]],
        #                    instance['ny_location'][used_driver['temp_route'][idx2][0]])
        return cost_d1 + dis3 + dis4 - used_driver['temp_route'][idx2][2] + used_driver['temp_route'][idx2 - 1][2]