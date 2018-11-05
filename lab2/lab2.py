# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import math

# 压缩文件
def compressWaveFile(wave_data) :       
    quantized_num = 200                         # 量化因子
    diff_value = []
    compressed_data = []
    decompressed_data = []
    diff_value = [wave_data[0]]
    compressed_data = [wave_data[0]]
    decompressed_data = [wave_data[0]]
    for index in range(len(wave_data)) :
        if index == 0 :
            continue
        diff_value.append(wave_data[index]  - decompressed_data[index - 1])
        compressed_data.append(calCompressedData(diff_value[index], quantized_num))
        decompressed_data.append(decompressed_data[index - 1] + compressed_data[index] * quantized_num)
    return compressed_data, decompressed_data

# 计算 映射
def calCompressedData(diff_value, quantized_num) :
    if diff_value > 7 * quantized_num :
        return 7
    elif diff_value < -8 * quantized_num :
        return -8
    for i in range(16) :
        j = i - 8
        if (j - 1) * quantized_num < diff_value and diff_value <= j * quantized_num :
            return j

for i in range(10) :
    f = wave.open("./语料/" + str(i + 1) + ".wav","rb")
    # getparams() 一次性返回所有的WAV文件的格式信息
    params = f.getparams()
    # nframes 采样点数目
    nchannels, sampwidth, framerate, nframes = params[:4]
    # readframes() 按照采样点读取数据
    str_data = f.readframes(nframes)            # str_data 是二进制字符串
    # 以上可以直接写成 str_data = f.readframes(f.getnframes())
    # 转成二字节数组形式（每个采样点占两个字节）
    wave_data = np.fromstring(str_data, dtype = np.short)
    print( "采样点数目：" + str(len(wave_data)))          #输出应为采样点数目
    f.close()
    compressed_data, decompressed_data = compressWaveFile(wave_data)
    # 写压缩文件
    with open("./压缩文件/" + str(i + 1) + ".dpc", "wb") as f :
        for num in compressed_data :
            f.write(np.int16(num))
    # 写还原文件
    with open("./还原文件/" + str(i + 1) + ".pcm", "wb") as f :
        for num in decompressed_data :
            f.write(np.int16(num))