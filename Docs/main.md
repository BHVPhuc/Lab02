# Main Module - Dieu phoi chuong trinh

## 1. Mo ta tong quan

`main.py` la entry point chinh cua toan bo project. File nay KHONG chua bat ky logic giai puzzle nao. Nhiem vu duy nhat cua `main.py` la:

1. **Nhan lenh tu nguoi dung** (command line arguments)
2. **Dieu phoi cac solver** (goi dung solver theo yeu cau)
3. **Thu thap va hien thi ket qua** (thoi gian, so nodes, so backtracks)

Tuong tu nhu mot "nguoi dieu phoi san khau", `main.py` khong tu bieu dien ma chi goi cac "nghe si" (solver) len san khau va bao cao ket qua cho khan gia.

---

## 2. Cac thanh phan import

```python
import sys          # De doc tham so dong lenh (sys.argv)
import os           # De lam viec voi duong dan file
import time         # De do thoi gian chay
import argparse     # De xu ly tham so dong lenh

from puzzle import FutoshikiPuzzle              # Class du lieu dung chung
from parser import read_input, save_solution    # Doc input, xuat output
from backtracking_solver import BacktrackingSolver    # Solver cua ban
from brute_force_solver import BruteForceSolver        # Solver cua ban
```

Cac import duoc dat trong `try-except` de khi nguoi khac chua viet xong solver cua ho, chuong trinh van chay duoc:

```python
try:
    from forward_chaining_solver import ForwardChainingSolver
except ImportError:
    ForwardChainingSolver = None    # Neu file chua ton tai, bo qua
```

---

## 3. AVAILABLE_SOLVERS - Dang ky solver

### Chuc nang
Day la "danh sach nhan su" cua cac solver. Main se chi goi cac solver co trong danh sach nay.

### Cach hoat dong
```python
AVAILABLE_SOLVERS = {}

if BruteForceSolver:        # Kiem tra solver da duoc import thanh cong chua
    AVAILABLE_SOLVERS['brute_force'] = BruteForceSolver

if BacktrackingSolver:
    AVAILABLE_SOLVERS['backtracking'] = BacktrackingSolver

# Khi nguoi khac them solver moi, chi can them vao day:
# if ForwardChainingSolver:
#     AVAILABLE_SOLVERS['forward_chaining'] = ForwardChainingSolver
```

### Loi ich
- **Tu dong phat hien**: Khong can sua code khi them solver moi
- **Linh hoat**: Neu 1 solver loi, cac solver khac van chay duoc
- **De mo rong**: Them solver = them 3 dong code

---

## 4. Ham run_solver() - Chay 1 solver tren 1 test case

### Chuc nang
La "bo phan van hanh" chinh. Nhan 1 file input, 1 ten solver, chay va tra ve ket qua.

### Tham so dau vao

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `input_file` | str | Duong dan file input (vi du: "Inputs/input-01.txt") |
| `output_file` | str | Duong dan file output (vi du: "Outputs/output-01.txt") |
| `algorithm` | str | Ten solver muon dung (vi du: "backtracking", "brute_force") |
| `**kwargs` | dict | Cac tham so tuy chon cho solver (vi du: use_mrv=True) |

### Gia tri tra ve

| Key | Kieu | Y nghia |
|-----|------|---------|
| `algorithm` | str | Ten solver da chay |
| `time` | float | Thoi gian chay (giay) |
| `nodes_expanded` | int | So o da duoc thu |
| `backtracks` | int | So lan quay lui (chi co voi Backtracking) |
| `solution_found` | bool | Co tim duoc loi giai khong |
| `input_file` | str | File input da dung |
| `output_file` | str | File output da ghi |

### Luong hoat dong (step-by-step)

```
1. Kiem tra solver co ton tai khong
   Neu khong -> Bao loi

2. puzzle = read_input(input_file)
   Doc file input -> tao object FutoshikiPuzzle
   
3. solver = solver_class(puzzle, **kwargs)
   Tao solver moi voi puzzle vua doc
   
4. start_time = time.time()
   Ghi lai thoi diem bat dau
   
5. solution = solver.solve()
   Chay thuat toan giai puzzle
   
6. end_time = time.time()
   Ghi lai thoi diem ket thuc
   
7. Neu co solution:
      save_solution(puzzle, solution.grid, output_file)
      Ghi ket qua ra file (co dau < > ^ v)
   
8. Tra ve dict thong ke
```

### Vi du su dung

```python
# Chay Backtracking + MRV + FC
stats = run_solver(
    "Inputs/input-01.txt",
    "Outputs/output-01.txt",
    "backtracking",
    use_mrv=True,
    use_forward_checking=True
)

# Ket qua:
# {
#     'algorithm': 'Backtracking (MRV=True, FC=True)',
#     'time': 0.0003,
#     'nodes_expanded': 19,
#     'backtracks': 7,
#     'solution_found': True,
#     'input_file': 'Inputs/input-01.txt',
#     'output_file': 'Outputs/output-01.txt'
# }
```

---

## 5. Ham compare_all_algorithms() - So sanh tat ca solver

### Chuc nang
Chay TAT CA solver co san tren TAT CA test cases, sau do in bang so sanh.

