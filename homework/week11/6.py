"""
題目 6：改用蒙地卡羅法做 n 變數積分，題目同上一題
分別用 1 維, 2 維, 5 維, 100 維來計算 f(x) = x_1^2 + ... + x_n^2, low=0, high=1

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import time
import numpy as np


def integral_mc(f, low, high, n_samples: int = 200000) -> float:
    """使用蒙地卡羅法計算 n 變數超體積積分"""
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    if low.shape != high.shape:
        raise ValueError("low 與 high 的陣列長度必須相同！")

    n_dim = len(low)
    samples = np.random.uniform(low, high, size=(n_samples, n_dim))
    hyper_volume = float(np.prod(high - low))

    values = np.apply_along_axis(f, 1, samples)
    return hyper_volume * float(np.mean(values))


if __name__ == "__main__":
    np.random.seed(42)
    print("=== 題目 6：蒙地卡羅法多維度測試 f(x) = x_1^2 + ... + x_n^2 ===")
    f_nd = lambda x: float(np.sum(x**2))
    dimensions = [1, 2, 5, 100]

    for n in dimensions:
        low_arr = np.zeros(n)
        high_arr = np.ones(n)
        exact_val = n / 3.0  # 解析解為 n / 3

        print(f"\n--- 維度 n = {n} (理論解析解 = {exact_val:.6f}) ---")
        t0 = time.time()
        res = integral_mc(f_nd, low_arr, high_arr, n_samples=200000)
        dt = time.time() - t0
        print(f"結果: {res:.6f} | 誤差: {abs(res - exact_val):.6f} | 耗時: {dt:.4f}s (抽樣 200,000 點)")