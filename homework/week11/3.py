"""
題目 3：用數值方法來算 n 變數微分(梯度）和積分（超體積）

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import itertools
import numpy as np


def grad_nd(f, x, h: float = 1e-6) -> np.ndarray:
    """使用中央差分法計算 n 變數函數在點 x 的梯度向量 (Gradient)"""
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2.0 * h)
    return grad


def integral_nd_riemann(f, low, high, steps_per_dim: int = 20) -> float:
    """使用多維中點黎曼和計算 n 變數超體積積分"""
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    n_dim = len(low)

    dx = (high - low) / steps_per_dim
    cell_volume = float(np.prod(dx))

    grids = [
        np.linspace(low[i] + dx[i] / 2.0, high[i] - dx[i] / 2.0, steps_per_dim)
        for i in range(n_dim)
    ]

    total_sum = 0.0
    for point in itertools.product(*grids):
        total_sum += f(np.array(point))

    return total_sum * cell_volume


if __name__ == "__main__":
    print("=== 題目 3：n 變數數值梯度與超體積積分測試 ===")
    # 1. 梯度測試: f(x, y, z) = x^2 + 2y^2 + 3z^2 在 (1, 2, 3) 的梯度
    # 解析解: [2x, 4y, 6z] -> [2.0, 8.0, 18.0]
    f_grad = lambda v: v[0] ** 2 + 2 * (v[1] ** 2) + 3 * (v[2] ** 2)
    grad_res = grad_nd(f_grad, [1.0, 2.0, 3.0])
    print(f"數值梯度 grad f(1,2,3) : {grad_res} (理論解析解: [ 2.  8. 18.])")

    # 2. 超體積積分測試: f(x, y, z) = x + y + z 在 [0, 1] x [0, 2] x [0, 1] 的三重積分
    # 解析解: \int_0^1 \int_0^2 \int_0^1 (x+y+z) dx dy dz = 2 * (0.5 + 1.0 + 0.5) = 4.0
    f_vol = lambda v: v[0] + v[1] + v[2]
    vol_res = integral_nd_riemann(f_vol, [0.0, 0.0, 0.0], [1.0, 2.0, 1.0], steps_per_dim=20)
    print(f"3D 超體積積分結果      : {vol_res:.6f} (理論解析解: 4.000000)")