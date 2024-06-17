import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('MyLogger'), '../core')))
import driver
import copy
import math
def swap(graph, priorityQ, index1, index2):
    # print(index1, index2)
    temp = priorityQ[index1]
    priorityQ[index1] = priorityQ[index2]
    graph[priorityQ[index2]]['queuePos'] = index1
    priorityQ[index2] = temp
    graph[temp]['queuePos'] = index2
    # print("swap", index1, index2, temp, priorityQ[index1], graph[priorityQ[index2]]['queuePos'], priorityQ[index2], graph[temp]['queuePos'])
    # print("swap", priorityQ[index2], graph[temp]['queuePos'])

def makeQueue(graph, forwpriorityQ, source, target):
    swap(graph, forwpriorityQ, 0, source)

def extractMin(graph, priorityQ, extractNum):
    vertex = priorityQ[0]
    size = len(priorityQ) - 1 - extractNum
    # print(vertex, size)
    swap(graph, priorityQ, 0, size)
    siftDown(0, graph, priorityQ, size)
    return vertex

def siftDown(index, graph, priorityQ, size):
    min = index
    # print("siftDown", min)
    # print("siftDown", min, 2 * index + 1, size, graph[priorityQ[index]]['dist'], graph[priorityQ[2 * index + 1]]['dist'])
    if 2 * index + 1 < size and graph[priorityQ[index]]['dist'] > graph[priorityQ[2 * index + 1]]['dist']:
        min = 2 * index + 1
    # print(2 * index + 2, size, graph[priorityQ[min]]['dist'], graph[priorityQ[2 * index + 2]]['dist'])
    if 2 * index + 2 < size and graph[priorityQ[min]]['dist'] > graph[priorityQ[2 * index + 2]]['dist']:
        min = 2 * index + 2
    # print(min)
    if min != index:
        swap(graph, priorityQ, min, index)
        siftDown(min, graph, priorityQ, size)

def changePriority(graph, priorityQ, index):
    # print(index, (index-1) // 2)
    t = (index-1) // 2
    if t < 0:
        t = 0
    # print("changePriority", index, (index-1) // 2, graph[priorityQ[index]]['dist'], graph[priorityQ[t]]['dist'])
    if (index-1) // 2 > -1 and graph[priorityQ[index]]['dist'] < graph[priorityQ[t]]['dist']:
        swap(graph, priorityQ, index, t)
        changePriority(graph, priorityQ, t)


def relaxEdges(graph, vertex, priorityQ, queue):
    vertexList = graph[vertex]['adjList']
    costList = graph[vertex]['costList']
    graph[vertex]['processed'] = True
    for i in range(len(vertexList)):
        temp = vertexList[i]
        cost = costList[i]
        # print(vertex, temp, cost, graph[temp]['dist'], graph[temp]['f_id'], graph[temp]['f_cost'], graph[temp]['queuePos'])
        if graph[temp]['dist'] > graph[vertex]['dist'] + cost:
            graph[temp]['dist'] = graph[vertex]['dist'] + cost
            graph[temp]['f_id'] = vertex
            graph[temp]['f_cost'] = cost
            changePriority(graph, priorityQ, graph[temp]['queuePos'])

def createGraph(graph, reverseGraph, forwPriorityQ, revPriorityQ):
    # print(len(graph))
    for i in range(len(graph)):
        graph[i]['queuePos'] = i
        graph[i]['processed'] = False
        graph[i]['dist'] = 1073741823
        # print(graph[i]['queuePos'], graph[i]['processed'], graph[i]['dist'])
        reverseGraph[i]['queuePos'] = i
        reverseGraph[i]['processed'] = False
        reverseGraph[i]['dist'] = 1073741823
        forwPriorityQ[i] = i
        revPriorityQ[i] = i

