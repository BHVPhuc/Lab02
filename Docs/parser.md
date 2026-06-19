# Parser Module - Doc Input va Xuat Output

## 1. Mo ta tong quan

`parser.py` la module chuyen trach viec **doc du lieu dau vao** tu file va **xuat ket qua** ra file. Module nay khong chua logic giai puzzle ma chi lam viec voi dinh dang file.

Nhiem vu chinh:
1. **Doc file input** (`input-XX.txt`) va chuyen thanh object `FutoshikiPuzzle`
2. **Ghi file output** (`output-XX.txt`) tu ma tran da giai, co dan xen dau bat dang thuc

Tuong tu nhu "thu ky dich thuat", parser chuyen doi giua dinh dang file van ban va dinh dang du lieu trong chuong trinh.

---

## 2. Cau truc file input

### Dinh dang chuan (theo yeu cau de bai)

```
N                                    <-- Dong 1: Kich thuoc N x N
# Comment (bo qua)                  <-- Dong bat dau bang # la comment
0, 2, 0, 0                           <-- N dong: Ma tran grid
0, 0, 0, 3                           <--     0 = o trong, 1..N = so da cho
1, 0, 0, 0                           <--
0, 0, 4, 0                           <--
# Horizontal constraints              <-- Comment
1, 0, -1                             <-- N dong: Rang buoc ngang
0, 0, 0                              <--     0 = khong co, 1 = <, -1 = >
0, 1, 0                              <--
-1, 0, 0                             <--
# Vertical constraints                <-- Comment
0, 1, 0, 0                           <-- N-1 dong: Rang buoc doc
0, 0, -1, 0                          <--     0 = khong co, 1 = <, -1 = >
-1, 0, 0, 0                          <--
```

### Y nghia cac gia tri

#### Grid (ma tran so)
| Gia tri | Y nghia |
|---------|---------|
| `0` | O trong, can dien |
| `1` den `N` | So da cho san (clue) |

#### Horizontal Constraints (rang buoc ngang)
| Gia tri | Y nghia | Vi du |
|---------|---------|-------|
| `0` | Khong co rang buoc | `3   1` |
| `1` | `<` (trai < phai) | `2 < 4` |
| `-1` | `>` (trai > phai) | `5 > 3` |

#### Vertical Constraints (rang buoc doc)
| Gia tri | Y nghia | Vi du |
|---------|---------|-------|
| `0` | Khong co rang buoc | `3` va `1` khong lien quan |
| `1` | `^` (tren < duoi) | `2` tren, `4` duoi -> `2 < 4` |
| `-1` | `v` (tren > duoi) | `5` tren, `3` duoi -> `5 > 3` |

---

## 3. Ham read_input() - Doc file input

### Chuc nang
Doc file `input-XX.txt` theo dinh dang chuan va tao object `FutoshikiPuzzle`.

### Tham so dau vao

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `file_path` | str | Duong dan den file input (vi du: "Inputs/input-01.txt") |

### Gia tri tra ve

| Kieu | Y nghia |
|------|---------|
| `FutoshikiPuzzle` | Object chua toan bo du lieu puzzle |

### Luong hoat dong (step-by-step)

```
1. Kiem tra file co ton tai khong
   Neu khong -> FileNotFoundError

2. Doc tung dong trong file
   
   2.1. Loai bo khoang trang 2 dau (strip)
   
   2.2. Neu dong trong hoac bat dau bang '#' -> bo qua
   
   2.3. Con lai -> luu vao danh sach valid_lines

3. Kiem tra co du lieu hop le khong
   Neu valid_lines rong -> ValueError

4. Dong dau tien -> n (kich thuoc puzzle)

5. Doc N dong tiep theo -> grid (ma tran N x N)
   
   Moi dong: tach bang dau phay, chuyen thanh int
   
   Vi du: "0,2,0,0" -> [0, 2, 0, 0]

6. Doc N dong tiep theo -> h_constraints (rang buoc ngang)
   
   Moi dong co N-1 gia tri
   
   Vi du: "1,0,-1" -> [1, 0, -1]

7. Doc N-1 dong tiep theo -> v_constraints (rang buoc doc)
   
   Moi dong co N gia tri
   
   Vi du: "0,1,0,0" -> [0, 1, 0, 0]

8. Tao va tra ve FutoshikiPuzzle(n, grid, h_constraints, v_constraints)
```

### Vi du su dung

```python
from parser import read_input
from puzzle import FutoshikiPuzzle

# Doc file input
puzzle = read_input("Inputs/input-01.txt")

# Kiem tra ket qua
print(puzzle.n)              # 4
print(puzzle.grid)           # [[0,0,0,0], [0,0,0,0], [0,0,2,0], [0,0,0,0]]
print(puzzle.h_constraints)  # [[0,0,1], [1,0,0], [0,0,0], [0,0,0]]
print(puzzle.v_constraints) # [[0,0,0,1], [0,0,0,1], [0,0,0,0]]
```

### Xu ly loi

| Loi | Nguyen nhan | Cach xu ly |
|-----|-------------|------------|
| `FileNotFoundError` | File khong ton tai | Thong bao duong dan khong dung |
| `ValueError` | File rong hoac khong hop le | Thong bao khong co du lieu |
| `IndexError` | Thieu dong du lieu | Python tu bao loi khi truy cap |
| `ValueError` (int) | Du lieu khong phai so | Python tu bao loi khi chuyen int |

