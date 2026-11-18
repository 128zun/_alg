"""
題目 5：用黎曼積分法，寫函數 integral(f, low, high) 來做 n 變數積分
分別用 1 維, 2 維, 5 維, 100 維來計算 f(x) = x_1^2 + ... + x_n^2, low=0, high=1

[AI 使用聲明 / AI Usage Statement]
本程式由人工智慧模型（Gemini）協助生成，並經過人工審閱、數學解析解驗證與測試。
"""

import itertools
import time
import numpy as np


def integral(f, low, high, steps_per_dim: int = 10) -> float:
    """
    使用多維中點黎曼積分法計算 n 變數超體積積分 (n = len(low))
    包含維度災難防呆機制，避免高維度計算量爆炸導致程式當機。
    """
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    if low.shape != high.shape:
        raise ValueError("low 與 high 的陣列長度必須相同！")

    n_dim = len(low)
    total_points = steps_per_dim ** n_dim

    # 防呆機制：網格點數超過 10^7 則拒絕執行（如 100 維）
    if total_points > 1e7:
        raise MemoryError(
            f"維度災難警告！{n_dim} 維度若每維切 {steps_per_dim} 格，"
            f"總網格數高達 {total_points:.2e}，無法在合理時間與記憶體內完成。"
        )

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
    print("=== 題目 5：黎曼積分法多維度測試 f(x) = x_1^2 + ... + x_n^2 ===")
    f_nd = lambda x: float(np.sum(x**2))
    dimensions = [1, 2, 5, 100]

    for n in dimensions:
        low_arr = np.zeros(n)
        high_arr = np.ones(n)
        exact_val = n / 3.0  # 解析解為 n / 3

        print(f"\n--- 維度 n = {n} (理論解析解 = {exact_val:.6f}) ---")
        t0 = time.time()
        try:
            # 1維切1000格，2維切100格，5維切10格，100維即便切2格也會觸發維度災難
            steps = 1000 if n == 1 else (100 if n == 2 else (10 if n == 5 else 2))
            res = integral(f_nd, low_arr, high_arr, steps_per_dim=steps)
            dt = time.time() - t0
            print(f"結果: {res:.6f} | 誤差: {abs(res - exact_val):.6f} | 耗時: {dt:.4f}s (每維切 {steps} 格)")
        except MemoryError as e:
            print(f"無法計算 -> {e}")