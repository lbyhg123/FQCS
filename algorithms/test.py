# d = {
#     'Alice': 45,
#     'Bob': 60,
#     'Candy': 75,
#     'David': 86,
#     'Ellena': 49
# }
# print(d)
# alice_score =d.pop('Bob')
# print(alice_score)
# print(d)
#
# bob_score =d.pop('David')
# print(bob_score)
# print(d)
#
#
# d = {'Alice': [50, 61, 66], 'Bob': [80, 61, 66], 'Candy': [88, 75, 90]}
# for key,value in d.items():
#     if value > 60:
#         print(key,value)
#    # ==>  #('Bob', [80, 61, 66])
# 	# 	#('Alice', [50, 61, 66])
# 	# 	#('Candy', [88, 75, 90])
#
# d = {'Alice': [50, 61, 66], 'Bob': [80, 61, 66], 'Candy': [88, 75, 90]}
# print(d) # ==> {'Alice': [50, 61, 66], 'Bob': [80, 61, 66], 'Candy': [88, 75, 90]}
# d.clear()
# print(d)  #====》[]

# zoneIdleTimeMap = {0:1,1:2}
# if zoneIdleTimeMap.get(0, -1) <= 0:
#     print(1)
    # idleTime = zoneIdleTimeMap[order['endZoneID']]

# import numpy as np
#
# # 计算的被除数A,以及除数B
# arrayA = np.arange(9).reshape(3,3)
# arrayA[0,2]=0
# arrayA[2,0]=-2
# arrayB = np.array([[1,4,0],
#                     [5,0,6],
#                     [0,7,2]])
# arrayC = arrayA / arrayB
# print(np.array(1)/np.array(0))
# # print(1/ (np.array(1)/np.array(0)))
# mu = 0.2000000000000000000000000000
#
# lamda = 0E-29
# K = 2
# t = np.array(mu)/np.array(lamda)
# print(t)
# pLB = (t ** (K+1) - 1) / (t - 1)
# print(pLB)
# if np.isnan(pLB):
#     print("yes")
# if not np.isfinite(t):
#     print("yes")
# print("arrayA:\n", arrayA)
# print("arrayB:\n", arrayB)
# print("*****************")
# print("arrayA / arrayB\n",arrayC)

# for i in range(10):
#     for j in range(10):
#         if i==j:
#             print('same')
#             break
#     print(1)
#

import numpy as np
np.random.seed(12)  # 先定义一个随机数种子
# np.random.seed(seed)
# np.random.randint(0, 10, size=1)
print(np.random.randint(0, 10, size=10))  # "随机"生成5个数