def shortestPath(graph, reverseGraph, forgraphprocessedVertices, revgraphprocessedVertices, source, target):
    distance = 2147483647
    best = -1
    path = {}
    for i in range(len(forgraphprocessedVertices)):
        vertex = forgraphprocessedVertices[i]
        if reverseGraph[vertex]['dist'] + graph[vertex]['dist'] < 0:
            continue
        tempdist = graph[vertex]['dist'] + reverseGraph[vertex]['dist']
        if distance > tempdist:
            distance = tempdist
            best = vertex

    for i in range(len(revgraphprocessedVertices)):
        vertex = revgraphprocessedVertices[i]
        if reverseGraph[vertex]['dist'] + graph[vertex]['dist'] < 0:
            continue
        tempdist = reverseGraph[vertex]['dist'] + graph[vertex]['dist']
        if distance > tempdist:
            distance = tempdist
            best = vertex
    if distance > 2147483647//3:
        return None
    ID = best
    path1 = {}
    path1[len(path)] = ID
    while (ID != source):
        ID = graph[ID]['f_id']
        path1[len(path1)] = ID

    for i in range(len(path1)):
        path[i] = path1[len(path1) - 1 - i]
    ID = best
    while (ID != target):
        ID = reverseGraph[ID]['f_id']
        path[len(path)] = ID
    return path


def dijkstra_lengths(N, S, distanceFromSource, graph):
    comp = {}
    prevNode = {}
    for i in range(N):
        prevNode[len(prevNode)] = -1
        distanceFromSource[len(distanceFromSource)] = 1000000
    distanceFromSource[S] = 0
    dj = {}
    dj[len(dj)] = S
    while dj != {}:
        x = dj[len(dj)-1]
        if distanceFromSource[x] >= 1000000:
            break

        for i in range(len(graph[x]['adjList'])):
            v = graph[x]['adjList'][i]
            alt = distanceFromSource[x] + graph[x]['costList'][i]
            if alt < distanceFromSource[v]:
                distanceFromSource[v] = alt
                dj[v] = -1 * alt
                prevNode[v] = u

    for i in range(N):
        if distanceFromSource[i] >= 1000000:
            distanceFromSource[i] = 1000000
            prevNode[i] = -1



def computePath(graph, reverseGraph, s, t):
    forwPriorityQ = {}
    revPriorityQ = {}

    createGraph(graph, reverseGraph, forwPriorityQ, revPriorityQ)

    graph[s]['dist'] = 0
    # print(graph[s])
    reverseGraph[t]['dist'] = 0
    # print(reverseGraph[t])
    makeQueue(graph, forwPriorityQ, s, t)
    makeQueue(reverseGraph, revPriorityQ, t, s)

    forgraphprocessedVertices = {}
    revgraphprocessedVertices = {}
    queue={}
    # print(len(graph))
    for i in range(len(graph)):

        vertex1 = extractMin(graph, forwPriorityQ, i)
        # print(vertex1)
        # print(graph[vertex1]['dist'])
        if graph[vertex1]['dist'] == 2147483647:
            continue


        relaxEdges(graph, vertex1, forwPriorityQ, queue)
        forgraphprocessedVertices[len(forgraphprocessedVertices)] = vertex1

        if reverseGraph[vertex1]['processed'] == True:
            return shortestPath(graph, reverseGraph, forgraphprocessedVertices, revgraphprocessedVertices, s, t)

        revVertex = extractMin(reverseGraph, revPriorityQ, i)
        if reverseGraph[revVertex]['dist'] == 2147483647:
            continue

        relaxEdges(reverseGraph, revVertex, revPriorityQ, queue)

        revgraphprocessedVertices[len(revgraphprocessedVertices)] = revVertex


        if graph[revVertex]['processed'] == True:
            return shortestPath(graph, reverseGraph, forgraphprocessedVertices, revgraphprocessedVertices, s, t)

    return None

