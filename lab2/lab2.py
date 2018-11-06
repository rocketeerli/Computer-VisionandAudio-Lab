# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import math

# 压缩文件
def compressWaveFile(wave_data) :       
    quantized_num = 0.05                         # 量化因子
    diff_value = []
    compressed_data = []
    decompressed_data = []
    diff_value = [wave_data[0]]
    compressed_data = [wave_data[0]]
    decompressed_data = [wave_data[0]]
    for index in range(len(wave_data)) :
        if index == 0 :
            continue
        # 做差的时候要取对数，对数的 自变量 x >= 0， 由于样本点有正有负，因此这里先取绝对值加一
        waveData_abs = abs(wave_data[index]) + 1
        decompressedData_abs = abs(decompressed_data[index - 1]) + 1 
        # 相当于对变换后的值，即取绝对值加一后的值进行加密
        diff_value.append(math.log(waveData_abs) - math.log(decompressedData_abs))
        compressed_data.append(calCompressedData(diff_value[index], quantized_num))
        # 这里进行解密，并直接将解密出来的数值进行减一操作
        de_num = math.exp(math.log(abs(decompressed_data[index - 1]) + 1) + compressed_data[index] * quantized_num) - 1
        # 判断加密之前的样本点符号是正还是负， 如果是负数，那么解密出来的也应该是负数，需要乘-1
        if wave_data[index] < 0 :
            decompressed_data.append((-1) * de_num)
            continue
        decompressed_data.append(de_num)
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

# 计算信噪比
def calSignalToNoiseRatio(wave_data, decompressed_data) :
    sum_son = np.int64(0)
    sum_mum = np.int64(0)
    for i in range(len(decompressed_data)) :
        sum_son = sum_son + int(decompressed_data[i]) * int(decompressed_data[i])
        sub = decompressed_data[i] - wave_data[i]
        sum_mum = sum_mum + sub * sub
    return 10 * math.log10(float(sum_son) / float(sum_mum))

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
    print("信噪比：" + str(calSignalToNoiseRatio(wave_data, decompressed_data)))