# Brute Force Solver

## 1. Mo ta tong quan

`brute_force_solver.py` chua class `BruteForceSolver` - thuat toan co ban nhat de giai Futoshiki puzzle. Thuat toan nay thu tat ca cac to hop co the ma khong dung bat ky heuristic hay pruning nao.

Tuong tu nhu "mo khoa bang cach thu tung chia khoa", Brute Force thu tung gia tri 1 den N cho moi o trong cho den khi tim duoc loi giai.

---

## 2. Class BruteForceSolver

### 2.1. Thuoc tinh

| Thuoc tinh | Kieu | Y nghia |
|-----------|------|---------|
| `original` | FutoshikiPuzzle | Puzzle goc (khong bi thay doi) |
| `nodes_expanded` | int | Dem so o da duoc thu gan gia tri |
| `solution` | FutoshikiPuzzle | Loi giai tim duoc (neu co) |

---

### 2.2. Phuong thuc khoi tao

#### `__init__(self, puzzle)`

Tao solver moi voi puzzle can giai.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Puzzle can giai |

**Vi du:**
```python
from puzzle import FutoshikiPuzzle
from brute_force_solver import BruteForceSolver

puzzle = FutoshikiPuzzle(...)  # Tao puzzle
solver = BruteForceSolver(puzzle)
```

---

### 2.3. Phuong thuc giai chinh

#### `solve(self) -> Optional[FutoshikiPuzzle]`

Giai puzzle bang Brute Force.

**Gia tri tra ve:**
- `FutoshikiPuzzle`: Loi giai tim duoc (puzzle da duoc dien day du)
- `None`: Khong tim duoc loi giai (puzzle khong co loi giai)

**Luong hoat dong:**
```
1. Tao ban sao puzzle de khong anh huong puzzle goc
   puzzle = self.original.clone()

2. Reset dem so nodes
   self.nodes_expanded = 0

3. Goi ham de quy _brute_force(puzzle)

4. Neu tim duoc loi giai:
       self.solution = puzzle
       return puzzle
   Neu khong:
       return None
```

**Vi du:**
```python
solver = BruteForceSolver(puzzle)
solution = solver.solve()

if solution:
    print("Tim duoc loi giai!")
    print(solution.grid)
else:
    print("Khong co loi giai.")
```

---

### 2.4. Phuong thuc de quy chinh

#### `_brute_force(self, puzzle) -> bool`

Ham de quy thu tung gia tri cho moi o trong.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Ban sao puzzle dang duoc thu nghiem |

**Gia tri tra ve:**
- `True`: Da tim duoc loi giai hoan chinh
- `False`: Nhanh hien tai khong dan den loi giai, can quay lui

**Luong hoat dong chi tiet:**

```
1. Tim o trong dau tien
   empty = puzzle.find_empty()

2. Neu khong con o trong -> Da giai xong!
   if empty is None:
       return True

3. Lay toa do o trong
   row, col = empty

4. Tang dem so nodes da thu
   self.nodes_expanded += 1

5. Thu tung gia tri tu 1 den N
   for value from 1 to puzzle.n:

       5.1. Kiem tra gia tri co hop le khong
            if puzzle.is_valid(row, col, value):

           5.2. Gan gia tri vao o
                puzzle.grid[row][col] = value

           5.3. De quy giai tiep
                if self._brute_force(puzzle):
                    return True  # Tim duoc loi giai!

           5.4. Quay lui (backtrack)
                puzzle.grid[row][col] = 0

6. Da thu het gia tri ma khong duoc -> that bai
   return False
```

**Giai thich bang vi du:**

Gia su puzzle 4x4, o dau tien trong la (0,0):

