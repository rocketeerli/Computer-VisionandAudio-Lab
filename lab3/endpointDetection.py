# -*- coding: utf-8 -*-
import wave
import os
import numpy as np

def sgn(data):
    if data >= 0 :
        return 1
    else :
        return 0

class EndPointDetect :
    # 构造函数
    def __init__(self, wave_data):
        self.wave_data = wave_data
        self.energy = EndPointDetect.calEnergy(wave_data)
        self.zeroCrossingRate = EndPointDetect.calZeroCrossingRate(wave_data)
        self.wave_data_detected = EndPointDetect.endPointDetect(wave_data, self.energy, self.zeroCrossingRate)

    # 计算每一帧的能量 256个采样点为一帧
    @staticmethod   
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
    @staticmethod   
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
    @staticmethod  
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
        # print("较高能量阈值，计算后的浊音A:" + str(A))

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
        # print("较低能量阈值，增加一段语言B:" + str(B))

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
        # print("过零率阈值，最终语音分段C:" + str(C))
        return C