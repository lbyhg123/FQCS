mapping_list = [[np.inf for i in range(0, 7)] for i in range(0, 7)]  # 构建全是无穷大的二维列表
for i in range(0, 7):
    mapping_list[i][i] = 0  # 对角线处的值为0