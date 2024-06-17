import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import BaseAlgorithm
import driver
import TaxiDemandSupplyOracle

def run(instance, isRealDemand, info,f):
    # print(info)
    if instance['orders'] == {}:
        return
    orderIndex, driverIndex = BaseAlgorithm.buildIndex(instance)
    currentTimeOffset = instance['currentTimeOffset']
    zoneIdleTimeMap = {}
    zoneDriverCount = {}
    oracle = {}
    for i in range(263):
        zoneDriverCount[i] = len(driverIndex[i])

    if isRealDemand:
        oracle = instance['orderReal']
    else:
        oracle = instance['orderOracle']
    for k in range(263):
        zoneOrders = orderIndex[k]
        zoneDrivers = driverIndex[k]
        # print(k, len(zoneOrders), len(zoneDrivers))
        # print(k, len(orderIndex[k]), len(driverIndex[k]))
        while not zoneDrivers == {} and not zoneOrders == {}:
            assignedDrivers = {}
            for i in range(len(zoneDrivers)):
                selectedOrder, j = BaseAlgorithm.findBestOrder(zoneOrders, zoneIdleTimeMap, oracle, instance['taxiWatchdog'],
                                              currentTimeOffset, zoneDriverCount)
                if zoneDrivers[i] != {} and selectedOrder != {}:
                    driver.serveOrder(zoneDrivers[i], selectedOrder, currentTimeOffset, instance['mapZone'])

                    # Distance = mapZone[selectedOrder['startZoneID'] - 1][selectedOrder['endZoneID'] - 1]
                    # AlgorithmEngine.set_value('RealTotalDistance', AlgorithmEngine.get_value('RealTotalDistance', 0) + Distance)

                    zoneOrders.pop(j)
                    assignedDrivers[len(assignedDrivers)] = zoneDrivers[i]
                    TaxiDemandSupplyOracle.addTimeRecord(instance['taxiWatchdog'], selectedOrder['endZoneID'], currentTimeOffset + selectedOrder['endTime'] - selectedOrder['startTime'], 1)
                    zoneIdleTimeMap.pop(selectedOrder['endZoneID'])
                    zoneDriverCount[selectedOrder['endZoneID']-1] = zoneDriverCount[selectedOrder['startZoneID']-1] - 1
            for i in range(len(assignedDrivers)):
                for j in range(len(zoneDrivers)):
                    if assignedDrivers[i]['id'] == zoneDrivers[j]['id']:
                        if not j == len(zoneDrivers)-1:
                            zoneDrivers[j], zoneDrivers[len(zoneDrivers)-1] = zoneDrivers[len(zoneDrivers)-1], zoneDrivers[j]
                        break
                zoneDrivers.pop(len(zoneDrivers)-1)
        # print(k, len(zoneOrders), len(zoneDrivers))
        # print(k, len(orderIndex[k]), len(driverIndex[k]))

