def hanoi_recursive(n, source, auxiliary, destination):
    if n == 1:
        print(f"將盤子 1 從 {source} 移動到 {destination}")
        return
    
    # 1. 將 n-1 個盤子從 source 移動到 auxiliary
    hanoi_recursive(n - 1, source, destination, auxiliary)
    
    # 2. 將第 n 個盤子從 source 移動到 destination
    print(f"將盤子 {n} 從 {source} 移動到 {destination}")
    
    # 3. 將 n-1 個盤子從 auxiliary 移動到 destination
    hanoi_recursive(n - 1, auxiliary, source, destination)

# 測試：3個盤子，柱子分別為 'A', 'B', 'C'
hanoi_recursive(3, 'A', 'B', 'C')