import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import order


def ordersZoneIndex(orders):
    # print(1)
    index = {}
    for i in range(800):
        index[i] = {}
    # print(index[0])
    # print(orders[0]['startZoneID']-1)
    # print(len(index[orders[0]['startZoneID']-1]))
    # print(len())
    for i in range(len(orders)):
        if orders[i]['startZoneID']-1 < 0:
            print("")
        if not order.isAssigned(orders[i]):
            # print(orders[i])
            index[orders[i]['startZoneID']-1][len(index[orders[i]['startZoneID']-1])] = orders[i]
    # print(len(index[orders[0]['startZoneID']-1]))
    return index


def driversZoneIndex(drivers, instance):
    # print(1)
    index = {}
    for i in range(63000):
        index[i] = {}
    # print(index[0])
    # print(drivers[0]['currentZoneID']-1)
    # print(len(index[drivers[0]['currentZoneID']-1]))
    for i in range(len(drivers)):
        if instance['node2region'][drivers[i]['temp_route'][0][0]] < 0:
            print("")
        index[instance['node2region'][drivers[i]['temp_route'][0][0]]][len(index[instance['node2region'][drivers[i]['temp_route'][0][0]]])] = drivers[i]
    # print(len(index[drivers[0]['currentZoneID']-1]))
    return index

def driversZoneIndex1(drivers):
    # print(1)
    index = {}
    for i in range(63000):
        index[i] = {}
    # print(index[0])
    # print(drivers[0]['currentZoneID']-1)
    # print(len(index[drivers[0]['currentZoneID']-1]))
    for i in range(len(drivers)):
        if drivers[i]['temp_route'][0][0] < 0:
            print("")
        index[drivers[i]['temp_route'][0][0]][len(index[drivers[i]['temp_route'][0][0]])] = drivers[i]
    # print(len(index[drivers[0]['currentZoneID']-1]))
    return index

def queryZoneObjects(index, zoneID):
    return index[zoneID-1]