Day la yeu cau cua de bai (phan "Comparison algorithms" - 5% diem).

### Tham so dau vao

| Tham so | Kieu | Mac dinh | Y nghia |
|---------|------|----------|---------|
| `input_dir` | str | 'Inputs' | Thu muc chua file input |
| `output_dir` | str | 'Outputs' | Thu muc ghi file output |

### Luong hoat dong

```
1. Tim tat ca file input-*.txt trong thu muc Inputs

2. Voi moi file input:
   
   2.1. Voi moi solver trong AVAILABLE_SOLVERS:
        
        a. Tao ten output file: output-01-brute_force.txt
        
        b. Chay run_solver() de giai
        
        c. Luu thong ke vao danh sach
        
        d. In ket qua ra man hinh

3. In bang tong hop so sanh tat ca
```

### Vi du output

```
====================================================================================================
SO SANH HIEU SUAT CAC THUAT TOAN
====================================================================================================
Cac thuat toan: ['brute_force', 'backtracking']

================================================================================
Test case: input-01.txt
================================================================================
[brute_force] Time: 0.0004s, Nodes: 142, Backtracks: -
[backtracking] Time: 0.0003s, Nodes: 19, Backtracks: 7

====================================================================================================
BANG TONG HOP KET QUA
====================================================================================================
File            Algorithm                 Time (s)     Nodes      Backtracks
----------------------------------------------------------------------------------------------------
input-01.txt    Brute Force               0.0004       142        -         
input-01.txt    Backtracking (MRV=Tru...  0.0003       19         7         
```

---

## 6. Ham main() - Entry point

### Chuc nang
Xu ly tham so dong lenh va goi dung ham tuong ung.

### Cac che do chay

#### Che do 1: Chay 1 file voi solver chi dinh
```bash
python main.py -i input-01.txt -o output.txt -a backtracking
```

Ket qua: Chi giai 1 file, dung 1 solver.

#### Che do 2: So sanh tat ca solver
```bash
python main.py --compare-all
```

Ket qua: Chay TAT CA solver tren TAT CA test cases, in bang so sanh.

#### Che do 3: Chay 1 solver tren tat ca test cases
```bash
python main.py -a brute_force --all-tests
```

Ket qua: Chi chay 1 solver, nhung tren TAT CA test cases.

#### Che do 4: Mac dinh (khong co tham so)
```bash
python main.py
```

Ket qua: Tu dong chay --compare-all.

### Cach xu ly tham so

```python
parser = argparse.ArgumentParser(description='Futoshiki Puzzle Solver')

# -i, --input: Ten file input
parser.add_argument('-i', '--input', help='File input (vi du: input-01.txt)')

# -o, --output: Ten file output
parser.add_argument('-o', '--output', default='output.txt', help='File output')

# -a, --algorithm: Ten solver
parser.add_argument('-a', '--algorithm', default='backtracking', 
                   choices=list(AVAILABLE_SOLVERS.keys()) + ['all'],
                   help='Thuat toan su dung')

# --compare-all: Bat co so sanh tat ca
parser.add_argument('--compare-all', action='store_true', 
                   help='So sanh tat ca cac thuat toan')

# --all-tests: Bat chay tren tat ca test cases
parser.add_argument('--all-tests', action='store_true',
                   help='Chay tren tat ca test cases')
```

---

## 7. Luong du lieu tong quan

```
Nguoi dung nhap lenh
       |
       v
  main.py (nhan lenh)
       |
       v
  run_solver() / compare_all_algorithms()
       |
       |---> parser.read_input() ---> FutoshikiPuzzle
       |                              |
       |                              v
       |                         solver.solve()
       |                              |
       |                              v
       |                         Solution (grid da giai)
       |                              |
       |                              v
       |---> parser.save_solution() ---> Output File
       |
       v
   In thong ke ra man hinh
```

---

## 8. Loi ich thiet ke

| Loi ich | Giai thich |
|---------|-----------|
| **Tach biet ro rang** | Main chi dieu phoi, khong biet gi ve cach giai puzzle |
| **De mo rong** | Them solver moi = them 3 dong import + 2 dong dang ky |
| **De bao tri** | Sua logic solver khong anh huong den main |
| **De test** | Co the test tung solver rieng biet ma khong can main |
| **Tu dong hoa** | So sanh hieu suat tu dong, khong can lam thu cong |

---

## 9. Vi du them solver moi (cua nguoi khac)

Gia su nguoi 1 viet xong `forward_chaining_solver.py`:

### Buoc 1: Them import
```python
# Them vao main.py
try:
    from forward_chaining_solver import ForwardChainingSolver
except ImportError:
    ForwardChainingSolver = None
```

### Buoc 2: Dang ky solver
```python
if ForwardChainingSolver:
    AVAILABLE_SOLVERS['forward_chaining'] = ForwardChainingSolver
```

### Buoc 3: Chay thu
```bash
# Chay 1 file
python main.py -i input-01.txt -o output.txt -a forward_chaining

# So sanh voi cac solver khac
python main.py --compare-all
```

Ket qua: `forward_chaining` tu dong xuat hien trong bang so sanh!