---

## 4. Ham save_solution() - Ghi file output

### Chuc nang
Nhan ma tran da giai va ghi ra file theo dinh dang dep, co dan xen dau bat dang thuc.

### Tham so dau vao

| Tham so | Kieu | Y nghia |
|---------|------|---------|
| `puzzle` | FutoshikiPuzzle | Object goc (chua rang buoc) |
| `solved_grid` | List[List[int]] | Ma tran da giai (chi chua so) |
| `output_path` | str | Duong dan file output (vi du: "Outputs/output-01.txt") |

### Luong hoat dong (step-by-step)

```
1. Khoi tao danh sach output_lines (rong)

2. Voi moi hang i tu 0 den N-1:
   
   2.1. Xay dung dong so kem dau rang buoc NGANG
        
        row_parts = []
        
        Voi moi cot j tu 0 den N-1:
            - Them solved_grid[i][j] vao row_parts
            - Neu j < N-1 (chua phai cot cuoi):
                + Lay h_constraints[i][j]
                + Neu 1 -> them "<"
                + Neu -1 -> them ">"
                + Neu 0 -> them " " (khoang trang)
        
        Ghép row_parts bang khoang trang -> "1 < 2   3   4"
        Them vao output_lines
   
   2.2. Xay dung dong dau rang buoc DOC (neu chua phai hang cuoi)
        
        vert_parts = []
        
        Voi moi cot j tu 0 den N-1:
            - Lay v_constraints[i][j]
            - Neu 1 -> them "^"
            - Neu -1 -> them "v"
            - Neu 0 -> them " " (khoang trang)
            - Neu j < N-1 -> them " " (de can chinh)
        
        Ghép vert_parts bang khoang trang -> "    v       "
        Them vao output_lines

3. Gom tat ca dong thanh 1 chuoi:
   final_output = "\n".join(output_lines)

4. Kiem tra va tao thu muc cha neu chua ton tai

5. Ghi final_output ra file

6. In ra man hinh de nguoi dung thay ket qua
```

### Vi du input va output

#### Input (solved_grid)
```python
solved_grid = [
    [4, 3, 1, 2],
    [1, 2, 4, 3],
    [3, 1, 2, 4],
    [2, 4, 3, 1]
]
```

#### Output (file text)
```
4   3   1 < 2
            ^
1 < 2   4   3
            ^
3   1   2   4
             
2   4   3   1
```

### Giai thich output

```
4   3   1 < 2      <-- Hang 1: so 1 < so 2 (rang buoc ngang)
            ^        <-- Cot 4: so tren < so duoi (rang buoc doc)
1 < 2   4   3      <-- Hang 2: so 1 < so 2
            ^        <-- Cot 4: so tren < so duoi
3   1   2   4      <-- Hang 3: khong co rang buoc
                     <-- Cot 4: khong co rang buoc
2   4   3   1      <-- Hang 4: khong co rang buoc
```

### Vi du su dung

```python
from parser import read_input, save_solution

# Doc puzzle goc (de lay rang buoc)
puzzle = read_input("Inputs/input-01.txt")

# Gia su da co solved_grid tu solver
solved_grid = [
    [4, 3, 1, 2],
    [1, 2, 4, 3],
    [3, 1, 2, 4],
    [2, 4, 3, 1]
]

# Ghi output
save_solution(puzzle, solved_grid, "Outputs/output-01.txt")

# Ket qua: file output-01.txt duoc tao voi dinh dang dep
```

---

## 5. Luong du lieu tong quan

### Doc input
```
File input-01.txt
       |
       v
  read_input("Inputs/input-01.txt")
       |
       v
  FutoshikiPuzzle (co grid, h_constraints, v_constraints)
       |
       v
  Solver (Backtracking, Brute Force, ...)
```

### Ghi output
```
Solver tra ve solved_grid
       |
       v
  save_solution(puzzle_goc, solved_grid, "Outputs/output-01.txt")
       |
       v
  File output-01.txt (co dau < > ^ v)
```

---

## 6. Loi ich thiet ke

| Loi ich | Giai thich |
|---------|-----------|
| **Tach biet I/O** | Parser chi lam viec voi file, khong lien quan logic giai |
| **De thay doi dinh dang** | Muon doi dinh dang input/output chi can sua parser |
| **Xu ly loi ro rang** | Kiem tra file ton tai, du lieu hop le truoc khi doc |
| **Output dep** | Tu dong dan xen dau bat dang thuc, de doc |
| **Tai su dung** | Cac solver khac nhau deu dung chung parser |

---

## 7. Luu y quan trong

### Parser khong biet gi ve solver
- Parser KHONG biet Brute Force la gi
- Parser KHONG biet Backtracking la gi
- Parser chi biet doc file va ghi file

### Parser khong sua du lieu puzzle
- `read_input()` chi doc, khong thay doi gi
- `save_solution()` chi ghi, khong thay doi puzzle goc

### Thu tu doc rat quan trong
1. Dong 1: N
2. N dong tiep: Grid
3. N dong tiep: Horizontal constraints
4. N-1 dong tiep: Vertical constraints

Neu thieu dong hoac thua dong, se bao loi.
