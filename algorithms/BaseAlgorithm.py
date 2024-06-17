import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../estimator')))
# import IdleRatioGreedyAlgorithm
import TaxiDemandSupplyOracle
import IdleTimeEstimator
import ZoneIndex
import myAlgorithm
import upperAlgorithm
import QCSAlgorithm
import FQCSAlgorithm

import IRGAlgorithm
import FQSAlgorithm
import computePath
import order
import math
from decimal import Decimal
def run(instance, j):
    IdleRatioGreedyAlgorithm.run(instance, False, "IdleRatioGreedyAlgorithm", j)

def run1(instance, j):
    # print(1)
    myAlgorithm.run(instance, False, "IdleRatioGreedyAlgorithm", j)
    # print(2)

def run2(instance, j):
    upperAlgorithm.run(instance, False, "upperAlgorithm", j)

def run3(instance, j):
    FQSAlgorithm.run(instance, False, "FQSAlgorithm", j)

def run4(instance, j):
    IRGAlgorithm.run(instance, False, "IRGAlgorithm", j)

def run5(instance, j):
    QCSAlgorithm.run(instance, False, "QCSAlgorithm", j)

def run6(instance, j):
    FQCSAlgorithm.run(instance, False, "FQCSAlgorithm", j)

def buildIndex(instance):
    # print("start")
    # print(len(instance['orders']))
    # print(len(instance['drivers']))
    orderIndex = ZoneIndex.ordersZoneIndex(instance['orders'])
    driverIndex = ZoneIndex.driversZoneIndex(instance['drivers'], instance)
    return orderIndex, driverIndex

def buildIndex1(instance):
    # print("start")
    # print(len(instance['orders']))
    # print(len(instance['drivers']))
    orderIndex = ZoneIndex.ordersZoneIndex(instance['orders'])
    driverIndex = ZoneIndex.driversZoneIndex1(instance['drivers'])
    return orderIndex, driverIndex

def getDistance(x, y):
    t1 = (float(x['longitude'])-float(y['longitude'])) ** 2
    t2 = (float(x['latitude'])-float(y['latitude']))**2
    # print(t1,t2)
    sum = t1+t2
    # print(sum)
    sqrt = math.sqrt(sum)
    # print(sqrt)
    return sqrt*10000


def findShortestOrder(zoneDrivers, zoneOrders, minTriLength, instance):
    # minIdleRatio = 100000000000000000000000000000000
    selectedDriver = {}
    # print(len(zoneOrders))
    j=0
    for i in range(len(zoneDrivers)):
        # print(zoneOrders[0])

        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion2(zoneOrders, zoneDrivers[i], instance)
        # print(idx_[0], idx_[1], cost, dist)
        if idx_[0] < 0 or idx_[1] == len(zoneDrivers[i]['temp_route']):
            continue

        if cost < minTriLength:
            minTriLength = cost
            selectedDriver = zoneDrivers[i]
            j = i

    return selectedDriver

def findBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    # minIdleRatio = 100000000000000000000000000000000
    selectedDriver = {}
    # print(len(zoneOrders))
    j = 0
    # if not order.isAssigned(zoneOrders[0]):
    #     print(1)
    # minIdx_ = {}
    # minIdx_[0], minIdx_[1] = -1, -1
    # currentIdleTime = zoneDrivers['servingOrder']['idletime']
    # print("+++++", len(zoneOrders))
    for i in range(len(zoneDrivers)):

        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion1(zoneOrders, zoneDrivers[i], instance)
        if idx_[0] < 0:
            continue
        idleRatio = estimateZoneIdleRatio(zoneDrivers[i], zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        # print(idx_[0], idx_[1], cost, dist)

        # t = float(zoneOrders['idletime'])/(cost + float(zoneOrders['idletime'])+float("1e-8"))
        t = cost + float(zoneOrders['idletime'])
        # print(cost, float(zoneOrders['idletime']), t, float(zoneOrders['idletime'])/(cost + float(zoneOrders['idletime'])+float("1e-8")))
        if t < minIdleRatio:
            minIdleRatio = t
            selectedDriver = zoneDrivers[i]
            j = i
        # print(selectedDriver['id'])
    return selectedDriver


def findBestOrders2(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    # minIdleRatio = 100000000000000000000000000000000
    selectedDriver = {}
    # print(len(zoneOrders))
    j = 0
    # if not order.isAssigned(zoneOrders[0]):
    #     print(1)
    # minIdx_ = {}
    # minIdx_[0], minIdx_[1] = -1, -1
    # currentIdleTime = zoneDrivers['servingOrder']['idletime']
    for i in range(len(zoneDrivers)):

        idleRatio = estimateZoneIdleRatio(zoneDrivers[i], zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        if zoneOrders['idletime'] > zoneDrivers[i]['servingOrder']['idletime']:
            continue
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion(zoneOrders, zoneDrivers[i], instance)
        # print(idx_[0], idx_[1], cost, dist)
        if idx_[0] < 0:
            continue
        # t = float(zoneOrders['idletime'])/(cost + float(zoneOrders['idletime'])+float("1e-8"))
        t = cost + float(zoneOrders['idletime'])
        # print(cost, float(zoneOrders['idletime']), t)
        if t < minIdleRatio:
            minIdleRatio = t
            selectedDriver = zoneDrivers[i]
            j = i

    return selectedDriver


def new_findBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    selectedOrder = {}
    j = 0
    for i in range(len(zoneOrders)):
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion1(zoneOrders[i], zoneDrivers, instance)
        if idx_[0] < 0:
            continue
        # print("start")
        # idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
        #                                   currentTimeOffset, zoneDriverCount, instance, cost)
        idleRatio = estimateZoneIdleRatio1(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
        t = cost + float(zoneOrders[i]['idletime'])/3
        # t = cost
        if t < minIdleRatio:
            minIdleRatio = t
            selectedOrder = zoneOrders[i]
            j = i
    return selectedOrder


def ITGfindBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    selectedOrder = {}
    j = 0
    for i in range(len(zoneOrders)):
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion1(zoneOrders[i], zoneDrivers, instance)
        if idx_[0] < 0:
            continue
        idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
        t = cost + float(zoneOrders[i]['idletime'])
        if t < minIdleRatio:
            minIdleRatio = t
            selectedOrder = zoneOrders[i]
            j = i
    return selectedOrder

def ITG2findBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    selectedOrder = {}
    j = 0

    for i in range(len(zoneOrders)):
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion(zoneOrders[i], zoneDrivers, instance)
        if idx_[0] < 0:
            continue
        idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
        if zoneOrders[i]['idletime'] > zoneDrivers['servingOrder']['idletime']:
            continue
        t = cost + float(zoneOrders[i]['idletime'])
        if t < minIdleRatio:
            minIdleRatio = t
            selectedOrder = zoneOrders[i]
            j = i
    return selectedOrder

def ITG2findBestOrders2(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    selectedOrder = {}
    j = 0

    for i in range(len(zoneOrders)):
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion(zoneOrders[i], zoneDrivers, instance)
        if idx_[0] < 0:
            continue
        idleRatio = estimateZoneIdleRatio1(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
                                          currentTimeOffset, zoneDriverCount, instance, cost)
        # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
        if zoneOrders[i]['idletime'] > zoneDrivers['servingOrder']['idletime']:
            continue
        t = cost + float(zoneOrders[i]['idletime'])/3
        if t < minIdleRatio:
            minIdleRatio = t
            selectedOrder = zoneOrders[i]
            j = i
    return selectedOrder

def ITGSortedfindBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
    selectedOrder = {}
    j = 0
    for i in range(len(zoneOrders)):
        idx_ = {}
        idx_[0], idx_[1], cost, dist = Leinsertion2(zoneOrders[i], zoneDrivers, instance)
        if cost + zoneDrivers['temp_route'][len(zoneDrivers['temp_route'])-1][2] - zoneDrivers['temp_route'][0][2] > (zoneDrivers['temp_route'][len(zoneDrivers['temp_route'])-1][2] - zoneDrivers['temp_route'][0][2]) * instance['detour_factor']:
            continue
        if idx_[0] < 0 or idx_[1] == len(zoneDrivers['temp_route']):
            continue
        # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
        # t = cost + float(zoneOrders[i]['idletime'])
        if cost < minIdleRatio:
            minIdleRatio = cost
            selectedOrder = zoneOrders[i]
            j = i
    return selectedOrder
# def findShortestOrder(zoneDrivers, zoneOrders, minTriLength, instance):
#     # minIdleRatio = 100000000000000000000000000000000
#     selectedOrder = {}
#     # print(len(zoneOrders))
#     j=0
#     for i in range(len(zoneOrders)):
#         # print(zoneOrders[0])
#         if order.isAssigned(zoneOrders[i]):
#             continue
#         idx_ = {}
#         idx_[0], idx_[1], cost, dist = Leinsertion2(zoneOrders[i], zoneDrivers, instance)
#         # print(idx_[0], idx_[1], cost, dist)
#         if idx_[0] < 0 or idx_[1] == len(zoneDrivers['temp_route']):
#             continue
#
#         if cost < minTriLength:
#             minTriLength = cost
#             selectedOrder = zoneOrders[i]
#             j = i
#     if len(zoneOrders) > 1 and j != len(zoneOrders)-1:
#             zoneOrders[j], zoneOrders[len(zoneOrders)-1] = zoneOrders[len(zoneOrders)-1], zoneOrders[j]
#     return selectedOrder, len(zoneOrders)-1
#
# def findBestOrders(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
#     # minIdleRatio = 100000000000000000000000000000000
#     selectedOrder = {}
#     # print(len(zoneOrders))
#     j = 0
#     # if not order.isAssigned(zoneOrders[0]):
#     #     print(1)
#     # minIdx_ = {}
#     # minIdx_[0], minIdx_[1] = -1, -1
#     # currentIdleTime = zoneDrivers['servingOrder']['idletime']
#     # print("+++++", len(zoneOrders))
#     for i in range(len(zoneOrders)):
#         if order.isAssigned(zoneOrders[i]):
#             continue
#         idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
#                                           currentTimeOffset, zoneDriverCount, instance, cost)
#         idx_ = {}
#         idx_[0], idx_[1], cost, dist = Leinsertion1(zoneOrders[i], zoneDrivers, instance)
#         # print(idx_[0], idx_[1], cost, dist)
#         if idx_[0] < 0:
#             continue
#         t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
#         # t = cost + float(zoneOrders[i]['idletime'])
#         if t < minIdleRatio:
#             minIdleRatio = t
#             selectedOrder = zoneOrders[i]
#             j = i
#     if len(zoneOrders) > 1 and j != len(zoneOrders)-1:
#             zoneOrders[j], zoneOrders[len(zoneOrders)-1] = zoneOrders[len(zoneOrders)-1], zoneOrders[j]
#     return selectedOrder, len(zoneOrders)-1
#
#
# def findBestOrders2(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
#     # minIdleRatio = 100000000000000000000000000000000
#     selectedOrder = {}
#     # print(len(zoneOrders))
#     j = 0
#     # if not order.isAssigned(zoneOrders[0]):
#     #     print(1)
#     # minIdx_ = {}
#     # minIdx_[0], minIdx_[1] = -1, -1
#     currentIdleTime = zoneDrivers['servingOrder']['idletime']
#     for i in range(len(zoneOrders)):
#         if order.isAssigned(zoneOrders[i]):
#             continue
#         idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
#                                           currentTimeOffset, zoneDriverCount, instance, cost)
#         if zoneOrders[i]['idletime'] > currentIdleTime:
#             continue
#         idx_ = {}
#         idx_[0], idx_[1], cost, dist = Leinsertion(zoneOrders[i], zoneDrivers, instance)
#         if idx_[0] < 0:
#             continue
#         # t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
#         t = cost + float(zoneOrders[i]['idletime'])
#         if t < minIdleRatio:
#             minIdleRatio = t
#             selectedOrder = zoneOrders[i]
#             j = i
#     if len(zoneOrders) > 1 and j != len(zoneOrders)-1:
#             zoneOrders[j], zoneOrders[len(zoneOrders)-1] = zoneOrders[len(zoneOrders)-1], zoneOrders[j]
#     return selectedOrder, len(zoneOrders)-1









#
# def findBestOrders2(zoneDrivers, zoneOrders, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, minIdleRatio, instance, cost):
#     # minIdleRatio = 100000000000000000000000000000000
#     selectedOrder = {}
#     # print(len(zoneOrders))
#     j = 0
#     # if not order.isAssigned(zoneOrders[0]):
#     #     print(1)
#     # minIdx_ = {}
#     # minIdx_[0], minIdx_[1] = -1, -1
#     currentIdleTime = zoneDrivers['servingOrder']['idletime']
#     for i in range(len(zoneOrders)):
#         if order.isAssigned(zoneOrders[i]):
#             continue
#         idleRatio = estimateZoneIdleRatio(zoneDrivers, zoneOrders[i], zoneIdleTimeMap, orderOracle, taxiWatchdog,
#                                           currentTimeOffset, zoneDriverCount, instance, cost)
#         if zoneOrders[i]['idletime'] > currentIdleTime:
#             continue
#         idx_ = {}
#         idx_[0], idx_[1], cost, dist = Leinsertion(zoneOrders[i], zoneDrivers, instance)
#         if idx_[0] < 0:
#             continue
#         t = float(zoneOrders[i]['idletime'])/(cost + float(zoneOrders[i]['idletime'])+float("1e-8"))
#         if t < minIdleRatio:
#             minIdleRatio = t
#             selectedOrder = zoneOrders[i]
#             j = i
#     if len(zoneOrders) > 1 and j != len(zoneOrders)-1:
#             zoneOrders[j], zoneOrders[len(zoneOrders)-1] = zoneOrders[len(zoneOrders)-1], zoneOrders[j]
#     return selectedOrder, len(zoneOrders)-1





lookupLength = 5*60

def estimateZoneIdleRatio(zoneDrivers, order, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, instance, cost):

    # tripTime = order['endTime'] - order['startTime']
    tripTime = cost
    lamda = TaxiDemandSupplyOracle.queryRate(orderOracle, currentTimeOffset + tripTime
                , currentTimeOffset + tripTime + lookupLength, order['endZoneID']) * 60
    mu = ((TaxiDemandSupplyOracle.queryDemand(taxiWatchdog, currentTimeOffset + tripTime,
        currentTimeOffset + tripTime+lookupLength, order['endZoneID']) + 1)/lookupLength) * 60
    maxDriverCount = zoneDriverCount[order['endZoneID']]
    idleTime = IdleTimeEstimator.estimateIdleTimeMix(lamda, mu, maxDriverCount) * 60
    # print(lamda, mu, maxDriverCount, idleTime)
    zoneIdleTimeMap[order['endZoneID']] = idleTime
    order['idletime'] = idleTime
    # print(lamda, mu, maxDriverCount, idleTime)
    if (idleTime + order['endTime'] - order['startTime']) == 0:
        # print(idleTime, order['endTime'], order['startTime'])
        idleRatio = 1
    else:
        idleRatio = idleTime / (idleTime + order['endTime'] - order['startTime'])
    order['idleRatio'] = idleRatio
    return idleRatio
    # return order['endTime'] + idleTime


def estimateZoneIdleRatio1(zoneDrivers, order, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, instance, cost):

    # tripTime = order['endTime'] - order['startTime']
    tripTime = zoneDrivers['temp_route'][len(zoneDrivers['temp_route'])-1][2] - zoneDrivers['temp_route'][0][2] + cost

    # tripTime = cost
    lamda = 0
    mu = 0
    maxDriverCount = 0
    # print(instance['NodeRange'][str(order['startNodeID'])])
    for value in instance['NodeRange'][str(order['endNodeID'])]:
        lamda = lamda + float(TaxiDemandSupplyOracle.queryRate(orderOracle, currentTimeOffset + tripTime
                                                               , currentTimeOffset + tripTime + lookupLength,
                                                               int(value))) \
                * 60 * instance['NodeRange'][str(order['endNodeID'])][str(value)]
    # print(lamda)
    for value in instance['NodeRange'][str(order['endNodeID'])]:
        mu = mu + ((float(TaxiDemandSupplyOracle.queryDemand(taxiWatchdog, currentTimeOffset + tripTime
                                                             , currentTimeOffset + tripTime + lookupLength,
                                                             int(value))) + 1) / lookupLength) * 60 * \
             instance['NodeRange'][str(order['endNodeID'])][str(value)]


    # tripTime = zoneDrivers['temp_route'][len(zoneDrivers['temp_route'])-1][2] + cost
    # lamda = 0
    # mu = 0
    # maxDriverCount = 0
    # # print(instance['NodeRange'][str(order['startNodeID'])])
    # for value in instance['NodeRange'][str(order['endNodeID'])]:
    #     lamda = lamda + float(TaxiDemandSupplyOracle.queryRate(orderOracle, tripTime
    #                 , tripTime + lookupLength, int(value))) \
    #             * 60 * instance['NodeRange'][str(order['endNodeID'])][str(value)]
    # # print(lamda)
    # for value in instance['NodeRange'][str(order['endNodeID'])]:
    #     mu = mu + ((float(TaxiDemandSupplyOracle.queryDemand(taxiWatchdog, tripTime
    #                                                            , tripTime + lookupLength,
    #                                                            int(value))) + 1) / lookupLength) * 60 * instance['NodeRange'][str(order['endNodeID'])][str(value)]
    #
    #

    # mu = mu + ((TaxiDemandSupplyOracle.queryDemand1(taxiWatchdog, currentTimeOffset + tripTime,
    #                                                 currentTimeOffset + tripTime + lookupLength,
    #                                                 instance['NodeRangeNode'][
    #                                                     str(order['endNodeID'])]) + 1) / lookupLength) * 60
    for value in instance['NodeRangeNode'][str(order['endNodeID'])]:
        maxDriverCount = maxDriverCount + zoneDriverCount[int(value)]
    # print(mu, maxDriverCount)
    idleTime = IdleTimeEstimator.estimateIdleTimeMix(lamda, float(mu), maxDriverCount) * 60
    if idleTime > 300:
        idleTime = 299
    # print(lamda, mu, maxDriverCount, idleTime)
    # if mu >0.2:
    #     print(lamda, mu, maxDriverCount, idleTime)
    zoneIdleTimeMap[order['endZoneID']] = idleTime
    order['idletime'] = idleTime
    if (idleTime + order['endTime'] - order['startTime']) == 0:
        # print(idleTime, order['endTime'], order['startTime'])
        idleRatio = 1
    else:
        idleRatio = idleTime / (idleTime + order['endTime'] - order['startTime'])
    order['idleRatio'] = idleRatio
    return idleRatio



def estimateZoneIdleTime(zoneDrivers, order, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, instance, cost):
    # print(order['endZoneID'])
    # print(zoneIdleTimeMap.get(order['endZoneID']))
    if zoneIdleTimeMap.get(order['endZoneID']) != None:
        idleTime = zoneIdleTimeMap[order['endZoneID']]
    else:
        c = order['endTime'] - order['startTime']
        # print("good")
        # print(tripTime)
        if len(zoneDrivers['temp_route']) == 1:
            dist = computePath.dis(zoneDrivers['temp_route'][0][0], instance['NewMapData'][order["startZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            dis2 = computePath.dis(instance['NewMapData'][order["startZoneID"]], instance['NewMapData'][order["endZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            tripTime = Decimal(dist + dis2)
        # print(dist + dis2)
        else:
            tripTime = zoneDrivers['temp_route'][zoneDrivers['temp_route']-1][0] + cost
        # print("start-------------")
        lamda = TaxiDemandSupplyOracle.queryRate(orderOracle, currentTimeOffset + tripTime
                    , currentTimeOffset + tripTime + lookupLength, order['endZoneID']) * 60
        # print("lamda")
        # print(lamda)
        mu = ((TaxiDemandSupplyOracle.queryDemand(taxiWatchdog, currentTimeOffset + tripTime,
            currentTimeOffset + tripTime+lookupLength, order['endZoneID']) + 1)/lookupLength) * 60
        # print("mu")
        # print(mu)
        maxDriverCount = zoneDriverCount[order['endZoneID']-1]
        idleTime = IdleTimeEstimator.estimateIdleTimeMix(lamda, mu, maxDriverCount) * 60
        # print("idleTime")
        # print(idleTime)
        # zoneIdleTimeMap.put(order['endZoneID'], idleTime)
        zoneIdleTimeMap[order['endZoneID']] = idleTime
    order['idletime'] = idleTime
    # print(type(idleTime))

    # print(type(order['endTime'] - order['startTime']))
    # print(idleTime)
    # print(order['endTime'] - order['startTime'])
    idleRatio = idleTime / (idleTime + order['endTime'] - order['startTime'])
    order['idleRatio'] = idleRatio
    # print(idleRatio)
    # print(idleTime + order['endTime'], idleTime)
    # return idleTime + order['endTime']
    return order['endTime'] + idleTime

def estimateZoneIdleTime2(zoneDrivers, order, zoneIdleTimeMap, orderOracle, taxiWatchdog, currentTimeOffset, zoneDriverCount, instance):
    # print(order['endZoneID'])
    # print(zoneIdleTimeMap.get(order['endZoneID']))
    if zoneIdleTimeMap.get(order['endZoneID']) != None:
        idleTime = zoneIdleTimeMap[order['endZoneID']]
    else:
        c = order['endTime'] - order['startTime']
        # print("good")
        # print(tripTime)
        idx_, cost_, dist = Leinsertion(zoneOrders[j], instance['secondDrivers'][i], instance)
        # dist = computePath.dis(zoneDrivers['temp_route'][0][0], instance['NewMapData'][order["startZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # dis2 = computePath.dis(instance['NewMapData'][order["startZoneID"]], instance['NewMapData'][order["endZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        # print(dist + dis2)
        tripTime = Decimal(cost_)
        # print("start-------------")
        lamda = TaxiDemandSupplyOracle.queryRate(orderOracle, currentTimeOffset + tripTime
                    , currentTimeOffset + tripTime + lookupLength, order['endZoneID']) * 60
        # print("lamda")
        # print(lamda)
        mu = ((TaxiDemandSupplyOracle.queryDemand(taxiWatchdog, currentTimeOffset + tripTime,
            currentTimeOffset + tripTime+lookupLength, order['endZoneID']) + 1)/lookupLength) * 60
        # print("mu")
        # print(mu)
        maxDriverCount = zoneDriverCount[order['endZoneID']-1]
        idleTime = IdleTimeEstimator.estimateIdleTimeMix(lamda, mu, maxDriverCount) * 60
        # print("idleTime")
        # print(idleTime)
        # zoneIdleTimeMap.put(order['endZoneID'], idleTime)
        zoneIdleTimeMap[order['endZoneID']] = idleTime
    order['idletime'] = idleTime
    # print(type(idleTime))

    # print(type(order['endTime'] - order['startTime']))
    # print(idleTime)
    # print(order['endTime'] - order['startTime'])
    idleRatio = idleTime / (idleTime + order['endTime'] - order['startTime'])
    order['idleRatio'] = idleRatio
    # print(idleRatio)
    # print(idleTime + order['endTime'], idleTime)
    # return idleTime + order['endTime']
    return order['endTime'] + idleTime



# def Leinsertion(order, used_driver, instance):
#     idx_ = {}
#     idx_[0] = -1
#     idx_[1] = -1
#     cost_ = 2147483647
#     dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
#                            instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                            instance['frequentPickup'], instance['frequentDrop'])
#     # dist = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#     #                        instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#     for i in range(1, len(used_driver['temp_route'])+1):
#         if feasible(i, len(used_driver['temp_route']), order, used_driver, instance):
#             # print("start")
#             cost_t = racost(i, len(used_driver['temp_route']), order, used_driver, instance, dist)
#             if cost_t < cost_:
#                 cost_ = cost_t
#                 idx_[0] = i
#                 idx_[1] = len(used_driver['temp_route'])
#         # if i == len(used_driver['temp_route'])-1:
#         #     # print(1)
#         #     break
#     return idx_[0], idx_[1], cost_, dist
#
#
#
#
# def Leinsertion2(order, used_driver, instance):
#     idx_ = {}
#     idx_[0] = -1
#     idx_[1] = -1
#     dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
#                            instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                            instance['frequentPickup'], instance['frequentDrop'])
#     # dist = getDistance(instance['ny_location'][order["startNodeID"]],
#     #                    instance['ny_location'][order["endNodeID"]])
#     # print("start")
#     # print(dist)
#     cost_ = 2147483647
#     Dio = {}
#     Pic = {}
#     Dio[len(Dio)] = 2147483647
#     Dio[len(Dio)] = 2147483647
#     Pic[len(Pic)] = -1
#     Pic[len(Pic)] = -1
#     for i in range(1, len(used_driver['temp_route'])+1):
#         if feasible(i, i, order, used_driver, instance):
#             # print("start")
#             cost_t = racost(i, i, order, used_driver, instance, dist)
#             # print(cost_t)
#             if cost_t < cost_:
#                 cost_ = cost_t
#                 idx_[0] = i
#                 idx_[1] = i
#         if i > 1 and Dio[i] != 2147483647:
#             dis1 = computePath.dis(used_driver['temp_route'][i - 1][0], order["endNodeID"], instance,
#                            instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                            instance['frequentPickup'], instance['frequentDrop'])
#             # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][i - 1][0]], instance['ny_location'][order["endNodeID"]])
#             if dis1 != -1:
#                 if i == len(used_driver['temp_route'])-1:
#                     cost_i = dis1 + Dio.get(i)
#                     if cost_i + used_driver['temp_route'][i - 1][2] > int(order["startTime"] + order["maxWaitTime"]):
#                         cost_i = 2147483647
#                 else:
#                     dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][i][0], instance,
#                                            instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                                            instance['frequentPickup'], instance['frequentDrop'])
#                     # dis2 = getDistance(instance['ny_location'][order["endNodeID"]], instance['ny_location'][used_driver['temp_route'][i][0]])
#                     if dis2 != 1:
#                         arr = dis1 + used_driver['temp_route'][i - 1][2] + Dio[i]
#                         cost_i = dis2 - used_driver['temp_route'][i][2] + arr
#                         if cost_i > used_driver['temp_route'][j][4] or arr > int(order["startTime"] + order["maxWaitTime"]):
#                             cost_i = 2147483647
#                     else:
#                         cost_i = 2147483647
#                 if cost_i < cost_:
#                     cost_ = cost_i
#                     idx_[0] = Pic[i]
#                     idx_[1] = i
#         if i == len(used_driver['temp_route'])-1:
#             break
#         if used_driver['temp_route'][i][2] > int(order["startTime"] + order["maxWaitTime"]):
#             break
#         if used_driver['temp_route'][i][5] + order['passengerCount'] > used_driver['passengerCount']:
#             Dio[len(Dio)] = 2147483647
#             Pic[len(Pic)] = -1
#         else:
#             dis1 = computePath.dis(used_driver['temp_route'][i - 1][0], order["startNodeID"], instance,
#                                    instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                                    instance['frequentPickup'], instance['frequentDrop'])
#             # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][i - 1][0]], instance['ny_location'][order["startNodeID"]])
#             dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][i][0], instance,
#                                    instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                                    instance['frequentPickup'], instance['frequentDrop'])
#             # dis2 = getDistance(instance['ny_location'][order["startNodeID"]], instance['ny_location'][used_driver['temp_route'][i][0]])
#             if dis1 == -1 and dis2 == -1:
#                 det = dis1 + dis2 + used_driver['temp_route'][i - 1][0] + used_driver['temp_route'][i][0]
#                 if det > used_driver['temp_route'][i][4] or det > Dio[i]:
#                     Dio[len(Dio)] = Dio[len(Dio)-1]
#                     Pic[len(Pic)] = Pic[len(Pic)-1]
#                 else:
#                     Dio[len(Dio)] = det
#                     Pic[len(Pic)] = i
#             else:
#                 Dio[len(Dio)] = Dio[len(Dio) - 1]
#                 Pic[len(Pic)] = Pic[len(Pic) - 1]
#     return idx_[0], idx_[1], cost_, dist
#
# def Leinsertion1(order, used_driver, instance):
#     idx_ = {}
#     idx_[0] = -1
#     idx_[1] = -1
#     cost_ = 2147483647
#     dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance,
#                            instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                            instance['frequentPickup'], instance['frequentDrop'])
#     # dist = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#     #                        instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#     for i in range(1, 2):
#         if feasible(1, 1, order, used_driver, instance):
#             # print("start")
#             cost_t = racost(1, 1, order, used_driver, instance, dist)
#             if cost_t < cost_:
#                 cost_ = cost_t
#                 idx_[0] = 1
#                 idx_[1] = 1
#         # if i == len(used_driver['temp_route'])-1:
#         #     # print(1)
#         #     break
#     return idx_[0], idx_[1], cost_, dist
#
#
#
#
# def racost(idx1, idx2, order, used_driver, instance, dist):
#     # print(idx1, idx2)
#     if idx1 == idx2:
#         # print(len(used_driver['temp_route']))
#         if len(used_driver['temp_route']) == 1:
#             # print(dist)
#             # print(computePath.dis(used_driver['temp_route'][0][0], instance['NewMapData'][order["startZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop']))
#             return dist + computePath.dis(used_driver['temp_route'][0][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#             # return dist + getDistance(instance['ny_location'][used_driver['temp_route'][0][0]],
#             #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         elif idx1 == len(used_driver['temp_route']):
#             return dist + computePath.dis(used_driver['temp_route'][len(used_driver['temp_route'])-1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#             # return dist + getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route'])-1][0]],
#             #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         else:
#             dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#             # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
#             #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#             dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#             # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["endZoneID"]]],
#             #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
#             return dist + dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
#     elif idx2 == len(used_driver['temp_route']):
#         dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
#         #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         # print(used_driver['temp_route'][idx1 - 1][0], instance['NewMapData'][order["startZoneID"]], dis1)
#         dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#         #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
#         # print(instance['NewMapData'][order["startZoneID"]], used_driver['temp_route'][idx1][0], dis2)
#         cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
#         # print(used_driver['temp_route'])
#         # print(cost_d1)
#         dis3 = computePath.dis(used_driver['temp_route'][len(used_driver['temp_route']) - 1][0], order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route']) - 1][0]],
#         #                    instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#         return cost_d1 + dis3
#     else:
#         dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance,
#                                instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                                instance['frequentPickup'], instance['frequentDrop'])
#         # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
#         #                    instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance,
#                                instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
#                                instance['frequentPickup'], instance['frequentDrop'])
#         # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#         #                    instance['ny_location'][used_driver['temp_route'][idx1][0]])
#         cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
#         dis3 = computePath.dis(used_driver['temp_route'][idx2 - 1][0],
#                                order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'],
#                                instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][idx2 - 1][0]],
#         #                    instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#         dis4 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx2][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis4 = getDistance(instance['ny_location'][instance['NewMapData'][order["endZoneID"]]],
#         #                    instance['ny_location'][used_driver['temp_route'][idx2][0]])
#         return cost_d1 + dis3 + dis4 - used_driver['temp_route'][idx2][2] + used_driver['temp_route'][idx2 - 1][2]


# def feasible(idx1, idx2, order, used_driver, instance):
#     # print("good",idx1, idx2)
#     dist = computePath.dis(order["startNodeID"], order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#     # dist = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#     #                        instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#     # print(used_driver['temp_route'])
#     EndIndex = instance['detour_factor']
#     # print(dist)
#     if idx1 == idx2:
#         arr1 = used_driver['temp_route'][idx1 - 1][2]
#         # print(arr1)
#         dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#         # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
#         #                        instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         # print(dis1)
#         if dis1 == -1:
#             return False
#         # print(int(order["startTime"] + order["maxWaitTime"]))
#         if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
#             # arr2 + detour1 + dis3 > float(order["startTime"]) + dist * 1.3
#             return False
#         if len(used_driver['temp_route']) > idx1:
#             dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
#             # dis2 = getDistance(order["endNodeID"],
#             #                        instance['ny_location'][used_driver['temp_route'][idx1][0]])
#             # print(dis2)
#             if dis2 == -1:
#                 return False
#             detour = dist + dis1 + dis2 + used_driver['temp_route'][idx1 - 1][2] - used_driver['temp_route'][idx1][2]
#             # print(detour, used_driver['temp_route'][idx1][4])
#             if detour > used_driver['temp_route'][idx1][4]:
#                 return False
#         return used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] <= used_driver['passengerCount']
#     else:
#         dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'],
#                                instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
#                                instance['frequentDrop'])
#         # print(dis1)
#         # dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
#         #                        instance['ny_location'][instance['NewMapData'][order["startZoneID"]]])
#         # print("good1")
#         # print(dis1)
#         if dis1 == -1:
#             return False
#         dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'],
#                                instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
#                                instance['frequentDrop'])
#         # dis2 = getDistance(instance['ny_location'][instance['NewMapData'][order["startZoneID"]]],
#         #                        instance['ny_location'][used_driver['temp_route'][idx1][0]])
#         # print(dis2)
#         if dis2 == -1:
#             return False
#         arr1 = used_driver['temp_route'][idx1 - 1][2]
#         # print(arr1)
#         detour1 = dist + dis1 + dis2 + used_driver['temp_route'][idx1 - 1][2] - used_driver['temp_route'][idx1][2]
#         # print(detour1)
#         # print(dis1, dis2, arr1, detour1, int(order["startTime"] + order["maxWaitTime"]), used_driver['temp_route'][idx1][4])
#         if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
#             # arr2 + detour1 + dis3 > float(order["startTime"]) + dist * 1.3
#             return False
#         if detour1 > used_driver['temp_route'][idx1][4]:
#             return False
#         for i in range(idx1-1, idx2, 1):
#             if used_driver['temp_route'][idx1 - 1][5] + order['passengerCount'] > used_driver['passengerCount']:
#                 return False
#         dis3 = computePath.dis(used_driver['temp_route'][idx2 - 1][0], order["endNodeID"], instance, instance['CHgraph'],
#                                instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
#                                instance['frequentDrop'])
#         # print(dis1, dis2, dis3, arr1, detour1, int(order["startTime"] + order["maxWaitTime"]),
#         #       used_driver['temp_route'][idx1][4])
#         # dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][idx2 - 1][0]],
#         #                        instance['ny_location'][instance['NewMapData'][order["endZoneID"]]])
#         if dis3 == -1:
#             return False
#         arr2 = used_driver['temp_route'][idx2 - 1][2]
#         # print(arr2 + detour1 + dis3, int(order["startTime"] + dist * 1.3))
#         if arr2 + detour1 + dis3 > float(order["startTime"]) + dist * EndIndex:
#             return False
#         # print(dis1, dis2, dis3, arr1, arr2, detour1, int(order["startTime"] + order["maxWaitTime"]),
#         #       used_driver['temp_route'][idx1][4])
#         if len(used_driver['temp_route']) > idx2:
#             dis4 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx2][0], instance, instance['CHgraph'],
#                                instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'],
#                                instance['frequentDrop'])
#             # dis4 = getDistance(instance['ny_location'][instance['NewMapData'][order["endZoneID"]]],
#             #                        instance['ny_location'][used_driver['temp_route'][idx2][0]])
#             if dis4 == -1:
#                 return False
#             detour2 = dis3 + dis4 + detour1 + used_driver['temp_route'][idx2-1][2] - used_driver['temp_route'][idx2][0]
#             return detour2 <= used_driver['temp_route'][idx2][4]
#     return True

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
            cost_t = racost1(i, len(used_driver['temp_route']), order, used_driver, instance, dist)
            if cost_t < cost_:
                cost_ = cost_t
                idx_[0] = i
                idx_[1] = len(used_driver['temp_route'])
        if i == len(used_driver['temp_route'])-1:
            break
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
            cost_t = racost1(1, 1, order, used_driver, instance, dist)
            if cost_t < cost_:
                cost_ = cost_t
                idx_[0] = 1
                idx_[1] = 1
        # if i == len(used_driver['temp_route'])-1:
        #     # print(1)
        #     break
    return idx_[0], idx_[1], cost_, dist


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
            cost_t = racost1(i, i, order, used_driver, instance, dist)
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
                        if cost_i > used_driver['temp_route'][j][4] or arr > int(order["startTime"] + dist * instance['detour_factor']):
                            cost_i = 2147483647
                    else:
                        cost_i = 2147483647
                if cost_i < cost_:
                    cost_ = cost_i
                    idx_[0] = Pic[i]
                    idx_[1] = i
        if i == len(used_driver['temp_route'])-1:
            break
        # print(used_driver['temp_route'])
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

def racost1(idx1, idx2, order, used_driver, instance, dist):
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


def racost(idx1, idx2, order, used_driver, instance, dist):
    # print(idx1, idx2)
    if idx1 == idx2:
        # print(len(used_driver['temp_route']))
        if len(used_driver['temp_route']) == 1:
            # print(dist)
            # print(computePath.dis(used_driver['temp_route'][0][0], instance['NewMapData'][order["startZoneID"]], instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop']))
            # return dist + computePath.dis(used_driver['temp_route'][0][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            return dist + getDistance(instance['ny_location'][used_driver['temp_route'][0][0]],
                               instance['ny_location'][order["startNodeID"]])
        elif idx1 == len(used_driver['temp_route']):
            # return dist + computePath.dis(used_driver['temp_route'][len(used_driver['temp_route'])-1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            return dist + getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route'])-1][0]],
                               instance['ny_location'][order["startNodeID"]])
        else:
            # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                               instance['ny_location'][order["startNodeID"]])
            # dis2 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
            dis2 = getDistance(instance['ny_location'][order["endNodeID"]],
                               instance['ny_location'][used_driver['temp_route'][idx1][0]])
            return dist + dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
    elif idx2 == len(used_driver['temp_route']):
        # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                           instance['ny_location'][order["startNodeID"]])
        # print(used_driver['temp_route'][idx1 - 1][0], instance['NewMapData'][order["startZoneID"]], dis1)
        # dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis2 = getDistance(instance['ny_location'][order["startNodeID"]],
                           instance['ny_location'][used_driver['temp_route'][idx1][0]])
        # print(instance['NewMapData'][order["startZoneID"]], used_driver['temp_route'][idx1][0], dis2)
        cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
        # print(used_driver['temp_route'])
        # print(cost_d1)
        # dis3 = computePath.dis(used_driver['temp_route'][len(used_driver['temp_route']) - 1][0], order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][len(used_driver['temp_route']) - 1][0]],
                           instance['ny_location'][order["endNodeID"]])
        return cost_d1 + dis3
    else:
        # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance,
        #                        instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
        #                        instance['frequentPickup'], instance['frequentDrop'])
        dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                           instance['ny_location'][order["startNodeID"]])
        # dis2 = computePath.dis(order["startNodeID"], used_driver['temp_route'][idx1][0], instance,
        #                        instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'],
        #                        instance['frequentPickup'], instance['frequentDrop'])
        dis2 = getDistance(instance['ny_location'][order["startNodeID"]],
                           instance['ny_location'][used_driver['temp_route'][idx1][0]])
        cost_d1 = dis1 + dis2 - used_driver['temp_route'][idx1][2] + used_driver['temp_route'][idx1 - 1][2]
        # dis3 = computePath.dis(used_driver['temp_route'][idx2 - 1][0],
        #                        order["endNodeID"], instance, instance['CHgraph'], instance['cacheSD'],
        #                        instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis3 = getDistance(instance['ny_location'][used_driver['temp_route'][idx2 - 1][0]],
                           instance['ny_location'][order["endNodeID"]])
        # dis4 = computePath.dis(order["endNodeID"], used_driver['temp_route'][idx2][0], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis4 = getDistance(instance['ny_location'][order["endNodeID"]],
                           instance['ny_location'][used_driver['temp_route'][idx2][0]])
        return cost_d1 + dis3 + dis4 - used_driver['temp_route'][idx2][2] + used_driver['temp_route'][idx2 - 1][2]

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
        # if arr1 + dis1 >instance['orders'][j]["startTime"] + instance['orders'][j]["maxWaitTime"]:
        #     return False
        # dis1 = computePath.dis(used_driver['temp_route'][idx1 - 1][0], order["startNodeID"], instance, instance['CHgraph'], instance['cacheSD'], instance['distanceFrequentNodes'], instance['frequentPickup'], instance['frequentDrop'])
        dis1 = getDistance(instance['ny_location'][used_driver['temp_route'][idx1 - 1][0]],
                               instance['ny_location'][order["startNodeID"]])
        # print(arr1 + dis1, order["startTime"] + order["maxWaitTime"])
        if arr1 + dis1 > order["startTime"] + order["maxWaitTime"]:
            return False
        # print(dis1)
        if dis1 == -1:
            return False
        # print(int(order["startTime"] + order["maxWaitTime"]))
        # print(arr1, dis1, dist, float(order["startTime"]), arr1 + dis1 + dist, float(order["startTime"]) + dist * EndIndex)
        # print(arr1 + dis1 + dist, float(order["startTime"]) + dist * EndIndex)
        # if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
        #     return False
        if arr1 + dis1 + dist > float(order["startTime"]) + dist * EndIndex:
            return False
        # instance['orders'][j]["dist"]
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
            if used_driver['temp_route'][i][5] + order['passengerCount'] > used_driver['passengerCount']:
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
        # print(arr1 + dis1, order["startTime"] + order["maxWaitTime"])
        if arr1 + dis1 > order["startTime"] + order["maxWaitTime"]:
            return False
        detour1 = dis1 + dis2 + used_driver['temp_route'][idx1 - 1][2] - used_driver['temp_route'][idx1][2]
        # print(detour1)
        # print(dis1, dis2, arr1, detour1, int(order["startTime"] + order["maxWaitTime"]), used_driver['temp_route'][idx1][4])
        if arr1 + dis1 + dist > float(order["startTime"]) + order["dist"] * EndIndex:
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
        if arr2 + detour1 + dis3 > float(order["startTime"]) + order["dist"] * EndIndex:
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
