# -*- coding: UTF-8 -*-
import numpy as np
import math
# YIQ 变换
def imgTranYIQ(r, g, b) :
    matrix_tran = np.array([[0.299, 0.587, 0.114], \
                            [0.596, -0.274, -0.322], \
                            [0.211, -0.523, 0.312]])
    Y = []
    I = []
    Q = []
    for row in range(len(r)) :
        Y_row = []
        I_row = []
        Q_row = []
        for col in range(len(r[row])) :
            Y_row.append(matrix_tran[0][0] * r[row][col] + matrix_tran[0][1] * g[row][col] + matrix_tran[0][2] * b[row][col])
            I_row.append(matrix_tran[1][0] * r[row][col] + matrix_tran[1][1] * g[row][col] + matrix_tran[1][2] * b[row][col])
            Q_row.append(matrix_tran[2][0] * r[row][col] + matrix_tran[2][1] * g[row][col] + matrix_tran[2][2] * b[row][col])
        Y.append(Y_row)
        I.append(I_row)
        Q.append(Q_row)
    # 标准化
    return Y, I, Q

# HSI 变换
def imgTranHSI(R, G, B) :
    # 变化后的 g, b, r
    g = []
    b = []
    r = []
    for row in range(len(R)) :
        r_row = []
        g_row = []
        b_row = []
        for col in range(len(R[row])) :
            g_value = G[row][col]
            b_value = B[row][col]
            r_value = R[row][col]
            rgb_sum = g_value + b_value + r_value
            if rgb_sum == 0 :
                b_row.append(0)
                g_row.append(0)
                r_row.append(0)
            else :
                b_row.append(b_value / rgb_sum)
                g_row.append(g_value / rgb_sum)
                r_row.append(r_value / rgb_sum)
        b.append(b_row)
        g.append(g_row)
        r.append(r_row)
    # 计算 H、S、I三维通道
    H = []
    S = []
    I = []
    for row in range(len(r)) :
        H_row = []
        S_row = []
        I_row = []
        for col in range(len(r[row])) :
            r_value = r[row][col]
            g_value = g[row][col]
            b_value = b[row][col]
            # 计算 H_row_value
            sqrt_value = (r_value - g_value) * (r_value - g_value) + (r_value - b_value) * (g_value - b_value)
            sqrt_value = math.sqrt(sqrt_value)
            son_value = 0.5 * (r_value - g_value + r_value - b_value)
            if sqrt_value == 0 :
                H_row_value = 0
            else :
                acos_value = son_value / sqrt_value
                if acos_value > 1 :
                    acos_value = 1
                elif acos_value < -1 :
                    acos_value = -1
                H_row_value = math.acos(acos_value)
            if b[row][col] <= g[row][col] :
                H_row.append(H_row_value)
            else :
                H_row.append(math.pi * 2 - H_row_value)
            # 存储 S_row、I_row
            S_row.append(1 - 3 * min(r_value, g_value, b_value))
            I_row.append((R[row][col] + G[row][col] + B[row][col]) / (3 * 255))
        H.append(H_row)
        S.append(S_row)
        I.append(I_row)
    return H, S, I

# YCbCr 变换
def imgTranYCbCr(R, G, B) :
    matrix_tran = np.array([[0.299, 0.587, 0.114], \
                            [-0.169, -0.331, 0.5], \
                            [0.5, -0.419, -0.081]])
    Y = []
    Cb = []
    Cr = []
    for row in range(len(R)) :
        Y_row = []
        Cb_row = []
        Cr_row = []
        for col in range(len(R[row])) :
            Y_row.append(matrix_tran[0][0] * R[row][col] + matrix_tran[0][1] * G[row][col] + matrix_tran[0][2] * B[row][col])
            Cb_row.append(matrix_tran[1][0] * R[row][col] + matrix_tran[1][1] * G[row][col] + matrix_tran[1][2] * B[row][col] + 128)
            Cr_row.append(matrix_tran[2][0] * R[row][col] + matrix_tran[2][1] * G[row][col] + matrix_tran[2][2] * B[row][col] + 128)
        Y.append(Y_row)
        Cb.append(Cb_row)
        Cr.append(Cr_row)
    # 标准化
    return Y, Cb, Cr

# XYZ 变换
def imgTranXYZ(R, G, B) :
    matrix_tran = np.array([[0.412453, 0.357580, 0.180423], \
                            [0.212671, 0.715160, 0.072169], \
                            [0.019334, 0.119193, 0.950227]])
    X = []
    Y = []
    Z = []
    for row in range(len(R)) :
        X_row = []
        Y_row = []
        Z_row = []
        for col in range(len(R[row])) :
            X_row.append(matrix_tran[0][0] * R[row][col] + matrix_tran[0][1] * G[row][col] + matrix_tran[0][2] * B[row][col])
            Y_row.append(matrix_tran[1][0] * R[row][col] + matrix_tran[1][1] * G[row][col] + matrix_tran[1][2] * B[row][col])
            Z_row.append(matrix_tran[2][0] * R[row][col] + matrix_tran[2][1] * G[row][col] + matrix_tran[2][2] * B[row][col])
        X.append(X_row)
        Y.append(Y_row)
        Z.append(Z_row)
    return X, Y, Z
