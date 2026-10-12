# BÁO CÁO TÁI LẬP (REPRODUCTION CANDIDATE) — KHAN 2025
> **Paper:** Efficient Story Point Estimation With Comparative Learning (arXiv:2507.14642 [cs.SE])

---

## 📌 1. Phải xác định chính xác cái gì của paper để tái lập?
* **Mục tiêu tái lập:** Tái lập thực nghiệm mô hình học máy theo khung tiếp cận **Học so sánh cặp (Pairwise Comparative Learning Framework)** đối với các User Story trong Agile, nhằm so sánh độ tương quan thứ hạng nỗ lực thay vì dự đoán giá trị điểm số tuyệt đối.
* **Câu hỏi nghiên cứu kiểm chứng:** Liệu việc chuyển bài toán ước lượng Story Point từ dạng hồi quy điểm số tuyệt đối (Absolute Direct Rating) sang so sánh cặp đôi (Relative Pairwise Judgments) có giúp cải thiện độ tin cậy và đạt tương quan thứ hạng cao hơn các mô hình hồi quy truyền thống trên tập dữ liệu chuẩn hay không?

---

## 📑 2. Thông tin bài báo & Tác giả (Paper & Metadata)
* **Tên bài báo:** *Efficient Story Point Estimation With Comparative Learning*
* **Tác giả:** Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, and Zhe Yu
* **Nơi xuất bản:** *arXiv preprint arXiv:2507.14642 [cs.SE]* (Công bố 07/2025; Đang nộp tại các hội thảo hàng đầu về Kỹ nghệ phần mềm ESEM / SANER)
* **DOI / Link:** [arXiv:2507.14642](https://arxiv.org/abs/2507.14642)
* **Replication Package:** [GitHub hil-se/EfficientSPEComparativeLearning](https://github.com/hil-se/EfficientSPEComparativeLearning)
* **Xếp hạng học thuật (Tier):** **Tier 2 (A)** — Nghiên cứu mới từ nhóm tác giả uy tín tại RIT & UMBC, hướng đến hội thảo Rank A.
* **Điểm đánh giá tái lập:** **89 / 100 điểm** (Ưu tiên số 3 - Ý tưởng mới ngoài GitHub repo).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Bài báo nằm ngoài repo GitHub hiện tại của nhóm:** Đây là hướng nghiên cứu hoàn toàn mới, mang tính bổ sung xuất sắc cho danh mục tài liệu nghiên cứu của nhóm.
2. **Khắc phục nhược điểm cốt lõi của Story Point:** Trong thực tế Agile, lập trình viên thường bất đồng về giá trị tuyệt đối (1 task là 3 hay 5 SP), nhưng rất dễ đồng thuận rằng: *"Task A phức tạp hơn Task B"*. Phương pháp Comparative Learning mô phỏng chính xác tâm lý này.
3. **Mã nguồn hoàn chỉnh & Dữ liệu tương thích 100%:** Tác giả cung cấp toàn bộ code trên GitHub (`hil-se/EfficientSPEComparativeLearning`) và thực nghiệm trực tiếp trên 16 dự án Choetkiertikul — hoàn toàn trùng khớp với dữ liệu TAWOS mà nhóm đang có.
4. **Mở ra hướng nghiên cứu mới:** Nếu kết hợp Comparative Learning với cơ chế kiểm soát rò rỉ thời gian (Planning-Time Snapshot của Nhóm 3), đây sẽ là một đóng góp rất sáng tạo cho đề tài.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset:** 
  * 16 dự án mã nguồn mở (tập Choetkiertikul / TAWOS) với **23.313 issues** có Story Point.
  * Tái lập trên dự án đại diện: **Spring XD, Mesos, hoặc Titanium**.
* **Target / Ground Truth:** 
  * Phán đoán thứ tự ưu tiên nỗ lực giữa 2 User Story: $Story_A \succ Story_B$ (Story A tốn nhiều effort hơn Story B).
* **Baseline / Model:**
  * **Model tái lập:** **Comparative Learning Classifier** (biểu diễn cặp văn bản qua text embeddings, đưa qua mô hình phân loại nhị phân cặp để suy ra thứ hạng nỗ lực).
  * **Baselines đối chứng:** Standard Regression Models (Direct Rating: Ridge Regression, Random Forest, SBERT Regressor).
* **Data Split:**
  * Tạo các cặp $(Story_i, Story_j)$ từ tập Train và Test được chia theo Chronological Split để đảm bảo tính thực tế.
* **Metrics đánh giá:**
  * **Spearman's Rank Correlation Coefficient ($\rho$):** Đo mức độ tương quan thứ hạng giữa nỗ lực dự báo và nỗ lực thực tế.
  * **Pairwise Classification Accuracy:** Tỷ lệ đoán đúng cặp task nào tốn nhiều effort hơn.

---

## 📊 5. Kết quả cụ thể muốn tái lập (Targeted Results)
* **Phạm vi tái lập:** Chạy tái lập pipeline huấn luyện mô hình so sánh cặp trên 1 dự án (Spring XD) để lấy chỉ số tương quan thứ hạng.
* **Kết quả chính trong bài báo công bố:**
  * Mô hình huấn luyện bằng Comparative Judgments đạt **Spearman's correlation trung bình là 0.34**, ngang ngửa hoặc vượt qua các mô hình hồi quy trực tiếp trên điểm tuyệt đối.
  * Giảm đáng kể thời gian gán nhãn và tăng mức độ đồng thuận của đội ngũ phát triển.
* **Mục tiêu nhóm cần tái lập:** Chạy mã nguồn của tác giả để tái tạo lại hệ số tương quan Spearman và kiểm tra xem khi áp dụng lọc dữ liệu trước mốc planning thì hiệu năng so sánh cặp thay đổi ra sao.

---

## 🛠️ 6. Khả năng tái lập: Code / Data & Dự kiến Khó / Dễ

| Tiêu chí | Hiện trạng | Đánh giá & Giải pháp |
| :--- | :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn 100%** | Dùng chung 16 dự án Choetkiertikul có sẵn trong CSDL TAWOS local. |
| **Mã nguồn (Code)** | **Có sẵn trên GitHub** | Repository `hil-se/EfficientSPEComparativeLearning` đã có sẵn kịch bản sinh cặp (pair generation) và huấn luyện. |
| **Điểm thuận lợi (Dễ)** | Thư viện chuẩn | Viết trên Python, Scikit-learn và PyTorch tiêu chuẩn, không phụ thuộc môi trường GPU chuyên biệt đắt tiền. |
| **Điểm khó khăn (Khó)** | Chi phí sinh cặp dữ liệu | Việc ghép cặp ($O(N^2)$) tạo ra số lượng mẫu huấn luyện lớn, cần chọn kỹ thuật sampling ngẫu nhiên các cặp để tránh tràn RAM khi huấn luyện. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
