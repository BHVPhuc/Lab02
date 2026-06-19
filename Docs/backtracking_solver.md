# Backtracking Solver

## 1. Mo ta tong quan

`backtracking_solver.py` chua class `BacktrackingSolver` - thuat toan cai tien tu Brute Force voi hai ky thuat quan trong:

1. **MRV (Minimum Remaining Values)**: Chon o co it gia tri hop le nhat de gan truoc
2. **Forward Checking**: Loai bo gia tri khong hop le khoi domain cua cac o lien quan sau moi lan gan

Tuong tu nhu "giai ma co chien luoc", Backtracking khong thu ngau nhien ma chon o kho nhat truoc, va phat hien som khi nao nhanh khong di duoc.

---

## 2. Class BacktrackingSolver

### 2.1. Thuoc tinh

| Thuoc tinh | Kieu | Y nghia |
|-----------|------|---------|
| `original` | FutoshikiPuzzle | Puzzle goc (khong bi thay doi) |
| `use_mrv` | bool | Co bat MRV khong |
| `use_forward_checking` | bool | Co bat Forward Checking khong |
| `nodes_expanded` | int | Dem so o da duoc thu gan gia tri |
| `backtracks` | int | Dem so lan phai quay lui |
| `solution` | FutoshikiPuzzle | Loi giai tim duoc (neu co) |

---

### 2.2. Phuong thuc khoi tao

#### `__init__(self, puzzle, use_mrv=True, use_forward_checking=True)`

Tao solver moi voi cac tuy chon.

**Tham so:**

| Tham so | Kieu | Mac dinh | Y nghia |
|---------|------|----------|---------|
| `puzzle` | FutoshikiPuzzle | bat buoc | Puzzle can giai |
| `use_mrv` | bool | True | Co dung MRV khong |
| `use_forward_checking` | bool | True | Co dung Forward Checking khong |

**Vi du:**
```python
from puzzle import FutoshikiPuzzle
from backtracking_solver import BacktrackingSolver

puzzle = FutoshikiPuzzle(...)  # Tao puzzle

# Day du tinh nang
solver = BacktrackingSolver(puzzle, use_mrv=True, use_forward_checking=True)

# Chi dung MRV, khong Forward Checking
solver = BacktrackingSolver(puzzle, use_mrv=True, use_forward_checking=False)

# Khong dung gi ca (gan giong Brute Force)
solver = BacktrackingSolver(puzzle, use_mrv=False, use_forward_checking=False)
```

---

### 2.3. Phuong thuc giai chinh

#### `solve(self) -> Optional[FutoshikiPuzzle]`

Giai puzzle bang Backtracking.

**Gia tri tra ve:**
- `FutoshikiPuzzle`: Loi giai tim duoc
- `None`: Khong tim duoc loi giai

**Luong hoat dong:**
```
1. Tao ban sao puzzle
   puzzle = self.original.clone()

2. Reset cac bo dem
   self.nodes_expanded = 0
   self.backtracks = 0

3. Khoi tao domain cho moi o
   domains = self._init_domains(puzzle)

4. Goi ham de quy _backtrack(puzzle, domains)

5. Neu tim duoc loi giai:
       self.solution = puzzle
       return puzzle
   Neu khong:
       return None
```

---

### 2.4. Phuong thuc khoi tao domain

#### `_init_domains(self, puzzle) -> List[List[Set[int]]]`

Tao danh sach cac gia tri hop le cho moi o.

**Gia tri tra ve:**
- `List[List[Set[int]]]`: Ma tran N x N, moi phan tu la Set cac gia tri hop le

**Luong hoat dong:**
```
1. Tao ma tran domains rong (N x N)

2. Voi moi o (i, j):
   
   Neu o da co gia tri (grid[i][j] != 0):
       domains[i][j] = {grid[i][j]}  # Chi co 1 gia tri
   
   Neu o trong (grid[i][j] == 0):
       Thu tung gia tri tu 1 den N
       Neu is_valid(i, j, value):
           Them value vao domains[i][j]
```

