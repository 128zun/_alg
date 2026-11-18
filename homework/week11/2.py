"""
題目 2：用蒙地卡羅法來算單變數積分

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import numpy as np


def integral_1d_mc(f, low: float, high: float, n_samples: int = 100000) -> float:
    """使用蒙地卡羅法 (Monte Carlo Integration) 計算單變數定積分"""
    x_rand = np.random.uniform(low, high, size=n_samples)
    volume = high - low
    return float(volume * np.mean(f(x_rand)))


if __name__ == "__main__":
    np.random.seed(42)
    print("=== 題目 2：單變數蒙地卡羅積分測試 ===")
    # 測試函數: f(x) = sin(x)，區間 [0, pi]
    # 解析解: \int_0^\pi \sin(x) dx = [-\cos(x)]_0^\pi = 1 - (-1) = 2.0
    f = lambda x: np.sin(x)

    res_mc = integral_1d_mc(f, 0.0, np.pi, n_samples=200000)
    print(f"蒙地卡羅積分 [0, pi]: {res_mc:.6f} (理論解析解: 2.000000)")