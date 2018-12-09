博客地址：[图像颜色空间转换—— Python 实现](https://blog.csdn.net/rocketeerLi/article/details/84927935)

# 实验内容

1. 完成如下颜色空间的转换。

* RGB -> YIQ 
* RGB -> HSI 
* RGB -> YCbCr 
* RGB -> XYZ 

2. 选做：自己实现对 BMP 文件头的读取，并解析 BMP 图像文件。

# 代码运行命令

	python .\main.py ./01.bmp
	
第一个参数是文件的命令，只支持读取 bmp 格式的文件

# 颜色空间转换的算法及流程

## RGB -> YIQ ：

首先，需要将读取的 R，G，B 分量进行归一化，归一到 $[0,1]$ 区间，然后再利用下面的公式进行计算：

![YIQ计算公式](https://img-blog.csdnimg.cn/20181209171549583.png)

计算完成后，需要将其标准化，即转成 $[0,255]$ 区间内。标准化的时候，要将I 和 Q 分量+128。不同的标准可能数值会有一些差异，但不会差别很大。

## RGB -> HSI ：

HSI 颜色模型介绍：

![HSI 色彩模型](https://img-blog.csdnimg.cn/2018120914100329.jpg)

RGB 转成 HSI 稍微复杂一些，具体步骤如下：

首先，需要将 R、G、B 三种颜色通道进行转换：

![HSI 中的RGB转换](https://img-blog.csdnimg.cn/20181209171644578.png)

然后再进行转换，其中 H 维度需要进行一次判断，具体公式如下：

![HSI转换公式](https://img-blog.csdnimg.cn/20181209171814692.png)

计算完成后，再进行转换，转换公式如下：

![HSI标准化](https://img-blog.csdnimg.cn/20181209171903734.png)

这样就算转换成功了，计算稍微复杂一点但也不算太麻烦。最后，记得将 H 维度截断成 $[0,255]$ 区间内。

## RGB -> YCbCr ：

先来看百度百科的介绍：

这个转换公式比较简单，直接乘上一个转换矩阵再转换一下就可以了：

![YCbCr计算公式](https://img-blog.csdnimg.cn/20181209172025943.png)

## RGB -> XYZ ：

还是先来看看百度百科：

这个跟 RGB 空间比较相似，计算也比较简单，直接乘上一个转换矩阵，转换公式如下：

![XYZ转换公式](https://img-blog.csdnimg.cn/20181209172105286.png)

# 实验结果

## 原始图片 ：

![海王-原始图片](https://img-blog.csdnimg.cn/20181209145327731.jpg)

## RGB -> YIQ ：

![RGB -> YIQ](https://img-blog.csdnimg.cn/20181209161544888.png)

## RGB -> HSI ：

![RGB -> HSI](https://img-blog.csdnimg.cn/20181209161605370.png)

## RGB -> YCbCr ：

![RGB -> YCbCr](https://img-blog.csdnimg.cn/2018120916192341.png)

## RGB -> XYZ ：

![RGB -> XYZ](https://img-blog.csdnimg.cn/201812091620085.png)


# 总结

这次的实验还是挺简单的，主要纠结的地方还是颜色空间的转换矩阵和转换方式有不同的标准，没有统一，因此不知道用哪个。总体的思路还是很清晰的。
