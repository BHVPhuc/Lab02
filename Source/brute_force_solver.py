from puzzle import FutoshikiPuzzle


class BruteForceSolver:
    """
    Brute Force Solver - Thu tat ca cac to hop co the
    Khong dung heuristic, khong pruning
    Dung lam baseline de so sanh
    """
    
    def __init__(self, puzzle: FutoshikiPuzzle):
        self.original = puzzle
        self.nodes_expanded = 0
        self.solution = None
        
    def solve(self):
        """Giai puzzle bang brute force"""
        puzzle = self.original.clone()
        self.nodes_expanded = 0
        
        if self._brute_force(puzzle):
            self.solution = puzzle
            return puzzle
        return None
    
    def _brute_force(self, puzzle: FutoshikiPuzzle) -> bool:
        """Recursive brute force - thu tat ca gia tri 1->N cho moi o"""
        empty = puzzle.find_empty()
        if empty is None:
            return True  # Da dien het
        
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
        """Tra ve thong ke"""
        return {
            'algorithm': 'Brute Force',
            'nodes_expanded': self.nodes_expanded,
            'solution_found': self.solution is not None
        }
