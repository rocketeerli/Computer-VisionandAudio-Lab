# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import math

# 压缩文件
def compressWaveFile(wave_data) :       
    quantized_num = 0.2                         # 量化因子
    diff_value = []                   # 存储差值
    compressed_data = []              # 存储压缩数据
    decompressed_data = []            # 存储解压数据
    # 初始化 将第一个采样点存起来 第一个采样点不进行加密
    diff_value = [wave_data[0]]
    compressed_data = [wave_data[0]]
    decompressed_data = [wave_data[0]]
    # 压缩每个数据
    # 除去第一个采样点 每 64 个数据一组，将每组的符号位存储在一个 16 位无符号整数中
    sig_array = []
    sig_num = 0
    for index in range(len(wave_data)) :
        if index == 0 :
            continue
        if index % 16 == 1 :
            if index != 1 :
                sig_array.append(sig_num)
            if wave_data[index] < 0 :
                sig_num = np.uint16(1)
            else :
                sig_num = np.uint16(0)
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
            sig_num = np.uint16((sig_num << 1) + 1)        # 负数 左移 1 位，加 1
            continue
        sig_num = np.uint16(sig_num << 1)                  # 正数 左移 1 位
        decompressed_data.append(de_num)
        # 最后几位也要存起来
        if index == len(wave_data) - 1 :
            sig_array.append(sig_num)
    compressed_data.insert(1, len(sig_array))
    for i in range(len(sig_array)) :
        compressed_data.insert(2 + i, sig_array[i])
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
def readCompressedFile(compressed_str) :
    compressed_data = []          #用来存储压缩数据的数组
    # 取出前两个压缩数据，即第一个样本点 和 符号数的个数
    data_first = np.fromstring(compressed_str[0:32], dtype = np.short)
    compressed_data.append(data_first[0])
    compressed_data.append(data_first[1])
    data_next = np.fromstring(compressed_str[32:data_first[1] * 16], dtype = np.short)
    for num in data_next :
        compressed_data.append(num)
    # 去除第一个样本点，剩余所有数据都以 4 bit 存储
    compressed_str = compressed_str[data_first[1] * 16:len(compressed_str)]
    compressed_data_append = np.fromstring(compressed_str, dtype = np.uint8)
    # 将读取出来的数据装进压缩数组中，每一个数据，拆成两个 4 bit 数
    for num in compressed_data_append :
        # 存储的时候，是转成 4 bit 无符号整数存储的， 解密时，需要转换回来
        compressed_data.append((num >> 4) - 8)
        compressed_data.append(((np.uint8(num << 4)) >> 4) - 8)
    print("compressed_data : " + str(len(compressed_data)))
    return compressed_data

# 解密 还原文件
def decompressWaveFile(compressed_data) :
    quantized_num = 0.2
    sig_array = compressed_data[2:compressed_data[1] + 2]
    decompressed_data = []
    decompressed_data.append(compressed_data[0])
    compressed_data = compressed_data[compressed_data[1] + 2: len(compressed_data)]
    compressed_data.insert(1, decompressed_data[0])
    for i in range(len(compressed_data)) :
        if i == 0 : 
            continue
        de_num = math.exp(math.log(abs(decompressed_data[i - 1]) + 1) + compressed_data[i]* quantized_num) - 1
        if np.uint16(1 << (15 - (i % 16))) & sig_array[int(i / 16)] != 0 :
            decompressed_data.append((-1) * de_num)
            continue
        decompressed_data.append(de_num)
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
        sig_num = compressed_data[1]
        flag = 0
        num = 0
        for j in range(len(compressed_data)) :
            # 压缩数据的前一部分
            if j < sig_num + 2 :
                f.write(np.int16(compressed_data[j]))
            # 压缩数据 如果有最后一个数据没拼上一个子节，则丢弃该样本点
            else :
                if flag == 0 :
                    num = np.uint8((compressed_data[j] + 8 )<< 4)
                else :
                    num = np.uint8(num + np.uint8(compressed_data[j] + 8))
                    f.write(num)
                    flag = 1

    # 读压缩文件 解压
    with open("./压缩文件/" + str(i + 1) + ".dpc", "rb") as f :
        compressed_data = readCompressedFile(f.read())
        decompressed_data = decompressWaveFile(compressed_data)

    # 写还原文件
    with open("./还原文件/" + str(i + 1) + ".pcm", "wb") as f :
        for num in decompressed_data :
            f.write(np.int16(num))
    print("信噪比：" + str(calSignalToNoiseRatio(wave_data, decompressed_data)))