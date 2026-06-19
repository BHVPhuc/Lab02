# Puzzle Module - Du lieu dung chung

## 1. Mo ta tong quan

`puzzle.py` chua class `FutoshikiPuzzle` - **lop du lieu trung tam** duoc su dung boi TAT CA cac solver trong project. Day la "ngon ngu chung" ma moi solver deu hieu.

Tuong tu nhu "bang trang" trong van phong, `FutoshikiPuzzle` la noi luu tru thong tin ma moi nguoi (solver) deu nhin vao va lam viec tren do.

Nhiem vu chinh:
1. **Luu tru du lieu puzzle**: grid, rang buoc ngang, rang buoc doc
2. **Cung cap ham kiem tra**: gia tri co hop le khong, con o trong khong
3. **Ho tro sao chep**: tao ban sao de thu nghiem khong anh huong ban goc

---

## 2. Class FutoshikiPuzzle

### 2.1. Thuoc tinh (Attributes)

| Thuoc tinh | Kieu | Kich thuoc | Y nghia |
|-----------|------|------------|---------|
| `n` | int | 1 so | Kich thuoc puzzle N x N |
| `grid` | List[List[int]] | N x N | Ma tran so, 0 = o trong |
| `h_constraints` | List[List[int]] | N x (N-1) | Rang buoc ngang giua cac o |
| `v_constraints` | List[List[int]] | (N-1) x N | Rang buoc doc giua cac o |

#### Chi tiet grid
```python
grid[i][j] = 0     # O (i,j) dang trong, can dien so
grid[i][j] = 3     # O (i,j) da co so 3 (hoac da dien so 3)
```

#### Chi tiet h_constraints (horizontal)
```python
h_constraints[i][j] = 0   # Khong co rang buoc giua (i,j) va (i,j+1)
h_constraints[i][j] = 1   # grid[i][j] < grid[i][j+1]
h_constraints[i][j] = -1  # grid[i][j] > grid[i][j+1]
```

#### Chi tiet v_constraints (vertical)
```python
v_constraints[i][j] = 0   # Khong co rang buoc giua (i,j) va (i+1,j)
v_constraints[i][j] = 1   # grid[i][j] < grid[i+1][j]
v_constraints[i][j] = -1  # grid[i][j] > grid[i+1][j]
```

---

### 2.2. Phuong thuc khoi tao

#### `__init__(self, n, grid, h_constraints, v_constraints)`

Tao puzzle moi voi du lieu day du.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `n` | int | Kich thuoc puzzle |
| `grid` | List[List[int]] | Ma tran so ban dau |
| `h_constraints` | List[List[int]] | Rang buoc ngang |
| `v_constraints` | List[List[int]] | Rang buoc doc |

**Vi du:**
```python
from puzzle import FutoshikiPuzzle

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
```

---

### 2.3. Phuong thuc kiem tra hop le

#### `is_valid(self, row, col, value) -> bool`

Kiem tra xem co the dat `value` tai o `(row, col)` khong.

**Tham so:**

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `row` | int | Chi so hang (0 den N-1) |
| `col` | int | Chi so cot (0 den N-1) |
| `value` | int | Gia tri muon dat (1 den N) |

**Gia tri tra ve:**
- `True`: Co the dat gia tri
- `False`: Khong the dat gia tri

**Cac dieu kien kiem tra:**

1. **Khong trung trong hang**: Khong co o nao cung hang co gia tri nay
2. **Khong trung trong cot**: Khong co o nao cung cot co gia tri nay
3. **Thoa man rang buoc ngang trai**: Neu co o ben trai va da co gia tri, kiem tra dau `<` hoac `>`
4. **Thoa man rang buoc ngang phai**: Neu co o ben phai va da co gia tri, kiem tra dau `<` hoac `>`
5. **Thoa man rang buoc doc tren**: Neu co o phia tren va da co gia tri, kiem tra dau `^` hoac `v`
6. **Thoa man rang buoc doc duoi**: Neu co o phia duoi va da co gia tri, kiem tra dau `^` hoac `v`

**Luong hoat dong chi tiet:**

