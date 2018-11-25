# -*- coding: utf-8 -*-
import wave
import os
import numpy as np

# 存储成 wav 文件的参数
framerate = 16000  # 采样频率 8000 or 16000
channels = 1       # 声道数
sampwidth = 2      # 采样字节 1 or 2

def sgn(data):
    if data >= 0 :
        return 1
    else :
        return 0

# 计算每一帧的能量 256个采样点为一帧
def calEnergy(wave_data) :
    energy = []
    sum = 0
    for i in range(len(wave_data)) :
        sum = sum + (int(wave_data[i]) * int(wave_data[i]))
        if (i + 1) % 256 == 0 :
            energy.append(sum)
            sum = 0
        elif i == len(wave_data) - 1 :
            energy.append(sum)
    return energy

#计算过零率
def calZeroCrossingRate(wave_data) :
    zeroCrossingRate = []
    sum = 0
    for i in range(len(wave_data)) :
        if i == 0:
            None
        #elif int(wave_data[i] - T) * int(wave_data[i - 1] - T) <= 0 or int(wave_data[i] + T) * int(wave_data[i - 1] + T) <= 0 :
        sum = sum + np.abs(sgn(wave_data[i]) - sgn(wave_data[i - 1]))
        if (i + 1) % 256 == 0 :
            zeroCrossingRate.append(float(sum) / 255)
            sum = 0
        elif i == len(wave_data) - 1 :
            zeroCrossingRate.append(float(sum) / 255)
    return zeroCrossingRate

# 利用短时能量，短时过零率，使用双门限法进行端点检测
def endPointDetect(wave_data, energy, zeroCrossingRate) :
    sum = 0
    energyAverage = 0
    for en in energy :
        sum = sum + en
    energyAverage = sum / len(energy)

    sum = 0
    for en in energy[:5] :
        sum = sum + en
    ML = sum / 5                        
    MH = energyAverage / 4              #较高的能量阈值
    ML = (ML + MH) / 4    #较低的能量阈值
    sum = 0
    for zcr in zeroCrossingRate[:5] :
        sum = float(sum) + zcr             
    Zs = sum / 5                     #过零率阈值

    A = []
    B = []
    C = []

    # 首先利用较大能量阈值 MH 进行初步检测
    flag = 0
    for i in range(len(energy)):
        if len(A) == 0 and flag == 0 and energy[i] > MH :
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > MH and i - 21 > A[len(A) - 1]:
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > MH and i - 21 <= A[len(A) - 1]:
            A = A[:len(A) - 1]
            flag = 1

        if flag == 1 and energy[i] < MH :
            # 检测帧长  如果帧长太短，那就去掉
            if i - A[len(A) - 1] <= 2 :
                A = A[:len(A) - 1]
            else :
                A.append(i)
            flag = 0
    print("较高能量阈值，计算后的浊音A:" + str(A))

    # 利用较小能量阈值 ML 进行第二步能量检测
    for j in range(len(A)) :
        i = A[j]
        if j % 2 == 1 :
            while i < len(energy) and energy[i] > ML :
                i = i + 1
            B.append(i)
        else :
            while i > 0 and energy[i] > ML :
                i = i - 1
            B.append(i)
    print("较低能量阈值，增加一段语言B:" + str(B))

    # 利用过零率进行最后一步检测
    for j in range(len(B)) :
        i = B[j]
        if j % 2 == 1 :
            while i < len(zeroCrossingRate) and zeroCrossingRate[i] >= 3 * Zs :
                i = i + 1
            C.append(i)
        else :
            while i > 0 and zeroCrossingRate[i] >= 3 * Zs :
                i = i - 1
            C.append(i)
    print("过零率阈值，最终语音分段C:" + str(C))
    return C

# 将语音文件存储成 wav 格式
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)   # 声道
    wf.setsampwidth(sampwidth)  # 采样字节 1 or 2
    wf.setframerate(framerate)  # 采样频率 8000 or 16000
    wf.writeframes(b"".join(data))
    wf.close()

for i in range(10) :
    for j in range(5) :
        f = wave.open("./RecordedVoice/" + str(i + 1) + "-" + str(j + 1) + ".wav","rb")
        # getparams() 一次性返回所有的WAV文件的格式信息
        params = f.getparams()
        # nframes 采样点数目
        nchannels, sampwidth, framerate, nframes = params[:4]
        # readframes() 按照采样点读取数据
        str_data = f.readframes(nframes)            # str_data 是二进制字符串

        # 以上可以直接写成 str_data = f.readframes(f.getnframes())

        # 转成二字节数组形式（每个采样点占两个字节）
        wave_data = np.fromstring(str_data, dtype = np.short)
        print(str(i + 1) + "-" + str(j + 1) + " 采样点数目：" + str(len(wave_data)))          #输出应为采样点数目
        f.close()
        energy = calEnergy(wave_data)
        zeroCrossingRate = calZeroCrossingRate(wave_data)
        N = endPointDetect(wave_data, energy, zeroCrossingRate)
        # 输出为 wav 格式
        m = 0
        while m < len(N) :
            save_wave_file("./EndPointedVoice/" + str(i + 1) + "-" + str(j + 1) + ".wav", wave_data[N[m] * 256 : N[m+1] * 256])
            m = m + 2
        