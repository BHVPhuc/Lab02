import time
import copy
import os
from typing import List, Tuple, Optional, Set


class FutoshikiPuzzle:
    """Đại diện cho một puzzle Futoshiki"""
    
    def __init__(self, n: int, grid: List[List[int]], 
                 h_constraints: List[List[int]], v_constraints: List[List[int]]):
        self.n = n
        self.grid = grid  # 0 = empty
        self.h_constraints = h_constraints  # N rows, N-1 cols: 0=none, 1=<, -1=>
        self.v_constraints = v_constraints  # N-1 rows, N cols: 0=none, 1=< (top<bottom), -1=> (top>bottom)
        
    def is_valid(self, row: int, col: int, value: int) -> bool:
        """Kiểm tra xem giá trị có thể đặt tại (row, col) không"""
        # Kiểm tra hàng không trùng
        for c in range(self.n):
            if c != col and self.grid[row][c] == value:
                return False
        
        # Kiểm tra cột không trùng
        for r in range(self.n):
            if r != row and self.grid[r][col] == value:
                return False
        
        # Kiểm tra ràng buộc ngang (horizontal)
        # Với ô (row, col), kiểm tra với ô bên trái (col-1) và bên phải (col)
        if col > 0:
            # Ràng buộc giữa (row, col-1) và (row, col)
            constraint = self.h_constraints[row][col - 1]
            left_val = self.grid[row][col - 1]
            if left_val != 0:
                if constraint == 1 and not (left_val < value):  # left < right
                    return False
                if constraint == -1 and not (left_val > value):  # left > right
                    return False
        
        if col < self.n - 1:
            # Ràng buộc giữa (row, col) và (row, col+1)
            constraint = self.h_constraints[row][col]
            right_val = self.grid[row][col + 1]
            if right_val != 0:
                if constraint == 1 and not (value < right_val):  # left < right
                    return False
                if constraint == -1 and not (value > right_val):  # left > right
                    return False
        
        # Kiểm tra ràng buộc dọc (vertical)
        # Với ô (row, col), kiểm tra với ô phía trên (row-1) và phía dưới (row)
        if row > 0:
            # Ràng buộc giữa (row-1, col) và (row, col): 1 = top < bottom
            constraint = self.v_constraints[row - 1][col]
            top_val = self.grid[row - 1][col]
            if top_val != 0:
                if constraint == 1 and not (top_val < value):  # top < bottom
                    return False
                if constraint == -1 and not (top_val > value):  # top > bottom
                    return False
        
        if row < self.n - 1:
            # Ràng buộc giữa (row, col) và (row+1, col)
            constraint = self.v_constraints[row][col]
            bottom_val = self.grid[row + 1][col]
            if bottom_val != 0:
                if constraint == 1 and not (value < bottom_val):  # top < bottom
                    return False
                if constraint == -1 and not (value > bottom_val):  # top > bottom
                    return False
        
        return True
    
    def find_empty(self) -> Optional[Tuple[int, int]]:
        """Tìm ô trống đầu tiên"""
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def is_complete(self) -> bool:
        """Kiểm tra puzzle đã đầy đủ chưa"""
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    return False
        return True
    
    def clone(self):
        """Tạo bản sao của puzzle"""
        return FutoshikiPuzzle(
            self.n,
            copy.deepcopy(self.grid),
            copy.deepcopy(self.h_constraints),
            copy.deepcopy(self.v_constraints)
        )
    
    def __str__(self):
        """In puzzle với ràng buộc"""
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


