# 命令词识别

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