def current_loc(l1, l2, cacheSP, graph, edges, reverseGraph, start_time, current_time, current_path):
    # key = l1 + "-" + l2
    # path
    # path = cacheSP[l1][l2]
    if l1 in cacheSP and l2 in cacheSP[l1]:
        path = cacheSP[l1][l2]
    else:
        path = computePath(graph, reverseGraph, l1, l2)
        if l1 in cacheSP:
            cacheSP[l1][l2] = path
        else:
            cacheSP[l1] = {}
            cacheSP[l1][l2] = path
    time_all = start_time
    flag = True
    current = {}
    for i in range(len(path)-1):
        if flag == True:
            if time_all >= current_time:
                # current = {}
                current[0] = path[i]
                current[1] = time_all
                current_path[len(current_path)] = current
                flag = False
        else:
            current1 = {}
            current1[0] = path[i]
            current1[1] = time_all
            current_path[len(current_path)] = current1
        time_all += edges[str(path[i])][str(path[i + 1])][0]
    current1 = {}
    current1[0] = path[i+1]
    current1[1] = time_all
    current_path[len(current_path)] = current1
    if flag==True:
        return current_path[len(current_path)-1]
    else:
        return current


def relaxEdge(graph, vertex, str, queryId, forwQ, revQ):
    if str == "f":
        vertexList = graph[vertex]['outEdges']
        costList = graph[vertex]['outECost']
        graph[vertex]['processed']['forwProcessed'] = True
        graph[vertex]['processed']['forwqueryId'] = queryId
        # print(vertex)
        for i in range(len(vertexList)):
            temp = vertexList[i]
            cost = costList[i]
            # print(temp, cost)
            # print(graph[vertex]['orderPos'], graph[temp]['orderPos'])
            if graph[vertex]['orderPos'] < graph[temp]['orderPos']:
                # print(graph[temp]['distance']['forwqueryId'], graph[vertex]['distance']['forwqueryId'])
                # print(graph[temp]['distance']['queryDist'], graph[vertex]['distance']['queryDist'] + cost)
                if graph[vertex]['distance']['forwqueryId'] != graph[temp]['distance']['forwqueryId'] or \
                    graph[temp]['distance']['queryDist'] > graph[vertex]['distance']['queryDist'] + cost:
                    graph[temp]['distance']['forwqueryId'] = graph[vertex]['distance']['forwqueryId']
                    graph[temp]['distance']['queryDist'] = graph[vertex]['distance']['queryDist'] + cost
                    t = 0
                    # print(forwQ)
                    for j in range(len(forwQ)-1):
                        if t == 0:
                            if forwQ[j] == graph[temp]:
                                # print("true")
                                forwQ[j] = forwQ[j+1]
                                t = 1
                        else:
                            forwQ[j] = forwQ[j + 1]
                    if t == 1:
                        forwQ.pop(len(forwQ)-1)
                    t = 0
                    temp1 = {}
                    for j in range(len(forwQ)):
                        if t == 0:
                            if forwQ[j]['distance']['queryDist'] < graph[temp]['distance']['queryDist']:
                                temp1 = copy.deepcopy(forwQ[j])
                                forwQ[j] = copy.deepcopy(graph[temp])
                                t = 1
                        else:
                            temp1, forwQ[j] = forwQ[j], temp1
                    if t == 1:
                        forwQ[len(forwQ)] = copy.deepcopy(temp1)
                    else:
                        forwQ[len(forwQ)] = copy.deepcopy(graph[temp])
                        # forwQ[len(forwQ)] = graph[temp]
                    # print(forwQ)

    else:
        vertexList = copy.deepcopy(graph[vertex]['inEdges'])
        costList = copy.deepcopy(graph[vertex]['inECost'])
        graph[vertex]['processed']['revProcessed'] = True
        graph[vertex]['processed']['revqueryId'] = queryId

        for i in range(len(vertexList)):
            temp = vertexList[i]
            cost = costList[i]
            if graph[vertex]['orderPos'] < graph[temp]['orderPos']:
                if graph[vertex]['distance']['revqueryId'] != graph[temp]['distance']['revqueryId'] or \
                        graph[temp]['distance']['revDistance'] > graph[vertex]['distance']['revDistance'] + cost:
                    graph[temp]['distance']['revqueryId'] = graph[vertex]['distance']['revqueryId']
                    graph[temp]['distance']['revDistance'] = graph[vertex]['distance']['revDistance'] + cost
                    # for i in range(len(revQ)):
                    #     if revQ[i] == graph[temp]:
                    #         revQ.pop(graph[temp])
                    #         revQ[i] = graph[temp]
                    #         break
                    t = 0
                    # print(forwQ)
                    for j in range(len(revQ) - 1):
                        if t == 0:
                            if revQ[j] == graph[temp]:
                                # print("true")
                                revQ[j] = revQ[j + 1]
                                t = 1
                        else:
                            revQ[j] = revQ[j + 1]
                    if t == 1:
                        revQ.pop(len(revQ) - 1)
                    # print(revQ)
                    # revQ[len(revQ)] = graph[temp]

                    t = 0
                    temp1 = {}
                    for j in range(len(revQ)):
                        if t == 0:
                            if revQ[j]['distance']['queryDist'] < graph[temp]['distance']['queryDist']:
                                temp1 = copy.deepcopy(revQ[j])
                                revQ[j] = copy.deepcopy(graph[temp])
                                t = 1
                        else:
                            temp1, revQ[j] = revQ[j], temp1
                    if t == 1:
                        revQ[len(revQ)] = copy.deepcopy(temp1)
                    else:
                        revQ[len(revQ)] = copy.deepcopy(graph[temp])