def read_input(filename: str) -> FutoshikiPuzzle:
    """Đọc puzzle từ file input"""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    n = int(lines[0])
    
    # Đọc grid (N dòng)
    grid = []
    for i in range(1, n + 1):
        row = [int(x.strip()) for x in lines[i].split(',')]
        grid.append(row)
    
    # Đọc horizontal constraints (N dòng)
    h_constraints = []
    for i in range(n + 1, 2 * n + 1):
        row = [int(x.strip()) for x in lines[i].split(',')]
        h_constraints.append(row)
    
    # Đọc vertical constraints (N-1 dòng)
    v_constraints = []
    for i in range(2 * n + 1, 3 * n):
        row = [int(x.strip()) for x in lines[i].split(',')]
        v_constraints.append(row)
    
    return FutoshikiPuzzle(n, grid, h_constraints, v_constraints)


def write_output(filename: str, puzzle: FutoshikiPuzzle):
    """Ghi puzzle đã giải ra file"""
    with open(filename, 'w') as f:
        for i in range(puzzle.n):
            row = [str(puzzle.grid[i][j]) for j in range(puzzle.n)]
            f.write(", ".join(row) + "\n")


class BruteForceSolver:
    """
    Brute Force Solver - Thử tất cả các tổ hợp có thể
    Không dùng heuristic, không pruning
    Dùng làm baseline để so sánh
    """
    
    def __init__(self, puzzle: FutoshikiPuzzle):
        self.original = puzzle
        self.nodes_expanded = 0
        self.solution = None
        
    def solve(self) -> Optional[FutoshikiPuzzle]:
        """Giải puzzle bằng brute force"""
        puzzle = self.original.clone()
        self.nodes_expanded = 0
        
        if self._brute_force(puzzle):
            self.solution = puzzle
            return puzzle
        return None
    
    def _brute_force(self, puzzle: FutoshikiPuzzle) -> bool:
        """Recursive brute force - thử tất cả giá trị 1->N cho mỗi ô"""
        empty = puzzle.find_empty()
        if empty is None:
            return True  # Đã điền hết
        
        row, col = empty
        self.nodes_expanded += 1
        
        for value in range(1, puzzle.n + 1):
            if puzzle.is_valid(row, col, value):
                puzzle.grid[row][col] = value
                
                if self._brute_force(puzzle):
                    return True
                
                puzzle.grid[row][col] = 0  # Backtrack
        
        return False
    
    def get_stats(self) -> dict:
        """Trả về thống kê"""
        return {
            'algorithm': 'Brute Force',
            'nodes_expanded': self.nodes_expanded,
            'solution_found': self.solution is not None
        }


