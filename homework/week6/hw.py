class Term:
    pass

class Var(Term):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Abs(Term):
    def __init__(self, param, body):
        self.param = param
        self.body = body
    def __repr__(self):
        return f"(λ{self.param}. {self.body})"

class App(Term):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    def __repr__(self):
        # 為了排版簡潔，適當加上括號
        func_str = f"({self.func})" if isinstance(self.func, Abs) else str(self.func)
        arg_str = f"({self.arg})" if not isinstance(self.arg, Var) else str(self.arg)
        return f"{func_str} {arg_str}"

# 計算自由變數 (Free Variables)
def free_vars(term):
    if isinstance(term, Var):
        return {term.name}
    elif isinstance(term, Abs):
        return free_vars(term.body) - {term.param}
    elif isinstance(term, App):
        return free_vars(term.func) | free_vars(term.arg)
    return set()

# 產生不衝突的新變數名稱（用於 Alpha 轉換）
def fresh_var(base, existing_vars):
    new_name = base
    i = 1
    while new_name in existing_vars:
        new_name = f"{base}_{i}"
        i += 1
    return new_name

# 避免變數捕捉的取代機制 (Capture-avoiding Substitution: term[var_name := replacement])
def substitute(term, var_name, replacement):
    if isinstance(term, Var):
        return replacement if term.name == var_name else term
    elif isinstance(term, App):
        return App(substitute(term.func, var_name, replacement),
                   substitute(term.arg, var_name, replacement))
    elif isinstance(term, Abs):
        if term.param == var_name:
            return term
        elif term.param not in free_vars(replacement):
            return Abs(term.param, substitute(term.body, var_name, replacement))
        else:
            # 進行 Alpha 轉換以避免變數捕捉
            new_param = fresh_var(term.param, free_vars(replacement) | free_vars(term.body))
            new_body = substitute(term.body, term.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var_name, replacement))
    return term

# 單步規約 (Normal-order reduction strategy)
def reduce_step(term):
    if isinstance(term, Var):
        return term, False
    elif isinstance(term, Abs):
        new_body, changed = reduce_step(term.body)
        return Abs(term.param, new_body), changed
    elif isinstance(term, App):
        # 如果函數部分是一個抽象，則執行 Beta 規約
        if isinstance(term.func, Abs):
            reduced = substitute(term.func.body, term.func.param, term.arg)
            return reduced, True
        # 否則先規約函數部分
        new_func, changed = reduce_step(term.func)
        if changed:
            return App(new_func, term.arg), True
        # 若函數無法規約，則規約引數部分
        new_arg, changed = reduce_step(term.arg)
        return App(term.func, new_arg), changed
    return term, False

# 完整評估並顯示所有計算步驟
def evaluate(term):
    current = term
    steps = [str(current)]
    while True:
        next_term, changed = reduce_step(current)
        if not changed:
            break
        current = next_term
        steps.append(str(current))
    return current, steps