def computeDist(graph, source, target, queryID):
    # print(graph[source])
    graph[source]['distance']['queryDist'] = 0
    graph[source]['distance']['forwqueryId'] = queryID
    graph[source]['processed']['forwqueryId'] = queryID

    graph[target]['distance']['revDistance'] = 0
    graph[target]['distance']['revqueryId'] = graph[target]['distance']['revqueryId']
    graph[target]['processed']['revqueryId'] = queryID
    forwQ = {}
    revQ = {}
    forwQ[len(forwQ)] = copy.deepcopy(graph[source])
    # print(graph[source])
    revQ[len(revQ)] = copy.deepcopy(graph[target])
    # print(revQ)
    estimate = 2147483647

    while len(forwQ) != 0 or len(revQ) != 0:
        if len(forwQ) != 0:
            # vertex1 = forwQ[0]
            vertex1 = forwQ[len(forwQ)-1]
            forwQ.pop(len(forwQ) - 1)
            # print(vertex1['distance']['queryDist'], estimate)
            if vertex1['distance']['queryDist'] <= estimate:
                relaxEdge(graph, vertex1['vertexNum'], "f", queryID, forwQ, revQ)
            if vertex1['processed']['revqueryId'] == queryID and vertex1['processed']['revProcessed']:
                if vertex1['distance']['queryDist'] + vertex1['distance']['revDistance'] < estimate:
                    estimate = vertex1['distance']['queryDist'] + vertex1['distance']['revDistance']
        if len(revQ) != 0:
            vertex2 = revQ[len(revQ)-1]
            revQ.pop(len(revQ) - 1)
            # print(vertex2['distance']['revDistance'], estimate)
            if vertex2['distance']['revDistance'] <= estimate:
                relaxEdge(graph, vertex2['vertexNum'], "r", queryID, forwQ, revQ)
            if vertex2['processed']['revqueryId'] == queryID and vertex2['processed']['revProcessed']:
                if vertex2['distance']['revDistance'] + vertex2['distance']['queryDist'] < estimate:
                    estimate = vertex2['distance']['queryDist'] + vertex2['distance']['revDistance']
    # if estimate == 2147483647:
    #     return -1
    return estimate

