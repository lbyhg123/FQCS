import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import json
from scipy.spatial.distance import cdist


def __line_magnitude(x1, y1, x2, y2):
    lineMagnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    return lineMagnitude


def __point_to_line_distance(point, line):
    px, py = point
    x1, y1, x2, y2 = line
    line_magnitude = __line_magnitude(x1, y1, x2, y2)
    if line_magnitude < 0.00000001:
        return 9999
    else:
        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (line_magnitude * line_magnitude)
        if (u < 0.00001) or (u > 1):
            ix = __line_magnitude(px, py, x1, y1)
            iy = __line_magnitude(px, py, x2, y2)
            if ix > iy:
                distance = iy
            else:
                distance = ix
        else:
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance = __line_magnitude(px, py, ix, iy)
        return distance

def MillierConvertion(lon, lat):
     L = 6381372*np.pi*2
     W = L
     H = L/2
     mill = 2.3
     x = float(lon)*np.pi/180
     y = float(lat)*np.pi/180
     y = 1.25*np.log(np.tan(0.25*np.pi+0.4*y))
     x = (W/2)+(W/(2*np.pi))*x
     y = (H/2)-(H/(2*mill))*y
     # dou = [x/1000,y/1000]
     return x/1000, y/1000

def get_distance_point2line(point, line):
    line_point1, line_point2 = np.array(line[0:2]), np.array(line[2:])
    # print(point)
    # print(line_point1, line_point2)
    vec1 = line_point1 - point
    vec2 = line_point2 - point
    # print(vec2)
    # print(vec1)
    # print(np.cross(vec1, vec2))
    # print(np.abs(np.cross(vec1, vec2)))
    # print(np.linalg.norm(line_point1 - line_point2))
    distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
    return distance * 100000



def deal_line(point2, point3):
    line = [float(point2['longitude']), float(point2['latitude']), float(point3['longitude']), float(point3['latitude'])]
    return line

def deal_point(point1):
    point = [float(point1['longitude']), float(point1['latitude'])]
    return point

def deal_location(point1,point2, point3):

    point = [float(point1['longitude']), float(point1['latitude'])]
    line = [float(point2['longitude']), float(point2['latitude']), float(point3['longitude']),
            float(point3['latitude'])]

    return point,line

def getLinearEquation(p1x, p1y, p2x, p2y):
    # print(p1x, p1y, p2x, p2y)
    sign = 1
    a = p2y - p1y
    # print(a)
    if a < 0:
        sign = -1
        a = sign * a
    b = sign * (p1x - p2x)
    # print(b)
    c = sign * (p1y * p2x - p1x * p2y)
    # print(a, b, c)
    return a, b, c

def getDistance(x, y):
    t1 = (float(x['longitude'])-float(y['longitude'])) ** 2
    t2 = (float(x['latitude'])-float(y['latitude']))**2
    # print(t1,t2)
    sum = t1+t2
    # print(sum)
    sqrt = math.sqrt(sum)
    # print(sqrt)
    return sqrt*100000

