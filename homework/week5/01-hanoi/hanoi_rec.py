def hanoi_iterative(n, source, auxiliary, destination):
    # 使用 Stack 儲存指令，初始放入主任務
    # 格式：('call', n, src, aux, dest) 或 ('move', n, src, dest)
    stack = [('call', n, source, auxiliary, destination)]
    
    while stack:
        action, *args = stack.pop()
        
        if action == 'move':
            n, src, dest = args
            print(f"將盤子 {n} 從 {src} 移動到 {dest}")
            
        elif action == 'call':
            n, src, aux, dest = args
            if n == 1:
                print(f"將盤子 1 從 {src} 移動到 {dest}")
            else:
                # 為了符合 LIFO（後進先出），壓入順序必須與遞迴執行順序相反：
                # 3. 處理下方 n-1 個盤子從 aux -> dest
                stack.append(('call', n - 1, aux, src, dest))
                # 2. 處理第 n 個盤子的移動
                stack.append(('move', n, src, dest))
                # 1. 處理上方 n-1 個盤子從 src -> aux
                stack.append(('call', n - 1, src, destination, aux))

# 測試：3個盤子，柱子分別為 'A', 'B', 'C'
hanoi_iterative(3, 'A', 'B', 'C')