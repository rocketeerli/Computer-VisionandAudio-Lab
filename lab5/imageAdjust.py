# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import copy

# 调整图像的亮度
def imageAdjustmentLightness(img) :
    B, G, R = cv2.split(img)
    b = copy.deepcopy(B)
    g = copy.deepcopy(G)
    r = copy.deepcopy(R)
    for row in range(len(b)) :
        for col in range(len(b[row])) :
            if b[row][col] > 235 :
                b[row][col] = 255
            else :
                b[row][col] = b[row][col] + 20
            if g[row][col] > 235 :
                g[row][col] = 255
            else :
                g[row][col] = g[row][col] + 20
            if r[row][col] > 235 :
                r[row][col] = 255
            else :
                r[row][col] = r[row][col] + 20
    merged = cv2.merge([b, g, r])
    cv2.imshow("after adjust lightness", merged)
    cv2.imwrite("imgeAdjustment-Lightness.png", merged)

# 调整图像的对比度
def imageAdjustmentContrast(img) :
    B, G, R = cv2.split(img)
    b = copy.deepcopy(B)
    g = copy.deepcopy(G)
    r = copy.deepcopy(R)
    for row in range(len(b)) :
        for col in range(len(b[row])) :
            if b[row][col] > 231 :
                b[row][col] = 255
            else :
                b[row][col] = np.int8(b[row][col] * 1.1)
            if g[row][col] > 231 :
                g[row][col] = 255
            else :
                g[row][col] = np.int8(g[row][col] * 1.1)
            if r[row][col] > 231 :
                r[row][col] = 255
            else :
                r[row][col] = np.int8(r[row][col] * 1.1)
    merged = cv2.merge([b, g, r])
    cv2.imshow("after adjust contrast", merged)
    cv2.imwrite("imgeAdjustment-Contrast.png", merged)

# 调整图像的饱和度
def imageAdjustmentSaturation(img) :
    HLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    H, L, S = cv2.split(HLS)
    for row in range(len(L)) :
        for col in range(len(L[row])) :
            if H[row][col] < 10 :
                S[row][col] = 0
            else :
                S[row][col] = S[row][col] - 10
    merged = cv2.merge([H, L, S])
    changed = cv2.cvtColor(merged, cv2.COLOR_HLS2BGR)
    cv2.imshow("after adjust the saturation", changed)
    cv2.imwrite("imgeAdjustment-Saturation.png", changed)

# 调整图像的色度
def imageAdjustmentHue(img) :
    HLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    H, L, S = cv2.split(HLS)
    for row in range(len(L)) :
        for col in range(len(L[row])) :
            if H[row][col] > 240 :
                H[row][col] = 255
            else :
                H[row][col] = H[row][col] + 15
    merged = cv2.merge([H, L, S])
    changed = cv2.cvtColor(merged, cv2.COLOR_HLS2BGR)
    cv2.imshow("after adjust the hue", changed)
    cv2.imwrite("imgeAdjustment-Hue.png", changed)