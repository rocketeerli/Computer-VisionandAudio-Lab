# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import copy
import imageAdjust

# 读取图片信息
img = cv2.imread("xunmeng.bmp")
# # 颜色空间转换 BGR -> HLS
# hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
# cv2.imshow("HLS",hls)  
# 通道分离
h, l, s = cv2.split(hls)

cv2.imshow("origin image", img)
# 调整图像亮度
imageAdjust.imageAdjustmentLightness(img)
# 调整图像对比度
imageAdjust.imageAdjustmentContrast(img)
# 调整图像饱和度
imageAdjust.imageAdjustmentSaturation(img)
# 调整图像色度
imageAdjust.imageAdjustmentHue(img)

cv2.waitKey(0)
