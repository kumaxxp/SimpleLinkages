from sympy import*
import numpy as np

def generate_k_matrix(eq, x):
    K = Matrix(np.zeros((len(x), len(x))))
    for i in range(len(eq)):
        for j in range(len(x)):
            K[i, j] = - expand(eq[i]).coeff(x[j])
    return K


# 変数リスト--------------------------------------------------------------------------------
# xの変数を定義
x1, x2 = symbols('x1 x2')
x = [x1, x2]

# kの変数を定義
k1, k2 = symbols('k1 k2')

# aの変数を定義(今回使わないけど式の整合ののために定義)
a1, a2 = symbols('a1 a2')

# mの変数を定義(今回使わないけど式の整合ののために定義)
m1, m2 = symbols('m1 m2')

# fの変数を定義(今回使わないけど式の整合ののために定義)
f1, f2 = symbols('f1 f2')

# 運動方程式をモデルを読んだ通りに書く----------------------------------------------------------
e1 = f1 - k1 * x1 + k2 * (x2 - x1) - m1 * a1
e2 = f2 - k2 * (x2 - x1)

eq = [e1, e2]

# 剛性マトリクスを生成する関数を実行
K = generate_k_matrix(eq, x)

print(K)

print(latex(K))
