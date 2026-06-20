import os
from typing import List, Tuple

from puzzle import FutoshikiPuzzle  # Lớp Puzzle từ parser.py


def generate_kb(puzzle: FutoshikiPuzzle) -> List[List[str]]:
    """
    Sinh Ground Knowledge Base cho bài toán Futoshiki.

    Mỗi phần tử trong danh sách trả về là một mệnh đề (clause) dạng CNF,
    được biểu diễn là list các literal (string).
      - Literal khẳng định:  "Value(i,j,v)" hoặc "Less(v1,v2)"
      - Literal phủ định:    "-Value(i,j,v)" hoặc "-Less(v1,v2)"

    Các mệnh đề bao gồm:
      - Ô đã biết (ground facts)
      - Cặp thứ tự Less/2
      - Mỗi ô có tối đa một giá trị (at most one)
      - Mỗi hàng / cột không trùng giá trị (distinctness)
      - Mỗi hàng / cột phải chứa đầy đủ các số (completeness)
      - Các ràng buộc bất đẳng thức ngang & dọc
    """
    n = puzzle.n
    clauses = []

    # ---- 1. Các ô đã biết (pre-filled cells) ----
    for i in range(n):
        for j in range(n):
            val = puzzle.grid[i][j]
            if val != 0:
                clauses.append([f"Value({i},{j},{val})"])

    # ---- 2. Tập sự kiện Less(v1,v2) cho mọi 1 <= v1 < v2 <= n ----
    for v1 in range(1, n):
        for v2 in range(v1 + 1, n + 1):
            clauses.append([f"Less({v1},{v2})"])

    # ---- 3. Mỗi ô chỉ có nhiều nhất một giá trị (at most one) ----
    #   ¬Value(i,j,v) ∨ ¬Value(i,j,w)  với v < w
    for i in range(n):
        for j in range(n):
            for v in range(1, n):
                for w in range(v + 1, n + 1):
                    clauses.append([f"¬Value({i},{j},{v})", f"¬Value({i},{j},{w})"])

    # ---- 4. Mỗi hàng: không được có hai ô khác cột cùng giá trị ----
    #   ¬Value(i,j,v) ∨ ¬Value(i,k,v)  với j < k
    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                for v in range(1, n + 1):
                    clauses.append([f"¬Value({i},{j},{v})", f"¬Value({i},{k},{v})"])

    # ---- 5. Mỗi cột: không được có hai ô khác hàng cùng giá trị ----
    #   ¬Value(i,j,v) ∨ ¬Value(k,j,v)  với i < k
    for j in range(n):
        for i in range(n):
            for k in range(i + 1, n):
                for v in range(1, n + 1):
                    clauses.append([f"¬Value({i},{j},{v})", f"¬Value({k},{j},{v})"])

    # ---- 6. Mỗi hàng phải chứa đầy đủ tất cả giá trị từ 1..n ----
    #   Value(i,0,v) ∨ Value(i,1,v) ∨ ... ∨ Value(i,n-1,v)
    for i in range(n):
        for v in range(1, n + 1):
            clause = [f"Value({i},{j},{v})" for j in range(n)]
            clauses.append(clause)

    # ---- 7. Mỗi cột phải chứa đầy đủ tất cả giá trị từ 1..n ----
    #   Value(0,j,v) ∨ Value(1,j,v) ∨ ... ∨ Value(n-1,j,v)
    for j in range(n):
        for v in range(1, n + 1):
            clause = [f"Value({i},{j},{v})" for i in range(n)]
            clauses.append(clause)

    # ---- 8. Ràng buộc ngang (horizontal constraints) ----
    # h_constraints[i][j] =  1 -> (i,j) < (i,j+1)
    # h_constraints[i][j] = -1 -> (i,j) > (i,j+1)
    for i in range(n):
        for j in range(n - 1):
            h = puzzle.h_constraints[i][j]
            if h == 1:      # cell_left < cell_right
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 >= v2:   # không được: left >= right
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i},{j+1},{v2})"])
            elif h == -1:   # cell_left > cell_right
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 <= v2:   # không được: left <= right
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i},{j+1},{v2})"])

    # ---- 9. Ràng buộc dọc (vertical constraints) ----
    # v_constraints[i][j] =  1 -> (i,j) < (i+1,j)  (top < bottom)
    # v_constraints[i][j] = -1 -> (i,j) > (i+1,j)  (top > bottom)
    for i in range(n - 1):
        for j in range(n):
            v = puzzle.v_constraints[i][j]
            if v == 1:      # top < bottom
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 >= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i+1},{j},{v2})"])
            elif v == -1:   # top > bottom
                for v1 in range(1, n + 1):
                    for v2 in range(1, n + 1):
                        if v1 <= v2:
                            clauses.append([f"¬Value({i},{j},{v1})", f"¬Value({i+1},{j},{v2})"])

    # Loại bỏ các mệnh đề trùng lặp (có thể xảy ra nếu ràng buộc chồng lấn)
    seen = set()
    unique_clauses = []
    for clause in clauses:
        key = tuple(sorted(clause))   # thứ tự literal trong clause không quan trọng
        if key not in seen:
            seen.add(key)
            unique_clauses.append(clause)
    return unique_clauses


def write_kb(clauses: List[List[str]], output_path: str) -> None:
    """
    Ghi Knowledge Base ra file văn bản, mỗi dòng là một mệnh đề,
    các literal cách nhau bằng dấu phẩy.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
    with open(output_path, 'w', encoding='utf-8') as f:
        for clause in clauses:
            f.write(",".join(clause) + "\n")


# ------------------------------------------------------------
# Chạy độc lập để sinh KB cho tất cả các file input trong thư mục Inputs/
if __name__ == "__main__":
    from parser import read_input
    
    # Định nghĩa các thư mục tuyệt đối
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "Inputs")
    kb_dir = os.path.join(current_dir, "KB")
    
    os.makedirs(kb_dir, exist_ok=True)
    
    # Lấy danh sách các file input-*.txt
    input_files = sorted([
        f for f in os.listdir(input_dir)
        if f.startswith("input-") and f.endswith(".txt")
    ])
    
    if not input_files:
        print(f"Khong tim thay file input nao trong: {input_dir}")
    else:
        for filename in input_files:
            input_path = os.path.join(input_dir, filename)
            
            # Chuyển đổi tên file từ input-XX.txt thành kb-XX.txt
            kb_filename = filename.replace("input-", "kb-")
            output_path = os.path.join(kb_dir, kb_filename)
            
            print(f"Dang xu ly: {filename} -> {kb_filename}")
            try:
                puzzle = read_input(input_path)
                kb = generate_kb(puzzle)
                write_kb(kb, output_path)
                print(f"  Thanh cong: Da tao {kb_filename} voi {len(kb)} menh de.")
            except Exception as e:
                print(f"  Loi khi xu ly {filename}: {e}")