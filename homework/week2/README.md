# 計算 $2^n$ 的演算法與效能比較 (`power2n.py`)

本專案透過實作四種不同的演算法來計算 $2^n$，並以 $n = 100$ 作為基準測試，觀察不同時間複雜度（Time Complexity）對程式執行速度與可行性的實際影響。

---

## 演算法實作說明

1. **方法 1：內建運算子 (`2 ** n`)**
   * 直接使用 Python 內建的次方運算子，底層由 C 語言最佳化（採用快速冪演算法），效率極高。
   * **時間複雜度**：$O(\log n)$

2. **方法 2a：純遞迴（雙重呼叫加法）**
   * 透過 `power2n(n - 1) + power2n(n - 1)` 進行計算。由於每次呼叫都會分裂成兩個相同的子問題，會產生極度嚴重的重複計算。
   * **時間複雜度**：$O(2^n)$

3. **方法 2b：純遞迴（單一呼叫乘法）**
   * 透過 `2 * power2n(n - 1)` 進行計算，將問題規模線性縮小，大幅減少呼叫次數。
   * **時間複雜度**：$O(n)$

4. **方法 3：遞迴 + 查表法 (Memoization)**
   * 延續方法 2a 的加法邏輯，但引入字典（`memo`）記錄已經計算過的結果，避免重複遞迴，屬於動態規劃（Dynamic Programming）的基礎應用。
   * **時間複雜度**：$O(n)$

---

## 完整程式碼 (`power2n.py`)

```python
import time

# 方法 1：內建運算子 (最快，由底層優化)
def power2n_1(n):
    return 2 ** n

# 方法 2a：用遞迴 (加法形式：power2n(n-1) + power2n(n-1))
# ⚠️ 注意：時間複雜度為 O(2^n)，當 n=100 時會完全跑不出來！
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

# 方法 2b：用遞迴 (乘法形式：2 * power2n(n-1))
# 時間複雜度為 O(n)，遞迴深度 100，在 Python 預設極限 (1000) 內可輕鬆完成。
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：用遞迴 + 查表 (Memoization)
# 透過字典紀錄已算過的值，避免重複計算，時間複雜度降為 O(n)。
memo = {0: 1}
def power2n_3(n):
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]


if __name__ == '__main__':
    n = 100
    print(f"=== 測試 n = {n} ===")

    # 1. 測試方法 1
    start = time.perf_counter()
    res1 = power2n_1(n)
    end = time.perf_counter()
    print(f"方法 1 (內建 2**n)       : 耗時 {(end - start) * 1000:.6f} ms")

    # 2. 測試方法 2b
    start = time.perf_counter()
    res2b = power2n_2b(n)
    end = time.perf_counter()
    print(f"方法 2b (遞迴乘法 O(n))   : 耗時 {(end - start) * 1000:.6f} ms")

    # 3. 測試方法 3
    start = time.perf_counter()
    res3 = power2n_3(n)
    end = time.perf_counter()
    print(f"方法 3 (遞迴+查表 O(n))   : 耗時 {(end - start) * 1000:.6f} ms")

    # 4. 測試方法 2a (特別說明與小規模測試)
    print("\n[方法 2a 狀態說明]")
    print("若對方法 2a 帶入 n = 100，其運算次數高達 2^100（約 1.26 × 10^30 次），電腦會直接卡死、跑不出來。")
    
    # 改用較小的 n = 25 示範方法 2a 的指數級消耗
    n_small = 25
    start = time.perf_counter()
    res2a = power2n_2a(n_small)
    end = time.perf_counter()
    print(f"-> 改用較小的 n = {n_small} 測試方法 2a: 耗時 {(end - start) * 1000:.6f} ms (結果: {res2a})")
```

---

## 測試結果與效能總結 ($n = 100$)

| 方法 | 核心邏輯 | 時間複雜度 | 空間複雜度 | $n=100$ 執行狀態 | 效能排名 |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **方法 1** | `2 ** n` | $O(\log n)$ | $O(1)$ | **瞬間完成** (約 $0.001\text{ ms}$) | 🥇 最快 |
| **方法 2b** | `2 * f(n-1)` | $O(n)$ | $O(n)$ | **極快完成** (約 $0.01\text{ ms}$) | 🥈 次快 |
| **方法 3** | `f(n-1) + f(n-1)` + 查表 | $O(n)$ | $O(n)$ | **極快完成** (約 $0.02\text{ ms}$) | 🥉 第三 |
| **方法 2a** | `f(n-1) + f(n-1)` | $O(2^n)$ | $O(n)$ | ❌ **無法算出** (程式卡死) | 🐢 最慢 |

### 關鍵結論
* **哪個出不來？**
  **方法 2a** 完全跑不出來。當 $n = 100$ 時，總運算次數高達 $2^{100} \approx 1.26 \times 10^{30}$ 次，即使用現代超級電腦也無法在有生之年算完。
* **哪個最快？**
  **方法 1** 最快，因為 Python 底層直接使用 C 語言實作的快速冪運算，不需要額外的函數呼叫開銷。
* **遞迴的限制：**
  雖然方法 2b 與方法 3 都能輕鬆算出 $n = 100$，但因為兩者皆依賴遞迴，當 $n \ge 1000$ 時，會觸發 Python 預設的遞迴深度限制而拋出 `RecursionError`。