**Vi du:**
```python
# Puzzle 4x4, o (0,0) trong, cac so 1,2,3,4 deu hop le
# o (0,1) da co so 2
# o (2,2) da co so 3

domains = solver._init_domains(puzzle)
# domains[0][0] = {1, 2, 3, 4}
# domains[0][1] = {2}
# domains[2][2] = {3}
```

---

### 2.5. Phuong thuc chon bien

#### `_select_unassigned_variable(self, puzzle, domains) -> Optional[Tuple[int, int]]`

Chon o trong tiep theo de gan gia tri.

**Co 2 che do:**

**Che do 1: Khong MRV (use_mrv=False)**
- Chon o trong dau tien tim thay (tu trai sang phai, tu tren xuong duoi)
- Giong Brute Force

**Che do 2: Co MRV (use_mrv=True)**
- Tim o co it gia tri hop le nhat (smallest domain)
- Neu nhieu o cung so luong, dung Degree Heuristic chon o co nhieu rang buoc nhat

**Luong hoat dong MRV:**
```
1. Khoi tao:
   min_remaining = vo cung
   best_cell = None

2. Duyet tat ca o trong:
   Voi moi o (i, j) ma grid[i][j] == 0:
       
       remaining = len(domains[i][j])
       
       Neu remaining < min_remaining:
           min_remaining = remaining
           best_cell = (i, j)
       
       Neu remaining == min_remaining:
           # Tie-breaker: Degree Heuristic
           Neu o (i,j) co nhieu rang buoc hon best_cell:
               best_cell = (i, j)

3. Tra ve best_cell
```

**Vi du:**
```python
# O (0,0) co domain {1, 2, 3, 4} -> 4 gia tri
# O (1,1) co domain {2} -> 1 gia tri
# O (2,3) co domain {1, 4} -> 2 gia tri

# MRV se chon o (1,1) vi chi co 1 gia tri (de nhat)
```

---

### 2.6. Phuong thuc dem rang buoc

#### `_count_constraints(self, puzzle, row, col) -> int`

Dem so rang buoc lien quan den o (row, col).

**Dung cho:** Degree Heuristic (tie-breaker cua MRV)

**Luong hoat dong:**
```
count = 0

# Kiem tra rang buoc ngang ben trai
Neu col > 0 va h_constraints[row][col-1] != 0:
    count += 1

# Kiem tra rang buoc ngang ben phai
Neu col < N-1 va h_constraints[row][col] != 0:
    count += 1

# Kiem tra rang buoc doc phia tren
Neu row > 0 va v_constraints[row-1][col] != 0:
    count += 1

# Kiem tra rang buoc doc phia duoi
Neu row < N-1 va v_constraints[row][col] != 0:
    count += 1

return count
```

**Vi du:**
```python
# O (0,0) co rang buoc ngang phai va rang buoc doc duoi
# -> count = 2

# O (1,1) khong co rang buoc nao
# -> count = 0
```

---

### 2.7. Phuong thuc Forward Checking

#### `_forward_check_with_log(self, puzzle, domains, row, col, value, removed) -> bool`

Sau khi gan gia tri cho o (row, col), loai bo gia tri khong hop le khoi domain cua cac o lien quan.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Puzzle dang giai |
| `domains` | List[List[Set]] | Domain hien tai cua cac o |
| `row` | int | Hang cua o vua gan |
| `col` | int | Cot cua o vua gan |
| `value` | int | Gia tri vua gan |
| `removed` | List | Danh sach luu cac thay doi de hoan tac |

**Gia tri tra ve:**
- `True`: Khong co van de, tiep tuc
- `False`: Co o nao do domain rong -> can quay lui ngay

**Luong hoat dong chi tiet:**

