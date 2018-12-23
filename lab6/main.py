# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import math

def bilateralFilter(img, rows, cols, sigmaColor, sigmaSpace) : 
    B, G, R = cv2.split(img)
    B_tran, G_tran, R_tran = cv2.split(img)
    cv2.imshow("Bg", B)
    img_height = len(B)
    img_width = len(B[0])
    dis_space = math.exp(-((i-k)**2 + (j-l)**2)/(2*sigmaSpace*sigmaSpace))
    for i in range(img_height) :
        for j in range(img_width) :
            value = 0
            weight = 0
            # 计算一个 rows * cols 的矩阵
            # rows * cols 的矩阵
            for k in range(i - int((rows-1)/2), i + int((rows+1)/2)) :
                for l in range(j - int((cols-1)/2), j + int((cols+1)/2)) :
                    # 计算 定义域核 dis_space 
                    # 计算颜色值
                    if k < 0 or k > img_height-1 or l < 0 or l > img_width-1 :
                        f_kl = 0
                    else :
                        f_kl = B[k][l]
                    # 计算 值域核 dis_color
                    dis_color = math.exp(-((int(B[i][j]) - int(f_kl))**2)/(2*sigmaColor*sigmaColor))
                    # 权值
                    weight_value = dis_space * dis_color
                    # 计算加权值
                    # print("k:" + str(k) + "\tl:" + str(l) + "\tvalue : " + str(value) + "\tf_kl : " + str(f_kl))
                    value = value + f_kl * weight_value
                    # 计算权值和
                    weight = weight + weight_value
            # print("value : " + str(value) + "\tweight : " + str(weight))
            B_tran[i][j] = value / weight
    cv2.imshow("BGR", B_tran)
    cv2.imwrite("beauty_after.png", cv2.merge([B_tran, G_tran, R_tran]))

img = cv2.imread("beauty.png")
cv2.imshow("original image", img)

dst = cv2.bilateralFilter(src=img, d=0, sigmaColor=100, sigmaSpace=15)
cv2.namedWindow('bi_demo',0)
cv2.resizeWindow('bi_demo',300,400)
cv2.imshow("bi_demo", dst)

bilateralFilter(img, 27, 27, 45, 100)

cv2.namedWindow('show',0)
cv2.resizeWindow('show',300,400)
cv2.imshow("show", img)
cv2.waitKey(0)
