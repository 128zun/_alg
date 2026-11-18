"""
題目 1：用數值方法來算單變數微分和積分

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import numpy as np


def diff_1d(f, x: float, h: float = 1e-6) -> float:
    """使用中央差分法 (Central Difference) 計算單變數函數在點 x 的一階導數"""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def integral_1d_riemann(f, low: float, high: float, n_steps: int = 10000) -> float:
    """使用中點黎曼和 (Midpoint Riemann Sum) 計算單變數定積分"""
    dx = (high - low) / n_steps
    x_mid = np.linspace(low + dx / 2.0, high - dx / 2.0, n_steps)
    return float(np.sum(f(x_mid)) * dx)


if __name__ == "__main__":
    print("=== 題目 1：單變數數值微分與積分測試 ===")
    # 測試函數: f(x) = x^3 + 2x
    # 解析解: f'(2) = 3(2^2) + 2 = 14.0
    # 積分 [0, 2]: \int_0^2 (x^3 + 2x) dx = [x^4/4 + x^2]_0^2 = 4 + 4 = 8.0
    f = lambda x: x**3 + 2 * x

    d_res = diff_1d(f, 2.0)
    int_res = integral_1d_riemann(f, 0.0, 2.0, n_steps=10000)

    print(f"數值微分 f'(2)     : {d_res:.6f} (理論解析解: 14.000000)")
    print(f"數值積分 [0, 2]    : {int_res:.6f} (理論解析解:  8.000000)")