def manhanttanDistance(x,y):
    # print("start")
    # print(x)
    # print(y)
    point = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    points = {}
    s = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    a, b, c = getLinearEquation(float(x['longitude']), float(x['latitude']), float(y['longitude']), float(y['latitude']))
    for i in range(20):
        if i % 2 == 0:
            t = random.random()
            if t<0.5:
                s[i] = -1
            else:
                s[i] = 1
        else:
            s[i] = 0
        # points[i]['select'] = t
    # print(s)
    # if float(x['longitude']) > float(y['longitude']):
    #     point[0] = float(y['longitude'])
    #     for i in range(18):
    #         if i % 2 == 0:
    #             t = random.uniform(float(y['longitude']), float(x['longitude']))
    #         point[i+1] = t
    #     point[19] = float(x['longitude'])
    #     point[20] = float(x['longitude'])
    # else:
    point[0] = float(x['longitude'])
    for i in range(18):
        if i % 2 == 0:
            t = random.uniform(float(y['longitude']), float(x['longitude']))
        point[i + 1] = t
    point[20] = float(y['longitude'])
    point[21] = float(y['longitude'])
    # print(s)
    # print(a, b, c)
    # print(point)
    if float(x['longitude']) > float(y['longitude']):
        point.sort(reverse=True)
    else:
        point.sort()
    point[0] = float(x['longitude'])
    point[19] = float(y['longitude'])
    point[20] = float(y['longitude'])
    # print("test")
    # print(point)
    k={}
    k['longitude'] = point[0]
    k['latitude'] = -1 * (a * point[0] + c) / b
    points[len(points)] = k
    for i in range(20):
        # t=len(points)
        # points[t] = i
        k = {}
        if s[i] == -1:
            k['longitude'] = point[i+1]
            k['latitude'] = -1 * (a * point[i] + c) / b
        if s[i] == 0:
            k['longitude'] = point[i + 1]
            k['latitude'] = -1 * (a * point[i+1] + c) / b
        if s[i] == 1:
            k['longitude'] = point[i]
            k['latitude'] = -1 * (a * point[i+1] + c) / b
        # print(k)
        points[len(points)] = k
    sum = 0
    for i in range(len(points)-1):
        sum = sum + getDistance(points[i], points[i+1])
    points[0]['time'] = 0
    timeadd = 0
    for i in range(0, len(points)-1):
        # print(timeadd, getDistance(points[i], points[i+1]))
        timeadd = getDistance(points[i], points[i+1]) + timeadd
        points[i+1]['time'] = timeadd/sum
    # print(points)
    # add = 0
    # k = {}
    # k['longitude'] = point[11]
    # k['latitude'] = -1 * (a * point[11] + c) / b
    return points



            # point1 = [float(x['longitude']), float(x['latitude'])]
    # point2 = [float(y['longitude']), float(y['latitude'])]
    # point3 = [float(x['longitude']), float(y['latitude'])]
    # point4 = [float(y['longitude']), float(x['latitude'])]

def getIsland(zone1, zone2, bridge, data,island):
    zoneIndex = {}
    zoneIndex[0] = zone1['LocationID']
    zoneIndex[1] = zone2['LocationID']
    # zoneIndex1 = {}
    for i in range(len(island)):
        if zone1['LocationID'] == island[i]['ZoneId']:
            for j in range(len(island[i]['crossArea'])):
                if zone2['Borough'] == island[i]['crossArea'][j]:
                    zoneIndex[0] = island[i]['crossId']
                    break
    for i in range(len(island)):
        if zone2['LocationID'] == island[i]['ZoneId']:
            for j in range(len(island[i]['crossArea'])):
                if zone1['Borough'] == island[i]['crossArea'][j]:
                    zoneIndex[1] = island[i]['crossId']
                    break
    return zoneIndex
    # zone = {}
    # print(zone1)
    # print(zone2)
    # print(island)
    # if zone1['LocationID'] == 103 or zone1['LocationID'] == 103 or zone1['LocationID'] == 103:
    # for i in range(len(island)):
    #     if island[i]['ZoneId'] == zone1['LocationID']:
    #         # print(i)
    #         # print(island[i])
    #         # print(len(island[i]['crossArea']))
    #         for j in range(len(island[i]['crossId'])):
    #             if zone2['Borough'] == island[i]['crossArea'][j]:
    #                 zone = manhanttanDistance(zone2, data[int(island[i]['crossId'][j])])
    #                 return zone
    #
    # return zone
# def getshortbridge(bridge,zone1,zone2):
#     shortdistance = 10000000000000
#     for i in range(len(bridge)):
#         if bridge[i]['StartZone']==zone1 and bridge[i]['EndZone']==zone2:

