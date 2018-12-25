# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import math

def bilateralFilter(img, radius, sigmaColor, sigmaSpace) : 
    B, G, R = cv2.split(img)
    B_tran, G_tran, R_tran = cv2.split(img)
    img_height = len(B)
    img_width = len(B[0])
    # 计算灰度值模板系数表
    color_coeff = -0.5 / (sigmaColor * sigmaColor)
    weight_color = []       # 存放颜色差值的平方
    for i in range(256) :
        weight_color.append(np.exp(i * i * color_coeff))
    # 计算空间模板
    space_coeff = -0.5 / (sigmaSpace * sigmaSpace)
    weight_space = []     # 存放模板系数
    weight_space_row = [] # 存放模板 x轴 位置
    weight_space_col = [] # 存放模板 y轴 位置
    maxk = 0
    for i in range(-radius, radius+1) :
        for j in range(-radius, radius+1) :
            r_square = i*i + j*j
            r = np.sqrt(r_square)
            weight_space.append(np.exp(r_square * space_coeff))
            weight_space_row.append(i)
            weight_space_col.append(j)
            maxk = maxk + 1
    # 进行滤波
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = B[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.abs(val - B[row][col])])
                value = value + val * w
                weight = weight + w
            B_tran[row][col] = np.uint8(value / weight)
    # 绿色通道
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = G[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.abs(val - G[row][col])])
                value = value + val * w
                weight = weight + w
            G_tran[row][col] = np.uint8(value / weight)
    # 红色通道
    for row in range(img_height) :
        for col in range(img_width) :
            value = 0
            weight = 0
            for i in range(maxk) :
                m = row + weight_space_row[i]
                n = col + weight_space_col[i]
                if m < 0 or n < 0 or m >= img_height or n >= img_width :
                    val = 0
                else :
                    val = R[m][n]
                w = np.float32(weight_space[i]) * np.float32(weight_color[np.abs(val - R[row][col])])
                value = value + val * w
                weight = weight + w
            R_tran[row][col] = np.uint8(value / weight)
    cv2.imshow("beauty_after", cv2.merge([B_tran, G_tran, R_tran]))
    cv2.imwrite("beauty_after.png", cv2.merge([B_tran, G_tran, R_tran]))

img = cv2.imread("beauty1.png")
cv2.imshow("original image", img)

# bilateralFilter(img, 5, 45, 100)
bilateralFilter(img, 3, 30, 80)

img = cv2.imread("beauty_after.png")
bilateralFilter(img, 3, 30, 80)

cv2.waitKey(0)
