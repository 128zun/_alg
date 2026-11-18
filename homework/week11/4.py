"""
題目 4：用蒙地卡羅法來算 n 變數積分(超體積）

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import numpy as np


def integral_nd_mc(f, low, high, n_samples: int = 200000) -> float:
    """使用蒙地卡羅法計算 n 變數超體積積分"""
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    n_dim = len(low)

    samples = np.random.uniform(low, high, size=(n_samples, n_dim))
    hyper_volume = float(np.prod(high - low))
    values = np.apply_along_axis(f, 1, samples)

    return hyper_volume * float(np.mean(values))


if __name__ == "__main__":
    np.random.seed(42)
    print("=== 題目 4：n 變數蒙地卡羅超體積積分測試 ===")
    # 測試函數: f(x, y, z) = x + y + z 在 [0, 1] x [0, 2] x [0, 1] 的三重積分
    # 解析解: 4.0
    f_vol = lambda v: v[0] + v[1] + v[2]
    mc_res = integral_nd_mc(f_vol, [0.0, 0.0, 0.0], [1.0, 2.0, 1.0], n_samples=200000)
    print(f"3D 蒙地卡羅超體積積分: {mc_res:.6f} (理論解析解: 4.000000)")