def getShortZone(bridge, zone1, zone2, data, map):
    # print("start")
    # print(zone1)
    # print(zone2)
    t = map[zone1['Borough']][zone2['Borough']]
    # print(t)
    distance = {}
    for j in range(len(t)):
        x = {}
        distance[j] = {}
        x['longitude'] = zone1['longitude']
        x['latitude'] = zone1['latitude']
        k = 0
        # for k in range(0,len(t[j])-1,1):
        while k < len(t[j])-1:
            # print(k)
            if t[j][k] == 'Queens' and t[j][k+1] == 'Brooklyn':
                if len(t[j])-1 == k+1:
                    break
                k = k + 1
            elif t[j][k] == 'Brooklyn' and t[j][k+1] == 'Queens':
                if len(t[j])-1 == k+1:
                    break
                k = k + 1
            # print(k)
            x['distance'] = 10000000000000
            x['point'] = -1
            # distance[j][len(distance[j])] = x
            # print(t[j][k])
            # print(t[j][k+1])
            # print(len(t[j])-1)
            for i in range(len(bridge)):
                if bridge[i]['StartZone'] == t[j][k] and bridge[i]['EndZone'] == t[j][k+1]:
                    # print(x)
                    # print(bridge[i])
                    # print(getDistance(x, bridge[i]))
                    if x['distance'] > getDistance(x, bridge[i]):
                        x['distance'] = getDistance(x, bridge[i])
                        x['point'] = i
            x['longitude'] = bridge[x['point']]['longitude']
            x['latitude'] = bridge[x['point']]['latitude']
            # print(x)
            distance[j][len(distance[j])] = x
            l = x['point']
            x = {}
            x['longitude'] = bridge[l]['longitude']
            x['latitude'] = bridge[l]['latitude']
            # print(distance)
            k = k + 1
    min = 10000000
    t=-1
    for i in range(len(distance)):
        sum = 0
        for j in range(len(distance[i])):
            sum = sum + distance[i][j]['distance']
        if sum < min:
            min = sum
            t = i
    # print(sum)
    # print(distance[t])
    # print(distance)
    # print(distance[10])
    return distance[t]




# 1.判断是不是本身，是的话data[i][j] ={}
# 2.判断是否在同一个地区是的话进入3否者进入4
# 3.判断是否隔着海，不隔直接计算，隔的话进入4
# 4.判断去可以到达目的地最近的桥，计算
# 40.635194, -74.196605 156 Staten Island
# 40.726977, -74.016934 231 Manhattan
def ZoneDeal(data, bridge1, island, map):
    datas = {}
    datas2 = {}
    datas3 = {}
    result_dir = "../resources/result/"
    files = "map_data13.txt"
    file = open(result_dir + files, "a", encoding='utf-8')

    for i in range(0, len(data)):
        # i = i
        for j in range(len(data)):
            # j= j
            print(i, j)
            # print(data[i], data[j])
            datas[j] = {}
            # print(data[i])
            # print(data[j])
            if i == j:
                datas[j] = {}
                # datas2[i] = datas
            else:
                if data[i]['island'] == 1 or data[j]['island'] == 1:
                    zoneIndex = getIsland(data[i], data[j], bridge1, data, island)
                else:
                    zoneIndex={}
                    zoneIndex[0] = i+1
                    zoneIndex[1] = j+1
                print(zoneIndex)
                if zoneIndex[0] == zoneIndex[1]:
                    # print(0)
                    datas[j] = {}
                elif data[zoneIndex[0]-1]['Borough'] == data[zoneIndex[1]-1]['Borough']:
                    # print(1)
                    datas[j] = manhanttanDistance(data[zoneIndex[0] - 1], data[zoneIndex[1] - 1])
                else:
                    # print("good")
                    # print(2)
                    sortZone = getShortZone(bridge1, data[zoneIndex[0] - 1], data[zoneIndex[1] - 1], data, map)
                    # print("good")
                    # print(data[zoneIndex[0] - 1])
                    # print(sortZone)
                    # print(data[zoneIndex[1] - 1])
                    if sortZone == {}:
                        datas[j] = manhanttanDistance(data[zoneIndex[0] - 1], data[zoneIndex[1] - 1])
                    else:
                        h = 0
                        datas[j] = manhanttanDistance(data[zoneIndex[0] - 1], sortZone[h])
                        while h < len(sortZone) - 1:
                            data2 = {}
                            data2 = manhanttanDistance(sortZone[h], sortZone[h + 1])
                            for n in range(len(data2)):
                                datas[j][len(datas[j])] = data2[n]
                            h = h+1
                        data2 = {}
                        data2 = manhanttanDistance(sortZone[h], data[zoneIndex[1] - 1])
                        for n in range(len(data2)):
                            datas[j][len(datas[j])] = data2[n]
                # print(datas[j])
                    # file = open(result_dir + files, "w", encoding='utf-8')
            # print(datas[j])
            # datas2={}
            # datas3 = {}
            # datas2[j] = datas[j]
            # datas3[i] = datas2
            # print(datas3)
            # templete = i + ":"""
            # file.write(json.dumps(datas3[i])+"\n")
            # # file.write('练习文本\n')
            # file.flush()
        datas2[i] = datas
        datas = {}
    # return datas2
    points_data = {}

    for i in range(0, 263):
        datas = {}
        for k in range(0, 263):
            print(i, k)
            # print(data[i], data[k])
            # if len(datas2[i][k]) ==60:
                # print(datas2[i][k])
            # print("start")
            points_data = {}
            zoneInstance = 0
            if len(datas2[i][k]) > 21:
                averge = 21 / len(datas2[i][k])
                for time in range(len(datas2[i][k])):
                    add1 = int((time) / 21) * averge
                    datas2[i][k][time]['time'] = datas2[i][k][time]['time'] * averge + add1
            # if len(datas2[i][k]) == 60:
            print(datas2[i][k])
            for t in range(len(datas2[i][k])-1):
                # print(i,k,t,len(datas2[i][k])-1)
                # print("start")
                # print(datas2[i][k][t])
                # print(datas2[i][k][t+1])
                # print(datas2[i][k][t], datas2[i][k][t+1])
                line = deal_line(datas2[i][k][t], datas2[i][k][t+1])
                line_instance = getDistance(datas2[i][k][t], datas2[i][k][t+1])
                # print(line_instance)
                # print(datas2[i][k][t]['time'], datas2[i][k][t+1]['time'])
                points_data[t] = {}
                points_data[t]['time'] = (datas2[i][k][t]['time'] + datas2[i][k][t + 1]['time']) / 2
                points_data[t]['all_instance'] = zoneInstance
                points_data[t]['zone'] = {}
                points_data[t]['instance'] = {}
                for j in range(len(data)):
                    point = deal_point(data[j])
                    # print(point)
                    # print("start")
                    # line_instance1 = getDistance(datas2[i][k][t], data[j])
                    # line_instance2 = getDistance(data[j], datas2[i][k][t + 1])
                    # point_line_instance = get_distance_point2line(point, line)
                    # print(point_line_instance)
                    point_line_instance = __point_to_line_distance(point, line) * 100000
                    # print(point_line_instance)
                    # print(t)
                    if point_line_instance < 1000:
                    # if point_line_instance < 1000 and \
                    #         (line_instance*2+point_line_instance) > (line_instance1 + line_instance2):
                    # if point_line_instance < 1000 and \
                    #         1000 > (point_line_instance + line_instance1 + line_instance2)/3:
                    #     print(point)
                    #     print(j)
                    #     print(point_line_instance)
                        points_data[t]['zone'][data[j]['LocationID']] = data[j]['LocationID']
                        points_data[t]['instance'][data[j]['LocationID']] = point_line_instance
                zoneInstance = zoneInstance + line_instance
            #     print(len(points_data))
            # print(points_data)
            # datas[k] = points_data
            # print(points_data)
            # print(len(points_data))
            # if len(points_data) != 0:
            #     print(len(points_data['instance']))
            template = "start_id: " + str(i) + ",end_id: " + str(k) + \
                       ",instance: " + str(zoneInstance) + \
                       ",cross_id: " + str(points_data) + "\n"
            file.write(template)
            # file.write('练习文本\n')
            file.flush()
        # datas3[i] = datas

    return datas3