```
1. Kiem tra hang khong trung
   Voi moi cot c tu 0 den N-1:
       Neu c != col va grid[row][c] == value:
           return False

2. Kiem tra cot khong trung
   Voi moi hang r tu 0 den N-1:
       Neu r != row va grid[r][col] == value:
           return False

3. Kiem tra rang buoc ngang ben trai
   Neu col > 0:
       constraint = h_constraints[row][col-1]
       left_val = grid[row][col-1]
       Neu left_val != 0:
           Neu constraint == 1 va left_val >= value: return False
           Neu constraint == -1 va left_val <= value: return False

4. Kiem tra rang buoc ngang ben phai
   Neu col < N-1:
       constraint = h_constraints[row][col]
       right_val = grid[row][col+1]
       Neu right_val != 0:
           Neu constraint == 1 va value >= right_val: return False
           Neu constraint == -1 va value <= right_val: return False

5. Kiem tra rang buoc doc phia tren
   Neu row > 0:
       constraint = v_constraints[row-1][col]
       top_val = grid[row-1][col]
       Neu top_val != 0:
           Neu constraint == 1 va top_val >= value: return False
           Neu constraint == -1 va top_val <= value: return False

6. Kiem tra rang buoc doc phia duoi
   Neu row < N-1:
       constraint = v_constraints[row][col]
       bottom_val = grid[row+1][col]
       Neu bottom_val != 0:
           Neu constraint == 1 va value >= bottom_val: return False
           Neu constraint == -1 va value <= bottom_val: return False

7. Tat ca dieu kien deu thoa man -> return True
```

**Vi du:**
```python
# Puzzle 4x4, o (0,0) dang trong
# Kiem tra co the dat 1 tai (0,0) khong
print(puzzle.is_valid(0, 0, 1))  # True hoac False

# Kiem tra co the dat 2 tai (0,0) khong
# Neu hang 0 da co so 2 o vi tri khac -> False
print(puzzle.is_valid(0, 0, 2))
```

---

### 2.4. Phuong thuc tim o trong

#### `find_empty(self) -> Optional[Tuple[int, int]]`

Tim o trong dau tien trong grid (gia tri 0).

**Gia tri tra ve:**
- `(row, col)`: Toa do o trong dau tien tim thay
- `None`: Khong con o trong nao (puzzle da giai)

**Luong hoat dong:**
```
Voi moi hang i tu 0 den N-1:
    Voi moi cot j tu 0 den N-1:
        Neu grid[i][j] == 0:
            return (i, j)
return None
```

**Vi du:**
```python
empty = puzzle.find_empty()
if empty:
    row, col = empty
    print(f"O trong dau tien: ({row}, {col})")
else:
    print("Puzzle da day!")
```

---

### 2.5. Phuong thuc kiem tra hoan thanh

#### `is_complete(self) -> bool`

Kiem tra xem puzzle da duoc dien day du chua.

**Gia tri tra ve:**
- `True`: Tat ca o deu co gia tri (khong con 0)
- `False`: Con it nhat 1 o trong

**Luong hoat dong:**
```
Voi moi hang i tu 0 den N-1:
    Voi moi cot j tu 0 den N-1:
        Neu grid[i][j] == 0:
            return False
return True
```

**Vi du:**
```python
if puzzle.is_complete():
    print("Puzzle da giai xong!")
else:
    print("Van con o trong can dien.")
```

---

### 2.6. Phuong thuc sao chep

#### `clone(self) -> FutoshikiPuzzle`

Tao ban sao sau (deep copy) cua puzzle.

**Muc dich:** Khi thu nghiem 1 gia tri, can tao ban sao de khong anh huong puzzle goc.

**Gia tri tra ve:**
- `FutoshikiPuzzle`: Ban sao doc lap, thay doi khong anh huong ban goc

**Luong hoat dong:**
```python
import copy

return FutoshikiPuzzle(
    self.n,                                    # n giong nhau
    copy.deepcopy(self.grid),                  # Sao chep sau grid
    copy.deepcopy(self.h_constraints),         # Sao chep sau h_constraints
    copy.deepcopy(self.v_constraints)          # Sao chep sau v_constraints
)
```

**Vi du:**
```python
# Tao ban sao de thu nghiem
puzzle_copy = puzzle.clone()

# Thay doi ban sao khong anh huong ban goc
puzzle_copy.grid[0][0] = 5
print(puzzle.grid[0][0])      # Van la 0 (khong doi)
print(puzzle_copy.grid[0][0])  # La 5 (da thay doi)
```

