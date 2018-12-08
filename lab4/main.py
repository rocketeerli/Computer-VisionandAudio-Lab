# -*- coding: UTF-8 -*-
import numpy as np
import sys
from ReadBMPFile import ReadBMPFile
import cv2
import math
import colorSpaceConversion

filePath = sys.argv[1]
# 读取 BMP 文件
bmpFile = ReadBMPFile(filePath)
# R, G, B 三个通道 [0, 255]
R = bmpFile.R
G = bmpFile.G
B = bmpFile.B
# 变化后的 g, b, r  [0, 1]
g = []
b = []
r = []
for row in range(len(R)) :
    r_row = []
    g_row = []
    b_row = []
    for col in range(len(R[row])) :
        r_row.append(R[row][col] / 255)
        g_row.append(G[row][col] / 255)
        b_row.append(B[row][col] / 255)
    r.append(r_row)
    g.append(g_row)
    b.append(b_row)

# YIQ
y, i, q = colorSpaceConversion.imgTranYIQ(r, g, b)
# 标准化 B、G、R 的值
for row in range(len(y)) :
    for col in range(len(y[row])) :
        y[row][col] = np.int8(y[row][col] * 255)
        i[row][col] = np.int8(i[row][col] * 255 + 128)
        q[row][col] = np.int8(q[row][col] * 255 + 128)
y = np.array(y, dtype = np.uint8)
i = np.array(i, dtype = np.uint8)
q = np.array(q, dtype = np.uint8)
merged = cv2.merge([y, i, q]) #合并R、G、B分量 默认顺序为 B、G、R
cv2.imshow("YIQ",merged)
cv2.imwrite(filePath.split("/")[-1].split(".")[0] + "-1160300426-YIQ.bmp", merged)

# HSI
h, s, i = colorSpaceConversion.imgTranHSI(R, G, B)
# 标准化 B、G、R 的值
for row in range(len(h)) :
    for col in range(len(h[row])) :
        h[row][col] = np.int8(h[row][col] * 180 / math.pi)
        s[row][col] = np.int8(s[row][col] * 100)
        i[row][col] = np.int8(i[row][col] * 255)
h = np.array(h, dtype = np.uint8)
s = np.array(s, dtype = np.uint8)
i = np.array(i, dtype = np.uint8)
merged = cv2.merge([h, s, i]) #合并R、G、B分量 默认顺序为 B、G、R
cv2.imshow("HSI",merged)
cv2.imwrite(filePath.split("/")[-1].split(".")[0] + "-1160300426-HSI.bmp", merged)

# YCbCr
y, Cb, Cr = colorSpaceConversion.imgTranYCbCr(R, G, B)
y_arr = np.array(y, dtype = np.uint8)
Cb_arr = np.array(Cb, dtype = np.uint8)
Cr_arr = np.array(Cr, dtype = np.uint8)
merged = cv2.merge([y_arr, Cb_arr, Cr_arr]) #合并R、G、B分量 默认顺序为 B、G、R
cv2.imshow("YCbCr",merged)
cv2.imwrite(filePath.split("/")[-1].split(".")[0] + "-1160300426-YCbCr.bmp", merged)

# XYZ
x, y, z = colorSpaceConversion.imgTranXYZ(R, G, B)
x_arr = np.array(x, dtype = np.uint8)
y_arr = np.array(y, dtype = np.uint8)
z_arr = np.array(z, dtype = np.uint8)
merged = cv2.merge([x_arr, y_arr, z_arr]) #合并R、G、B分量 默认顺序为 B、G、R
cv2.imshow("XYZ",merged)
cv2.imwrite(filePath.split("/")[-1].split(".")[0] + "-1160300426-XYZ.bmp", merged)

cv2.waitKey(0)
