# Lab02_AI

## Kiến trúc dự án

```
Lab02_AI/
├── Source/                          # Source code chính
│   ├── puzzle.py                    # Class FutoshikiPuzzle (dùng chung)
│   ├── parser.py                    # Đọc input + Xuất output
│   ├── validator.py                 # Bộ kiểm tra ràng buộc và kết quả toàn cục
│   ├── brute_force_solver.py        # Brute Force Solver
│   ├── backtracking_solver.py       # Backtracking Solver (MRV + Forward Checking)
│   ├── forward_chaining.py          # Forward Chaining Solver
│   ├── backward_chaining.py         # Backward Chaining Solver
│   ├── astar_solver.py              # A* Search Solver
│   ├── kb_generator.py              # Bộ sinh tri thức FOL -> CNF -> Grounding
│   ├── main.py                      # Entry point - Điều phối tất cả thuật toán
│   ├── Inputs/                      # 10 test cases (input-01.txt → input-10.txt)
│   └── Outputs/                     # Kết quả giải (output-XX.txt)
│
├── Resource/                        # Hình ảnh puzzle
│   ├── 1.4x4.png, 1.4x4_sol.png
│   ├── 2.4x4.png, 2.4x4_sol.png, 2.4x4_trick.png
│   ├── 3.5x5.png, 3.5x5_sol.png
│   ├── 4.5x5.png, 4.5x5_sol.png
│   ├── 5.6x6.png
│   └── image.png
│
├── KB/                  ← thư mục mới
│   ├── kb-01.txt
│   ├── kb-02.txt
│   ...
│   └── kb-10.txt
│
├── Report.pdf                       # Báo cáo project
└── README.md                        # Mô tả dự án
```

## Phân công nhiệm vụ

| Thành viên | Nhiệm vụ | File chính |
|-----------|---------|-----------|
| **Người 1** | Core Engine & Parser & Validator | `puzzle.py`, `parser.py`, `validator.py` |
| **Người 2** | Brute Force + Backtracking | `brute_force_solver.py`, `backtracking_solver.py` |
| **Người 3** | A* Search | `astar_solver.py` |
| **Người 4** | FOL + CNF + KB Generation | `kb_generator.py` |
| **Người 5** | Forward Chaining + Backward Chaining + Report | `forward_chaining.py`, `backward_chaining.py`, `report/` |

## Luồng dữ liệu

```
Input File (input-XX.txt)
    │
    ▼
parser.read_input() → FutoshikiPuzzle (puzzle.py)
    │
    ├──→ BruteForceSolver.solve() ──→ parser.save_solution() ──→ Output File
    │
    ├──→ BacktrackingSolver.solve() ──→ parser.save_solution() ──→ Output File
    │
    ├──→ ForwardChainingSolver.solve() ──→ parser.save_solution() ──→ Output File
    │
    ├──→ BackwardChainingSolver.solve() ──→ parser.save_solution() ──→ Output File
    │
    └──→ AStarSolver.solve() ──→ parser.save_solution() ──→ Output File
```

## Các thành phần chính

### `puzzle.py` - Dữ liệu dùng chung
- `FutoshikiPuzzle`: Class đại diện cho puzzle N×N
- Chứa: grid, h_constraints, v_constraints
- Các hàm: `is_valid()`, `find_empty()`, `is_complete()`, `clone()`

### `parser.py` - I/O
- `read_input(file_path)`: Đọc file input → `FutoshikiPuzzle`
- `save_solution(puzzle, solved_grid, output_path)`: Ghi output có dấu `< > ^ v`

### `main.py` - Điều phối
- Tự động phát hiện các solver có sẵn
- Chạy 1 solver hoặc so sánh tất cả
- Thu thập thống kê hiệu suất

## Test cases

| File | Kích thước | Mô tả |
|------|-----------|-------|
| input-01.txt | 4×4 | Có given values + constraints |
| input-02.txt | 4×4 | Nhiều constraints |
| input-03.txt | 5×5 | Empty puzzle |
| input-04.txt | 5×5 | Có given values |
| input-05.txt | 6×6 | Empty puzzle |
| input-06.txt | 6×6 | Có given values |
| input-07.txt | 7×7 | Empty puzzle |
| input-08.txt | 7×7 | Có given values |
| input-09.txt | 9×9 | Empty puzzle |
| input-10.txt | 9×9 | Có given values |
