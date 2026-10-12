# BÁO CÁO TÁI LẬP (REPRODUCTION CANDIDATE) — TAWOSI 2022
> **Paper:** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study (IEEE TSE 2022)

---

## 📌 1. Phải xác định chính xác cái gì của paper để tái lập?
* **Mục tiêu tái lập:** Tái lập thực nghiệm quy trình đánh giá chuẩn mực (Replication Benchmark Pipeline) đối với các mô hình ước lượng Story Point cơ bản và học sâu (bao gồm: **Median Effort, Mean Effort, TF-IDF + SVM, và Deep-SE**) trên các tập dữ liệu mã nguồn mở quy mô lớn.
* **Câu hỏi nghiên cứu kiểm chứng:** Liệu các kỹ thuật học sâu phức tạp (như Deep-SE) có thực sự vượt trội hơn các đường cơ sở thống kê đơn giản (Median Baseline) khi được kiểm định thống kê nghiêm ngặt (Wilcoxon Signed-Rank Test và Vargha-Delaney $\hat{A}_{12}$)?

---

## 📑 2. Thông tin bài báo & Tác giả (Paper & Metadata)
* **Tên bài báo:** *Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study*
* **Tác giả:** Vali Tawosi, Rebecca Moussa, and Federica Sarro (SOLAR Research Group - UCL)
* **Nơi xuất bản:** *IEEE Transactions on Software Engineering (TSE)*, Vol. 49, No. 4, 2022 (arXiv:2201.05401)
* **DOI:** [10.1109/TSE.2022.3204902](https://doi.org/10.1109/TSE.2022.3204902)
* **Xếp hạng học thuật (Tier):** **Tier 1 (A*)** — Tạp chí đầu ngành Software Engineering thế giới.
* **Điểm đánh giá tái lập:** **97 / 100 điểm** (Ưu tiên số 2 - Bộ khung Benchmark đối chứng).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Bộ khung thực nghiệm chuẩn mực nhất:** Đây là công trình tái lặp mẫu mực nhất trong lĩnh vực ước lượng nỗ lực phần mềm, chỉ ra các sai lầm phổ biến trong thiết kế thực nghiệm ML/DL (như bóp outlier 90th percentile trên test set gây sai số giả tạo).
2. **Kho mã nguồn & Dữ liệu hoàn chỉnh (Public Replication Package):** Tác giả cung cấp toàn bộ mã nguồn kiểm chứng sạch sẽ, được tổ chức bài bản tại [`SOLAR-group/AgileEffortEstimation`](https://github.com/SOLAR-group/AgileEffortEstimation).
3. **Mối liên hệ trực tiếp với CSDL TAWOS của Đề tài:** Tác giả chính (Vali Tawosi) cũng chính là người xây dựng tập dữ liệu TAWOS v1.1 mà Nhóm 3 đang sử dụng làm nguồn dữ liệu chính trong CSDL cục bộ.
4. **Cơ sở xây dựng Baseline:** Cung cấp bộ công cụ tính toán thống kê (Statistical Tests: Wilcoxon, $\hat{A}_{12}$) đạt chuẩn mực xuất bản quốc tế cho đề tài của nhóm.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset:** 
  * Bộ dữ liệu Choetkiertikul (16 dự án, 23.313 issues) và Tawosi mở rộng (26 dự án).
  * Quy mô tái lập chọn lọc: Các dự án tiêu biểu như **Spring XD, Mule, Appcelerator**.
* **Target / Ground Truth:** 
  * Giá trị Story Point (SP) thực tế ghi nhận trong hệ thống Jira.
* **Baseline / Model:**
  * **Statistical Baselines:** Random Guessing (RG), Mean Effort, **Median Effort** (đường cơ sở quan trọng nhất).
  * **Machine Learning Baseline:** TF-IDF + Support Vector Machine (SVM) / Ridge Regression.
  * **Deep Learning Baseline:** Deep-SE (Word2Vec + LSTM + Recurrent Highway Network).
* **Data Split:**
  * **Chronological Split** (60% Train / 20% Val / 20% Test) theo thứ tự mốc thời gian tạo issue (`created_date`), triệt tiêu việc xáo trộn dữ liệu tương lai vào quá khứ.
* **Metrics đánh giá:**
  * **MAE** (Mean Absolute Error), **MdAE** (Median Absolute Error), **SA** (Standardized Accuracy).
  * **Kiểm định thống kê:** Wilcoxon Signed-Rank Test ($\alpha = 0.05$) và Vargha-Delaney $\hat{A}_{12}$ Effect Size (đo độ vượt trội thực chất giữa 2 phân phối sai số).

---

## 📊 5. Kết quả cụ thể muốn tái lập (Targeted Results)
* **Phạm vi tái lập:** Tái lập kết quả đánh giá các **Statistical Baselines (Median, Mean) & TF-IDF** so với mô hình học máy trên dự án Spring XD.
* **Kết quả chính trong bài báo công bố:**
  * Mô hình học sâu Deep-SE **không vượt trội hơn Median Baseline ở 58% các dự án** thử nghiệm within-project.
  * Kỹ thuật Data Augmentation làm giảm hiệu năng ở 67% dự án.
  * Median Baseline đạt độ ổn định rất cao và là thước đo bắt buộc phải vượt qua đối với bất kỳ mô hình AI nào.
* **Kết quả nhóm cần kiểm chứng:** Xác nhận lại chỉ số MAE của Median Baseline trên tập Spring XD (~1.7153) để làm ngưỡng chặn dưới (lower bound) cho các mô hình phức tạp.

---

## 🛠️ 6. Khả năng tái lập: Code / Data & Dự kiến Khó / Dễ

| Tiêu chí | Hiện trạng | Đánh giá & Giải pháp |
| :--- | :--- | :--- |
| **Dữ liệu (Data)** | **Rất sẵn sàng** | Toàn bộ dữ liệu nằm trong hệ thống TAWOS v1.1 local của nhóm. |
| **Mã nguồn (Code)** | **Có sẵn 100%** | Repo GitHub `SOLAR-group/AgileEffortEstimation` có đầy đủ scripts chạy python, tính metrics và kiểm định thống kê. |
| **Điểm thuận lợi (Dễ)** | Code cực sạch & chuẩn hóa | Các baseline Median, Mean, TF-IDF chạy rất nhanh, tiêu tốn ít RAM/CPU, không đòi hỏi GPU. |
| **Điểm khó khăn (Khó)** | Kiểm định thống kê | Cần hiểu sâu về kiểm định phi tham số (Non-parametric tests: Wilcoxon và $\hat{A}_{12}$) để diễn giải đúng kết quả học thuật. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
