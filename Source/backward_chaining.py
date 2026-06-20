from puzzle import FutoshikiPuzzle

class BackwardChainingSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.puzzle = puzzle.clone()
        self.n = puzzle.n
        # Khởi tạo state copy từ grid gốc
        self.state = [row[:] for row in puzzle.grid]
        self.queries_count = 0
        self.solution = None

    def solve(self):
        """
        Bắt đầu Backward Chaining (Mô phỏng SLD Resolution).
        """
        self.queries_count = 0
        
        # Bắt đầu truy vấn từ ô (0, 0)
        success = self._query_cell(0, 0)
        
        if success:
            self.puzzle.grid = self.state
            self.solution = self.puzzle
            return self.solution
        else:
            return None

    def get_stats(self) -> dict:
        return {
            'algorithm': 'Backward Chaining',
            'nodes_expanded': self.queries_count,
            'solution_found': self.solution is not None
        }

    def _query_cell(self, r, c):
        if r == self.n:
            return True
            
        next_c = c + 1
        next_r = r
        if next_c == self.n:
            next_c = 0
            next_r += 1

        if self.puzzle.grid[r][c] != 0:
            return self._query_cell(next_r, next_c)

        for v in range(1, self.n + 1):
            self.queries_count += 1
            if self._prove_value(r, c, v):
                self.state[r][c] = v
                if self._query_cell(next_r, next_c):
                    return True
                self.state[r][c] = 0
                
        return False

    def _prove_value(self, r, c, v):
        for i in range(self.n):
            if self.state[r][i] == v: return False
            if self.state[i][c] == v: return False
            
        if c > 0 and self.state[r][c-1] != 0:
            h_val = self.puzzle.h_constraints[r][c-1]
            if h_val == 1 and not (self.state[r][c-1] < v): return False
            if h_val == -1 and not (self.state[r][c-1] > v): return False
            
        if c < self.n - 1 and self.state[r][c+1] != 0:
            h_val = self.puzzle.h_constraints[r][c]
            if h_val == 1 and not (v < self.state[r][c+1]): return False
            if h_val == -1 and not (v > self.state[r][c+1]): return False

        if r > 0 and self.state[r-1][c] != 0:
            v_val = self.puzzle.v_constraints[r-1][c]
            if v_val == 1 and not (self.state[r-1][c] < v): return False
            if v_val == -1 and not (self.state[r-1][c] > v): return False
            
        if r < self.n - 1 and self.state[r+1][c] != 0:
            v_val = self.puzzle.v_constraints[r][c]
            if v_val == 1 and not (v < self.state[r+1][c]): return False
            if v_val == -1 and not (v > self.state[r+1][c]): return False

        return True