---

### 2.7. Phuong thuc in ra man hinh

#### `__str__(self) -> str`

In puzzle duoi dang de doc, co dan xen dau bat dang thuc.

**Gia tri tra ve:**
- `str`: Chuoi dai dien puzzle

**Dinh dang output:**
```
4   3   1 < 2
            ^
1 < 2   4   3
            ^
3   1   2   4
             
2   4   3   1
```

**Luong hoat dong:**
```
1. Khoi tao danh sach lines (rong)

2. Voi moi hang i:
   
   2.1. Xay dung dong so:
        row_str = ""
        Voi moi cot j:
            - Neu grid[i][j] == 0: them "."
            - Neu khac 0: them gia tri
            - Neu j < N-1: them dau rang buoc ngang
        Them row_str vao lines
   
   2.2. Xay dung dong rang buoc doc (neu chua phai hang cuoi):
        v_str = ""
        Voi moi cot j:
            - Them dau rang buoc doc
        Them v_str vao lines

3. Tra ve "\n".join(lines)
```

**Vi du:**
```python
print(puzzle)
# Output:
# .   .   . < .
#             ^
# . < .   .   .
#             ^
# .   .   2   .
#              
# .   .   .   .
```

---

## 3. Luong du lieu trong toan bo he thong

```
File input-01.txt
       |
       v
  parser.read_input() 
       |
       v
  +------------------+
  | FutoshikiPuzzle  |
  | - n: 4           |
  | - grid: [...]    |
  | - h_constraints  |
  | - v_constraints  |
  +------------------+
       |
       +---> BruteForceSolver.solve()
       |          |
       |          v
       |      Solution (grid da giai)
       |          |
       |          v
       |      parser.save_solution()
       |
       +---> BacktrackingSolver.solve()
       |          |
       |          v
       |      Solution (grid da giai)
       |          |
       |          v
       |      parser.save_solution()
       |
       +---> ForwardChainingSolver.solve()
       |          |
       |          ...
       |
       +---> AStarSolver.solve()
                  |
                  ...
```

---

## 4. Vi du su dung day du

```python
from puzzle import FutoshikiPuzzle

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

# 2. In puzzle ban dau
print("Puzzle ban dau:")
print(puzzle)

# 3. Kiem tra gia tri hop le
print("\nKiem tra:")
print(f"is_valid(0,0,1) = {puzzle.is_valid(0, 0, 1)}")
print(f"is_valid(0,0,2) = {puzzle.is_valid(0, 0, 2)}")

# 4. Tim o trong
empty = puzzle.find_empty()
print(f"\nO trong dau tien: {empty}")

# 5. Kiem tra hoan thanh
print(f"\nDa hoan thanh? {puzzle.is_complete()}")

# 6. Tao ban sao va thu nghiem
puzzle_copy = puzzle.clone()
puzzle_copy.grid[0][0] = 1
print(f"\nBan sao sau khi gan (0,0)=1:")
print(puzzle_copy)

# 7. Puzzle goc khong doi
print(f"Puzzle goc van con:")
print(puzzle)
```

---

## 5. Loi ich thiet ke

| Loi ich | Giai thich |
|---------|-----------|
| **Dung chung** | Tat ca solver deu dung cung 1 class du lieu |
| **Khong phu thuoc** | Khong phu thuoc vao bat ky solver nao |
| **De test** | Co the test rieng ma khong can solver |
| **Nhat quan** | Dam bao tat ca solver lam viec voi cung kieu du lieu |
| **An toan** | `clone()` giup thu nghiem khong anh huong du lieu goc |

---

## 6. Luu y quan trong

### Class nay KHONG chua logic giai puzzle
- Khong co ham `solve()`
- Chi chua du lieu va cac ham kiem tra co ban
- Moi solver se tu viet logic giai cua minh

### Grid co the bi thay doi
- Solver co the truc tiep sua `puzzle.grid[i][j] = value`
- Nen dung `clone()` truoc khi thu nghiem

### Rang buoc khong thay doi
- `h_constraints` va `v_constraints` la co dinh
- Chi co `grid` la thay doi trong qua trinh giai
