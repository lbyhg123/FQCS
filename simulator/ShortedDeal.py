import math
import numpy as np
# result_dir = "../resources/result4/"
# files11 = str(i) + "_TestMapData.txt"
# file10 = open(result_dir + files11, "a", encoding='utf-8')
# print(template)
# file10.write(template)
# file10.write(str(node_costs))
# file10.close()
# fileName4 = '../resources2/raw_data/TestMap.txt'
# file4 = open(fileName4, "r", encoding='utf-8')
# file4lines = file4.readlines()
# NewMapData = {}
# print(file4lines[0])

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

def count_cost(mapping_list, node_cost, close_list, node0, t):
    t = t + 1
    for i in mapping_list[int(node0)].keys():
        if mapping_list[node0][i] + node_cost[node0][1] < node_cost[i][1]:
            t = 0
            node_cost[i][2] = node0
            node_cost[i][1] = mapping_list[node0][i] + node_cost[node0][1]
            # node_cost[i][3] = node_cost[i][3] + 1
            # print(node_cost[i])
            # print(node_cost[i])
    close_list.append(node0)
    return [node_cost, close_list, t]

def Dijkstra(x, y, mapping_list):
    # ② 初始化
    node_cost = [[np.inf for i in range(0, 3)] for i in range(0, 61298)]  # 构建全是无穷大的二维列表
    for i in range(0, 61298):
        node_cost[i][0] = i
        # node_cost[i][3] = 0
    node0 = x
    close_list = []
    for i in mapping_list[int(node0)].keys():
        if mapping_list[int(node0)][i] < node_cost[i][1]:
            node_cost[i][2] = node0
            node_cost[i][1] = mapping_list[int(node0)][i]
            # node_cost[i][3] = node_cost[i][3] + 1
    close_list.append(int(node0))
    t = 0
    # while y not in close_list:
    while node_cost[node0][1] < 1500:
        node0 = choose_min(node_cost, close_list)  # 找node_cost最小的节点
        # print(node_cost[node0][1])
        [node_cost, close_list, t] = count_cost(mapping_list, node_cost, close_list, node0, t)  # 计算邻节点
    xn = y
    x0 = x
    destination_list = [xn]
    # print(node_cost)
    # print("good")
    node_cost2 = []
    for i in range(len(node_cost)):
        if not np.isinf(float(node_cost[i][1])):
            node_cost2.append(node_cost[i])
            # print(node_cost[i])
    # print(node_cost2)
    # print(len(node_cost2))
    return node_cost2
    # print("最短的路径代价为:", node_cost[xn][1])
    # while x0 not in destination_list:
    #     xn = node_cost[xn][2]
    #     destination_list.append(xn)
    # print("最短路径为：", destination_list)
    # return node_cost, node_cost[xn][1], destination_list
import sys  # 导入sys模块
sys.setrecursionlimit(60000)  # 将默认的递归深度修改为3000


def end(x, y, node_cost):
    xn = y
    x0 = x
    # print(node_cost[0])
    # print(node_cost[0][0])
    # print(node_cost[xn][1])
    destination_list = [xn]
    cost_list = [node_cost[xn][1]]
    # print("最短的路径代价为:", node_cost[xn][1])
    if not np.isinf(float(node_cost[xn][1])):
        while x0 not in destination_list:
            xn = node_cost[xn][2]
            cost = node_cost[xn][1]
            destination_list.append(xn)
            cost_list.append(cost)
    else:
        print("1")
    # print("最短路径为：", destination_list)
    return destination_list, cost_list

def getDistance(x, y):
    t1 = (float(x['longitude'])-float(y['longitude'])) ** 2
    t2 = (float(x['latitude'])-float(y['latitude']))**2
    # print(t1,t2)
    sum = t1+t2
    # print(sum)
    sqrt = math.sqrt(sum)
    # print(sqrt)
    return sqrt*100000

# for i in range(len(file4lines)):
#     zoneMessage = {}
#     # print(file4lines[i].split(','))
#     # print(file4lines[i].split(',')[0].split(':')[1])
#     zoneMessage['LocationID'] = int(file4lines[i].split(',')[0].split(':')[1])
#     zoneMessage['Borough'] = file4lines[i].split(',')[1].split(':')[1]
#     zoneMessage['longitude'] = float(file4lines[i].split(',')[2].split(':')[1])
#     zoneMessage['latitude'] = float(file4lines[i].split(',')[3].split(':')[1])
#     zoneMessage['island'] = int(file4lines[i].split(',')[4].split(':')[1])
#     zoneMessage['NodeId'] = int(file4lines[i].split(',')[5].split(':')[1].split('\n')[0])
#     NewMapData[i] = zoneMessage
# print(NewMapData[0])



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