# datas = {}
# datas2 = {}
# for i in range(10):
#     for j in range(10):
#         if i == j:
#             data = {}
#             datas[j] = {}
#             print(datas[0])
#             datas2[i] = datas
#             print(datas2[0][0])


df = pd.read_csv('../resources/raw_data/MapData.csv')
# LocationID  Borough  Zone service_zone longitude and latitude  island
df1 = pd.read_csv('../resources/raw_data/bridge.csv')
df2 = pd.read_csv('../resources/raw_data/island.csv')
# edges = pd.read_csv('../resources/raw_data/ny_location')
# vertices = pd.read_csv('../resources/raw_data/ny_edge')
# nyIndex = pd.read_csv('../resources/raw_data/ny_edge')
fileName3 = '../resources/raw_data/nyIndex'
file3 = open(fileName3, "r", encoding='utf-8')
file3lines = file3.readlines()

fileName2 = '../resources/raw_data/ny_location'
file2 = open(fileName2, "r", encoding='utf-8')
file2lines = file2.readlines()

fileName = '../resources/raw_data/ny_nodes_j.json'
file1 = open(fileName, "r", encoding='utf-8')
file1lines = file1.read()

fileName4 = '../resources/result3/TestMap.txt'
file4 = open(fileName4, "r", encoding='utf-8')
file4lines = file4.readlines()

