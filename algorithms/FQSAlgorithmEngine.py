import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../simulator')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../algorithms')))
import IdleRatioGreedyAlgorithm
import MyLogger
import ProblemInstanceLoader
import ProblemInstance
import order
import DataBatchProvider
import BaseAlgorithm
import Constants
import OrderDistribution
import driver
day = 28
# round = 0
frameLength = 10
driverCount = 4*1000

def varyDriverCounts(seed):
    logger = MyLogger.MyLogger("varyingDriver.txt", seed, day)
    # MyLogger.MyLogger("varyingDriver.txt", seed)
    print(1)
    varyingDriver("DriversCount:1K", 1000, seed)
    # varyingDriver("DriversCount:2K", 2000, seed)
    # varyingDriver("DriversCount:3K", 3000, seed)
    # varyingDriver("DriversCount:4K", 4000, seed)
    # varyingDriver("DriversCount:5K", 5000, seed)

def varyingMaxWaitingTimes(seed):
    logger = MyLogger.MyLogger("varyingWaitingTime.txt", seed, day)
    varyingMaxWaitingTime("baseTime:60", 60, seed)
    varyingMaxWaitingTime("baseTime:120", 120, seed)
    varyingMaxWaitingTime("baseTime:180", 180, seed)
    varyingMaxWaitingTime("baseTime:240", 240, seed)
    varyingMaxWaitingTime("baseTime:300", 300, seed)

def varyFrameLength(seed):
    logger = MyLogger.MyLogger("varyingFrameLength.txt", seed, day)
    varyingFrameLength("FrameLength:3", 3, seed)
    varyingFrameLength("FrameLength:5", 5, seed)
    varyingFrameLength("FrameLength:10", 10, seed)
    varyingFrameLength("FrameLength:20", 20, seed)
    varyingFrameLength("FrameLength:30", 30, seed)

def varyingLookupLengths(seed):
    logger = MyLogger.MyLogger("varyingLookupLength.txt", seed, day)
    varyingLookupLength("lookup:300", 300, seed)
    varyingLookupLength("lookup:600", 600, seed)
    varyingLookupLength("lookup:900", 900, seed)
    varyingLookupLength("lookup:1200", 1200, seed)
    varyingLookupLength("lookup:2400", 2400, seed)
    varyingLookupLength("lookup:3600", 3600, seed)
    varyingLookupLength("lookup:4800", 4800, seed)
    varyingLookupLength("lookup:6000", 6000, seed)


def loadProblem(info , day , diverCount, seed):
    data = ProblemInstanceLoader.loadProblemInstance(day, diverCount, seed, 1)
    data["info"] = info
    # print(len(data['orders']))
    return data

def varyingDriver(info, driverCount, seed):
    data = loadProblem(info, day, driverCount, seed)
    Constants._init()
    Constants.set_value('lookupLength', 5 * 60)
    Constants.set_value('showlookupLength', 5 * 60)
    # Constants = {
    #     "showlookupLength": 5 * 60,
    #     "lookupLength": 5 * 60,
    # }
    # print(len(data['orders']))
    # print(data['info'])
    runAlgorithms(data,  frameLength)

def varyingFrameLength(info, framelenth, seed):
    data = loadProblem(info, day, 4000, seed)
    frameLength = framelenth
    Constants._init()
    Constants.set_value('lookupLength', 5 * 60)
    Constants.set_value('showlookupLength', 5 * 60)
    runAlgorithms(data, frameLength)

def varyingLookupLength(info, lookupLength, seed):
    data = loadProblem(info, day, 4000, seed)
    # frameLength = framelenth
    Constants._init()
    Constants.set_value('lookupLength', 5 * 60)
    Constants.set_value('showlookupLength', lookupLength)
    runAlgorithms(data, frameLength)

def varyingMaxWaitingTime(info, framelenth, seed):
    data = loadProblem(info, day, 4000, seed)
    frameLength = framelenth
    Constants._init()
    Constants.set_value('lookupLength', 5 * 60)
    Constants.set_value('showlookupLength', 5 * 60)
    runAlgorithms(data, frameLength)

