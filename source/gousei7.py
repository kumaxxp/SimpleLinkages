from sympy import*
import numpy as np

# 変数リスト--------------------------------------------------------------------------------
# xの変数を定義
x_p0, x_p1, x_p2, x_p3, x_p4, x_p5, x_p6 = symbols('x_p0 x_p1 x_p2 x_p3 x_p4 x_p5 x_p6')
x = [x_p0, x_p1, x_p2, x_p3, x_p4, x_p5, x_p6]

# kの変数を定義
k_p0, k_p1, k_p2, k_p3, k_p4, k_p5, k_p6 = symbols('k_p0 k_p1 k_p2 k_p3 k_p4 k_p5 k_p6')

# aの変数を定義(今回使わないけど式の整合ののために定義)
a_p0, a_p1, a_p2, a_p3, a_p4, a_p5, a_p6 = symbols('a_p0 a_p1 a_p2 a_p3 a_p4 a_p5 a_p6')

# mの変数を定義(今回使わないけど式の整合ののために定義)
m_p0, m_p1, m_p2, m_p3, m_p4, m_p5, m_p6 = symbols('m_p0 m_p1 m_p2 m_p3 m_p4 m_p5 m_p6')

# fの変数を定義(今回使わないけど式の整合ののために定義)
f_p0, f_p1, f_p2, f_p3, f_p4, f_p5, f_p6 = symbols('f_p0 f_p1 f_p2 f_p3 f_p4 f_p5 f_p6')

# 運動方程式をモデルを読んだ通りに書く----------------------------------------------------------
eq_p0 = f_p0 - k_p0 * x_p0 + k_p1 * (x_p1 - x_p0) + k_p2 * (x_p2 - x_p0) + k_p3 * (x_p3 - x_p0) - m_p0 * a_p0
eq_p1 = f_p1 - k_p1 * (x_p1 - x_p0) + k_p4 * (x_p4 - x_p1) - m_p1 * a_p1
eq_p2 = f_p2 - k_p2 * (x_p2 - x_p0) + k_p5 * (x_p5 - x_p2) - m_p2 * a_p2
eq_p3 = f_p3 - k_p3 * (x_p3 - x_p0) + k_p6 * (x_p6 - x_p3) - m_p3 * a_p3
eq_p4 = f_p4 - k_p4 * (x_p4 - x_p1) - m_p4 * a_p4
eq_p5 = f_p5 - k_p5 * (x_p5 - x_p1) - m_p5 * a_p5
eq_p6 = f_p6 - k_p6 * (x_p6 - x_p1) - m_p6 * a_p6

eq = [eq_p0, eq_p1, eq_p2, eq_p3, eq_p4, eq_p5, eq_p6]

def generate_k_matrix(eq, x):
    K = Matrix(np.zeros((len(x), len(x))))
    for i in range(len(eq)):
        for j in range(len(x)):
            K[i, j] = - expand(eq[i]).coeff(x[j])
    return K

# 剛性マトリクスを生成する関数を実行
K = generate_k_matrix(eq, x)

print(K)

print(latex(K))

