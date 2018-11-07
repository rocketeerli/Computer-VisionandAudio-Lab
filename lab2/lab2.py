# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import math

# 压缩文件
def compressWaveFile(wave_data) :       
    quantized_num = 0.0005                         # 量化因子
    diff_value = []                   # 存储差值
    compressed_data = []              # 存储压缩数据
    decompressed_data = []            # 存储解压数据
    # 初始化 将第一个采样点存起来 第一个采样点不进行加密
    diff_value = [wave_data[0]]
    compressed_data = [wave_data[0]]
    decompressed_data = [wave_data[0]]
    # 找到绝对值最大的样本点
    num_absMax = 0
    for num in wave_data :
        num_abs = abs(num)
        if num_abs > num_absMax :
            num_absMax = num_abs
    num_absMax = np.int64(num_absMax)
    # 将这个最大的数据存到压缩数组中  用于解压
    compressed_data.append(num_absMax)
    # 压缩每个数据
    for index in range(len(wave_data)) :
        if index == 0 :
            continue 
        # 由于取 log 值，对每个样本点，加上绝对值最大的点再加 1 ，使所有值都大于等于 1
        waveData_tran = wave_data[index] + num_absMax + 1
        decompressedData_tran = decompressed_data[index - 1] + num_absMax + 1 
        # 相当于对变换后的值（即加上绝对值最大的点再加 1 后的值）进行加密
        diff_value.append(math.log(waveData_tran) - math.log(decompressedData_tran))
        compressed_data.append(calCompressedData(diff_value[index], quantized_num))
        # 这里进行解密，并直接将解密出来的数值进行减一操作
        de_num = math.exp(math.log(decompressedData_tran) + compressed_data[index] * quantized_num) - 1 - num_absMax
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

# 读取压缩文件
def readCompressedFile(file_address) :
    compressed_data = []          #用来存储压缩数据的数组
    f = open(file_address, 'rb')
    compressed_str = f.read()
    # 取出第一个压缩数据，即第一个样本点
    data_first = np.fromstring(compressed_str[0:16], dtype = np.short)
    compressed_data.append(data_first)
    # 去除第一个样本点，剩余所有数据都以 4 bit 存储
    compressed_str = compressed_str[16:len(compressed_str)]
    compressed_data_append = np.fromstring(compressed_str, dtype = np.uint8)
    # 将读取出来的数据装进压缩数组中，每一个数据，拆成两个 4 bit 数
    for num in compressed_data_append :
        # 存储的时候，是转成 4 bit 无符号整数存储的， 解密时，需要转换回来
        compressed_data.append((num >> 4) - 8)
        compressed_data.append(((np.uint8(num << 4)) >> 4) - 8)
    return compressed_data

# 解密 还原文件
def decompressWaveFile(compressed_data) :
    decompressed_data = []
    decompressed_data.append(compressed_data[0])
    for i in range(len(compressed_data)) :
        if i == 0 : 
            continue
        decompressed_data.append(decompressed_data[i - 1] + compressed_data[i] - 8)
    return decompressed_data

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
    
    # # 读压缩文件 解压
    # with open("./压缩文件/" + str(i + 1) + ".dpc", "rb") as f :
    #     compressed_data = readCompressedFile(f)
    #     decompressed_data = decompressWaveFile(compressed_data)

    # 写还原文件
    with open("./还原文件/" + str(i + 1) + ".pcm", "wb") as f :
        for num in decompressed_data :
            f.write(np.int16(num))
    print("信噪比：" + str(calSignalToNoiseRatio(wave_data, decompressed_data)))