def dis(l1, l2, instance, graph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop):
    # queryID = driver.get_value('count', 0)
    # t = graph
    # CHgraph = copy.deepcopy(t)

    queryID = 0
    # set_value('count', get_value('count', 0) + 1)
    # t = {}
    # t == graph
    # print("start")
    # print(graph[l1])
    # print(t[l1])
    # print(graph[l2])

    # print(l1, l2)
    if l1 == l2:
        return 0
    # print(str(l1) in distanceFrequentNodes)
    if str(l1) in distanceFrequentNodes and str(l2) in distanceFrequentNodes[str(l1)]:
    # if frequentPickup[l1] and frequentDrop[l2]:

        # if l1 == 45473 and l2 == 33813:
        # print(1)
        # print("test", l1, l2, distanceFrequentNodes[str(l1)][str(l2)])
        return distanceFrequentNodes[str(l1)][str(l2)]

    if l1 in cacheSD and l2 in cacheSD[l1]:
        # if l1 == 45473 and l2 == 33813:
        # print(2)
        path = cacheSD[l1][l2]
    else:
        # print(3)
        path = computeDist(graph, l1, l2, queryID)
        # print(path)
        # time_all = 0
        if path == 2147483647 or path == 0:
            path1 = computePath(instance['graph'], instance['reverseGraph'], l1, l2)
            # print(len(path1))
            time_all = 0
            for node in range(len(path1)-1):
                # print()
                time_all = time_all + instance['edges'][str(path1[node])][str(path1[node+1])][0]
            path = time_all
        if path == 0:

        # print(path)
            result_dir = "../resources/raw_data/"
            files = "ny_graph_h_j.json"
            filePath = result_dir + files
            with open(filePath, 'r', encoding='utf8') as fp:
                graph = json.load(fp)
                if fp:
                    fp.close()
            path = computeDist(graph, l1, l2, queryID)
        if l1 in cacheSD:
            cacheSD[l1][l2] = path
        else:
            cacheSD[l1] = {}
            cacheSD[l1][l2] = path
        # print(path)
    return path



def racost(idx1, idx2, length):
    cost = 0
    t = 0
    s = "s"
    e = "e"
    if idx2 == idx1:
        if idx1 == length:
            while t < length - 1:
                print(t, t + 1)
                t = t + 1
            print(t, s)
            print(s, e)
        else:
            while t < length-1:
            # for i in range(len(driver['temp_route'])):
                if idx1 == t + 1:
                    print(t, s)
                    t = t+1
                    print(s, e)
                    if t != length:
                        print(e, t)
                else:
                    print(t,t+1)
                    t = t+1
    else:
        while t < length-1:
            if idx1 == t + 1:
                print(t, s)
                t = t + 1
                print(s, t)
            elif idx2 == t + 1:
                    print(t, e)
                    t = t + 1
                    print(e, t)

            else:
                print(t, t+1)
                t = t+1
        if idx2 == length:
            print(t, e)
    return cost

def getDistance(x, y):
    t1 = (float(x['longitude']) - float(y['longitude'])) ** 2
    t2 = (float(x['latitude']) - float(y['latitude'])) ** 2
    # print(t1,t2)
    sum = t1 + t2
    # print(sum)
    sqrt = math.sqrt(sum)
    # print(sqrt)
    return sqrt * 100000

