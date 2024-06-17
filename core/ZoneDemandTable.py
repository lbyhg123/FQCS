from decimal import Decimal

def ZoneDemandTable():
    return initZoneDemandTable()

def initZoneDemandTable():
    zoneDemandTable = {}
    for i in range(46033):
        zoneDemandTable[i] = Decimal(0)
    return zoneDemandTable

def getTotalDemand():
    return 0

def getDemandDistribution():
    return 0

def addDemand():
    return 0

def getZoneDemand():
    return 0
