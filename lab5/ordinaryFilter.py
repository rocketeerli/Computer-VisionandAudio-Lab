# -*- coding: UTF-8 -*-
import numpy as np
import cv2

# 十字 窗口，中值滤波
def medianFiltering(img) :
    B, G, R = cv2.split(img)
    # 对 蓝色通道 进行均值滤波
    for row in range(len(B) - 1) :
        for col in range(len(B[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 3 * 3
            # arr = B[[row - 1, row, row + 1], :]
            # arr = arr[:, [col - 1, col, col + 1]]
            # 十字
            arr = np.array([B[row - 1][col], B[row][col - 1], B[row][col], B[row][col + 1], B[row + 1][col]])
            B[row][col] = np.uint8(np.median(arr))
    # 对 绿色通道 进行均值滤波
    for row in range(len(G) - 1) :
        for col in range(len(G[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 3 * 3
            # arr = G[[row - 1, row, row + 1], :]
            # arr = arr[:, [col - 1, col, col + 1]]
            # 十字
            arr = np.array([G[row - 1][col], G[row][col - 1], G[row][col], G[row][col + 1], G[row + 1][col]])
            G[row][col] = np.uint8(np.median(arr))
    # 对 红色通道 进行均值滤波
    for row in range(len(R) - 1) :
        for col in range(len(R[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 3 * 3
            # arr = R[[row - 1, row, row + 1], :]
            # arr = arr[:, [col - 1, col, col + 1]]
            # 十字
            arr = np.array([R[row - 1][col], R[row][col - 1], R[row][col], R[row][col + 1], R[row + 1][col]])
            R[row][col] = np.uint8(np.median(arr))
    return cv2.merge([B, G, R])

# 十字 窗口，均值滤波
def meanFiltering(img) :
    B, G, R = cv2.split(img)
    # 对 蓝色通道 进行均值滤波
    for row in range(len(B) - 1) :
        for col in range(len(B[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 十字
            arr = np.array([B[row - 1][col], B[row][col - 1], B[row][col], B[row][col], \
                            B[row][col + 1], B[row + 1][col]])
            B[row][col] = np.uint8(np.mean(arr))
    # 对 绿色通道 进行均值滤波
    for row in range(len(G) - 1) :
        for col in range(len(G[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 十字
            arr = np.array([G[row - 1][col], G[row][col - 1], G[row][col], G[row][col], G[row][col], \
                            G[row][col + 1], G[row + 1][col]])
            G[row][col] = np.uint8(np.mean(arr))
    # 对 红色通道 进行均值滤波
    for row in range(len(R) - 1) :
        for col in range(len(R[row]) - 1) :
            # 边界，暂时不处理
            if row == 0 or col == 0 :
                continue
            # 十字
            arr = np.array([R[row - 1][col], R[row][col - 1], R[row][col], R[row][col], R[row][col], \
                            R[row][col + 1], R[row + 1][col]])
            R[row][col] = np.uint8(np.mean(arr))
    return cv2.merge([B, G, R])
