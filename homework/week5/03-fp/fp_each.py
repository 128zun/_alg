# 1. 自製 map：對串列每個元素套用函數
def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

# 2. 自製 filter：根據條件過濾串列元素
def my_filter(func, lst):
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)

# 3. 自製 reduce：將串列元素進行累加/摺疊
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