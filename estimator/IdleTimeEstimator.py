import math
from decimal import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../simulator')))
import Constants
import OrderDistribution
import numpy as np
from decimal import Decimal
positivate = 0

def estimateIdleTimeMix(lamda, mu, K):
    if lamda > mu:
        return estimateIdleTimeSimple(lamda, mu, K)
    else:
        return estimateIdleTime(lamda, mu, K)

# lookupLength = 5*60
def estimateIdleTimeSimple(lamda, mu, K):
    # print("start")
    if lamda == 0:
        # print(1)
        return Decimal(Constants.get_value("lookupLength")/6)

    if lamda >= mu:
        # print(2)
        OrderDistribution.add_value("moreOrder", 1)
        return Decimal(1/lamda)
    else:
        # print(3)
        OrderDistribution.add_value("moreDriver", 1)
        return Decimal(K/lamda + 1/lamda)

def estimateIdleTime(lamda, mu, K):
    idleTime = 0
    p0 = pZore(lamda, mu, K)
    # print(p0)
    if (lamda - mu) < 0.3 and (lamda - mu) > -0.3:
        idleTime = p0 * ((K+1)*(K+2) / np.array((2*float(lamda))) + positivate/np.array(float(lamda)))
    if lamda < mu:
        OrderDistribution.add_value("moreDriver", 1)
        # if lamda == 0E-29:
        t = np.array(float(mu)) / np.array(float(lamda))
        # print(((t - 1) ** 2 * float(lamda)) + p0 * positivate / float(lamda))
        idleTime = p0 * ((K + 1) * t ** (K + 2) - (K + 2) * t ** (K + 1) + 1) / \
                   ((t - 1) ** 2 * float(lamda)) + p0 * positivate / float(lamda)
        # print(idleTime)
        # else:
        #     t = np.array(mu) / np.array(lamda)
        #     idleTime = p0 * ((K+1) * t ** (K+2) - (K+2) * t ** (K+1) + 1) / \
        #            ((t - 1)**2 * lamda) + p0 * positivate/lamda
    if lamda > mu:
        OrderDistribution.add_value("moreOrder", 1)
        idleTime = float(p0) * (float(mu) / np.array(float((lamda-mu))**2)) + positivate / np.array((float(lamda)))
    
    if lamda == 0:
        idleTime = Constants.get_value("lookupLength")
    else:
        if mu > lamda and not np.isfinite(float(idleTime)) or np.isnan(float(idleTime)):
            if np.isnan(float(idleTime)):
                idleTime = 1/lamda
            if not np.isfinite(float(idleTime)):
                idleTime = Constants.get_value("lookupLength")/60
    # print(idleTime)
    idleTime = Decimal(idleTime)
    # if idleTime > 300:
    #     idleTime = 299
    # print(idleTime)
    # print(lamda, mu, K, p0, idleTime)
    return idleTime


def estimateIdleTime1(lamda, mu, K):
    idleTime = 0
    p0 = pZore(lamda, mu, K)
    # print(p0)
    if (lamda - mu) < 0.3 and (lamda - mu) > -0.3:
        idleTime = p0 * ((K + 1) * (K + 2) / np.array((2 * float(lamda))) + positivate / np.array(float(lamda)))
    if lamda < mu:
        OrderDistribution.add_value("moreDriver", 1)
        # if lamda == 0E-29:
        t = np.array(float(mu)) / np.array(float(lamda))
        # print(((t - 1) ** 2 * float(lamda)) + p0 * positivate / float(lamda))
        idleTime = p0 * ((K + 1) * t ** (K + 2) - (K + 2) * t ** (K + 1) + 1) / \
                   ((t - 1) ** 2 * float(lamda)) + p0 * positivate / float(lamda)
        # print(idleTime)
        # else:
        #     t = np.array(mu) / np.array(lamda)
        #     idleTime = p0 * ((K+1) * t ** (K+2) - (K+2) * t ** (K+1) + 1) / \
        #            ((t - 1)**2 * lamda) + p0 * positivate/lamda
    if lamda > mu:
        OrderDistribution.add_value("moreOrder", 1)
        idleTime = float(p0) * (float(mu) / np.array(float((lamda - mu)) ** 2)) + positivate / np.array((float(lamda)))

    if lamda == 0:
        idleTime = Constants.get_value("lookupLength")
    else:
        if mu > lamda and not np.isfinite(float(idleTime)) or np.isnan(float(idleTime)):
            if np.isnan(float(idleTime)):
                idleTime = 1 / lamda
            if not np.isfinite(float(idleTime)):
                idleTime = Constants.get_value("lookupLength") / 60
    # print(idleTime)
    idleTime = Decimal(idleTime)
    # if idleTime > 300:
    #     idleTime = 299
    # print(idleTime)
    # print(lamda, mu, K, p0, idleTime)
    return idleTime


def pZore(lamda, mu, K):
    p0 = 1 / (np.array(float(pLeftBottom(lamda, mu, K))) + positivate)
    return p0


def pLeftBottom(lamda, mu, K):
    pLB = 0
    if lamda == mu:
        pLB = K + 1
    if lamda < mu:
        # print(mu)
        # print(lamda)
        # print(((mu /lamda) - 1))
        # print(lamda)
        # print(mu)
        # print(float(lamda))
        # print(float(mu))
        # print(np.array(mu))
        # print(np.array(lamda))
        # print(np.array(float(mu)) / np.array(float(lamda)))
        # print(lamda)
        # print(mu)
        if lamda == 0E-29:
            t = np.array(float(mu)) / np.array(float(lamda))
        else:
            t = np.array(mu) / np.array(lamda)
        if t ** (K + 1) - 1 == t - 1:
            pLB = K + 1
            return pLB
        # print((t ** (K + 1) - 1))
        # print((t - 1))
        pLB = (t ** (K + 1) - 1) / (t - 1)
        # pLB = ((mu /lamda) ** (K+1) - 1) / (mu /lamda - 1)

    if lamda > mu:
        pLB = float(mu) / np.array(float(lamda - mu))

    return pLB