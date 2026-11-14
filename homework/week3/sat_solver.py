import sys
import re


def solve_sat(expression: str):
    # 提取變數（排除 Python 邏輯關鍵字與布林常數）
    keywords = {'and', 'or', 'not', 'True', 'False'}
    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', expression)
    variables = sorted(list(set(tokens) - keywords))

    # 手動遞迴搜尋組合
    def backtrack(index, current_env):
        if index == len(variables):
            if eval(expression, {"__builtins__": {}}, current_env):
                return True, current_env
            return False, {}

        var = variables[index]

        current_env[var] = True
        sat, res = backtrack(index + 1, current_env)
        if sat:
            return True, res

        current_env[var] = False
        sat, res = backtrack(index + 1, current_env)
        if sat:
            return True, res

        del current_env[var]
        return False, {}

    return backtrack(0, {})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python sat_solver.py \"<邏輯表達式>\"")
        sys.exit(1)

    expr = sys.argv[1]
    satisfiable, assignment = solve_sat(expr)

    if satisfiable:
        print(f"SAT {assignment}")
    else:
        print("UNSAT")