MapData = {}
bridge = {}
island = {}
ny_location = {}
np_edges = {}
# print(file2lines[0].split('\n')[0])
# for i in range(len(file2lines)):
#     point = {}

# print(close_list)
NewMapData = {}
print(file4lines[0])
for i in range(len(file4lines)):
    zoneMessage = {}
    # print(file4lines[i].split(','))
    # print(file4lines[i].split(',')[0].split(':')[1])
    zoneMessage['LocationID'] = int(file4lines[i].split(',')[0].split(':')[1])
    zoneMessage['Borough'] = file4lines[i].split(',')[1].split(':')[1]
    zoneMessage['longitude'] = float(file4lines[i].split(',')[2].split(':')[1])
    zoneMessage['latitude'] = float(file4lines[i].split(',')[3].split(':')[1])
    zoneMessage['island'] = int(file4lines[i].split(',')[4].split(':')[1])
    zoneMessage['NodeId'] = int(file4lines[i].split(',')[5].split(':')[1].split('\n')[0])
    NewMapData[i] = zoneMessage
    # print(NewMapData[i])
# file1lines = file1lines.split("{")[1].split("}")[0].split(",")
# npIndex = {}
# for i in range(len(file1lines)):
#     npIndex[int(file1lines[i].split(":")[0][1:-1])] = int(file1lines[i].split(":")[1])
#
# for i in range(len(file2lines)):
#     point = {}
#     npLocation = file2lines[i].split('\n')[0].split(',')
#     point['longitude'] = float(npLocation[1])
#     point['latitude'] = float(npLocation[2])
#     ny_location[npIndex[int(npLocation[0])]] = point

for i in range(len(file2lines)):
    point = {}
    npLocation = file2lines[i].split('\n')[0].split(',')
    point['longitude'] = float(npLocation[1])
    point['latitude'] = float(npLocation[2])
    ny_location[i] = point
print(len(ny_location))
print(ny_location[0])
print(file3lines[1])

for i in range(0, len(file3lines)-1):
    np_edges[i] = {}
    np_edges[i][i] = 0

for i in range(1, len(file3lines)):
    npEdge = file3lines[i].split('\n')[0].split(' ')
    # print(i)
    # print(npEdge)
    # print(npEdge[0], npEdge[1])
    # print(ny_location[int(npEdge[0])], ny_location[int(npEdge[1])])
    np_edges[int(npEdge[0])][int(npEdge[1])] = getDistance(ny_location[int(npEdge[0])], ny_location[int(npEdge[1])])
print(np_edges[40411])

# ③ 构建一系列函数以实现迭代功能

# 1、构建函数用来选择node_cost最小的节点
# 选择node_cost值最小的节点->node 0
def choose_min(node_cost, close_list):
    node_cost = np.array(node_cost)  # 将node_cost从list转换成array
    open_list = list(set(node_cost[:, 0].tolist()) - set(close_list))  # 建立一个open_list放入没有被遍历的点
    final_list = []
    for i in open_list:
        final_list.append(node_cost[int(i)].tolist())
    final_list = np.array(final_list)  # final_list转换成array，才可以利用np.where找最小值
    node0 = final_list[np.where(final_list[:, 1] == final_list[:, 1].min())][0][0]  # 将node_cost最小的点的节点名给node0
    return int(node0)


# -------------------------------------------------------------------------------------------------------
# 2、构建count_cost函数用来计算相邻节点的node_cost
# 计算node0邻节点的node_cost，此时的node_cost值就是地图上的代价值加上父节点的代价值，如果已经比原来小则更新node_cost和父节点
# 并将node0放入close_list里面
def count_cost(mapping_list, node_cost, close_list, node0, t):
    # print("good")
    # print(mapping_list)
    # print(node_cost)
    # print(close_list)
    # t = 1
    t = t + 1
    for i in mapping_list[int(node0)].keys():
        if mapping_list[node0][i] + node_cost[node0][1] < node_cost[i][1]:
            t = 0
            node_cost[i][2] = node0
            node_cost[i][1] = mapping_list[node0][i] + node_cost[node0][1]
            node_cost[i][3] = node_cost[i][3] + 1
            print(node_cost[i])
            print(node_cost[i])
    close_list.append(node0)
    # print(node_cost)
    # print(close_list)
    return [node_cost, close_list, t]

