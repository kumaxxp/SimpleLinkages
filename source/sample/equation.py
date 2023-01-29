from sympy import*

if __name__ == '__main__':
    # 変数を定義
    x, y, a, b, c, d, e, f = symbols('x, y, a, b, c, d, e, f')

    # 連立方程式を定義(右辺を0にした式として記述する）
    eq1 = a * x + b * y + e
    eq2 = c * x + d * y + f

    # 連立方程式を文字式のまま解く
    sol = solve([eq1, eq2], [x, y])
    
    # 結果を表示
#    print(sol)

    print(latex(eq1))
    print(latex(eq2))
    print(latex(sol))
