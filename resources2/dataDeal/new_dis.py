import json
import math


result_dir = ""
files = "ny_fre_dis123.json"
filePath = result_dir + files
with open(filePath, 'r', encoding='utf8') as fp:
    distanceFrequentNodes = json.load(fp)
    print(len(distanceFrequentNodes))
    print('这是文件中的json数据：', len(distanceFrequentNodes["1"]))
    print('这是读取到文件数据的数据类型：', type(distanceFrequentNodes))
print(distanceFrequentNodes["1"])
fileName2 = '../raw_data/ny_location'
file2 = open(fileName2, "r", encoding='utf-8')
file2lines = file2.readlines()
ny_location = {}
for i in range(len(file2lines)):
    point = {}
    npLocation = file2lines[i].split('\n')[0].split(',')
    point['longitude'] = float(npLocation[1])
    point['latitude'] = float(npLocation[2])
    ny_location[i] = point

result_dir = "../raw_data/"
files = "ny_node2region_j.json"
filePath = result_dir + files
with open(filePath, 'r', encoding='utf8') as fp:
    Node2region = json.load(fp)
    print(len(Node2region))
    # print('这是文件中的json数据：', Node2region[0])
    print('这是读取到文件数据的数据类型：', type(Node2region))




result_dir = ""
files = "nodeRange.txt"
file = open(result_dir + files, "a", encoding='utf-8')

zoneNumber = {}
for i in range(1, 263):
    zoneNumber[i] = 0


for i in range(len(Node2region)):
    zoneNumber[Node2region[i]] = zoneNumber[Node2region[i]] + 1

print(zoneNumber)

# for i in range(1, 2000):
nodeRange = {}
# for value in distanceFrequentNodes:
#     print(value)
#     nodeRange[int(value)] = {}
#     for value1 in distanceFrequentNodes[value]:
#         # print(distanceFrequentNodes[value][value1])
#         # print(value1, Node2region[int(value1)])
#         if Node2region[int(value1)] not in nodeRange[int(value)]:
#             nodeRange[int(value)][Node2region[int(value1)]] = 0
#         nodeRange[int(value)][Node2region[int(value1)]] = nodeRange[int(value)][Node2region[int(value1)]] + 1
#         #     print(len(distanceFrequentNodes[str(i)]))
#
#     for value1 in nodeRange[int(value)]:
#         nodeRange[int(value)][value1] = nodeRange[int(value)][value1] / zoneNumber[value1]

for value in distanceFrequentNodes:
    # print(value)
    nodeRange[int(value)] = []
    for value1 in distanceFrequentNodes[value]:
        # print(distanceFrequentNodes[value][value1])
        # print(value1, Node2region[int(value1)])
        nodeRange[int(value)].append(int(value1))
        # if Node2region[int(value1)] not in nodeRange[int(value)]:
        #     nodeRange[int(value)][Node2region[int(value1)]] = 0
        # nodeRange[int(value)][Node2region[int(value1)]] = nodeRange[int(value)][Node2region[int(value1)]] + 1
        #     print(len(distanceFrequentNodes[str(i)]))

    for value1 in nodeRange[int(value)]:
        nodeRange[int(value)][value1] = nodeRange[int(value)][value1] / zoneNumber[value1]

    # print(nodeRange)
    # template = ""
    # for value1 in nodeRange:
    #     template = template + str(value1) + ":" + str(nodeRange[value1]) + ","
    # template = template + "\n"
    # # print(template)
    # file.write(template)
    # # file.write('练习文本\n')
    # file.flush()
with open('nodeRangeNode.json','w',encoding='utf8') as f2:
    # ensure_ascii=False才能输入中文，否则是Unicode字符
    # indent=2 JSON数据的缩进，美观
    json.dump(nodeRange, f2)

print(zoneNumber)