```
1. Loai bo gia tri khoi cac o cung hang
   Voi moi cot c != col:
       Neu o (row, c) trong va value trong domain:
           Xoa value khoi domain[row][c]
           Luu lai: removed.append((row, c, value))
           
           Neu domain[row][c] rong:
               return False  # That bai!

2. Loai bo gia tri khoi cac o cung cot
   Voi moi hang r != row:
       Neu o (r, col) trong va value trong domain:
           Xoa value khoi domain[r][col]
           Luu lai: removed.append((r, col, value))
           
           Neu domain[r][col] rong:
               return False

3. Kiem tra rang buoc ngang ben trai
   Neu col > 0 va o (row, col-1) trong:
       
       constraint = h_constraints[row][col-1]
       
       Neu constraint == 1 (left < right):
           # right = value, nen left phai < value
           Xoa cac gia tri >= value khoi domain[row][col-1]
       
       Neu constraint == -1 (left > right):
           # right = value, nen left phai > value
           Xoa cac gia tri <= value khoi domain[row][col-1]
       
       Neu domain[row][col-1] rong:
           return False

4. Kiem tra rang buoc ngang ben phai
   Neu col < N-1 va o (row, col+1) trong:
       
       constraint = h_constraints[row][col]
       
       Neu constraint == 1 (left < right):
           # left = value, nen right phai > value
           Xoa cac gia tri <= value khoi domain[row][col+1]
       
       Neu constraint == -1 (left > right):
           # left = value, nen right phai < value
           Xoa cac gia tri >= value khoi domain[row][col+1]
       
       Neu domain[row][col+1] rong:
           return False

5. Kiem tra rang buoc doc phia tren
   Neu row > 0 va o (row-1, col) trong:
       
       constraint = v_constraints[row-1][col]
       
       Neu constraint == 1 (top < bottom):
           # bottom = value, nen top phai < value
           Xoa cac gia tri >= value khoi domain[row-1][col]
       
       Neu constraint == -1 (top > bottom):
           # bottom = value, nen top phai > value
           Xoa cac gia tri <= value khoi domain[row-1][col]
       
       Neu domain[row-1][col] rong:
           return False

6. Kiem tra rang buoc doc phia duoi
   Neu row < N-1 va o (row+1, col) trong:
       
       constraint = v_constraints[row][col]
       
       Neu constraint == 1 (top < bottom):
           # top = value, nen bottom phai > value
           Xoa cac gia tri <= value khoi domain[row+1][col]
       
       Neu constraint == -1 (top > bottom):
           # top = value, nen bottom phai < value
           Xoa cac gia tri >= value khoi domain[row+1][col]
       
       Neu domain[row+1][col] rong:
           return False

7. Tat ca deu on -> return True
```

**Vi du:**
```python
# Gan (0,0) = 3
# O (0,1) cung hang, domain = {1, 2, 3, 4}
# -> Xoa 3 khoi domain[0][1], con {1, 2, 4}

# O (1,0) cung cot, domain = {1, 2, 3, 4}
# -> Xoa 3 khoi domain[1][0], con {1, 2, 4}

# O (0,1) ben phai, rang buoc <
# -> (0,0) < (0,1), nen (0,1) phai > 3
# -> Xoa {1, 2, 3} khoi domain[0][1], con {4}
```

---

### 2.8. Phuong thuc hoan tac

#### `_undo_removal(self, domains, removed)`

Hoan tac cac thay doi domain khi backtrack.

**Luong hoat dong:**
```
Voi moi (r, c, val) trong removed:
    Them val lai vao domains[r][c]
```

---

### 2.9. Phuong thuc de quy chinh

#### `_backtrack(self, puzzle, domains) -> bool`

Ham de quy chinh cua Backtracking.

