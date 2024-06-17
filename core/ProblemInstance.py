
# orders
# drivers
# driverCount
# orderOracle
# orderReal
# taxiWatchdog
# info
def ProblemInstance(instance, need):
    tmpInstance = {}
    tmpInstance['info'] = instance['info']
    tmpInstance['startRunningMillis'] = 0
    tmpInstance['endRunningMillis'] = 0
    tmpInstance['solverName'] = {}
    tmpInstance['orderOracle'] = instance['orderOracle']
    tmpInstance['orderReal'] = instance['orderReal']
    tmpInstance['taxiWatchdog'] = instance['taxiWatchdog']
    tmpInstance['orders'] = instance['orders']
    tmpInstance['drivers1'] = instance['drivers']

    # tmpInstance['zoneToZone'] = instance['zoneToZone']
    tmpInstance['velocity'] = instance['velocity']
    # tmpInstance['mapZone'] = instance['mapZone']

    tmpInstance['cacheSD'] = instance['cacheSD']
    tmpInstance['cacheSP'] = instance['cacheSP']
    tmpInstance['graph'] = instance['graph']
    tmpInstance['reverseGraph'] = instance['reverseGraph']
    tmpInstance['edges'] = instance['edges']
    tmpInstance['distanceFrequentNodes'] = instance['distanceFrequentNodes']
    tmpInstance['frequentPickup'] = instance['frequentPickup']
    tmpInstance['frequentDrop'] = instance['frequentDrop']
    tmpInstance['CHgraph'] = instance['CHgraph']
    tmpInstance['CHgraph1'] = instance['CHgraph1']
    tmpInstance['ny_location'] = instance['ny_location']
    tmpInstance['time_list'] = instance['time_list']
    tmpInstance['node2region'] = instance['node2region']
    if need == 1:
        tmpInstance['NodeRange'] = instance['NodeRange']
        tmpInstance['NodeRangeNode'] = instance['NodeRangeNode']
    # tmpInstance['NewMapData'] = instance['NewMapData']
    # tmpInstance['NewMapData2'] = instance['NewMapData2']
    tmpInstance['count'] = instance['count']
    tmpInstance['completedOrders'] = {}
    tmpInstance['expiredOrders'] = {}
    # print(tmpInstance['info'])
    # print(tmpInstance['startRunningMillis'])
    # print(tmpInstance['endRunningMillis'])
    # print(tmpInstance['solverName'])
    # print(tmpInstance['orderOracle'])
    # print(tmpInstance['orderReal'])
    # print(tmpInstance['taxiWatchdog'])
    # print(len(tmpInstance['orders']))
    # print(len(tmpInstance['drivers']))
    # print(len(tmpInstance['completedOrders']))
    return tmpInstance


def calculateTotalRevenue(drivers, orders):
    totalRevenue = 0
    for i in range(len(drivers)):
        for j in drivers["order"]:
            totalRevenue = totalRevenue + orders[j]["cost"]
    return totalRevenue

def calculateTotalDistance(drivers):
    totalDistance = 0
    for i in range(len(drivers)):
        for j in range(len(drivers[i]["orders"])):
            totalDistance = totalDistance + drivers[i]["orders"][j]["tripLength"]
    return totalDistance

def calculateTotalServingTime(drivers):
    totalTime = 0
    for i in range(len(drivers)):
        # for j in range(len(drivers[i]["orders"])):
            # totalTime = totalTime + drivers[i]["orders"][j]["endTime"] - drivers[i]["orders"][j]["startTime"]
        totalTime = totalTime + drivers[i]["serveTime"]
    return totalTime

def calculateTotalAssignedOrderCount(drivers):
    totalAssignedOrderCount = 0
    for i in range(len(drivers)):
        totalAssignedOrderCount = totalAssignedOrderCount + len(drivers[i]["orders"])
    return totalAssignedOrderCount
