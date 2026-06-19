import copy
from typing import List, Tuple, Optional


class FutoshikiPuzzle:
    """
    Class dung chung dai dien cho puzzle Futoshiki.
    Duoc su dung boi tat ca cac thuat toan (Brute Force, Backtracking, Forward Chaining, ...)
    """
    
    def __init__(self, n: int, grid: List[List[int]], 
                 h_constraints: List[List[int]], v_constraints: List[List[int]]):
        self.n = n
        self.grid = grid  # 0 = empty
        self.h_constraints = h_constraints  # N rows, N-1 cols: 0=none, 1=<, -1=>
        self.v_constraints = v_constraints  # N-1 rows, N cols: 0=none, 1=< (top<bottom), -1=> (top>bottom)
        
    def is_valid(self, row: int, col: int, value: int) -> bool:
        """Kiem tra xem gia tri co the dat tai (row, col) khong"""
        # Kiem tra hang khong trung
        for c in range(self.n):
            if c != col and self.grid[row][c] == value:
                return False
        
        # Kiem tra cot khong trung
        for r in range(self.n):
            if r != row and self.grid[r][col] == value:
                return False
        
        # Kiem tra rang buoc ngang (horizontal)
        if col > 0:
            constraint = self.h_constraints[row][col - 1]
            left_val = self.grid[row][col - 1]
            if left_val != 0:
                if constraint == 1 and not (left_val < value):
                    return False
                if constraint == -1 and not (left_val > value):
                    return False
        
        if col < self.n - 1:
            constraint = self.h_constraints[row][col]
            right_val = self.grid[row][col + 1]
            if right_val != 0:
                if constraint == 1 and not (value < right_val):
                    return False
                if constraint == -1 and not (value > right_val):
                    return False
        
        # Kiem tra rang buoc doc (vertical)
        if row > 0:
            constraint = self.v_constraints[row - 1][col]
            top_val = self.grid[row - 1][col]
            if top_val != 0:
                if constraint == 1 and not (top_val < value):
                    return False
                if constraint == -1 and not (top_val > value):
                    return False
        
        if row < self.n - 1:
            constraint = self.v_constraints[row][col]
            bottom_val = self.grid[row + 1][col]
            if bottom_val != 0:
                if constraint == 1 and not (value < bottom_val):
                    return False
                if constraint == -1 and not (value > bottom_val):
                    return False
        
        return True
    
    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Tim o trong dau tien"""
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def is_complete(self) -> bool:
        """Kiem tra puzzle da day du chua"""
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    return False
        return True
    
    def clone(self):
        """Tao ban sao cua puzzle"""
        return FutoshikiPuzzle(
            self.n,
            copy.deepcopy(self.grid),
            copy.deepcopy(self.h_constraints),
            copy.deepcopy(self.v_constraints)
        )
    
    def __str__(self):
        """In puzzle voi rang buoc"""
        lines = []
        for i in range(self.n):
            row_str = ""
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    row_str += "."
                else:
                    row_str += str(self.grid[i][j])
                if j < self.n - 1:
                    if self.h_constraints[i][j] == 1:
                        row_str += " < "
                    elif self.h_constraints[i][j] == -1:
                        row_str += " > "
                    else:
                        row_str += "   "
            lines.append(row_str)
            if i < self.n - 1:
                v_str = ""
                for j in range(self.n):
                    if self.v_constraints[i][j] == 1:
                        v_str += "v   "
                    elif self.v_constraints[i][j] == -1:
                        v_str += "^   "
                    else:
                        v_str += "    "
                lines.append(v_str)
        return "\n".join(lines)
