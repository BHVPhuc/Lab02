# Huong Dan Su Dung GUI - Futoshiki Puzzle Solver

## Gioi Thieu

Giao dien do hoa (GUI) duoc xay dung bang **Tkinter**, cho phep nguoi dung:
- Tai puzzle tu file input
- Giai puzzle bang cac thuat toan khac nhau
- So sanh hieu nang cua tat ca thuat toan
- Luu ket qua ra file

## Cach Chay GUI

```bash
cd Source
python gui.py
```

Hoac tu `main.py`:
```bash
python main.py --gui
```

## Cac Thanh Phan Chinh

### 1. Input
- **File input**: Nhap duong dan file puzzle (vi du: `input-01.txt`)
- **Browse**: Mo hop thoai chon file
- **Load Puzzle**: Tai va hien thi puzzle len man hinh

### 2. Algorithm
- **Solver**: Chon thuat toan tu dropdown
  - `brute_force`: Thu tat ca to hop (cham, dung de so sanh)
  - `backtracking`: MRV + Forward Checking (nhanh)
  - `forward_chaining`: Cua nhom (neu co)
  - `backward_chaining`: Cua nhom (neu co)
  - `a_star`: Cua nhom (neu co)
- **GIAI**: Chay thuat toan da chon
- **SO SANH TAT CA**: Chay tat ca thuat toan va hien thi bang so sanh

### 3. Puzzle Display
- Hien thi puzzle duoi dang luoi
- **Mau cam nhat**: So da cho (clue)
- **Mau xanh la nhat**: So do thuat toan tim ra
- **Dau do**: Rang buoc nho hon (`<`)
- **Dau xanh**: Rang buoc lon hon (`>`)
- **Dau v**: Rang buoc doc (tren xuong duoi)
- **Dau ^**: Rang buoc doc (duoi len tren)

### 4. Statistics
- Hien thi thong ke ket qua
- Khi giai 1 thuat toan: Time, Nodes expanded, Backtracks
- Khi so sanh: Bang so sanh tat ca thuat toan

### 5. Log
- Hien thi cac thong bao trang thai
- Bao loi neu co

## Luong Su Dung Co Ban

### Giai 1 Puzzle
1. Nhap duong dan file input (hoac nhan **Browse** de chon)
2. Nhan **Load Puzzle** de hien thi
3. Chon thuat toan tu dropdown
4. Nhan **GIAI**
5. Xem ket qua tren Puzzle Display va Statistics
6. (Tuy chon) Nhan **Yes** de luu ket qua ra file

### So Sanh Cac Thuat Toan
1. Tai puzzle (buoc 1-2 o tren)
2. Nhan **SO SANH TAT CA**
3. Xem bang so sanh o Statistics
4. Thuat toan nhanh nhat se duoc highlight

## Luu Y

- **Timeout**: Cac puzzle 9x9 phuc tap co the timeout (>30s). Day la gioi han binh thuong cua backtracking, dung de so sanh voi A*/Forward Chaining.
- **Backtracking luon co MRV + FC**: Khong the tat MRV hoac Forward Checking.
- **Font dau rang buoc**: Da duoc tang len size 14 de de nhin.
- **Statistics width**: Da mo rong de hien thi bang so sanh day du.

## Cau Truc File

```
Source/
  gui.py              # Giao dien chinh
  main.py             # Entry point (co the goi --gui)
  puzzle.py           # Class FutoshikiPuzzle
  parser.py           # Doc/ghi file
  brute_force_solver.py
  backtracking_solver.py
  forward_chaining.py   # Cua nhom (neu co)
  backward_chaining.py  # Cua nhom (neu co)
  astar_solver.py      # Cua nhom (neu co)
```

## Tro Giup

Neu gap loi import solver khong co, dam bao cac file solver da duoc dat trong thu muc `Source/`.
