# 通用迭代演算法框架 (Generic Iterator Framework)

本專案將數值分析、線性代數、微分方程數值解以及機器學習中的多種經典迭代法，抽象為一個統一的推進模型：

$$s_{k+1} = g(s_k)$$

透過分離**狀態轉移邏輯**、**收斂判定條件**與**主迭代迴圈**，任何迭代演算法均能以高度模組化且乾淨的形式實作。

---

## 核心設計理念

核心函式 `generic_iterator` 僅定義演算法主幹，運算細節與終止條件交由呼叫端透過函式指標（Lambda 或自訂函式）注入：

```python
def generic_iterator(transition_func, is_converged, initial_state, max_iter=1000):
    """
    通用迭代法框架
    :param transition_func: 狀態推進函數 g(state) -> next_state
    :param is_converged: 終止/收斂判定函數 is_converged(state, next_state, iteration) -> bool
    :param initial_state: 初始狀態（純量、向量、矩陣或 Tuple）
    :param max_iter: 最大迭代步數限制
    :return: (最終狀態, 實際迭代次數)
    """
```

---

## 實作範例一覽

本專案在 `iter_framework.py` 中展示了 9 種經典演算法的框架套用：

| 範例名稱 | 領域 | 狀態形式 ($s$) | 轉移運算 ($g(s)$) | 收斂判斷標準 |
|---|---|---|---|---|
| **二維不動點迭代** (`demo_fixed_point`) | 數值分析 | 2D 向量 | 仿射變換矩陣相乘 | $\Vert s_{new} - s_{old}\Vert_2 < 10^{-6}$ |
| **牛頓求根法** (`demo_newton`) | 方程式求根 | 純量 | $x - \frac{f(x)}{f'(x)}$ | $\vert x_{new} - x_{old}\vert < 10^{-6}$ |
| **高斯-賽得爾法** (`demo_gauss_seidel`) | 線性方程組 | 向量 | 逐分量利用最新估計值回代 | $\max \vert x_{new} - x_{old}\vert < 10^{-6}$ |
| **冪次迭代法** (`demo_power_iteration`) | 線性代數 | 特徵向量 | $A v / \Vert A v\Vert_2$ | `np.allclose(old, new, atol=1e-6)` |
| **QR 演算法** (`demo_qr_algorithm`) | 特徵值計算 | 方陣 | $A_k = Q_k R_k \to A_{k+1} = R_k Q_k$ | 非對角線絕對值和 $< 10^{-6}$ |
| **4 階龍格-庫塔** (`demo_rk4`) | 常微分方程 (ODE) | $(t, y)$ 元組 | RK4 步進加權公式 | 抵達終點時間 $t \ge t_{end}$ |
| **PageRank 演算法** (`demo_pagerank`) | 網路分析 | 排名向量 | Google 矩陣轉移乘法 $G r$ | $\Vert r_{new} - r_{old}\Vert_2 < 10^{-6}$ |
| **K-Means 聚類** (`demo_kmeans`) | 非監督學習 | 群中心矩陣 | E 步 (最近鄰分配) + M 步 (重算中心) | 質心變動最大差值 $< 10^{-6}$ |
| **EM 演算法** (`demo_em_two_coin`) | 統計估計 | 機率元組 $(\theta_A, \theta_B)$ | E 步 (隱變數期望) + M 步 (最大似然更新) | 雙參數變動均小於 $10^{-6}$ |

---

## 環境依賴與執行方式

### 1. 安裝依賴
確保環境中安裝有 `numpy`：
```bash
pip install numpy
```

### 2. 執行程式
在終端機或 VS Code 內建終端執行：
```bash
python iter_framework.py
```

---

## 擴充指引

若要將其他演算法套入此框架，僅需定義三要素：

1. **初始狀態 (`initial_state`)**：決定資料結構（純量、`np.ndarray` 或 `tuple`）。
2. **轉移函式 (`transition_func`)**：接受目前狀態，計算並回傳下一狀態。
3. **收斂判定 (`is_converged`)**：接收 `(old_state, new_state, iteration)`，符合終止條件時回傳 `True`。

```python
# 範例：利用框架進行簡易梯度下降求 y = x^2 極小值
lr = 0.1
transition = lambda x: x - lr * (2 * x)
converged = lambda old, new, i: abs(new - old) < 1e-6

x_min, iters = generic_iterator(transition, converged, initial_state=10.0)
print(f"極小值點: {x_min}, 迭代次數: {iters}")
```