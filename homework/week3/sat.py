from typing import Dict, List, Optional, Set

Clause = Set[int]
CNF = List[Clause]
Assignment = Dict[int, bool]


def simplify(clauses: CNF, literal: int) -> CNF:
    """根據賦值 (literal 為 True) 化簡子句集:

    1. 移除所有包含該文字的子句 (該子句已滿足)
    2. 從剩餘子句中移除 -literal (因為該文字的相反必定為 False)
    """
    neg_literal = -literal
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue  # 子句已滿足，略過
        # 若子句含有反向文字，該文字無法成立，將其過濾
        new_clause = {lit for lit in clause if lit != neg_literal}
        new_clauses.append(new_clause)
    return new_clauses


def dpll(clauses: CNF, assignment: Assignment) -> Optional[Assignment]:
    """DPLL 遞迴求解函式"""
    # 1. 終止條件檢查
    # 所有子句皆已滿足
    if not clauses:
        return assignment
    # 存在空子句，代表衝突（無法滿足）
    if any(len(c) == 0 for c in clauses):
        return None

    # 2. 單元傳播 (Unit Propagation)
    for clause in clauses:
        if len(clause) == 1:
            unit_lit = next(iter(clause))
            var = abs(unit_lit)
            val = unit_lit > 0
            new_assign = assignment.copy()
            new_assign[var] = val
            simplified_clauses = simplify(clauses, unit_lit)
            return dpll(simplified_clauses, new_assign)

    # 3. 純文字消除 (Pure Literal Elimination)
    all_literals = {lit for clause in clauses for lit in clause}
    pure_literals = [
        lit for lit in all_literals if -lit not in all_literals
    ]
    if pure_literals:
        pure_lit = pure_literals[0]
        var = abs(pure_lit)
        val = pure_lit > 0
        new_assign = assignment.copy()
        new_assign[var] = val
        simplified_clauses = simplify(clauses, pure_lit)
        return dpll(simplified_clauses, new_assign)

    # 4. 分支選擇 (選第一個出現的變數嘗試 True 與 False)
    chosen_lit = next(iter(clauses[0]))
    chosen_var = abs(chosen_lit)

    # 先嘗試令 chosen_var 為 True
    assign_true = assignment.copy()
    assign_true[chosen_var] = True
    res = dpll(simplify(clauses, chosen_var), assign_true)
    if res is not None:
        return res

    # 若失敗，回溯嘗試令 chosen_var 為 False
    assign_false = assignment.copy()
    assign_false[chosen_var] = False
    return dpll(simplify(clauses, -chosen_var), assign_false)


def solve_sat(clauses: CNF) -> Optional[Assignment]:
    """SAT 求解入口"""
    return dpll(clauses, {})


# ==========================
# 範例測試
# ==========================
if __name__ == "__main__":
    # 範例 1: 可滿足問題 (SAT)
    # (x1 OR x2) AND (NOT x1 OR x3) AND (NOT x2 OR NOT x3)
    # 寫成 DIMACS 格式:
    cnf_sat: CNF = [{1, 2}, {-1, 3}, {-2, -3}]

    solution = solve_sat(cnf_sat)
    print("--- 範例 1: SAT 測試 ---")
    if solution:
        print("狀態: SATISFIABLE")
        print("解法 (變數賦值):", sorted(solution.items()))
    else:
        print("狀態: UNSATISFIABLE")

    # 範例 2: 不可滿足問題 (UNSAT)
    # (x1) AND (NOT x1)
    cnf_unsat: CNF = [{1}, {-1}]

    print("\n--- 範例 2: UNSAT 測試 ---")
    solution_unsat = solve_sat(cnf_unsat)
    if solution_unsat:
        print("狀態: SATISFIABLE")
        print("解法:", solution_unsat)
    else:
        print("狀態: UNSATISFIABLE")