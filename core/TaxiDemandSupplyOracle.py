import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../utils')))
import Constants
import ZoneDemandTable
from decimal import Decimal
frameTime = 30*60
def initialTimeFrames(frameTime):
    totalTime = 24 * 60 * 60
    currentTimeFrameHead = 0
    zoneDemandTables = {}
    i = 0
    while currentTimeFrameHead < totalTime:
        zoneDemandTables[i] = ZoneDemandTable.initZoneDemandTable()
        currentTimeFrameHead = currentTimeFrameHead + frameTime
        i = i + 1
    return zoneDemandTables
    # print(len(zoneDemandTables[0]))

def queryRate(orderOracle, startOffset, endOffset, zoneID):
    demand = queryDemand(orderOracle, startOffset, endOffset, zoneID)
    if endOffset <= startOffset:
        return 0
    else:
        return demand / (endOffset - startOffset)

def queryDemand(taxiWatchdog, startOffset, endOffset, zoneID):
    totalDemand = 0
    startIndex = int(startOffset / frameTime)
    endIndex = int(endOffset / frameTime)

    for i in range(startIndex, endIndex+1, 1):
        if i >= len(taxiWatchdog):
            break
        try:
            totalDemand += taxiWatchdog[i][zoneID-1]
        except:
            print(i, zoneID-1)
    # print(totalDemand)
    startAdjustRatio = (startOffset % frameTime) / frameTime
    endAdjustRatio = 1 - (endOffset % frameTime) / frameTime
    if startIndex < len(taxiWatchdog):
        totalDemand -= - Decimal(startAdjustRatio) * taxiWatchdog[startIndex][zoneID-1]
    if endIndex < len(taxiWatchdog):
        totalDemand -= Decimal(endAdjustRatio) * taxiWatchdog[endIndex][zoneID-1]
        # print(totalDemand)
    return totalDemand

def queryDemand1(taxiWatchdog, startOffset, endOffset, NodeRangeNode):
    totalDemand = 0
    startIndex = int(startOffset / frameTime)
    endIndex = int(endOffset / frameTime)

    for i in range(startIndex, endIndex+1, 1):
        if i >= len(taxiWatchdog):
            break
        for value in NodeRangeNode:
            totalDemand += taxiWatchdog[i][int(value)]
    # print(totalDemand)
    startAdjustRatio = (startOffset % frameTime) / frameTime
    endAdjustRatio = 1 - (endOffset % frameTime) / frameTime
    if startIndex < len(taxiWatchdog):
        for value in NodeRangeNode:
            totalDemand -= - Decimal(startAdjustRatio) * taxiWatchdog[startIndex][int(value)]
    if endIndex < len(taxiWatchdog):
        for value in NodeRangeNode:
            totalDemand -= Decimal(endAdjustRatio) * taxiWatchdog[endIndex][int(value)]
    # print(totalDemand)
    return totalDemand

def addTimeRecord(zoneDemandTables, zoneID, timeOffset, demand):
    index = int(timeOffset / frameTime)
    if index >= len(zoneDemandTables):
        return
    table = zoneDemandTables[index]
    table[zoneID-1] = table[zoneID-1] + demand

def removeTimeRecord(zoneDemandTables, zoneID, timeOffset, demand):
    index = int(timeOffset / frameTime)
    if index >= len(zoneDemandTables):
        return
    table = zoneDemandTables[index]
    table[zoneID-1] = table[zoneID-1] - demand
