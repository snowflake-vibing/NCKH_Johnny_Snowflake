# BÁO CÁO TÁI LẬP (REPRODUCTION CANDIDATE) — KHAN 2025
> **Paper:** Efficient Story Point Estimation With Comparative Learning (arXiv:2507.14642 [cs.SE])

---

## 📌 1. Phải xác định chính xác cái gì của paper để tái lập?
* **Mục tiêu tái lập:** Tái lập thực nghiệm mô hình học máy theo khung tiếp cận **Học so sánh cặp (Pairwise Comparative Learning Framework)** đối với các User Story trong Agile, nhằm so sánh độ tương quan thứ hạng nỗ lực thay vì dự đoán giá trị điểm số tuyệt đối.
* **Câu hỏi nghiên cứu kiểm chứng:** Liệu việc chuyển bài toán ước lượng Story Point từ dạng hồi quy điểm số tuyệt đối (Absolute Direct Rating) sang so sánh cặp đôi (Relative Pairwise Judgments) có giúp cải thiện độ tin cậy và đạt tương quan thứ hạng cao hơn các mô hình hồi quy truyền thống trên tập dữ liệu chuẩn hay không?

---

## 📑 2. Thông tin bài báo & Tác giả (Paper & Metadata)
* **Tên bài báo:** *Efficient Story Point Estimation With Comparative Learning*
* **Tác giả:** Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, and Zhe Yu (RIT & UMBC)
* **Nơi xuất bản:** *arXiv preprint arXiv:2507.14642 [cs.SE]* (Công bố 07/2025; Đang nộp tại các hội thảo hàng đầu về Kỹ nghệ phần mềm ESEM / SANER)
* **Preprint / Link:** [arXiv:2507.14642](https://arxiv.org/abs/2507.14642)
* **Xếp hạng học thuật (Tier):** **Tier 2 (A)** — Nghiên cứu mới hướng đến hội thảo Rank A (CORE Rank A: ESEM / SANER).
* **Điểm đánh giá tái lập:** **89 / 100 điểm** (Ứng viên ưu tiên số 3 - Ý tưởng mới đột phá ngoài repo).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Bài báo nằm ngoài repo GitHub hiện tại của nhóm:** Đây là hướng nghiên cứu hoàn toàn mới, mang tính mở rộng xuất sắc cho danh mục tài liệu nghiên cứu của nhóm.
2. **Khắc phục nhược điểm cốt lõi của Story Point:** Trong thực tế Agile, lập trình viên thường bất đồng về giá trị tuyệt đối (1 task là 3 hay 5 SP), nhưng rất dễ đồng thuận rằng: *"Task A phức tạp hơn Task B"*. Phương pháp Comparative Learning mô phỏng chính xác tâm lý này.
3. **Mã nguồn hoàn chỉnh & Dữ liệu tương thích 100%:** Tác giả cung cấp toàn bộ code trên GitHub và thực nghiệm trực tiếp trên 16 dự án Choetkiertikul — hoàn toàn trùng khớp với dữ liệu TAWOS mà nhóm đang có.
4. **Mở ra hướng nghiên cứu mới:** Nếu kết hợp Comparative Learning với cơ chế kiểm soát rò rỉ thời gian (Planning-Time Snapshot của Nhóm 3), đây sẽ là một đóng góp rất sáng tạo cho đề tài.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset & Đường dẫn dữ liệu (Data Links):** 
  * 16 dự án mã nguồn mở (tập Choetkiertikul / TAWOS) với **23.313 issues** có Story Point.
  * **Link Dữ liệu Gốc GitHub:** [morakotch/datasets (GitHub)](https://github.com/morakotch/datasets) | [SOLAR-group/TAWOS (GitHub)](https://github.com/SOLAR-group/TAWOS)
  * **Link HuggingFace Mirror:** [giseldo/deep-se (HuggingFace Datasets)](https://huggingface.co/datasets/giseldo/deep-se)
* **Mã nguồn & Replication Package (Code Links):**
  * **GitHub Official Package:** [hil-se/EfficientSPEComparativeLearning (GitHub)](https://github.com/hil-se/EfficientSPEComparativeLearning)
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

## 📊 5. Kết quả cụ thể muốn tái lập & Kỳ vọng khoa học (Targeted Results & Expectations)
* **Phạm vi tái lập cụ thể:** Chạy tái lập pipeline huấn luyện mô hình so sánh cặp trên 2 dự án tiêu biểu (**Spring XD** và **Mesos**) để lấy chỉ số tương quan thứ hạng.
* **Kết quả chính trong bài báo công bố:**
  * Mô hình huấn luyện bằng Comparative Judgments đạt **Spearman's correlation trung bình là 0.34**, ngang ngửa hoặc vượt qua các mô hình hồi quy trực tiếp trên điểm tuyệt đối.
  * Giảm đáng kể thời gian gán nhãn và tăng mức độ đồng thuận của đội ngũ phát triển.
* **Mục tiêu nhóm cần tái lập:** Chạy mã nguồn của tác giả để tái tạo lại hệ số tương quan Spearman và kiểm tra xem khi áp dụng lọc dữ liệu trước mốc planning thì hiệu năng so sánh cặp thay đổi ra sao.
* **🎯 Kỳ vọng đạt được nếu tái lập & mở rộng thành công:**
  * **Xếp hạng hội nghị / Tạp chí kỳ vọng:** 
    * **Hội thảo Quốc tế:** **ACM/IEEE International Conference on Software Engineering (ICSE - CORE Rank A* / Poster/Artifact Track)** hoặc **IEEE/ACM ESEM (CORE Rank A)**.
    * **Tạp chí Quốc tế:** **Journal of Systems and Software (JSS - Q1/Tier 2)**.
  * **Giá trị đóng góp đề tài:** Tạo ra một hướng tiếp cận đột phá khi tích hợp: *Học so sánh cặp (Comparative Learning)* + *Kiểm soát rò rỉ thời gian (Temporal Leakage Control)*, nâng cao tính khả thi của mô hình khi triển khai vào các buổi họp Sprint Planning thực tế.

---

## 🛠️ 6. Khả năng tái lập: Công cụ, Thời gian & Dự kiến Khó / Dễ

| Tiêu chí | Chi tiết đánh giá |
| :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn 100% trực tuyến:** Dùng chung 16 dự án Choetkiertikul/TAWOS có sẵn link GitHub và local DB. |
| **Mã nguồn (Code)** | **Có sẵn 100% trực tuyến:** Repo GitHub `hil-se/EfficientSPEComparativeLearning` cung cấp đầy đủ script. |
| **Công cụ & Môi trường cần thiết** | • **Ngôn ngữ:** Python 3.9+<br>• **Thư viện AI/ML:** `scikit-learn`, `sentence-transformers`, `torch`, `scipy`, `pandas`, `numpy`<br>• **Phần cứng:** Google Colab GPU (Tesla T4) hoặc Máy tính cá nhân (16GB RAM + CPU đa nhân). |
| **Thời gian tái lập dự kiến** | • **Sinh tập cặp dữ liệu (Pair Generation):** ~1 – 2 giờ.<br>• **Huấn luyện & Đánh giá Spearman Correlation:** ~2 – 4 giờ.<br>• **Tổng thời gian hoàn thiện:** **2 – 3 ngày làm việc**. |
| **Độ thuận lợi (Dễ)** | Code viết bằng thư viện Machine Learning và PyTorch chuẩn mực, cấu trúc module rõ ràng. |
| **Thách thức (Khó)** | Độ phức tạp số lượng cặp $O(N^2)$ có thể gây tràn bộ nhớ (RAM) nếu không áp dụng kỹ thuật Pair Subsampling hợp lý. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