# mapping_list = [[np.inf for i in range(0, 61298)] for i in range(0, 61298)]  # 构建全是无穷大的二维列表
# print("goods")
# for i in range(0, 61298):
#     mapping_list[i][i] = 0  # 对角线处的值为0
# for i in range(1, len(file3lines)):
#     npEdge = file3lines[i].split('\n')[0].split(' ')
#     mapping_list[int(npEdge[0])][int(npEdge[1])] = getDistance(ny_location[int(npEdge[0])], ny_location[int(npEdge[1])])
# print(mapping_list[40411][44303])
# mapping_list = np.array(mapping_list)

# result_dir = "../resources/result3/"
# files11 = "TestMapData.txt"
# file10 = open(result_dir + files11, "a", encoding='utf-8')

def Dijkstra(x, y, mapping_list):
    # ② 初始化
    node_cost = [[np.inf for i in range(0, 4)] for i in range(0, 61298)]  # 构建全是无穷大的二维列表
    for i in range(0, 61298):
        node_cost[i][0] = i
        node_cost[i][3] = 0
    node0 = x
    close_list = []
    # print(1)
    # print(node_cost[0])
    # print(node_cost[0][1])
    # for i in range(61298):
    #     # if node_cost[0][1] == "inf":
    #     if not np.isinf(float(node_cost[0][1])):
    #         print(node_cost[i][0])
    for i in mapping_list[int(node0)].keys():
        # print(mapping_list[int(node0)][i], node_cost[i][1])
        if mapping_list[int(node0)][i] < node_cost[i][1]:
            node_cost[i][2] = node0
            node_cost[i][1] = mapping_list[int(node0)][i]
            node_cost[i][3] = node_cost[i][3] + 1
            # print(node_cost[i])
    close_list.append(int(node0))
    # print(2)
    # for i in range(61298):
    #     # if node_cost[0][1] == "inf":
    #     if not np.isinf(float(node_cost[0][1])):
    #         print(node_cost[i][0])
    # ④ 开始迭代----->迭代中止的条件：终点在close_list里面
    t = 0
    while y not in close_list:
    # while t < 200000:
    # t = 0
    # while t != 1:
        # print(node_cost)
        # print(close_list)
        # print(1)
        node0 = choose_min(node_cost, close_list)  # 找node_cost最小的节点
        # print(node0)
        [node_cost, close_list, t] = count_cost(mapping_list, node_cost, close_list, node0, t)  # 计算邻节点
        # print(close_list)
    xn = y
    x0 = x
    # print(node_cost[0])
    # print(node_cost[0][0])
    destination_list = [xn]
    print("最短的路径代价为:", node_cost[xn][1])
    while x0 not in destination_list:
        xn = node_cost[xn][2]
        destination_list.append(xn)
    print("最短路径为：", destination_list)
    return node_cost, node_cost[xn][1], destination_list


import sys  # 导入sys模块
sys.setrecursionlimit(60000)  # 将默认的递归深度修改为3000

# 找到一条从start到end的路径
def findPath(graph, start, end, path=[]):
    path = path + [start]
    # # print(path)
    # print(start)
    # print(end)
    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath:
                return newpath
    return None


