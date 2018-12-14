# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import imageAdjust
import matplotlib.pyplot as plt
import imageHistogram
import ordinaryFilter
import copy
import operatorRobertsandSobel

# 读取图片信息
img = cv2.imread("xunmeng.bmp")
# cv2.imshow("original", img)
# # 颜色空间转换 BGR -> HLS
# hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
# cv2.imshow("HLS",hls)  
# 通道分离
# h, l, s = cv2.split(hls)

# # 第一部分 实现对图像的亮度、对比度、饱和度、色度的调整。（
# cv2.imshow("origin image", img)
# # 调整图像亮度
# imageAdjust.imageAdjustmentLightness(img)
# # 调整图像对比度
# imageAdjust.imageAdjustmentContrast(img)
# # 调整图像饱和度
# imageAdjust.imageAdjustmentSaturation(img)
# # 调整图像色度
# imageAdjust.imageAdjustmentHue(img)

# # 第二部分 统计图像的直方图。
# imageHistogram.drawHistogram(img)

# 第三部分 实现图像的空域滤波：中值滤波和均值滤波
# 中值滤波
# img_median = ordinaryFilter.medianFiltering(img)
# cv2.imshow("median filtering", img_median)
# # 均值滤波
# img_mean = ordinaryFilter.meanFiltering(img)
# cv2.imshow("mean filtering", img_mean)

# 第四部分 实现图像的边缘检测：Roberts 算子和 Sobel 算子。
# Roberts 算子
B, G, R = operatorRobertsandSobel.calRoberts(img)
cv2.imshow("Blue Roberts", B)
cv2.imshow("Green Roberts", G)
cv2.imshow("Red Roberts", R)
cv2.imshow("BGR Roberts", cv2.merge([B, G, R]))
# Sobel 算子
B, G, R = operatorRobertsandSobel.calSobel(img)
cv2.imshow("Blue Sobel", B)
cv2.imshow("Green Sobel", G)
cv2.imshow("Red Sobel", R)
cv2.imshow("BGR Sobel", cv2.merge([B, G, R]))

cv2.waitKey(0)
