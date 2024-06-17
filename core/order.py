




def assignDriver(order, driver):
    order['driver'] = driver
    return order

def withdrawDriver(order , driver):
    if order['driver'] != {} and order['driver'] != driver:
        print("Bad withdraw driver")
    else:
        order['driver'] = {}

def isAssigned(order):
    # print(order['driver'])
    if order['driver'] != {}:
        return True
    else:
        return False
def isExpired(order, currentTimeOffset):
    if order['startTime'] + order['maxWaitTime'] > currentTimeOffset:
        return False
    else:
        return True