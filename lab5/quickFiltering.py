# -*- coding: UTF-8 -*-
import numpy as np
import cv2

def quickMedianFiltering(img) :
    B, G, R = cv2.split(img)
    # 对 蓝色通道 进行中值滤波
    H = np.zeros(256, dtype=int)    # 直方图
    for row in range(1, len(B) - 1) :
        # 到达一个新的行 初始化
        H = np.zeros(256, dtype=int)    # 直方图
        # 求中值
        med = np.uint8(np.median(B[row - 1 : row + 2, 0:3]))
        n = 0
        for i in range(-1, 2) :
            for j in range(0, 3) :
                H[B[row+i][j]] = H[B[row+i][j]] + 1
                if B[row+i][j] <= med :
                    n = n + 1
        for col in range(1, len(B[row]) - 1) :
            if col == 1 :
                None
            # 移到下一列
            else :
                # 更新直方图 并计算 n 的值
                for i in range(-1, 2) :
                    # 对左列元素 值减一 
                    H[B[row+i][col-2]] = H[B[row+i][col-2]] - 1
                    if B[row+i][col-2] <= med :
                        n = n - 1
                    # 对右列元素 值加一
                    H[B[row+i][col+1]] = H[B[row+i][col+1]] + 1
                    if B[row+i][col+1] <= med :
                        n = n + 1
                # 重新计算中值
                if n > 5 :
                    while n > 5 :
                        if med == 0 :
                            break
                        n = n - H[med]
                        med = med - 1
                elif n < 5 :
                    while n < 5 :
                        med = med + 1
                        n = n + H[med]
            sum = 0
            for k in range(med + 1) :
                sum = sum + H[k]
            # 更新中值后的直方图
            H[B[row][col]] = H[B[row][col]] - 1
            if med < B[row][col] :
                n = n + 1
            B[row][col] = med
            H[med] = H[med] + 1
    # 对 绿色通道 进行中值滤波
    H = np.zeros(256, dtype=int)    # 直方图
    for row in range(1, len(G) - 1) :
        # 到达一个新的行 初始化
        H = np.zeros(256, dtype=int)    # 直方图
        # 求中值
        med = np.uint8(np.median(G[row - 1 : row + 2, 0:3]))
        if med == -128 :
            print(G[row - 1 : row + 2, 0:3])
        n = 0
        for i in range(-1, 2) :
            for j in range(0, 3) :
                H[G[row+i][j]] = H[G[row+i][j]] + 1
                if G[row+i][j] <= med :
                    n = n + 1
        for col in range(1, len(G[row]) - 1) :
            if col == 1 :
                None
            # 移到下一列
            else :
                # 更新直方图 并计算 n 的值
                for i in range(-1, 2) :
                    # 对左列元素 值减一 
                    H[G[row+i][col-2]] = H[G[row+i][col-2]] - 1
                    if G[row+i][col-2] <= med :
                        n = n - 1
                    # 对右列元素 值加一
                    H[G[row+i][col+1]] = H[G[row+i][col+1]] + 1
                    if G[row+i][col+1] <= med :
                        n = n + 1
                # 重新计算中值
                if n > 5 :
                    while n > 5 :
                        if med == 0 :
                            break
                        n = n - H[med]
                        med = med - 1
                elif n < 5 :
                    while n < 5 :
                        med = med + 1
                        n = n + H[med]
            # 更新中值后的直方图
            H[G[row][col]] = H[G[row][col]] - 1
            if med < G[row][col] :
                n = n + 1
            G[row][col] = med
            H[med] = H[med] + 1
    # 对 红色通道 进行中值滤波
    H = np.zeros(256, dtype=int)    # 直方图
    for row in range(1, len(R) - 1) :
        # 到达一个新的行 初始化
        H = np.zeros(256, dtype=int)    # 直方图
        # 求中值
        med = np.uint8(np.median(R[row - 1 : row + 2, 0:3]))
        if med == -128 :
            print(R[row - 1 : row + 2, 0:3])
        n = 0
        for i in range(-1, 2) :
            for j in range(0, 3) :
                H[R[row+i][j]] = H[R[row+i][j]] + 1
                if R[row+i][j] <= med :
                    n = n + 1
        for col in range(1, len(R[row]) - 1) :
            if col == 1 :
                None
            # 移到下一列
            else :
                # 更新直方图 并计算 n 的值
                for i in range(-1, 2) :
                    # 对左列元素 值减一 
                    H[R[row+i][col-2]] = H[R[row+i][col-2]] - 1
                    if R[row+i][col-2] <= med :
                        n = n - 1
                    # 对右列元素 值加一
                    H[R[row+i][col+1]] = H[R[row+i][col+1]] + 1
                    if R[row+i][col+1] <= med :
                        n = n + 1
                # 重新计算中值
                if n > 5 :
                    while n > 5 :
                        if med == 0 :
                            break
                        n = n - H[med]
                        med = med - 1
                elif n < 5 :
                    while n < 5 :
                        med = med + 1
                        n = n + H[med]
            sum = 0
            # 更新中值后的直方图
            H[R[row][col]] = H[R[row][col]] - 1
            if med < R[row][col] :
                n = n + 1
            R[row][col] = med
            H[med] = H[med] + 1
    
    return cv2.merge([B,G,R])
