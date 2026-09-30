# 定義三種求解 sqrt(5) 的迭代推進函數
f1 = lambda x: 5 / x
f2 = lambda x: x - 1 / 6 * (x * x - 5)
f3 = lambda x: 1 / 2 * (x + 5 / x)

# 初始猜測值皆設為 1.0
x1 = x2 = x3 = 1.0

print(f"{'回合':>4} | {'f1 (5/x)':^12} | {'f2 (線性調整)':^14} | {'f3 (牛頓法/巴比倫)':^18}")
print("-" * 56)

for i in range(1, 13):
    x1, x2, x3 = f1(x1), f2(x2), f3(x3)
    print(f"{i:4d} | {x1:12.6f} | {x2:14.6f} | {x3:18.10f}")

print("-" * 56)
print(f"真實數值 sqrt(5) = {5**0.5:.10f}")