# 找到所有从start到end的路径
def findAllPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]

    paths = []  # 存储所有路径
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPath(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


# 查找最短路径
def findShortestPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path

    shortestPath = []
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath:
                if not shortestPath or len(newpath) < len(shortestPath):
                    shortestPath = newpath
    return shortestPath


# graph = {'A': ['B', 'C', 'D'],
#          'B': ['E'],
#          'C': ['D', 'F'],
#          'D': ['B', 'E', 'G'],
#          'E': [],
#          'F': ['D', 'G'],
#          'G': ['E']}
# print(NewMapData[1]['NodeId'], NewMapData[7]['NodeId'])
# onepath = findPath(np_edges, NewMapData[1]['NodeId'], NewMapData[7]['NodeId'])
# print('一条路径:', onepath)
#
# allpath = findAllPath(np_edges, NewMapData[1]['NodeId'], NewMapData[7]['NodeId'])
# print('\n所有路径：', allpath)
#
# shortpath = findShortestPath(np_edges, NewMapData[1]['NodeId'], NewMapData[7]['NodeId'])
# print('\n最短路径：', shortpath)



print(NewMapData[0])
for i in range(3, 4):
    # max = 0
    # p = -1
    # for j in range(len(NewMapData)):
    #     if getDistance(NewMapData[i], NewMapData[j]) > max:
    #         max = getDistance(NewMapData[i], NewMapData[j])
    #         p = j
    p = 27
    print(NewMapData[i]['NodeId'], NewMapData[p]['NodeId'])
    node_costs, node_cost, destination_list = Dijkstra(NewMapData[i]['NodeId'], NewMapData[p]['NodeId'], np_edges)
    template = "StartId:" + str(NewMapData[i]['LocationID']) \
                + ",endId:" + str(NewMapData[p]['LocationID']) \
                       + ",node_cost:" + str(node_cost) \
                       + ",destination_list:" + str(destination_list) \
                       + "\n"
    result_dir = "../resources/result4/"
    files11 = str(i) + "_TestMapData.txt"
    file10 = open(result_dir + files11, "a", encoding='utf-8')
    print(template)
    file10.write(template)
    file10.write(str(node_costs))
    file10.close()


for i in range(44):
    x_list = df1['longitude and latitude'][i].split(", ")
    x={}
    x['StartId'] = df1['StartId'][i]
    x['StartZone'] = df1['StartZone'][i]
    x['EndId'] = df1['EndId'][i]
    x['EndZone'] = df1['EndZone'][i]
    # x['longitude'], x['latitude'] = MillierConvertion(x_list[0], x_list[1])
    x['longitude'] = x_list[0]
    x['latitude'] = x_list[1]
    bridge[i] = x
print(bridge[0])

for i in range(27):
    # x_list = df2['crossId'][i].split(",")
    y_list = df2['crossArea'][i].split(",")
    # x_cross = {}
    # for i in range(len(x_list)):
    #     x_cross[]
    x = {}
    x['ZoneId'] = df2['ZoneId'][i]
    x['ZoneArea'] = df2['ZoneArea'][i]
    x['crossId'] = df2['crossId'][i]
    x['crossArea'] = y_list
    island[i] = x

print(island[0])
for i in range(263):
    x_list = df['longitude and latitude'][i].split(", ")
    x = {}
    # MillierConvertion()
    x['LocationID'] = df['LocationID'][i]
    x['Borough'] = df['Borough'][i]
    # x['Zone'] = df['Zone'][i]
    # x['service_zone'] = df['service_zone'][i]
    # print(x_list[0], x_list[1])
    # x['longitude'], x['latitude'] = MillierConvertion(x_list[0], x_list[1])
    # print(x['longitude'], x['latitude'])
    x['longitude'] = x_list[0]
    x['latitude'] = x_list[1]
    if np.isnan(df['island'][i]):
        np.isnan(df['island'][i])
        x['island'] = 0
    else:
        x['island'] = 1
    MapData[i] = x

print(MapData[0], MapData[1])
# for i in range(len(MapData)):
x[len(MapData)] = 0



# result_dir = "../resources/result3/"
# files10 = "TestMap.txt"
# file = open(result_dir + files10, "a", encoding='utf-8')
# for i in range(len(MapData)):
#     max = 500
#     test_longitude = 0
#     test_latitude = 0
#     t = -1
#     for j in range(len(ny_location)):
#         if getDistance(MapData[i], ny_location[j]) < max:
#             max = getDistance(MapData[i], ny_location[j])
#             test_longitude = ny_location[j]['longitude']
#             test_latitude = ny_location[j]['latitude']
#             t = j
#             # print(MapData[i], ny_location[j])
#             # print(getDistance(MapData[i], ny_location[j]))
#     # print(max)
#     if max != 500:
#         # print(MapData[i])
#         MapData[i]['longitude'] = test_longitude
#         MapData[i]['latitude'] = test_latitude
#         # print(MapData[i])
#         x[i] = 1
#         template = "LocationID:" + str(MapData[i]['LocationID']) \
#                    + ",Borough:" + str(MapData[i]['Borough']) \
#                    + ",longitude:" + str(MapData[i]['longitude']) \
#                    + ",latitude:" + str(MapData[i]['latitude']) \
#                    + ",island:" + str(MapData[i]['island']) \
#                    + ",NodeId:" + str(t) \
#                    + "\n"
#         file.write(template)
#     else:
#         # print(max)
#         print(i)
        # template = "LocationID:" + str(MapData[i]['LocationID']) \
        #            + ",Borough:" + str(MapData[i]['Borough']) \
        #            + ",longitude:" + str(MapData[i]['longitude']) \
        #            + ",latitude:" + str(MapData[i]['latitude']) \
        #            + ",island:" + str(MapData[i]['island']) \
        #            + ",NodeId:" + str(t) \
        #            + "\n"
        # file.write(template)


# test = getDistance(MapData[0], MapData[1])
# print(test)
map = {'Bronx': {'Manhattan': {0: {0: 'Bronx', 1: 'Manhattan'}},
                 'Queens': {0: {0: 'Bronx', 1: 'Queens'}},
                'Brooklyn': {0: {0: 'Bronx', 1: 'Manhattan', 2: 'Brooklyn'},
                             1: {0: 'Bronx', 1: 'Queens', 2: 'Brooklyn'}},
                  'Staten Island': {0: {0: 'Bronx', 1: 'Manhattan', 2: 'Brooklyn', 3: 'Staten Island'},
                                    1: {0: 'Bronx', 1: 'Queens', 2: 'Brooklyn', 3: 'Staten Island'}}}
        , 'Manhattan': {'Brooklyn': {0: {0: 'Manhattan', 1: 'Brooklyn'}},
                        'Queens': {0: {0: 'Manhattan', 1: 'Queens'}},
                        'Bronx': {0: {0: 'Manhattan', 1: 'Bronx'}},
                  'Staten Island': {0: {0: 'Manhattan', 1: 'Brooklyn', 2: 'Staten Island'}}}
        , 'Queens': {'Manhattan': {0: {0: 'Queens', 1: 'Manhattan'}},
                     'Bronx': {0: {0: 'Queens', 1: 'Bronx'}},
                     'Brooklyn': {0: {0: 'Queens', 1: 'Brooklyn'}},
                  'Staten Island': {0: {0: 'Queens', 1: 'Brooklyn', 2: 'Staten Island'}}}
        , 'Brooklyn': {'Manhattan': {0: {0: 'Brooklyn', 1: 'Manhattan'}},
                       'Queens': {0: {0: 'Brooklyn', 1: 'Queens'}},
                'Bronx': {0: {0: 'Brooklyn', 1: 'Manhattan', 2: 'Bronx'},
                          1: {0: 'Brooklyn', 1: 'Queens', 2: 'Bronx'}},
                  'Staten Island': {0: {0: 'Brooklyn', 1: 'Staten Island'}}}
        , 'Staten Island': {'Brooklyn': {0: {0: 'Staten Island', 1: 'Brooklyn'}},
                            'Queens': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens'}}
                , 'Manhattan': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens'}},
                  'Bronx': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Manhattan', 3: 'Queens'},
                            1: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens', 3: 'Queens'}}}
        }

t = ZoneDeal(MapData, bridge, island, map)

# print(len(t))
# print(len(t[0]))
# print(t[0][1])
# print(df)
#
# Manhattan 12 to 105  middle(40.692179, -74.012133)
# Manhattan (12,209,45) to Brooklyn (195 , 33 ,256 )
# Manhattan (232,229,(74,194)) to Queens (145 , 193 ,8 )
# Manhattan ((74,194),74,42,42,120,127,153,128) to Bronx (168,168,247,119,119,136,220,220)

point, line = deal_location(MapData[0], MapData[1], MapData[2])
# print(getDistance(MapData[0], MapData[1]))
# point = [1, 0]
# line = [0, 0, 1, 1]
# print(point,line)
dis = get_distance_point2line(point, line)
print(dis)
point = [1, 0]
line = [0, 0, 1, 1]
dis = get_distance_point2line(point, line)
print(dis)
print("start")

# print(getDistance(float(MapData[0]['latitude']), float(MapData[0]['longitude']), float(MapData[1]['latitude']), float(MapData[1]['longitude'])))
# from math import radians, sin, cos, asin, sqrt
#
#


# lonlat1 = [[40.724697, -73.976470]]    # 经度、维度
# lonlat2 = [[40.703264, -74.015998]]   # 经度、维度
# distance = cdist(lonlat1,lonlat2,metric='euclidean')
# distance = list(list(list(distance))[0]*100000)[0]
# print("start")
# print(MapData[0], MapData[1])
# print(GetRealDistance(MapData[2], MapData[3]))
# print(getDistance(MapData[2], MapData[3]))


