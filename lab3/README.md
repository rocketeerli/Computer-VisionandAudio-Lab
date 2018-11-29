# 命令词识别

**注意：运行的时候，需要更改我代码中的地址路径，虽然没几个路径，但有些是绝对路径，不更改是运行不了的。**

博客地址：[DTW 算法的实时语音识别——命令词识别（Python 实现）](https://blog.csdn.net/rocketeerLi/article/details/84638701)

# 实验要求

1. **设计命令词识别任务**
	* 设想一个任务，如智能家居、或车辆控制等
	* 确定词表，要求词表中不少于10个词
	* 录制语料。采集特定人（自己）语料，每个词不少于五遍。取其中一遍为模板，其它四遍用来测试。可以用采集工具(如cooledit)或编程实现语音采集。
	* 检查语料。通过听辩检查保证语料质量。
	* 去除静音。可以用端点检测算法实现，也可以手工实现

2. **特征提取**
	* 每帧提取39维MFCC特征，帧长25ms，帧移10ms
	* 可以采用HTK工具包中的hcopy命令实现（要求语料是WAV格式）
	hcopy -A -D -T 1 -C tr_wav.cfg -S .\data\list.scp

3. **识别测试**
	* N个模板，M个待测命令词语料，进行N*M次DTW计算，得到N*M个DTW距离
		* 分别载入模板和待测语料的MFCC特征矢量序列
		* 计算两个特征序列的 DTW 距离

4. **计算测试结果**
	* 每个测试语料都有一个类别标签 $l_i$
	* 每个测试语料都有一个识别结果 $r_i$
	* $r_i = maxD_{ij}$  其中， $D_{ij}$ 为第 i 个测试语料和第 j 个模板间的DTW距离（规整后）
	* 若 $r_i = l_i$ 表示识别结果正确
	* 计算正确率=识别结果正确的语料数/总测试语料数

5. **扩展尝试**
	* 开集扩展：采集一批集外命令词，重新计算正确率？
	* **实用扩展**：将经过实验验证的算法，转化为能实时采集，在线检测的命令词识别系统？（这里我做的就是这个扩展）
	* 算法扩展：尝试基于HMM的识别算法？

# 文件夹介绍

## 三个存放语音的文件夹

* **RecordedVoice** ： 我自己录制的语音命令，一共 10 个命令，每个命令录了 5 遍，共 50 个语音
* **RecordedVoice-EndPointed** ：对录好的 50 个语音命令进行端点检测后的语音，处理的代码是 endpointDetection_RecordedVoice.py
* **RecordedVoice-RealTime** ： 在代码中实时录取的语音存放的位置

## 两个 HTK 工具包

两个工具包都是一样的，除了其中的 list.scp ，这是该工具包的配置文件，存放了源文件和目的文件的路径
* **HTK-EndPointedVoice** : 这是对 50 个端点检测后的语音，进行 MFCC 特征提取的工具包。 该工具包的源文件路径为：RecordedVoice；目标文件路径为：MFCC-EndPointedVoice
* **HTK-RealTimeRecordedVoice** ： 这是对实时录音好的语音文件进行 MFCC 特征提取的工具包。 该工具包的源文件路径为：RecordedVoice-RealTime；目标文件路径为：

## 两个存放 MFCC 特征的文件夹

* **MFCC-EndPointedVoice** ：存放利用 Hcopy 提取录制的 50 个命令词的 MFCC 特征。
* **MFCC-RealTimeRecordedVoice** ：存放利用 Hcopy 提取实时录音的语音文件的 MFCC 特征。

## 三个 Python 脚本文件

* **endpointDetection.py** ： 一个端点检测的库，由实验一的代码改造的
* **endpointDetection_RecordedVoice.py** ： 对录取的语音进行端点检测的脚本
* **VoiceRecognition.py** ： 语音识别的脚本，包括静态语音匹配和语音实时匹配，是该实验的主要脚本

# 命令词 10 个

* 1. 开门
* 2. 关门
* 3. 播放音乐
* 4. 关闭音乐
* 5. 打开空调
* 6. 关闭空调
* 7. 打开电视
* 8. 关闭电视
* 9. 开始扫地
* 10. 停止扫地


