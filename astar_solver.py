import heapq
import time
import copy
import tracemalloc  # Thư viện đo bộ nhớ của Python

class AStarSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.nodes_expanded = 0
        self.start_time = 0

    def freeze_state(self, grid):
        return tuple(tuple(row) for row in grid)

    def heuristic(self, grid):
        # h(s): Số ô chưa được gán (giá trị 0)
        return sum(row.count(0) for row in grid)
    
    def heuristic_2(self, grid):
        """
        Heuristic 2: Đếm số ô trống + Cắt tỉa ngõ cụt (Dead-end pruning)
        """
        empty_count = 0
        N = self.puzzle.N
        
        for r in range(N):
            for c in range(N):
                if grid[r][c] == 0:
                    empty_count += 1
                    
                    # Cập nhật grid hiện tại cho Puzzle để test
                    self.puzzle.grid = grid 
                    
                    # Đếm số lượng giá trị hợp lệ cho ô (r, c) này
                    valid_options = 0
                    for val in range(1, N + 1):
                        if self.puzzle.is_valid(r, c, val):
                            valid_options += 1
                    
                    # TÍNH NĂNG "SÁT THỦ": Nếu ô này không thể điền số nào -> Ngõ cụt!
                    if valid_options == 0:
                        return float('inf') # Trả về Vô cực để A* loại bỏ node này ngay
                        
        return empty_count

    def find_empty_cell(self, grid):
        """
        Tìm ô trống sử dụng kỹ thuật MRV (Minimum Remaining Values).
        Chọn ô trống có ít lựa chọn giá trị hợp lệ nhất để mở rộng trước.
        """
        N = self.puzzle.N
        best_r, best_c = -1, -1
        min_options = float('inf')

        for r in range(N):
            for c in range(N):
                if grid[r][c] == 0:
                    # Gán lưới hiện tại cho puzzle để kiểm tra luật
                    self.puzzle.grid = grid
                    
                    # Đếm số lượng giá trị hợp lệ có thể điền vào ô (r, c)
                    valid_count = 0
                    for val in range(1, N + 1):
                        if self.puzzle.is_valid(r, c, val):
                            valid_count += 1
                    
                    # Cập nhật ô tốt nhất nếu ô này có ít sự lựa chọn hơn
                    if valid_count < min_options:
                        min_options = valid_count
                        best_r, best_c = r, c
                        
                        # Tối ưu hóa cực mạnh (Ngắt sớm): 
                        # Nếu tìm thấy một ô chỉ có 1 lựa chọn duy nhất (chắc chắn phải điền số đó)
                        # hoặc 0 lựa chọn (ngõ cụt), ta trả về luôn ô đó để xử lý ngay lập tức!
                        if min_options <= 1:
                            return best_r, best_c
                            
        return best_r, best_c

    def solve(self):
        # Bắt đầu đo bộ nhớ và thời gian
        tracemalloc.start()
        self.start_time = time.time()
        self.nodes_expanded = 0

        queue = []
        tie_breaker = 0 
        
        initial_grid = copy.deepcopy(self.puzzle.grid)
        initial_g = 0
        initial_h = self.heuristic_2(initial_grid)
        
        heapq.heappush(queue, (initial_g + initial_h, tie_breaker, initial_g, initial_grid))
        
        visited = set()
        visited.add(self.freeze_state(initial_grid))

        print(f"=== KHỞI ĐỘNG THUẬT TOÁN A* ===")
        print(f"Trạng thái ban đầu có: {initial_h} ô trống cần giải.\n")

        while queue:
            f, _, g, current_grid = heapq.heappop(queue)
            self.nodes_expanded += 1

            # LOGGING CHO VIDEO DEMO: Cứ mỗi 100 node expanded thì in tiến trình ra màn hình
            if self.nodes_expanded % 100 == 0 or g == 0:
                print(f"[A* Log] Đã duyệt: {self.nodes_expanded} nodes | Ô trống còn lại (h): {self.heuristic_2(current_grid)} | f_score: {f}")

            # Kiểm tra trạng thái đích
            if self.heuristic_2(current_grid) == 0:
                runtime = time.time() - self.start_time
                
                # Lấy dữ liệu bộ nhớ (mảng trả về: current, peak)
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Chuyển đổi từ Bytes sang Megabytes (MB)
                peak_memory_mb = peak_memory / (1024 * 1024)
                
                print(f"\n[A*] TÌM THẤY LỜI GIẢI THÀNH CÔNG!")
                return current_grid, self.nodes_expanded, runtime, peak_memory_mb

            row, col = self.find_empty_cell(current_grid)
            
            if row != -1:
                for val in range(1, self.puzzle.N + 1):
                    self.puzzle.grid = current_grid 
                    
                    if self.puzzle.is_valid(row, col, val):
                        next_grid = copy.deepcopy(current_grid)
                        next_grid[row][col] = val
                        
                        frozen = self.freeze_state(next_grid)
                        if frozen not in visited:
                            visited.add(frozen)
                            next_g = g + 1
                            next_h = self.heuristic_2(next_grid)
                            
                            tie_breaker += 1
                            heapq.heappush(queue, (next_g + next_h, tie_breaker, next_g, next_grid))
                            
        # Kết thúc khi không tìm thấy lời giải
        runtime = time.time() - self.start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_mb = peak_memory / (1024 * 1024)
        
        print(f"\n[A*] Thất bại: Không tìm thấy lời giải hợp lệ.")
        return None, self.nodes_expanded, runtime, peak_memory_mb
    
