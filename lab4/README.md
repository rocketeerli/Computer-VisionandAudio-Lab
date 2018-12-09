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

# 介绍

在介绍颜色空间转换之前，先来介绍一下什么是颜色空间。

**颜色空间指的是组织颜色的特定方式**。我们知道，一种颜色可以由 红、绿、蓝 三种颜色组合出来，这里的 红、绿、蓝 三原色就是一种颜色模型。而这种由三原色组织颜色的方法就是一种颜色空间。任何一种颜色，在颜色空间中，都可以通过一个函数表示出来，在 RGB 模型中，函数的参数就是 R、G、B 三原色。

当然，同一种颜色，在不同的颜色空间中，由于侧重点不同，表现出来的色彩是不一样的。通常的图片是采用的 RGB 三原色来表示的，所以，现在，我们的目的就是将同一幅图片转换成用其他颜色空间来表示。

这篇文章中一共有四张颜色空间的转换：

* RGB -> YIQ 
* RGB -> HSI 
* RGB -> YCbCr 
* RGB -> XYZ 

# 颜色空间转换的算法及流程

## RGB -> YIQ ：

先来介绍一下 YIQ 这个颜色空间，百度百科：

> YIQ色彩空间属于NTSC系统。这里Y是指颜色的明视度，即亮度。其实Y就是图像灰度值，I和Q都指的是指色调，即描述图像色彩与饱和度的属性。YIQ颜色空间具有能将图像中的亮度分量分离提取出来的优点，并且YIQ颜色空间与RGB颜色空间之间是线性变换的关系，计算量小，聚类特性也比较好，可以适应光照强度不断变化的场合。

首先，需要将读取的 R，G，B 分量进行归一化，归一到 $[0,1]$ 区间，然后再利用下面的公式进行计算：

$$\begin{bmatrix} Y \\ I \\ Q \\  \end{bmatrix} = 
\begin{bmatrix} 0.299 & 0.587 & 0.114 \\ 
				0.596 & -0.274 & -0.322 \\ 
				0.211 & -0.523 & 0.312 \\  \end{bmatrix}
\begin{bmatrix} R \\ G \\ B \\  \end{bmatrix}$$

计算完成后，需要将其标准化，即转成 $[0,255]$ 区间内。标准化的时候，要将I 和 Q 分量+128。不同的标准可能数值会有一些差异，但不会差别很大。

## RGB -> HSI ：

HSI 颜色模型介绍：

> HSI〔Hue-Saturation-Intensity(Lightness),HSI或HSL〕颜色模型用H、S、I三参数描述颜色特性，其中H定义颜色的波长，称为色调；S表示颜色的深浅程度，称为饱和度；I表示强度或亮度。在HSI颜色模型的双六棱锥表示，I是强度轴，色调H的角度范围为[0，2π]，其中，纯红色的角度为0，纯绿色的角度为2π/3，纯蓝色的角度为4π/3。

![HSI 色彩模型](https://img-blog.csdnimg.cn/2018120914100329.jpg)

RGB 转成 HSI 稍微复杂一些，具体步骤如下：

首先，需要将 R、G、B 三种颜色通道进行转换：

$$r = \frac{R}{R + G + B} \ \ \ \ 
    g = \frac{G}{R + G + B} \ \ \ \ 
    b =  \frac{B}{R + G + B} $$

然后再进行转换，其中 H 维度需要进行一次判断，具体公式如下：

$$h = \cos^{-1}  
\left( \frac{0.5\cdot
	\left[ \left(r - g\right) + \left(r - b\right)\right] }
	{\left[\left(r - g\right)^2 +  \left(r - b \right)  \left(g - b \right) \right]^{\frac12}}
\right) \ \ \ \  
h \in [0, \pi] \ for \ \ b \leq g$$

$$h = 2\pi -  \cos^{-1}  
\left( \frac{0.5\cdot
	\left[ \left(r - g\right) + \left(r - b\right)\right] }
	{\left[\left(r - g\right)^2 +  \left(r - b \right)  \left(g - b \right) \right]^{\frac12}}
\right) \ \ \ \  
h \in [0, \pi] \ for \ \ b > g$$

$$s = 1 - 3 \cdot min(r, g, b) \ \ \ s \in [0,1]$$

$$i = \frac{R + G + B} { 3 \cdot 255} \ \ \ i \in [0,1]$$

计算完成后，再进行转换，转换公式如下：

$$ H = \frac{h \times 180} {\pi}$$

$$ S = s \times 100$$

$$ I = i \times 255$$

这样就算转换成功了，计算稍微复杂一点但也不算太麻烦。最后，记得将 H 维度截断成 $[0,255]$ 区间内。

## RGB -> YCbCr ：

先来看百度百科的介绍：

> YCbCr或Y'CbCr有的时候会被写作：YCBCR或是Y'CBCR，是色彩空间的一种，通常会用于影片中的影像连续处理，或是数字摄影系统中。Y'为颜色的亮度(luma)成分、而CB和CR则为蓝色和红色的浓度偏移量成份。Y'和Y是不同的，而Y就是所谓的流明(luminance)，表示光的浓度且为非线性，使用伽马修正(gamma correction)编码处理。

这个转换公式比较简单，直接乘上一个转换矩阵再转换一下就可以了：

$$\begin{bmatrix} Y \\ Cb \\ Cr \\  \end{bmatrix} = 
\begin{bmatrix} 0 \\ 128 \\ 128 \\  \end{bmatrix} + 
\begin{bmatrix} 0.299 & 0.587 & 0.114 \\ 
				-0.169 & -0.331 & 0.5 \\ 
				0.5 & -0.419 & -0.081 \\  \end{bmatrix}
\begin{bmatrix} R \\ G \\ B \\  \end{bmatrix}$$

## RGB -> XYZ ：

还是先来看看百度百科：

> 1931CIE-XYZ系统，就是在RGB系统的基础上，用数学方法，选用三个理想的原色来代替实际的三原色，从而将CIE-RGB系统中的光谱三刺激值和色度坐标r、g、b均变为正值。

这个跟 RGB 空间比较相似，计算也比较简单，直接乘上一个转换矩阵，转换公式如下：

$$\begin{bmatrix} X \\ Y \\ Z \\  \end{bmatrix} = 
\begin{bmatrix} 0.412453 & 0.357580 & 0.180423 \\ 
				0.212671 & 0.715160 & 0.072169 \\ 
				0.019334 & 0.119193 & 0.950227 \\  \end{bmatrix}
\begin{bmatrix} R \\ G \\ B \\  \end{bmatrix}$$

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

