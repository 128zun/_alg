# ==========================================
# 1. 自製高階函數（無迴圈、使用遞迴）
# ==========================================

def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

def my_filter(func, lst):
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)

def my_reduce(func, lst, initializer=None):
    if initializer is None:
        if not lst:
            raise TypeError("reduce() of empty sequence with no initial value")
        return _reduce_rec(func, lst[1:], lst[0])
    return _reduce_rec(func, lst, initializer)

def _reduce_rec(func, lst, acc):
    if not lst:
        return acc
    return _reduce_rec(func, lst[1:], func(acc, lst[0]))


# ==========================================
# 2. 泡沫排序邏輯（無迴圈）
# ==========================================

# 單次冒泡掃描：使用自製的 my_reduce 將最大值推到最後方
def bubble_pass(lst):
    if not lst:
        return []
    
    # 累加函數：比較前一個保留值與當前元素，較大的繼續往右傳
    def compare_and_swap(acc, x):
        res, prev = acc
        if prev > x:
            return (res + [x], prev)  # 交換位置
        else:
            return (res + [prev], x)  # 維持順序
            
    res_list, last = my_reduce(compare_and_swap, lst[1:], ([], lst[0]))
    return res_list + [last]

# 整體泡沫排序：利用遞迴重複進行冒泡過程
def bubble_sort(lst):
    if len(lst) <= 1:
        return lst
    
    # 執行一次冒泡，此時最大的元素已被推到最右側
    passed = bubble_pass(lst)
    
    # 遞迴排序扣除最後一個已定位元素之外的其餘部分，並將其與最後一個元素串接
    return bubble_sort(passed[:-1]) + [passed[-1]]


# ==========================================
# 3. 測試程式
# ==========================================
if __name__ == "__main__":
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始陣列: {test_data}")
    
    sorted_data = bubble_sort(test_data)
    print(f"排序結果: {sorted_data}")