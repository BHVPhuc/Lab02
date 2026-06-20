# Báo Cáo Tổng Hợp Thuật Toán Futoshiki

## 1. Giới Thiệu
Báo cáo này tổng hợp kết quả chạy thử nghiệm 4 thuật toán trên 10 test cases được yêu cầu trong đồ án:
1. Brute Force
2. Backtracking (có sử dụng Minimum Remaining Values (MRV) và Forward Checking)
3. Forward Chaining (kết hợp Backtracking khi gặp điểm nghẽn)
4. Backward Chaining (Mô phỏng SLD Resolution)

## 2. Bảng Thống Kê Benchmark (Thời gian và Số phép duyệt)

| File | Thuật toán | Thời gian (s) | Số phép duyệt (Nodes/Inferences) |
|------|-----------|--------------|--------------------------------|
| **input-01.txt** | Brute Force | 0.0005 | 142 |
| | Backtracking | 0.0008 | 19 |
| | Forward Chaining | 0.0002 | 41 |
| | Backward Chaining | 0.0004 | 546 |
| **input-02.txt** | Brute Force | 0.0001 | 18 |
| | Backtracking | 0.0005 | 16 |
| | Forward Chaining | 0.0001 | 43 |
| | Backward Chaining | 0.0001 | 48 |
| **input-03.txt** | Brute Force | 0.0011 | 250 |
| | Backtracking | 0.0005 | 25 |
| | Forward Chaining | 0.0002 | 76 |
| | Backward Chaining | 0.0007 | 1209 |
| **input-04.txt** | Brute Force | 0.0002 | 30 |
| | Backtracking | 0.0007 | 22 |
| | Forward Chaining | 0.0006 | 222 |
| | Backward Chaining | 0.0001 | 108 |
| **input-05.txt** | Brute Force | 1.5493 | 237,832 |
| | Backtracking | 0.0011 | 56 |
| | Forward Chaining | 0.0019 | 528 |
| | Backward Chaining | 0.8719 | 1,426,904 |
| **input-06.txt** | Brute Force | 0.0009 | 99 |
| | Backtracking | 0.0012 | 34 |
| | Forward Chaining | 0.0025 | 653 |
| | Backward Chaining | 0.0005 | 509 |
| **input-07.txt** | Brute Force | 0.0010 | 131 |
| | Backtracking | 0.0015 | 49 |
| | Forward Chaining | 0.0041 | 1306 |
| | Backward Chaining | 0.0008 | 770 |
| **input-08.txt** | Brute Force | 0.0007 | 96 |
| | Backtracking | 0.0013 | 47 |
| | Forward Chaining | 0.0045 | 1385 |
| | Backward Chaining | 0.0003 | 531 |
| **input-09.txt** | Brute Force | 0.0035 | 302 |
| | Backtracking | 0.0033 | 83 |
| | Forward Chaining | 0.0186 | 4182 |
| | Backward Chaining | 0.0015 | 2394 |
| **input-10.txt** | Brute Force | 0.0027 | 233 |
| | Backtracking | 0.0044 | 79 |
| | Forward Chaining | 0.0187 | 4094 |
| | Backward Chaining | 0.0013 | 1781 |

## 3. Nhận Xét & Đánh Giá
- **Brute Force:** Rất nhanh ở các test case nhỏ hoặc có nhiều gợi ý sẵn. Tuy nhiên với `input-05.txt` (nhiều ô trống và ít gợi ý), thời gian bùng nổ lên tới **1.5 giây** và hơn **237,000** số bước duyệt.
- **Backtracking (với MRV & Forward Checking):** Cực kỳ ổn định và tối ưu hóa cao nhất trên toàn bộ các bộ test. Số node duyệt dao động chỉ dưới 100 kể cả với `input-05.txt`, minh chứng sức mạnh tuyệt đối của hàm heuristic MRV.
- **Forward Chaining & Backward Chaining:** Đóng vai trò là thuật toán suy diễn logic. Tốc độ rất nhanh ở đa số test case (~0.001s). Tuy nhiên điểm hạn chế của SLD Resolution (Backward) được thể hiện rõ ở `input-05.txt` khi phải đệ quy và thử nghiệm tới **1.4 triệu** lần, mất **0.87s** mới tìm được nghiệm. Forward Chaining thì khắc phục được điểm yếu này do được kết hợp nhánh tìm kiếm chặn mâu thuẫn tốt hơn.

## 4. Biểu đồ Benchmark
Bạn có thể copy bảng số liệu ở phần 2 sang Excel để insert biểu đồ Cột (Bar Chart). Đề xuất làm 2 biểu đồ:
- Biểu đồ **Thời gian thực thi (s)**: So sánh tốc độ giữa 4 thuật toán trên các test case.
- Biểu đồ **Số phép duyệt (Nodes/Inferences)**: Minh họa không gian tìm kiếm thực sự của từng thuật toán.