fileName3 = '../resources2/raw_data/nyIndex'
file3 = open(fileName3, "r", encoding='utf-8')
file3lines = file3.readlines()
np_edges = {}
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

# datas2 = {}
# datas3 = {}
# result_dir = "../resources/result/"
# files = "new_map_data3.txt"
# file = open(result_dir + files, "a", encoding='utf-8')

# for j in range(len(NewMapData)):
#     result_dir = "../resources/result4/"
#     files11 = str(j) + "_TestMapData.txt"
#     # fileName4 = '../resources/result3/TestMap.txt'
#     file4 = open(result_dir + files11, "r", encoding='utf-8')
#     file4lines = file4.readlines()
#     file4lines = file4lines[1].split('[')[2:]
#     node_cost = [[np.inf for i in range(0, 4)] for i in range(0, 61298)]
#     datas2[j] = {}
#     # datas3[j] = {}
#     # print("start")
#     for i in range(len(file4lines)):
#         # print(i)
#         # print(file4lines[1].split('[')[i+2].split(']')[0])
#         if not np.isinf(float(file4lines[i].split(']')[0].split(', ')[2])):
#             node_cost[i][0] = int(file4lines[i].split(']')[0].split(', ')[0])
#             node_cost[i][1] = float(file4lines[i].split(']')[0].split(', ')[1])
#             node_cost[i][2] = int(file4lines[i].split(']')[0].split(', ')[2])
#             node_cost[i][3] = int(file4lines[i].split(']')[0].split(', ')[3])
#         else:
#             node_cost[i][0] = int(file4lines[i].split(']')[0].split(', ')[0])
#             node_cost[i][3] = int(file4lines[i].split(']')[0].split(', ')[3])
#     # print(NewMapData[j])
#     # print(len(NewMapData))
#     for i in range(len(NewMapData)):
#         datas2[j][i] = {}
#         # datas3[j][i] = {}
#         print(j, i, NewMapData[j]['LocationID'], NewMapData[i]['LocationID'], NewMapData[j]['NodeId'], NewMapData[i]['NodeId'])
#         destination_list, cost_list = end(NewMapData[j]['NodeId'], NewMapData[i]['NodeId'], node_cost)
#         # print(NewMapData[j]['LocationID'], NewMapData[i]['LocationID'], NewMapData[j]['NodeId'], NewMapData[i]['NodeId'], destination_list, cost_list)
#         point1 = 0
#         k = 0
#         # print(len(destination_list))
#         # print(ny_location[destination_list[0]])
#         # print(NewMapData[j])
#         # while k < len(destination_list):
#         for k in range(len(destination_list)):
#             t = {}
#             t['Adjacent_nodes1'] = {}
#             t['Adjacent_nodes_distance'] = {}
#             for length in range(len(NewMapData)):
#                 if getDistance(NewMapData[length], ny_location[destination_list[len(destination_list) - 1 - k]]) < 1000:
#                     t['Adjacent_nodes1'][len(t['Adjacent_nodes1'])] = NewMapData[length]['LocationID']
#                     t['Adjacent_nodes_distance'][len(t['Adjacent_nodes_distance'])] = \
#                         (abs(NewMapData[length]['longitude'] - ny_location[destination_list[len(destination_list) - 1 - k]]['longitude']) +\
#                     abs(NewMapData[length]['latitude'] - ny_location[destination_list[len(destination_list) - 1 - k]]['latitude']))*100000
#
#             datas2[j][i][point1] = {}
#
#             t['longitude'] = ny_location[destination_list[len(destination_list) - 1 - k]]['longitude']
#             t['latitude'] = ny_location[destination_list[len(destination_list) - 1 - k]]['latitude']
#             t['cost'] = cost_list[len(destination_list) - 1 - k]
#             if cost_list[0] == 0:
#                 t['time'] = 0
#             else:
#                 t['time'] = cost_list[len(destination_list) - 1 - k] / cost_list[0]
#
#             datas2[j][i][point1] = t
#
#             point1 = point1 + 1
#
#         template = "start_id: " + str(NewMapData[j]['LocationID']) + ",end_id: " + str(NewMapData[i]['LocationID']) + \
#                     ",destination_list: " + str(destination_list) + \
#                     ",cost_list: " + str(cost_list) + \
#                    ",cross_id: " + str(datas2[j][i]) + "\n"
#         file.write(template)
#         # file.write('练习文本\n')
#         file.flush()





