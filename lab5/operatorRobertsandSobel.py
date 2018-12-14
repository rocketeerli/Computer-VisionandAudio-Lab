# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import copy

# Roberts 算子
def calRoberts(img) :
    B, G, R = cv2.split(img)
    operator_first = np.array([[-1,0],[0,1]])
    operator_second = np.array([[0,-1],[1,0]])
    # 对 蓝色通道 进行边缘检测
    for row in range(len(B) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(len(B[row]) - 1) :
            arr = B[row:row+2, col:col+2]
            B[row][col] = np.abs(np.sum(arr * operator_first)) + np.abs(np.sum(arr * operator_second))
    # 对 绿色通道 进行边缘检测
    for row in range(len(G) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(len(G[row]) - 1) :
            arr = G[row:row+2, col:col+2]
            G[row][col] = np.abs(np.sum(arr * operator_first)) + np.abs(np.sum(arr * operator_second))
    # 对 红色通道 进行边缘检测
    for row in range(len(R) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(len(R[row]) - 1) :
            arr = R[row:row+2, col:col+2]
            R[row][col] = np.abs(np.sum(arr * operator_first)) + np.abs(np.sum(arr * operator_second))
    return B, G, R

# Sobel 算子
def calSobel(img) :
    B, G, R = cv2.split(img)
    b = copy.deepcopy(B)
    g = copy.deepcopy(G)
    r = copy.deepcopy(R)
    # 水平和垂直的算子
    operator_vertical = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    operator_horizontal = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    # 对 蓝色通道 进行边缘检测
    for row in range(1, len(B) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(1, len(B[row]) - 1) :
            arr = B[row-1:row+2, col-1:col+2]
            value = np.abs(np.sum(arr*operator_vertical)) + np.abs(np.sum(arr*operator_horizontal))
            if value > 255 :
                b[row][col] = 255
            elif value < 0 :
                b[row][col] = 0
            else :
                b[row][col] = value 
    # 对 绿色通道 进行边缘检测
    for row in range(1, len(G) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(1, len(G[row]) - 1) :
            arr = G[row-1:row+2, col-1:col+2]
            value = np.abs(np.sum(arr*operator_vertical)) + np.abs(np.sum(arr*operator_horizontal))
            if value > 255 :
                g[row][col] = 255
            elif value < 0 :
                g[row][col] = 0
            else :
                g[row][col] = value 
    # 对 红色通道 进行边缘检测
    for row in range(1, len(R) - 1) :   # 最后一行和最后一列不进行检测
        for col in range(1, len(R[row]) - 1) :
            arr = R[row-1:row+2, col-1:col+2]
            value = np.abs(np.sum(arr*operator_vertical)) + np.abs(np.sum(arr*operator_horizontal))
            if value > 255 :
                r[row][col] = 255
            elif value < 0 :
                r[row][col] = 0
            else :
                r[row][col] = value 
    return b, g, r