```
Buoc 1: Thu value = 1 tai (0,0)
        -> is_valid? Neu co -> gan (0,0) = 1
        -> De quy tim o trong tiep theo
        -> Neu that bai o sau -> quay lui, gan (0,0) = 0

Buoc 2: Thu value = 2 tai (0,0)
        -> is_valid? Neu co -> gan (0,0) = 2
        -> De quy tim o trong tiep theo
        -> ...

Buoc 3: Thu value = 3 tai (0,0)
        -> ...

Buoc 4: Thu value = 4 tai (0,0)
        -> ...

Neu ca 4 gia tri deu khong duoc -> return False
(Thong bao cho o truoc biet nhanh nay khong di duoc)
```

---

### 2.5. Phuong thuc thong ke

#### `get_stats(self) -> dict`

Tra ve thong tin ve qua trinh giai.

**Gia tri tra ve:**

| Key | Kieu | Y nghia |
|-----|------|---------|
| `algorithm` | str | Ten thuat toan: "Brute Force" |
| `nodes_expanded` | int | So o da thu gan gia tri |
| `solution_found` | bool | Co tim duoc loi giai khong |

**Vi du:**
```python
solver = BruteForceSolver(puzzle)
solution = solver.solve()

stats = solver.get_stats()
print(stats)
# Output: {'algorithm': 'Brute Force', 'nodes_expanded': 142, 'solution_found': True}
```

---

## 3. Do phuc tap

### Thoi gian
- **Truong hop xau nhat**: O(N^(N^2))
  - Co N^2 o, moi o co N gia tri co the
  - Voi N=4: 4^16 = 4,294,967,296 trang thai
  - Voi N=5: 5^25 = 298,023,223,876,953,125 trang thai

### Khong gian
- **Do sau de quy**: O(N^2) - so o trong puzzle
- **Khong gian luu tru**: O(N^2) - ma tran grid

---

## 4. Han che

| Van de | Giai thich |
|--------|-----------|
| **Rat cham voi N lon** | Voi N=5, co the mat hang gio de giai |
| **Khong co pruning** | Khong biet som nhanh nao khong di duoc |
| **Khong co heuristic** | Thu mot cach "mu quang", khong uu tien o nao |
| **Chi dung cho N <= 4** | Thuc te chi chay duoc voi puzzle nho |

---

## 5. Vi du su dung day du

```python
from puzzle import FutoshikiPuzzle
from brute_force_solver import BruteForceSolver

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

# 2. Tao solver
solver = BruteForceSolver(puzzle)

# 3. Giai
print("Dang giai bang Brute Force...")
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
print(f"  Co loi giai: {stats['solution_found']}")
```

**Output:**
```
Dang giai bang Brute Force...
Tim duoc loi giai!
4   3   1 < 2
            ^
1 < 2   4   3
            ^
3   1   2   4
             
2   4   3   1

Thong ke:
  Thuat toan: Brute Force
  So nodes da thu: 142
  Co loi giai: True
```

---

## 6. So sanh voi Backtracking

| Tieu chi | Brute Force | Backtracking + MRV + FC |
|----------|-------------|------------------------|
| **Y tuong** | Thu tat ca | Thu co chon loc |
| **Chon o** | O trong dau tien | O co it gia tri nhat (MRV) |
| **Pruning** | Khong | Forward Checking |
| **Toc do** | Cham | Nhanh |
| **N=4** | ~0.0004s | ~0.0003s |
| **N=6** | ~1.0s | ~0.001s |
| **Ung dung** | Baseline, so sanh | Su dung thuc te |

---

## 7. Luu y quan trong

### Brute Force khong sua puzzle goc
- `self.original` luon giu nguyen
- Moi thu nghiem deu tren ban sao `puzzle.clone()`

### nodes_expanded dem gi?
- Dem moi lan thu gan gia tri cho 1 o
- Khong dem lan backtrack (xoa gia tri)

### Khi nao dung Brute Force?
- Chi dung cho puzzle nho (N <= 4)
- Lam baseline de so sanh voi thuat toan khac
- Hieu ve cach hoat dong co ban cua tim kiem