def run(seed, frameLength):
    print(day)
    varyDriverCounts(seed)
    # varyingMaxWaitingTimes(seed)
    # varyFrameLength(seed)
    # varyingLookupLengths(seed)

def AlgorithmEngine(seed):
    np.random.seed(seed)
    BaseAlgorithm.run1()


def runAlgorithms(data, frameLength):
    # round += 1
    tmpInstance = ProblemInstance.ProblemInstance(data, 1)
    millisStart = time.perf_counter()
    lastInstance = {}
    currentInstance = {}
    s = 1
    DataBatchProvider._init()
    OrderDistribution._init()
    DataBatchProvider.set_value('currentTimeOffset', 0)
    DataBatchProvider.set_value('currentOrderIndex', 0)
    print(len(tmpInstance['orders']))
    driver._init()
    driver.set_value('RealTotalDistance', 0)
    driver.set_value('OracleTotalDistance', 0)
    driver.set_value('TotalDistance', 0)
    driver.set_value('count', 0)
    print(driver.get_value('RealTotalDistance', 0))
    print(driver.get_value('OracleTotalDistance', 0))
    print(driver.get_value('TotalWaitTime', 0))
    print(driver.get_value('count', 0))
    # print("currentTimeOffset:")
    # print(DataBatchProvider.get_value('currentTimeOffset'))
    # print(DataBatchProvider.get_value('currentOrderIndex'))
    # currentTimeOffset = 0
    # currentOrderIndex = 0
    print("frameLength: ")
    print(frameLength)
    # print("end")
    j=1
    # print(tmpInstance['orders'][5622])
    currentInstance = DataBatchProvider.fetchCurrentProblemInstance(tmpInstance, frameLength, 1)
    while currentInstance != {}:
        # print(len(currentInstance['drivers']),len(currentInstance['orders']),currentInstance['currentTimeOffset'])
        if lastInstance != {}:
            currentTimeOffset = currentInstance['currentTimeOffset']
            # print(len(currentInstance['drivers']))
            # # print(len(lastInstance['orders']))
            # print(len(currentInstance['orders']))
            # print("completedOrders")
            # print(len(tmpInstance['completedOrders']))
            # print(len(tmpInstance['expiredOrders']))
            # print(not order.isExpired(lastInstance['orders'][0], currentTimeOffset))
            # print(not order.isAssigned(lastInstance['orders'][0]))
            # print(not order.isExpired(lastInstance['orders'][0], currentTimeOffset) and not order.isAssigned(lastInstance['orders'][0]))
            for i in range(len(lastInstance['orders'])):
                # print(1)
                if not order.isExpired(lastInstance['orders'][i], currentTimeOffset) and not order.isAssigned(lastInstance['orders'][i]):
                    currentInstance['orders'][len(currentInstance['orders'])] = lastInstance['orders'][i]
                if order.isAssigned(lastInstance['orders'][i]):
                    tmpInstance['completedOrders'][len(tmpInstance['completedOrders'])] = lastInstance['orders'][i]
                if not order.isAssigned(lastInstance['orders'][i]) and order.isExpired(lastInstance['orders'][i], currentTimeOffset):
                    tmpInstance['expiredOrders'][len(tmpInstance['expiredOrders'])] = lastInstance['orders'][i]
            if currentInstance["currentTimeOffset"] % 100 == 0:

                servingTime = ProblemInstance.calculateTotalServingTime(tmpInstance['drivers1'])

            j = j + 1
        # print(1)
        BaseAlgorithm.run3(currentInstance, j)
        lastInstance = currentInstance
        tmpInstance["currentTimeOffset"] = currentInstance["currentTimeOffset"]
        currentInstance = DataBatchProvider.fetchCurrentProblemInstance(tmpInstance, frameLength, 1)
    millisEnd = time.perf_counter()
    tmpInstance["info"] = "myAlgorithm" + ":" + tmpInstance["info"]
    tmpInstance["startRunningMillis"] = millisStart
    tmpInstance["endRunningMillis"] = millisEnd
    MyLogger.logResult(tmpInstance, "myalgorithm")


if __name__ == '__main__':
    seed = 1
    # print(1)
    for i in range(7, 8, 1):
        # day = i
        seed = i
        run(seed, frameLength)
    # day = 2
    # run(seed, frameLength)