import os
from typing import List

from puzzle import FutoshikiPuzzle


def read_input(file_path: str) -> FutoshikiPuzzle:
    """
    Doc file cau truc du lieu input-XX.txt, bo qua comment '#' va cac dong trong,
    sau do khoi tao va tra ve doi tuong FutoshikiPuzzle.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Khong tim thay file du lieu tai duong dan: {file_path}")

    valid_lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            clean_line = line.strip()
            # Bo qua dong trong hoac dong ghi chu (comment)
            if not clean_line or clean_line.startswith('#'):
                continue
            valid_lines.append(clean_line)

    if not valid_lines:
        raise ValueError(f"File {file_path} khong chua du lieu hop le.")

    # 1. Doc kich thuoc luoi N
    n = int(valid_lines[0])
    idx = 1

    # 2. Doc ma tran Grid so (N dong, moi dong N phan tu)
    grid = []
    for _ in range(n):
        grid.append([int(x) for x in valid_lines[idx].split(',')])
        idx += 1

    # 3. Doc ma tran rang buoc ngang (N dong, moi dong N-1 phan tu)
    horiz = []
    for _ in range(n):
        horiz.append([int(x) for x in valid_lines[idx].split(',')])
        idx += 1

    # 4. Doc ma tran rang buoc doc (N-1 dong, moi dong N phan tu)
    vert = []
    for _ in range(n - 1):
        vert.append([int(x) for x in valid_lines[idx].split(',')])
        idx += 1

    return FutoshikiPuzzle(n, grid, horiz, vert)


def save_solution(puzzle: FutoshikiPuzzle, solved_grid: List[List[int]], output_path: str) -> None:
    """
    Nhan ma tran loi giai hoan chinh, thuc hien dan xen cac ky tu so sanh (<, >, ^, v)
    de can chinh hien thi truc quan, sau do ghi file output va in ra man hinh console.
    """
    output_lines = []

    for i in range(puzzle.n):
        # --- Xay dung dong so kem dau rang buoc NGANG ---
        row_parts = []
        for j in range(puzzle.n):
            row_parts.append(str(solved_grid[i][j]))
            if j < puzzle.n - 1:
                h_val = puzzle.h_constraints[i][j]
                if h_val == 1:
                    row_parts.append("<")
                elif h_val == -1:
                    row_parts.append(">")
                else:
                    row_parts.append(" ")  # Khoang trang neu khong co rang buoc ngang
        
        # Ghep cac phan tu cach nhau bang khoang trang de ma tran thang hang
        output_lines.append(" ".join(row_parts))

        # --- Xay dung dong chua dau rang buoc DOC (neu chua toi dong cuoi cung) ---
        if i < puzzle.n - 1:
            vert_parts = []
            for j in range(puzzle.n):
                v_val = puzzle.v_constraints[i][j]
                if v_val == 1:
                    vert_parts.append("^")
                elif v_val == -1:
                    vert_parts.append("v")
                else:
                    vert_parts.append(" ")  # Khoang trang neu khong co rang buoc doc
                
                # Them khoang trong dem o giua de tuong thich vi tri voi hang so ben tren
                if j < puzzle.n - 1:
                    vert_parts.append(" ")
            
            output_lines.append(" ".join(vert_parts))

    # Gom toan bo du lieu van ban hoan chinh
    final_output = "\n".join(output_lines)

    # Dam bao thu muc cha cua file output ton tai truoc khi ghi file
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Ghi noi dung vao tep dau ra
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_output + "\n")

    # Dong thoi in ra stdout theo yeu cau dac ta cua do an
    print(f"\n================ [XUAT FILE: {os.path.basename(output_path)}] ================")
    print(final_output)
    print("========================================================\n")
