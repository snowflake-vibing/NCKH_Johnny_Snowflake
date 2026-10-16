# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** Efficient Story Point Estimation With Comparative Learning  
> **Nguồn công bố:** arXiv:2507.14642 [cs.SE], 2025

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | Efficient Story Point Estimation With Comparative Learning |
| **2**  | **Cite Key**             | `khan2025comparative` |
| **3**  | **Authors**              | Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, Zhe Yu |
| **4**  | **Year**                 | 2025 |
| **5**  | **Venue**                | arXiv preprint (Mục tiêu hội thảo ESEM / SANER 2025/2026) |
| **6**  | **Files & media**        | [Preprint arXiv:2507.14642](https://arxiv.org/abs/2507.14642) \| [GitHub Code](https://github.com/hil-se/EfficientSPEComparativeLearning) |
| **7**  | **Venue Type**           | Preprint / Conference Candidate |
| **8**  | **SJR Quartile**         | N/A (Conference / Preprint) |
| **9**  | **CORE Rank**            | CORE Rank A (Hội nghị mục tiêu ESEM / SANER) |
| **10** | **Rank**                 | Candidate Tier 2 (A) |
| **11** | **Problem**              | Giải quyết hạn chế của việc hồi quy điểm số tuyệt đối (Direct Rating): lập trình viên thường bất đồng khi chấm một con số cụ thể (3 hay 5 SP), nhưng lại đồng thuận rất nhanh khi so sánh tương đối giữa 2 task (Task A tốn nhiều công sức hơn Task B). |
| **12** | **Dataset**              | 16 dự án mã nguồn mở từ tập Choetkiertikul / TAWOS với 23.313 issues có gán điểm Story Point. |
| **13** | **Ground Truth**         | Quan hệ thứ tự ưu tiên nỗ lực giữa 2 User Story: $Story_A \succ Story_B$, suy ra từ giá trị SP ghi nhận trong Jira. |
| **14** | **Method**               | **Pairwise Comparative Learning Framework**: Mã hóa text bằng Sentence-BERT (`all-MiniLM-L6-v2`), xây dựng vector quan hệ cặp đôi $x_{ij} = [v_i, v_j, v_i - v_j, v_i \odot v_j]$, huấn luyện bộ phân loại nhị phân cặp (LightGBM/MLP) với hàm Binary Cross-Entropy và suy diễn thứ hạng toàn cục qua Borda Count. |
| **15** | **Baseline**             | Các mô hình hồi quy điểm số tuyệt đối truyền thống: Ridge Regression, Random Forest, SBERT Regressor. |
| **16** | **Split**                | Chronological Split trên từng dự án để mô phỏng chính xác thứ tự công việc thực tế trong Agile. |
| **17** | **Metrics**              | Spearman's Rank Correlation Coefficient ($\rho$), Pairwise Classification Accuracy. |
| **18** | **Main Result**          | Hệ số tương quan Spearman trung bình đạt $\rho = 0.34$ trên 16 dự án, vượt trội hơn các mô hình hồi quy tuyệt đối; thử nghiệm người dùng (Human study) cho thấy giảm đáng kể thời gian thảo luận và tăng độ tự tin của lập trình viên. |
| **19** | **Critical Notes**       | 1. **Bùng nổ tổ hợp cặp ($O(N^2)$):** Với hàng chục nghìn issues, số cặp lên tới hàng trăm triệu, bắt buộc phải dùng kỹ thuật Pair Subsampling ($K \approx 10-20$).<br>2. **Vẫn dính bẫy Temporal Leakage:** Tác giả sử dụng text tĩnh sau khi issue hoàn thành từ bộ dữ liệu Choetkiertikul cũ, chưa kiểm soát rò rỉ tại thời điểm Sprint Planning. |
| **20** | **Takeaways**            | 1. Chuyển đổi bài toán từ hồi quy điểm số tuyệt đối sang học so sánh cặp (Ranking/Comparative) là hướng tiếp cận rất phù hợp với tâm lý con người trong Agile.<br>2. SBERT kết hợp feature engineering theo cặp ($v_i - v_j$, Hadamard product) chạy nhẹ và nhanh hơn nhiều so với fine-tune toàn bộ LLM như GPT-2. |
| **21** | **Relevance to Topic**   | Cung cấp góc nhìn mở rộng cực kỳ giá trị ngoài các baseline truyền thống: Nhóm 3 có thể đánh giá xem *"Khi bịt lỗ hổng rò rỉ dữ liệu, độ chính xác xếp hạng nỗ lực của mô hình so sánh cặp có còn giữ vững được hệ số Spearman 0.34 hay không?"*. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Nghịch lý của điểm số tuyệt đối:** Trong Sprint Planning thực tế, việc gán một con số Story Point tuyệt đối thường gây tranh luận kéo dài và chịu ảnh hưởng nặng nề bởi tính chủ quan. Ngược lại, con người lại rất nhạy bén và đồng thuận nhanh khi so sánh tương đối độ phức tạp giữa hai công việc.
- **Hạn chế của mô hình hồi quy truyền thống:** Các mô hình học máy dự báo số tuyệt đối (Ridge, Random Forest, Deep-SE, GPT2SP) dễ bị lệch bởi phân phối nhãn không cân bằng (đa số task là 1, 2, 3 điểm; rất ít task 8, 13, 20 điểm) và khó chuyển giao giữa các nhóm có thước đo Story Point khác nhau.

### 2.2. Chi Tiết Kiến Trúc Kỹ Thuật (Comparative Learning Framework)
1. **Ghép cặp User Story (Pair Generation):**
   - Với mỗi cặp $(Story_i, Story_j)$, xác định nhãn nhị phân:
     $$z_{ij} = \begin{cases} 1 & \text{nếu } SP_i > SP_j \\ 0 & \text{nếu } SP_i < SP_j \end{cases}$$
   - Lọc bỏ các cặp có cùng điểm ($SP_i = SP_j$) để tránh gây nhiễu biên phân lớp.
2. **Trích xuất đặc trưng ngữ nghĩa bằng Sentence-BERT:**
   - Dùng mô hình SBERT tiền huấn luyện trích xuất embedding:
     $$v_i = \text{SBERT}(Story_i) \in \mathbb{R}^{d}, \quad v_j = \text{SBERT}(Story_j) \in \mathbb{R}^{d}$$
3. **Tổng hợp vector tương tác cặp:**
   - Kết hợp 4 thành phần: vector gốc, vector đối ngẫu, vector hiệu khoảng cách và tích Hadamard:
     $$x_{ij} = [v_i, \; v_j, \; (v_i - v_j), \; (v_i \odot v_j)] \in \mathbb{R}^{4d}$$
4. **Phân loại nhị phân & Suy diễn thứ hạng:**
   - Huấn luyện bộ phân loại (Logistic Regression / LightGBM / MLP) với hàm mất mát Binary Cross-Entropy (BCE).
   - Suy diễn thứ hạng toàn cục backlog bằng giải thuật tích lũy điểm thắng (Borda Count Voting) hoặc PageRank.

### 2.3. Đánh Giá Phản Biện Dành Riêng Cho Đề Tài Nhóm 3
- Bài báo của Khan et al. (2025) là minh chứng cho thấy xu hướng nghiên cứu Story Point đang dịch chuyển sang các mô hình ngữ nghĩa nhẹ (SBERT) và cơ chế so sánh thứ tự.
- **Điểm yếu chí mạng chưa giải quyết:** Toàn bộ thực nghiệm của Khan et al. vẫn sử dụng Final Snapshot. Nếu mô tả của issue sau khi làm xong đã bị lập trình viên thêm vào các câu từ chỉ ra lỗi và giải pháp, bộ phân loại cặp sẽ dễ dàng "nhìn trộm" thông tin để phán đoán task nào phức tạp hơn, dẫn đến hệ số Spearman bị thổi phồng.
- **Cơ hội cho bài báo của Nhóm 3:** Kiểm tra độ bền vững của mô hình Comparative Learning trên bộ dữ liệu `Planning-Time Snapshot` do nhóm tái dựng.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
