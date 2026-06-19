from typing import List, Tuple, Optional, Set

from puzzle import FutoshikiPuzzle


class BacktrackingSolver:
    """
    Backtracking Solver voi cac cai tien:
    - MRV (Minimum Remaining Values): Chon o co it gia tri hop le nhat
    - Forward Checking: Loai bo gia tri khong hop le khoi domain cua cac o lien quan
    """
    
    def __init__(self, puzzle: FutoshikiPuzzle, use_mrv: bool = True, 
                 use_forward_checking: bool = True):
        self.original = puzzle
        self.use_mrv = use_mrv
        self.use_forward_checking = use_forward_checking
        self.nodes_expanded = 0
        self.backtracks = 0
        self.solution = None
        
    def solve(self) -> Optional[FutoshikiPuzzle]:
        """Giai puzzle bang backtracking voi cac cai tien"""
        puzzle = self.original.clone()
        self.nodes_expanded = 0
        self.backtracks = 0
        
        # Khoi tao domain cho moi o
        domains = self._init_domains(puzzle)
        
        if self._backtrack(puzzle, domains):
            self.solution = puzzle
            return puzzle
        return None
    
    def _init_domains(self, puzzle: FutoshikiPuzzle) -> List[List[Set[int]]]:
        """Khoi tao domain cho moi o"""
        domains = [[set() for _ in range(puzzle.n)] for _ in range(puzzle.n)]
        
        for i in range(puzzle.n):
            for j in range(puzzle.n):
                if puzzle.grid[i][j] != 0:
                    domains[i][j] = {puzzle.grid[i][j]}
                else:
                    for val in range(1, puzzle.n + 1):
                        if puzzle.is_valid(i, j, val):
                            domains[i][j].add(val)
        
        return domains
    
    def _get_possible_values(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]], 
                             row: int, col: int) -> List[int]:
        """Lay danh sach gia tri hop le cho o (row, col)"""
        if self.use_forward_checking:
            return sorted(domains[row][col])
        else:
            return [v for v in range(1, puzzle.n + 1) if puzzle.is_valid(row, col, v)]
    
    def _select_unassigned_variable(self, puzzle: FutoshikiPuzzle, 
                                    domains: List[List[Set[int]]]) -> Optional[Tuple[int, int]]:
        """Chon o trong de gan gia tri - co the dung MRV"""
        if self.use_mrv:
            # MRV: Chon o co it gia tri hop le nhat
            min_remaining = float('inf')
            best_cell = None
            
            for i in range(puzzle.n):
                for j in range(puzzle.n):
                    if puzzle.grid[i][j] == 0:
                        remaining = len(domains[i][j])
                        if remaining < min_remaining:
                            min_remaining = remaining
                            best_cell = (i, j)
                        # Tie-breaker: chon o co nhieu rang buoc nhat (degree heuristic)
                        elif remaining == min_remaining and best_cell is not None:
                            if self._count_constraints(puzzle, i, j) > self._count_constraints(puzzle, best_cell[0], best_cell[1]):
                                best_cell = (i, j)
            
            return best_cell
        else:
            # Khong dung MRV: chon o trong dau tien
            return puzzle.find_empty()
    
    def _count_constraints(self, puzzle: FutoshikiPuzzle, row: int, col: int) -> int:
        """Dem so rang buoc lien quan den o (row, col)"""
        count = 0
        # Rang buoc ngang
        if col > 0 and puzzle.h_constraints[row][col - 1] != 0:
            count += 1
        if col < puzzle.n - 1 and puzzle.h_constraints[row][col] != 0:
            count += 1
        # Rang buoc doc
        if row > 0 and puzzle.v_constraints[row - 1][col] != 0:
            count += 1
        if row < puzzle.n - 1 and puzzle.v_constraints[row][col] != 0:
            count += 1
        return count
    
    def _forward_check_with_log(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]], 
                                 row: int, col: int, value: int, removed: List[Tuple[int, int, int]]) -> bool:
        """
        Forward checking voi log cac thay doi
        Tra ve False neu co o nao domain rong (failure)
        """
        # Cac o cung hang (tru o da gan va o da co gia tri)
        for c in range(puzzle.n):
            if c != col and puzzle.grid[row][c] == 0 and value in domains[row][c]:
                domains[row][c].remove(value)
                removed.append((row, c, value))
                if len(domains[row][c]) == 0:
                    return False
        
        # Cac o cung cot
        for r in range(puzzle.n):
            if r != row and puzzle.grid[r][col] == 0 and value in domains[r][col]:
                domains[r][col].remove(value)
                removed.append((r, col, value))
                if len(domains[r][col]) == 0:
                    return False
        
        # Kiem tra rang buoc bat dang thuc voi cac o lien ke
        # O ben trai: (row, col-1) voi rang buoc h_constraints[row][col-1]
        if col > 0 and puzzle.grid[row][col - 1] == 0:
            constraint = puzzle.h_constraints[row][col - 1]
            if constraint == 1:  # left < right = value, nen left phai < value
                to_remove = [v for v in domains[row][col - 1] if v >= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            elif constraint == -1:  # left > right = value, nen left phai > value
                to_remove = [v for v in domains[row][col - 1] if v <= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            if len(domains[row][col - 1]) == 0:
                return False
        
        # O ben phai: (row, col+1) voi rang buoc h_constraints[row][col]
        if col < puzzle.n - 1 and puzzle.grid[row][col + 1] == 0:
            constraint = puzzle.h_constraints[row][col]
            if constraint == 1:  # value < right, nen right phai > value
                to_remove = [v for v in domains[row][col + 1] if v <= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            elif constraint == -1:  # value > right, nen right phai < value
                to_remove = [v for v in domains[row][col + 1] if v >= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            if len(domains[row][col + 1]) == 0:
                return False
        
        # O phia tren: (row-1, col) voi rang buoc v_constraints[row-1][col]
        if row > 0 and puzzle.grid[row - 1][col] == 0:
            constraint = puzzle.v_constraints[row - 1][col]
            if constraint == 1:  # top < bottom = value, nen top phai < value
                to_remove = [v for v in domains[row - 1][col] if v >= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            elif constraint == -1:  # top > bottom = value, nen top phai > value
                to_remove = [v for v in domains[row - 1][col] if v <= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            if len(domains[row - 1][col]) == 0:
                return False
        
        # O phia duoi: (row+1, col) voi rang buoc v_constraints[row][col]
        if row < puzzle.n - 1 and puzzle.grid[row + 1][col] == 0:
            constraint = puzzle.v_constraints[row][col]
            if constraint == 1:  # value < bottom, nen bottom phai > value
                to_remove = [v for v in domains[row + 1][col] if v <= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            elif constraint == -1:  # value > bottom, nen bottom phai < value
                to_remove = [v for v in domains[row + 1][col] if v >= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            if len(domains[row + 1][col]) == 0:
                return False
        
        return True
    
    def _undo_removal(self, domains: List[List[Set[int]]], removed: List[Tuple[int, int, int]]):
        """Hoan tac cac thay doi domain"""
        for r, c, val in removed:
            domains[r][c].add(val)
    
    def _backtrack(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]]) -> bool:
        """Backtracking recursive voi MRV va Forward Checking"""
        # Kiem tra neu da giai xong
        if puzzle.is_complete():
            return True
        
        # Chon o trong (dung MRV neu duoc bat)
        var = self._select_unassigned_variable(puzzle, domains)
        if var is None:
            return True
        
        row, col = var
        self.nodes_expanded += 1
        
        # Lay cac gia tri co the gan
        values = self._get_possible_values(puzzle, domains, row, col)
        
        for value in values:
            # Kiem tra lai tinh hop le (an toan)
            if puzzle.is_valid(row, col, value):
                # Gan gia tri
                puzzle.grid[row][col] = value
                
                # Luu lai cac thay doi domain de hoan tac
                removed = []
                
                # Forward checking
                fc_success = True
                if self.use_forward_checking:
                    fc_success = self._forward_check_with_log(puzzle, domains, row, col, value, removed)
                
                if fc_success:
                    if self._backtrack(puzzle, domains):
                        return True
                
                # Hoan tac cac thay doi domain
                if self.use_forward_checking:
                    self._undo_removal(domains, removed)
                
                # Backtrack: xoa gia tri da gan
                puzzle.grid[row][col] = 0
                self.backtracks += 1
        
        return False
    
    def get_stats(self) -> dict:
        """Tra ve thong ke"""
        return {
            'algorithm': f'Backtracking (MRV={self.use_mrv}, FC={self.use_forward_checking})',
            'nodes_expanded': self.nodes_expanded,
            'backtracks': self.backtracks,
            'solution_found': self.solution is not None
        }