if __name__ == '__main__':
    # computePath

    result_dir = "../resources2/raw_data/"
    files = "ny_graph_o_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        graph = json.load(fp)
        print('这是文件中的json数据：', graph[1])
        print('这是读取到文件数据的数据类型：', type(graph))

    result_dir = "../resources2/raw_data/"
    files = "ny_graph_r_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        reverseGraph = json.load(fp)
        print('这是文件中的json数据：', reverseGraph[1])
        print('这是读取到文件数据的数据类型：', type(reverseGraph))
        # for i in range(len(json_data)):
        #     print(json_data[i])
    result_dir = "../resources2/raw_data/"
    files = "ny_edges_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        edges = json.load(fp)
        print('这是文件中的json数据：', edges[str(1)])
        print('这是读取到文件数据的数据类型：', type(edges))

    result_dir = "../resources2/raw_data/"
    files = "ny_fre_dis.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        distanceFrequentNodes = json.load(fp)
        print(len(distanceFrequentNodes))
        print('这是文件中的json数据：', distanceFrequentNodes[str(3585)])
        print('这是读取到文件数据的数据类型：', type(distanceFrequentNodes))

    result_dir = "../resources2/raw_data/"
    files = "ny_fre_pick.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        frequentPickup = json.load(fp)
        print(len(frequentPickup))
        print('这是文件中的json数据：', frequentPickup[1])
        print('这是读取到文件数据的数据类型：', type(frequentPickup))

    result_dir = "../resources2/raw_data/"
    files = "ny_fre_drop.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        frequentDrop = json.load(fp)
        print(len(frequentDrop))
        print('这是文件中的json数据：', frequentDrop[1])
        print('这是读取到文件数据的数据类型：', type(frequentDrop))

    result_dir = "../resources2/raw_data/"
    files = "ny_graph_h_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        CHgraph = json.load(fp)
        print(len(CHgraph))
        print('这是文件中的json数据：', CHgraph[1])
        print('这是读取到文件数据的数据类型：', type(CHgraph))

    fileName2 = '../resources2/raw_data/ny_location'
    file2 = open(fileName2, "r", encoding='utf-8')
    file2lines = file2.readlines()
    ny_location = {}
    for i in range(len(file2lines)):
        point = {}
        npLocation = file2lines[i].split('\n')[0].split(',')
        point['longitude'] = float(npLocation[1])
        point['latitude'] = float(npLocation[2])
        ny_location[i] = point

    result_dir = "../resources2/raw_data/"
    files = "ny_edges_j.json"
    filePath = result_dir + files
    with open(filePath, 'r', encoding='utf8') as fp:
        edges = json.load(fp)
        print('这是文件中的json数据：', edges[str(1)])
        print('这是读取到文件数据的数据类型：', type(edges))

    instance = {}
    instance['graph'], instance['reverseGraph'] = graph, reverseGraph
    cacheSD = {}
    instance['edges'] = edges
    for i in range(len(ny_location)):
        sum = 0
        for j in range(len(ny_location)):
            distance = getDistance(ny_location[i], ny_location[j])
            # dis1 = dis(i+1, j+1, instance, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop)
            if distance>6000 and distance < 8000:

                dis1 = dis(i + 1, j + 1, instance, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup,
                           frequentDrop)
                if dis1 <240:
                    print(distance, dis1)
                sum = sum + 1
        print(sum)
    # path = computePath(graph, reverseGraph, 2158, 52180)
    # current_path = {}
    # # for i in range(len(path)-1):
    # #     current = {}
    # #     current[0] = path[i]
    # #     current[1] = edges[str(path[i])][str(path[i+1])][0]
    # #     current_path[i] = current
    # # print(current_path)
    # start_time = 10
    # current_time = 20
    # cacheSP = {}
    # current = current_loc(2158, 52180, cacheSP, graph, edges, reverseGraph, start_time, current_time, current_path)
    # print(current)
    # print(current_path)
    # print(cacheSP)
    print()
    # racost(1, 3, 4)
    # cacheSD = {}
    # count = 0

    # dis(l1, l2, graph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop)

    # print(dis(30768   , 14127 , CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    print(dis(25887, 42583, instance, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # print(dis(42583, 13724, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # print(dis(25887 , 13724, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # # # result_dir = "../resources/raw_data/"
    # # # files = "ny_graph_h_j.json"
    # # # filePath = result_dir + files
    # # # with open(filePath, 'r', encoding='utf8') as fp:
    # # #     CHgraph = json.load(fp)
    # print(dis(33813, 32458, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # print(dis(4300 , 44769, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # print(dis(25796, 44769, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))
    # print(dis(4300, 44769, CHgraph, cacheSD, distanceFrequentNodes, frequentPickup, frequentDrop))


    # print(count)
    # print(computeDist(CHgraph, 14997, 18907, 0))


