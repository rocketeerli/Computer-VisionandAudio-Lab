# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
from struct import unpack
import pyaudio
from endpointDetection import EndPointDetect


# 存储成 wav 文件的参数
framerate = 16000  # 采样频率 8000 or 16000
channels = 1       # 声道数
sampwidth = 2      # 采样字节 1 or 2

# 实时录音的参数
CHUNK = 1024         # 录音的块大小
RATE = 16000         # 采样频率 8000 or 16000
RECORD_SECONDS = 2.5 # 录音时长 单位 秒(s)

# 读取已经用 HTK 计算好的 MFCC 特征
def getMFCC() :
    MFCC = []
    for i in range(10) :
        MFCC_rows = []
        for j in range(5) :
            f = open("./MFCC-EndPointedVoice/" + str(i + 1) + "-" + str(j + 1) + ".mfc","rb")
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
def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)   # 声道
    wf.setsampwidth(sampwidth)  # 采样字节 1 or 2
    wf.setframerate(framerate)  # 采样频率 8000 or 16000
    wf.writeframes(b"".join(data))
    wf.close()

def getMFCCRecorded() :
    f = open("./MFCC-RealTimeRecordedVoice/recordedVoice.mfc", "rb")
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
    return feature

# 存储所有语音文件的 MFCC 特征
# 读取已经用 HTK 计算好的 MFCC 特征
MFCC = getMFCC()

# 取出其中的模板命令的 MFCC 特征 
MFCC_models = getMFCCModels(MFCC)

# 取出其中的待分类语音的 MFCC 特征
MFCC_undetermined = getMFCCUndetermined(MFCC)

# 开始匹配
n = 0
for i in range(len(MFCC_undetermined)) :
    flag = 0
    min_dis = dtw(MFCC_undetermined[i], MFCC_models[0])
    for j in range(1, len(MFCC_models)) :
        dis = dtw(MFCC_undetermined[i], MFCC_models[j])
        if dis < min_dis :
            min_dis = dis
            flag = j
    if i + 1 <= (flag + 1) * 4 and i + 1 >= flag * 4 :
        n = n + 1
    print(str(i + 1) + "\t" + str(flag + 1) + "\n")
print("正确率为：" + str(n / 40))
# 录音
pa = pyaudio.PyAudio()
stream = pa.open(format = pyaudio.paInt16, channels = 1, \
                   rate = framerate ,    input = True, \
                   frames_per_buffer = CHUNK)
print("开始录音,请说话......")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    
print("录音结束,请停止说话!!!")

# 存储刚录制的语音文件
save_wave_file("./RecordedVoice-RealTime/recordedVoice_before.wav", frames)

# 对刚录制的语音进行端点检测
f = wave.open("./RecordedVoice-RealTime/recordedVoice_before.wav", "rb")
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes) 
wave_data = np.fromstring(str_data, dtype = np.short)
f.close()
end_point_detect = EndPointDetect(wave_data)

# 存储端点检测后的语音文件
N = end_point_detect.wave_data_detected
m = 0
print(N)
while m < len(N) :
    save_wave_file("./RecordedVoice-RealTime/recordedVoice_after.wav", wave_data[N[m] * 256 : N[m+1] * 256])
    m = m + 2

# 利用 HCopy 工具对录取的语音进行 MFCC 特征提取
os.chdir("C:\\Users\\13144\\Desktop\\Computer-VisionandAudio-Lab\\lab3\HTK-RealTimeRecordedVoice")
os.system("hcopy -A -D -T 1 -C tr_wav.cfg -S .\list.scp")
os.chdir("C:\\Users\\13144\\Desktop\\Computer-VisionandAudio-Lab\\lab3")

# 对录好的语音进行匹配
MFCC_recorded = getMFCCRecorded()

# 进行匹配
flag = 0
min_dis = dtw(MFCC_recorded, MFCC_models[0])
for j in range(1, len(MFCC_models)) :
    dis = dtw(MFCC_recorded, MFCC_models[j])
    if dis < min_dis :
        min_dis = dis
        flag = j
print( "\t" + str(flag + 1) + "\n")