**Luong hoat dong:**
```
1. Kiem tra da giai xong chua
   if puzzle.is_complete():
       return True

2. Chon o trong (dung MRV neu bat)
   var = self._select_unassigned_variable(puzzle, domains)
   if var is None:
       return True

3. Lay toa do
   row, col = var
   self.nodes_expanded += 1

4. Lay cac gia tri co the gan
   values = self._get_possible_values(puzzle, domains, row, col)

5. Thu tung gia tri
   for value in values:
       
       5.1. Kiem tra an toan
            if puzzle.is_valid(row, col, value):
           
           5.2. Gan gia tri
                puzzle.grid[row][col] = value
           
           5.3. Forward Checking
                removed = []
                fc_success = True
                
                if self.use_forward_checking:
                    fc_success = self._forward_check_with_log(
                        puzzle, domains, row, col, value, removed
                    )
           
           5.4. De quy
                if fc_success:
                    if self._backtrack(puzzle, domains):
                        return True
           
           5.5. Hoan tac
                if self.use_forward_checking:
                    self._undo_removal(domains, removed)
           
           5.6. Backtrack
                puzzle.grid[row][col] = 0
                self.backtracks += 1

6. Khong gia tri nao duoc -> return False
```

---

### 2.10. Phuong thuc thong ke

#### `get_stats(self) -> dict`

Tra ve thong tin ve qua trinh giai.

**Gia tri tra ve:**

| Key | Kieu | Y nghia |
|-----|------|---------|
| `algorithm` | str | Ten thuat toan va cac tuy chon |
| `nodes_expanded` | int | So o da thu gan gia tri |
| `backtracks` | int | So lan quay lui |
| `solution_found` | bool | Co tim duoc loi giai khong |

---

## 3. Do phuc tap

### Thoi gian
- **Truong hop xau nhat**: O(N^(N^2)) - van la ham mu
- **Thuc te**: Nhanh hon Brute Force rat nhieu (x10 den x1000)

### Khong gian
- **Domain**: O(N^3) - N x N o, moi o co toi da N gia tri
- **Do sau de quy**: O(N^2)

---

## 4. Vi du su dung day du

```python
from puzzle import FutoshikiPuzzle
from backtracking_solver import BacktrackingSolver

# 1. Tao puzzle
puzzle = FutoshikiPuzzle(
    n=4,
    grid=[
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 0]
    ],
    h_constraints=[
        [0, 0, 1],
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    v_constraints=[
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
)

# 2. Tao solver voi day du tinh nang
solver = BacktrackingSolver(puzzle, use_mrv=True, use_forward_checking=True)

# 3. Giai
print("Dang giai bang Backtracking + MRV + FC...")
solution = solver.solve()

# 4. Kiem tra ket qua
if solution:
    print("Tim duoc loi giai!")
    print(solution)
else:
    print("Khong tim duoc loi giai.")

# 5. Xem thong ke
stats = solver.get_stats()
print(f"\nThong ke:")
print(f"  Thuat toan: {stats['algorithm']}")
print(f"  So nodes da thu: {stats['nodes_expanded']}")
print(f"  So lan quay lui: {stats['backtracks']}")
print(f"  Co loi giai: {stats['solution_found']}")
```

---

## 5. So sanh cac che do

| Che do | MRV | FC | Nodes | Backtracks | Thoi gian |
|--------|-----|----|-------|-----------|-----------|
| Day du | On | On | 19 | 7 | 0.0003s |
| Chi MRV | On | Off | 142 | 127 | 0.0008s |
| Chi FC | Off | On | ? | ? | ? |
| Khong gi | Off | Off | 142 | 127 | 0.0008s |

---

## 6. Luu y quan trong

### MRV giup chon dung o
- O co it gia tri nhat -> it kha nang sai nhat
- Giam so lan thu va backtrack

### Forward Checking giup phat hien som
- Phat hien ngay khi 1 o domain rong
- Khong mat thoi gian thu tiep nhanh khong di duoc

### Khong bat buoc dung ca hai
- Co the dung MRV khong FC
- Co the dung FC khong MRV
- Co the khong dung gi (gan giong Brute Force)