# Tự viết một lưới 4x4 giả để test A* của bạn trước khi ghép code
class MockPuzzle:
    def __init__(self):
        self.N = 4
        # Lưới 4x4, số 0 là ô trống
        self.grid = [
            [0, 2, 0, 0],
            [0, 0, 0, 3],
            [1, 0, 0, 0],
            [0, 0, 4, 0]
        ]
        
    def is_valid(self, row, col, val):
        # Tạm thời chỉ kiểm tra trùng hàng, trùng cột (bỏ qua dấu <, >)
        # Để test xem A* có điền đầy đủ bảng Sudoku cơ bản không
        if val in self.grid[row]:
            return False
        if val in [self.grid[i][col] for i in range(self.N)]:
            return False
        return True

# =====================================================================
# MINI PARSER DÀNH CHO NGƯỜI SỐ 3 TỰ TEST (KHÔNG CẦN ĐỢI NGƯỜI SỐ 1)
# =====================================================================
class MockPuzzle:
    def __init__(self, filename):
        self.N = 0
        self.grid = []
        self.horiz_constr = []
        self.vert_constr = []
        self.load_from_file(filename)

    def load_from_file(self, filename):
        # Đọc file và bỏ qua các dòng trống
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        self.N = int(lines[0])
        # Đọc N dòng lưới
        self.grid = [list(map(int, lines[i+1].split(','))) for i in range(self.N)]
        # Đọc N dòng ràng buộc ngang
        self.horiz_constr = [list(map(int, lines[i+1+self.N].split(','))) for i in range(self.N)]
        # Đọc N-1 dòng ràng buộc dọc
        self.vert_constr = [list(map(int, lines[i+1+2*self.N].split(','))) for i in range(self.N-1)]

    def is_valid(self, row, col, val):
        """Kiểm tra toàn bộ luật Sudoku và Bất đẳng thức ngang/dọc"""
        # 1. Kiểm tra trùng hàng và cột
        if val in self.grid[row]: return False
        if val in [self.grid[i][col] for i in range(self.N)]: return False

        # 2. Kiểm tra Ràng buộc Ngang (với ô bên trái và bên phải)
        if col > 0 and self.horiz_constr[row][col-1] != 0:
            left_val = self.grid[row][col-1]
            if left_val != 0:
                if self.horiz_constr[row][col-1] == 1 and not (left_val < val): return False
                if self.horiz_constr[row][col-1] == -1 and not (left_val > val): return False
                
        if col < self.N - 1 and self.horiz_constr[row][col] != 0:
            right_val = self.grid[row][col+1]
            if right_val != 0:
                if self.horiz_constr[row][col] == 1 and not (val < right_val): return False
                if self.horiz_constr[row][col] == -1 and not (val > right_val): return False

        # 3. Kiểm tra Ràng buộc Dọc (với ô phía trên và phía dưới)
        if row > 0 and self.vert_constr[row-1][col] != 0:
            top_val = self.grid[row-1][col]
            if top_val != 0:
                if self.vert_constr[row-1][col] == 1 and not (top_val < val): return False
                if self.vert_constr[row-1][col] == -1 and not (top_val > val): return False
                
        if row < self.N - 1 and self.vert_constr[row][col] != 0:
            bottom_val = self.grid[row+1][col]
            if bottom_val != 0:
                if self.vert_constr[row][col] == 1 and not (val < bottom_val): return False
                if self.vert_constr[row][col] == -1 and not (val > bottom_val): return False

        return True

# =====================================================================
# CHẠY THỬ VỚI TEST CASE VỪA TẠO
# =====================================================================
# Bạn có thể đổi tên file thành 'input-02.txt' để test lưới 5x5
test_file = 'input-04.txt' 
print(f"Đang giải mã file: {test_file} ...\n")

mock_puzzle = MockPuzzle(test_file)
solver = AStarSolver(mock_puzzle)

# Gọi hàm giải (đảm bảo hàm solve đang dùng Heuristic 2 và MRV mà chúng ta đã làm)
solved_grid, nodes, time_run, memory_used = solver.solve()

if solved_grid:
    print("\nLưới kết quả:")
    for row in solved_grid:
        print(row)
else:
    print("\nKhông tìm ra kết quả (Ngõ cụt toàn cục)!")
    
print(f"Số node đã mở: {nodes}")
print(f"Thời gian chạy: {time_run:.4f} giây")
print(f"Bộ nhớ tiêu thụ: {memory_used:.4f} MB")