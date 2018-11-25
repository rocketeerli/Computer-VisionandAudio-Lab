# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
from struct import unpack

framerate = 16000  # 采样频率 8000 or 16000
channels = 1       # 声道数
sampwidth = 2      # 采样字节 1 or 2

# 读取已经用 HTK 计算好的 MFCC 特征
def getMFCC() :
    MFCC = []
    for i in range(10) :
        MFCC_rows = []
        for j in range(5) :
            f = open("./EndPointedVoice-MFCC/" + str(i + 1) + "-" + str(j + 1) + ".mfc","rb")
            nframes = unpack(">i", f.read(4))[0]
            frate = unpack(">i", f.read(4))[0]     # 100 ns 内的
            nbytes = unpack(">h", f.read(2))[0]    # 特征的字节数
            feakind = unpack(">h", f.read(2))[0]
            # print("nframes : " + str(nframes) + "\n" + "frate : " + str(frate) + "\n" + \
            #         "nbytes : " + str(nbytes) + "\n" + "feakind : " + str(feakind))
            ndim = nbytes / 4   # 维数
            feature = []
            for m in range(nframes) :
                feature_frame = []
                for n in range(int(ndim)) :
                    feature_frame.append(unpack(">f", f.read(4))[0])
                feature.append(feature_frame)
            f.close()
            MFCC_rows.append(feature)
        MFCC.append(MFCC_rows)
    return MFCC

# 取出其中的模板命令的 MFCC 特征 
def getMFCCModels(MFCC) :
    MFCC_models = []
    for i in range(len(MFCC)) :
        MFCC_models.append(MFCC[i][0])
    return MFCC_models

# 取出其中的待分类语音的 MFCC 特征
def getMFCCUndetermined(MFCC) :
    MFCC_undetermined = []
    for i in range(len(MFCC)) :
        for j in range(1, len(MFCC[i])) :
            MFCC_undetermined.append(MFCC[i][j])
    return MFCC_undetermined

# DTW 算法...
def dtw(M1, M2) :
    # 初始化数组 大小为 M1 * M2
    M1_len = len(M1)
    M2_len = len(M2)
    cost = [[0 for i in range(M2_len)] for i in range(M1_len)]
    
    # 初始化 dis 数组
    dis = []
    for i in range(M1_len) :
        dis_row = []
        for j in range(M2_len) :
            dis_row.append(distance(M1[i], M2[j]))
        dis.append(dis_row)
    
    # 初始化 cost 的第 0 行和第 0 列
    cost[0][0] = dis[0][0]
    for i in range(1, M1_len) :
        cost[i][0] = cost[i - 1][0] + dis[i][0]
    for j in range(1, M2_len) :
        cost[0][j] = cost[0][j - 1] + dis[0][j]
    
    # 开始动态规划
    for i in range(1, M1_len) :
        for j in range(1, M2_len) :
            cost[i][j] = min(cost[i - 1][j] + dis[i][j] * 1, \
                            cost[i- 1][j - 1] + dis[i][j] * 2, \
                            cost[i][j - 1] + dis[i][j] * 1)
    return cost[M1_len - 1][M2_len - 1]

# 两个维数相等的向量之间的距离
def distance(x1, x2) :
    sum = 0
    for i in range(len(x1)) :
        sum = sum + abs(x1[i] - x2[i])
    return sum

# 将语音文件存储成 wav 格式
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)   # 声道
    wf.setsampwidth(sampwidth)  # 采样字节 1 or 2
    wf.setframerate(framerate)  # 采样频率 8000 or 16000
    wf.writeframes(b"".join(data))
    wf.close()

# 存储所有语音文件的 MFCC 特征
# 读取已经用 HTK 计算好的 MFCC 特征
MFCC = getMFCC()

# 取出其中的模板命令的 MFCC 特征 
MFCC_models = getMFCCModels(MFCC)

# 取出其中的待分类语音的 MFCC 特征
MFCC_undetermined = getMFCCUndetermined(MFCC)

# 开始匹配
for i in range(len(MFCC_undetermined)) :
    flag = 0
    min_dis = dtw(MFCC_undetermined[i], MFCC_models[0])
    for j in range(1, len(MFCC_models)) :
        dis = dtw(MFCC_undetermined[i], MFCC_models[j])
        if dis < min_dis :
            min_dis = dis
            flag = j
    print(str(i + 1) + "\t" + str(flag + 1) + "\n")