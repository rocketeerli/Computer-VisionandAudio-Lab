# 写在前面

花了几天时间写完了第一个视听觉信号处理的实验，其实还挺简单的，在这里分享一下。

本文介绍一下利用双门限法进行语音端点检测的方法，该方法主要利用了语音的**短时能量**和**短时过零率**，关于这两个语音特征如何求解，前两篇文章已经介绍过了（[短时能量](https://blog.csdn.net/rocketeerLi/article/details/83271399)和[短时过零率](https://blog.csdn.net/rocketeerLi/article/details/83307319)），这里就不详细介绍了。这篇文章的重点在双门限法的算法思想和实现过程。

先来解释一下什么叫**端点检测**：

**端点检测就是在一段包含语音的信号中，准确地确定语音的起始点和终止点，将语音段和非语音段区分开**。我们知道，一段语音中，有静音部分和浊音部分，静音部分包括清音、噪音和无声（噪音可以归结到无声中），浊音部分和清音才是我们需要听的语音，因此，可以说只有这两部分才是对我们有用的语音。可以说，端点检测就是将这两部分区分出来。（注意，清音部分属于声音中的辅音，能量小，过零率高，一般是在浊音部分的前面）

# 算法介绍

## 算法简介

双门限法有三个阈值，前两个是语音能量的阈值，最后一个是语音过零率的阈值，至于为什么三个阈值却称为“双门限法”呢？我觉得这里的双门限不是指两个阈值，而是指，能量和过零率这两个时域特征。

至于为什么能用这两个特征来进行端点检测呢？最主要的原因就是：**浊音的能量高于清音，清音的过零率高于无声部分**。这样的话，我们就可以先利用能量，将浊音部分区分出来，再利用过零率，将清音也提取出来，就完成了端点检测。

## 算法步骤：

![双门限法](https://img-blog.csdn.net/20181023192209554?/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3JvY2tldGVlckxp/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

 1. 第一步是取一个较高的短时能量作为阈值MH，利用这个阈值，我们就可以先分出语音中的浊音部分（如图，A1到A2区间）。本次实验的MH，我取的是所有帧的短时能量的平均数的一半（平均数我试过了，偏大，处理有问题）。
 2. 第二步是取一个较低的能量阈值ML，利用这个阈值，我们可以从A1，A2，向两端进行搜索，将较低能量段的语音部分也加入到语音段，进一步扩大语音段范围（如图所示，B1-B2之间还是语音段）。本次实验中，我首先计算语音前一段的静音部分的能量均值（前5帧），我将静音部分的能量均值和MH的平均数的一半作为ML。
 3. 第三步是利用短时过零率，短时过零率的阈值为Zs。由于语音的两端部分是辅音（也就是清音部分），也是语音中的一部分，但是辅音的能量与静音部分的能量一样低，但是过零率比静音部分高出很多。为了区分开二者，将利用短时能量区分完的语音段继续向两端进行搜索，短时过零率大于3倍Zs的部分，则认为是语音的清音部分。将该部分加入语言段，就是求得的语音段（如图C1-C2部分）。

**至于为什么要这么设置这三个阈值，我只能告诉你，这是经验，或许你的比我设的更好**
 
 # Python实现：
```
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
```

# 写在后面

具体的实现过程在[这里](https://github.com/rocketeerli/Computer-VisionandAudio-Lab/tree/master/lab1)，包括前两篇文章的能量和过零率的提取。