class BacktrackingSolver:
    """
    Backtracking Solver với các cải tiến:
    - MRV (Minimum Remaining Values): Chọn ô có ít giá trị hợp lệ nhất
    - Forward Checking: Loại bỏ giá trị không hợp lệ khỏi domain của các ô liên quan
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
        """Giải puzzle bằng backtracking với các cải tiến"""
        puzzle = self.original.clone()
        self.nodes_expanded = 0
        self.backtracks = 0
        
        # Khởi tạo domain cho mỗi ô
        domains = self._init_domains(puzzle)
        
        if self._backtrack(puzzle, domains):
            self.solution = puzzle
            return puzzle
        return None
    
    def _init_domains(self, puzzle: FutoshikiPuzzle) -> List[List[Set[int]]]:
        """Khởi tạo domain cho mỗi ô"""
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
        """Lấy danh sách giá trị hợp lệ cho ô (row, col)"""
        if self.use_forward_checking:
            return sorted(domains[row][col])
        else:
            return [v for v in range(1, puzzle.n + 1) if puzzle.is_valid(row, col, v)]
    
    def _select_unassigned_variable(self, puzzle: FutoshikiPuzzle, 
                                    domains: List[List[Set[int]]]) -> Optional[Tuple[int, int]]:
        """Chọn ô trống để gán giá trị - có thể dùng MRV"""
        if self.use_mrv:
            # MRV: Chọn ô có ít giá trị hợp lệ nhất
            min_remaining = float('inf')
            best_cell = None
            
            for i in range(puzzle.n):
                for j in range(puzzle.n):
                    if puzzle.grid[i][j] == 0:
                        remaining = len(domains[i][j])
                        if remaining < min_remaining:
                            min_remaining = remaining
                            best_cell = (i, j)
                        # Tie-breaker: chọn ô có nhiều ràng buộc nhất (degree heuristic)
                        elif remaining == min_remaining and best_cell is not None:
                            # Đếm số ràng buộc liên quan
                            if self._count_constraints(puzzle, i, j) > self._count_constraints(puzzle, best_cell[0], best_cell[1]):
                                best_cell = (i, j)
            
            return best_cell
        else:
            # Không dùng MRV: chọn ô trống đầu tiên
            return puzzle.find_empty()
    
    def _count_constraints(self, puzzle: FutoshikiPuzzle, row: int, col: int) -> int:
        """Đếm số ràng buộc liên quan đến ô (row, col)"""
        count = 0
        # Ràng buộc ngang
        if col > 0 and puzzle.h_constraints[row][col - 1] != 0:
            count += 1
        if col < puzzle.n - 1 and puzzle.h_constraints[row][col] != 0:
            count += 1
        # Ràng buộc dọc
        if row > 0 and puzzle.v_constraints[row - 1][col] != 0:
            count += 1
        if row < puzzle.n - 1 and puzzle.v_constraints[row][col] != 0:
            count += 1
        return count
    
    def _forward_check(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]], 
                       row: int, col: int, value: int) -> bool:
        """
        Forward checking: sau khi gán giá trị cho ô (row, col),
        loại bỏ giá trị không hợp lệ khỏi domain của các ô liên quan
        Trả về False nếu có ô nào domain rỗng (failure)
        """
        if not self.use_forward_checking:
            return True
        
        # Lưu lại các thay đổi để có thể hoàn tác
        removed = []  # List of (r, c, val)
        
        # Các ô cùng hàng (trừ ô đã gán và ô đã có giá trị)
        for c in range(puzzle.n):
            if c != col and puzzle.grid[row][c] == 0 and value in domains[row][c]:
                domains[row][c].remove(value)
                removed.append((row, c, value))
                if len(domains[row][c]) == 0:
                    # Domain rỗng, hoàn tác và báo failure
                    self._undo_removal(domains, removed)
                    return False
        
        # Các ô cùng cột
        for r in range(puzzle.n):
            if r != row and puzzle.grid[r][col] == 0 and value in domains[r][col]:
                domains[r][col].remove(value)
                removed.append((r, col, value))
                if len(domains[r][col]) == 0:
                    self._undo_removal(domains, removed)
                    return False
        
        # Kiểm tra ràng buộc bất đẳng thức với các ô liền kề
        # Ô bên trái: (row, col-1) với ràng buộc h_constraints[row][col-1]
        if col > 0 and puzzle.grid[row][col - 1] == 0:
            constraint = puzzle.h_constraints[row][col - 1]
            if constraint == 1:  # left < right = value, nên left phải < value
                to_remove = [v for v in domains[row][col - 1] if v >= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            elif constraint == -1:  # left > right = value, nên left phải > value
                to_remove = [v for v in domains[row][col - 1] if v <= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            if len(domains[row][col - 1]) == 0:
                self._undo_removal(domains, removed)
                return False
        
        # Ô bên phải: (row, col+1) với ràng buộc h_constraints[row][col]
        if col < puzzle.n - 1 and puzzle.grid[row][col + 1] == 0:
            constraint = puzzle.h_constraints[row][col]
            if constraint == 1:  # value < right, nên right phải > value
                to_remove = [v for v in domains[row][col + 1] if v <= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            elif constraint == -1:  # value > right, nên right phải < value
                to_remove = [v for v in domains[row][col + 1] if v >= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            if len(domains[row][col + 1]) == 0:
                self._undo_removal(domains, removed)
                return False
        
        # Ô phía trên: (row-1, col) với ràng buộc v_constraints[row-1][col]
        if row > 0 and puzzle.grid[row - 1][col] == 0:
            constraint = puzzle.v_constraints[row - 1][col]
            if constraint == 1:  # top < bottom = value, nên top phải < value
                to_remove = [v for v in domains[row - 1][col] if v >= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            elif constraint == -1:  # top > bottom = value, nên top phải > value
                to_remove = [v for v in domains[row - 1][col] if v <= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            if len(domains[row - 1][col]) == 0:
                self._undo_removal(domains, removed)
                return False
        
        # Ô phía dưới: (row+1, col) với ràng buộc v_constraints[row][col]
        if row < puzzle.n - 1 and puzzle.grid[row + 1][col] == 0:
            constraint = puzzle.v_constraints[row][col]
            if constraint == 1:  # value < bottom, nên bottom phải > value
                to_remove = [v for v in domains[row + 1][col] if v <= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            elif constraint == -1:  # value > bottom, nên bottom phải < value
                to_remove = [v for v in domains[row + 1][col] if v >= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            if len(domains[row + 1][col]) == 0:
                self._undo_removal(domains, removed)
                return False
        
        return True
    
    def _undo_removal(self, domains: List[List[Set[int]]], removed: List[Tuple[int, int, int]]):
        """Hoàn tác các thay đổi domain"""
        for r, c, val in removed:
            domains[r][c].add(val)
    
    def _backtrack(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]]) -> bool:
        """Backtracking recursive với MRV và Forward Checking"""
        # Kiểm tra nếu đã giải xong
        if puzzle.is_complete():
            return True
        
        # Chọn ô trống (dùng MRV nếu được bật)
        var = self._select_unassigned_variable(puzzle, domains)
        if var is None:
            return True
        
        row, col = var
        self.nodes_expanded += 1
        
        # Lấy các giá trị có thể gán
        values = self._get_possible_values(puzzle, domains, row, col)
        
        for value in values:
            # Kiểm tra lại tính hợp lệ (an toàn)
            if puzzle.is_valid(row, col, value):
                # Gán giá trị
                puzzle.grid[row][col] = value
                
                # Lưu lại các thay đổi domain để hoàn tác
                removed = []
                
                # Forward checking
                fc_success = True
                if self.use_forward_checking:
                    fc_success = self._forward_check_with_log(puzzle, domains, row, col, value, removed)
                
                if fc_success:
                    if self._backtrack(puzzle, domains):
                        return True
                
                # Hoàn tác các thay đổi domain
                if self.use_forward_checking:
                    self._undo_removal(domains, removed)
                
                # Backtrack: xóa giá trị đã gán
                puzzle.grid[row][col] = 0
                self.backtracks += 1
        
        return False
    
    def _forward_check_with_log(self, puzzle: FutoshikiPuzzle, domains: List[List[Set[int]]], 
                                 row: int, col: int, value: int, removed: List[Tuple[int, int, int]]) -> bool:
        """
        Forward checking với log các thay đổi
        Trả về False nếu có ô nào domain rỗng (failure)
        """
        # Các ô cùng hàng (trừ ô đã gán và ô đã có giá trị)
        for c in range(puzzle.n):
            if c != col and puzzle.grid[row][c] == 0 and value in domains[row][c]:
                domains[row][c].remove(value)
                removed.append((row, c, value))
                if len(domains[row][c]) == 0:
                    return False
        
        # Các ô cùng cột
        for r in range(puzzle.n):
            if r != row and puzzle.grid[r][col] == 0 and value in domains[r][col]:
                domains[r][col].remove(value)
                removed.append((r, col, value))
                if len(domains[r][col]) == 0:
                    return False
        
        # Kiểm tra ràng buộc bất đẳng thức với các ô liền kề
        # Ô bên trái: (row, col-1) với ràng buộc h_constraints[row][col-1]
        if col > 0 and puzzle.grid[row][col - 1] == 0:
            constraint = puzzle.h_constraints[row][col - 1]
            if constraint == 1:  # left < right = value, nên left phải < value
                to_remove = [v for v in domains[row][col - 1] if v >= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            elif constraint == -1:  # left > right = value, nên left phải > value
                to_remove = [v for v in domains[row][col - 1] if v <= value]
                for v in to_remove:
                    domains[row][col - 1].remove(v)
                    removed.append((row, col - 1, v))
            if len(domains[row][col - 1]) == 0:
                return False
        
        # Ô bên phải: (row, col+1) với ràng buộc h_constraints[row][col]
        if col < puzzle.n - 1 and puzzle.grid[row][col + 1] == 0:
            constraint = puzzle.h_constraints[row][col]
            if constraint == 1:  # value < right, nên right phải > value
                to_remove = [v for v in domains[row][col + 1] if v <= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            elif constraint == -1:  # value > right, nên right phải < value
                to_remove = [v for v in domains[row][col + 1] if v >= value]
                for v in to_remove:
                    domains[row][col + 1].remove(v)
                    removed.append((row, col + 1, v))
            if len(domains[row][col + 1]) == 0:
                return False
        
        # Ô phía trên: (row-1, col) với ràng buộc v_constraints[row-1][col]
        if row > 0 and puzzle.grid[row - 1][col] == 0:
            constraint = puzzle.v_constraints[row - 1][col]
            if constraint == 1:  # top < bottom = value, nên top phải < value
                to_remove = [v for v in domains[row - 1][col] if v >= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            elif constraint == -1:  # top > bottom = value, nên top phải > value
                to_remove = [v for v in domains[row - 1][col] if v <= value]
                for v in to_remove:
                    domains[row - 1][col].remove(v)
                    removed.append((row - 1, col, v))
            if len(domains[row - 1][col]) == 0:
                return False
        
        # Ô phía dưới: (row+1, col) với ràng buộc v_constraints[row][col]
        if row < puzzle.n - 1 and puzzle.grid[row + 1][col] == 0:
            constraint = puzzle.v_constraints[row][col]
            if constraint == 1:  # value < bottom, nên bottom phải > value
                to_remove = [v for v in domains[row + 1][col] if v <= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            elif constraint == -1:  # value > bottom, nên bottom phải < value
                to_remove = [v for v in domains[row + 1][col] if v >= value]
                for v in to_remove:
                    domains[row + 1][col].remove(v)
                    removed.append((row + 1, col, v))
            if len(domains[row + 1][col]) == 0:
                return False
        
        return True
    
    def get_stats(self) -> dict:
        """Trả về thống kê"""
        return {
            'algorithm': f'Backtracking (MRV={self.use_mrv}, FC={self.use_forward_checking})',
            'nodes_expanded': self.nodes_expanded,
            'backtracks': self.backtracks,
            'solution_found': self.solution is not None
        }


def solve_puzzle(input_file: str, output_file: str, algorithm: str = 'backtracking',
                 use_mrv: bool = True, use_forward_checking: bool = True) -> dict:
    """
    Giải puzzle từ file input và ghi kết quả ra file output
    
    Args:
        input_file: Đường dẫn file input
        output_file: Đường dẫn file output
        algorithm: 'brute_force' hoặc 'backtracking'
        use_mrv: Bật MRV cho backtracking
        use_forward_checking: Bật Forward Checking cho backtracking
    
    Returns:
        dict chứa thống kê
    """
    # Đọc puzzle
    puzzle = read_input(input_file)
    
    # Chọn solver
    if algorithm == 'brute_force':
        solver = BruteForceSolver(puzzle)
    else:
        solver = BacktrackingSolver(puzzle, use_mrv=use_mrv, 
                                   use_forward_checking=use_forward_checking)
    
    # Giải và đo thời gian
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    
    # Thống kê
    stats = solver.get_stats()
    stats['time'] = end_time - start_time
    stats['input_file'] = input_file
    
    # Ghi output
    if solution:
        write_output(output_file, solution)
        stats['output_file'] = output_file
        print(f"✓ Giải thành công: {input_file}")
        print(f"  Thời gian: {stats['time']:.4f}s")
        print(f"  Nodes expanded: {stats['nodes_expanded']}")
        if 'backtracks' in stats:
            print(f"  Backtracks: {stats['backtracks']}")
    else:
        print(f"✗ Không tìm được lời giải: {input_file}")
    
    return stats


def run_all_tests(input_dir: str = 'Inputs', output_dir: str = 'Outputs'):
    """Chạy tất cả test cases và so sánh hiệu suất"""
    # Tạo thư mục output nếu chưa có
    os.makedirs(output_dir, exist_ok=True)
    
    # Tìm tất cả file input
    input_files = sorted([f for f in os.listdir(input_dir) if f.startswith('input-') and f.endswith('.txt')])
    
    if not input_files:
        print(f"Không tìm thấy file input trong {input_dir}")
        return
    
    print("=" * 80)
    print("SO SÁNH HIỆU SUẤT: BRUTE FORCE vs BACKTRACKING")
    print("=" * 80)
    
    results = []
    
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_num = input_file.replace('input-', '').replace('.txt', '')
        
        print(f"\n{'='*60}")
        print(f"Test case: {input_file}")
        print(f"{'='*60}")
        
        # 1. Brute Force (chỉ chạy với puzzle nhỏ)
        puzzle = read_input(input_path)
        if puzzle.n <= 4:  # Chỉ chạy brute force với N <= 4
            output_bf = os.path.join(output_dir, f"output-{output_num}-bf.txt")
            stats_bf = solve_puzzle(input_path, output_bf, algorithm='brute_force')
            results.append(stats_bf)
        else:
            print(f"  [Bỏ qua Brute Force với N={puzzle.n} - quá lớn]")
        
        # 2. Backtracking với MRV + Forward Checking
        output_bt = os.path.join(output_dir, f"output-{output_num}-bt.txt")
        stats_bt = solve_puzzle(input_path, output_bt, algorithm='backtracking',
                                use_mrv=True, use_forward_checking=True)
        results.append(stats_bt)
        
        # 3. Backtracking không MRV, không Forward Checking (baseline)
        output_bt_basic = os.path.join(output_dir, f"output-{output_num}-bt-basic.txt")
        stats_bt_basic = solve_puzzle(input_path, output_bt_basic, algorithm='backtracking',
                                      use_mrv=False, use_forward_checking=False)
        results.append(stats_bt_basic)
    
    # In bảng tổng hợp
    print(f"\n{'='*80}")
    print("BẢNG TỔNG HỢP KẾT QUẢ")
    print(f"{'='*80}")
    print(f"{'File':<20} {'Algorithm':<35} {'Time (s)':<12} {'Nodes':<12} {'Backtracks':<12}")
    print("-" * 80)
    
    for r in results:
        algo = r['algorithm']
        if len(algo) > 34:
            algo = algo[:31] + "..."
        backtracks = str(r.get('backtracks', '-'))
        print(f"{os.path.basename(r['input_file']):<20} {algo:<35} {r['time']:<12.4f} {r['nodes_expanded']:<12} {backtracks:<12}")
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Chạy với file input cụ thể
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
        algorithm = sys.argv[3] if len(sys.argv) > 3 else 'backtracking'
        
        stats = solve_puzzle(input_file, output_file, algorithm=algorithm)
        print(f"\nThống kê: {stats}")
    else:
        # Chạy tất cả test cases
        # Điều chỉnh đường dẫn tương đối từ vị trí file này
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_dir = os.path.join(script_dir, 'Inputs')
        output_dir = os.path.join(script_dir, 'Outputs')
        
        run_all_tests(input_dir, output_dir)
