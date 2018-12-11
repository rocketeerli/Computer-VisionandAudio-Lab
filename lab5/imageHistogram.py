# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 第二部分 统计图像的直方图。
def drawHistogram(img) :
    B, G, R = cv2.split(img)
    b = np.array(B).flatten()
    g = np.array(G).flatten()
    r = np.array(R).flatten()
    # 需要将 normed 改为 density
    # n, bins, patches = plt.hist(b, bins=256, normed=1, facecolor='green', alpha=0.75)
    # 蓝色通道的直方图
    plt.xlabel("chroma")
    plt.ylabel("pixel number")
    plt.title("Histogram of Blue Channel")
    plt.hist(b, bins=256, label = "blue", density=1, facecolor='green', edgecolor='b', alpha=0.75)
    plt.show()
    # 绿色通道的直方图
    plt.xlabel("chroma")
    plt.ylabel("pixel number")
    plt.title("Histogram of Green Channel")
    plt.hist(g, bins=256, label = "green", density=1, facecolor='green', edgecolor='g', alpha=0.75)
    plt.show()
    # 红色通道的直方图
    # plt.cla()  # 可以清空上面存留的信息，防止直方图叠加
    plt.style.use( 'ggplot')
    plt.xlabel("chroma")
    plt.ylabel("pixel number")
    plt.title("Histogram of Red Channel")
    plt.hist(r, bins=256, label = "red", density=1, facecolor='green', edgecolor='g', alpha=0.75)
    plt.show()