import heapq
from typing import List, Tuple, Optional

from puzzle import FutoshikiPuzzle

class AStarSolver:
    def __init__(self, puzzle: FutoshikiPuzzle, **kwargs):
        self.original = puzzle
        self.nodes_expanded = 0
        self.solution = None


    def freeze_state(self, grid: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
        return tuple(tuple(row) for row in grid)

    def get_domain(
        self,
        puzzle: FutoshikiPuzzle,
        row: int,
        col: int
    ) -> List[int]:
        return [
            val
            for val in range(1, puzzle.n + 1)
            if puzzle.is_valid(row, col, val)
        ]

    def get_degree(
        self,
        puzzle: FutoshikiPuzzle,
        row: int,
        col: int
    ) -> int:
        """
        Degree Heuristic nâng cấp cho Futoshiki:
        - Đếm số biến chưa gán cùng hàng/cột.
        - Cộng thêm điểm thưởng (trọng số 2) cho các ràng buộc bất đẳng thức (<, >) nối với ô trống.
        """
        degree = 0

        # 1. Ràng buộc cơ bản (Khác biệt trên cùng hàng & cột)
        for c in range(puzzle.n):
            if c != col and puzzle.grid[row][c] == 0:
                degree += 1

        for r in range(puzzle.n):
            if r != row and puzzle.grid[r][col] == 0:
                degree += 1

        # 2. Ràng buộc nâng cao (Bất đẳng thức Futoshiki)
        # Mỗi ràng buộc bất đẳng thức với ô trống kề cạnh sẽ được cộng 2 điểm (vì sức mạnh cắt tỉa cao hơn)

        # Kiểm tra ô kề trái
        if col > 0 and puzzle.grid[row][col - 1] == 0 and puzzle.h_constraints[row][col - 1] != 0:
            degree += 2

        # Kiểm tra ô kề phải
        if col < puzzle.n - 1 and puzzle.grid[row][col + 1] == 0 and puzzle.h_constraints[row][col] != 0:
            degree += 2

        # Kiểm tra ô kề trên
        if row > 0 and puzzle.grid[row - 1][col] == 0 and puzzle.v_constraints[row - 1][col] != 0:
            degree += 2

        # Kiểm tra ô kề dưới
        if row < puzzle.n - 1 and puzzle.grid[row + 1][col] == 0 and puzzle.v_constraints[row][col] != 0:
            degree += 2

        return degree

    def heuristic_2(self, puzzle: FutoshikiPuzzle) -> float:
        """
        Heuristic:
        - Số ô trống còn lại.
        - Nếu tồn tại ô có domain rỗng => dead-end.
        """
        empty_count = 0

        for r in range(puzzle.n):
            for c in range(puzzle.n):

                if puzzle.grid[r][c] == 0:

                    empty_count += 1

                    domain = self.get_domain(puzzle, r, c)

                    if len(domain) == 0:
                        return float('inf')

        return empty_count

    def find_empty_cell(
        self,
        puzzle: FutoshikiPuzzle
    ) -> Tuple[int, int, List[int]]:

        best_r = -1
        best_c = -1
        best_domain = []

        min_options = float('inf')
        max_degree = -1

        for r in range(puzzle.n):
            for c in range(puzzle.n):

                if puzzle.grid[r][c] == 0:

                    domain = self.get_domain(
                        puzzle,
                        r,
                        c
                    )

                    domain_size = len(domain)

                    # MRV
                    if domain_size < min_options:

                        min_options = domain_size

                        best_r = r
                        best_c = c
                        best_domain = domain

                        max_degree = self.get_degree(
                            puzzle,
                            r,
                            c
                        )

                        if domain_size <= 1:
                            return best_r, best_c, best_domain

                    # Degree Heuristic (tie-break)
                    elif domain_size == min_options:

                        degree = self.get_degree(
                            puzzle,
                            r,
                            c
                        )

                        if degree > max_degree:

                            max_degree = degree

                            best_r = r
                            best_c = c
                            best_domain = domain

        return best_r, best_c, best_domain

    def solve(self) -> Optional[FutoshikiPuzzle]:

        self.nodes_expanded = 0
        self.solution = None

        queue = []
        tie_breaker = 0

        initial_puzzle = self.original.clone()

        initial_h = self.heuristic_2(initial_puzzle)

        heapq.heappush(
            queue,
            (
                initial_h,
                0,
                tie_breaker,
                0,
                initial_puzzle
            )
        )

       
        closed_set = set()

        while queue:

            (
                f,
                _domain_size,
                _,
                g,
                current_puzzle
            ) = heapq.heappop(queue)

            current_state = self.freeze_state(
                current_puzzle.grid
            )

            if current_state in closed_set:
                continue

            closed_set.add(current_state)

            self.nodes_expanded += 1

            # Goal test
            if current_puzzle.is_complete():
                self.solution = current_puzzle
                return current_puzzle

            row, col, domain = self.find_empty_cell(
                current_puzzle
            )

            if row == -1:
                continue

            for val in domain:

                next_puzzle = current_puzzle.clone()
                next_puzzle.grid[row][col] = val

                frozen = self.freeze_state(
                    next_puzzle.grid
                )

                if frozen in closed_set:
                    continue

                next_h = self.heuristic_2(next_puzzle)

                # Dead-end
                if next_h == float('inf'):
                    continue

                next_g = g + 1

                tie_breaker += 1

                heapq.heappush(
                    queue,
                    (
                        next_g + next_h,
                        len(domain),
                        tie_breaker,
                        next_g,
                        next_puzzle
                    )
                )

        return None

    def get_stats(self) -> dict:
        return {
            'algorithm': 'A* (Heuristic 2 + MRV)',
            'nodes_expanded': self.nodes_expanded,
            'solution_found': self.solution is not None
        }

