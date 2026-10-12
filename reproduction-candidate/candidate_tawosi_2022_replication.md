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
* **Nơi xuất bản:** *IEEE Transactions on Software Engineering (TSE)*, Vol. 49, No. 4, 2022
* **Preprint / DOI:** [arXiv:2201.05401](https://arxiv.org/abs/2201.05401) | [10.1109/TSE.2022.3204902](https://doi.org/10.1109/TSE.2022.3204902)
* **Xếp hạng học thuật (Tier):** **Tier 1 (A*)** — Tạp chí đầu ngành Software Engineering thế giới (Q1 Scopus, CCF-A, H-index 180+).
* **Điểm đánh giá tái lập:** **97 / 100 điểm** (Ứng viên ưu tiên số 2 - Bộ khung Benchmark đối chứng).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Bộ khung thực nghiệm chuẩn mực nhất:** Đây là công trình tái lặp mẫu mực nhất trong lĩnh vực ước lượng nỗ lực phần mềm, chỉ ra các sai lầm phổ biến trong thiết kế thực nghiệm ML/DL (như bóp outlier 90th percentile trên test set gây sai số giả tạo).
2. **Kho mã nguồn & Dữ liệu hoàn chỉnh (Public Replication Package):** Tác giả cung cấp toàn bộ mã nguồn kiểm chứng sạch sẽ, được tổ chức bài bản trên GitHub.
3. **Mối liên hệ trực tiếp với CSDL TAWOS của Đề tài:** Tác giả chính (Vali Tawosi) cũng chính là người xây dựng tập dữ liệu TAWOS v1.1 mà Nhóm 3 đang sử dụng làm nguồn dữ liệu chính trong CSDL cục bộ.
4. **Cơ sở xây dựng Baseline:** Cung cấp bộ công cụ tính toán thống kê (Statistical Tests: Wilcoxon, $\hat{A}_{12}$) đạt chuẩn mực xuất bản quốc tế cho đề tài của nhóm.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset & Đường dẫn dữ liệu (Data Links):** 
  * Bộ dữ liệu Choetkiertikul (16 dự án, 23.313 issues) và Tawosi mở rộng (26 dự án).
  * **Link TAWOS Dataset GitHub:** [SOLAR-group/TAWOS (GitHub)](https://github.com/SOLAR-group/TAWOS)
  * **Link Zenodo / Data Archive:** [TAWOS v1.1 Zenodo Archive](https://doi.org/10.5281/zenodo.5828456)
* **Mã nguồn & Replication Package (Code Links):**
  * **GitHub Official Package:** [SOLAR-group/AgileEffortEstimation (GitHub)](https://github.com/SOLAR-group/AgileEffortEstimation)
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

## 📊 5. Kết quả cụ thể muốn tái lập & Kỳ vọng khoa học (Targeted Results & Expectations)
* **Phạm vi tái lập cụ thể:** Tái lập toàn bộ các **Statistical Baselines (Median, Mean) & TF-IDF/SVM** trên dự án Spring XD và 3 dự án Jira tiêu biểu.
* **Kết quả chính trong bài báo công bố:**
  * Mô hình học sâu Deep-SE **không vượt trội hơn Median Baseline ở 58% các dự án** thử nghiệm within-project.
  * Kỹ thuật Data Augmentation làm giảm hiệu năng ở 67% dự án.
  * Median Baseline đạt độ ổn định rất cao và là thước đo bắt buộc phải vượt qua đối với bất kỳ mô hình AI nào.
* **Kết quả nhóm cần kiểm chứng:** Xác nhận lại chỉ số MAE của Median Baseline trên tập Spring XD (~1.7153) để làm ngưỡng chặn dưới (lower bound) cho các mô hình phức tạp.
* **🎯 Kỳ vọng đạt được nếu tái lập & mở rộng thành công:**
  * **Xếp hạng hội nghị / Tạp chí kỳ vọng:** 
    * **Hội thảo Quốc tế:** **ACM/IEEE ESEM (Empirical Software Engineering and Measurement - CORE Rank A)** hoặc **IEEE SANER (CORE Rank A)**.
    * **Tạp chí Quốc tế:** **Information and Software Technology (IST - Q1/Tier 2)** hoặc **Journal of Systems and Software (JSS - Q1/Tier 2)**.
  * **Giá trị đóng góp đề tài:** Thiết lập một bộ benchmark kiểm thử tiêu chuẩn, khách quan và đạt chuẩn mực khoa học cao cho toàn bộ các mô hình học máy mà Nhóm 3 thử nghiệm.

---

## 🛠️ 6. Khả năng tái lập: Công cụ, Thời gian & Dự kiến Khó / Dễ

| Tiêu chí | Chi tiết đánh giá |
| :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn 100% trực tuyến:** TAWOS v1.1 đã được công bố trên GitHub và Zenodo. |
| **Mã nguồn (Code)** | **Có sẵn 100% trực tuyến:** Repo GitHub `SOLAR-group/AgileEffortEstimation` có đầy đủ scripts sạch sẽ. |
| **Công cụ & Môi trường cần thiết** | • **Ngôn ngữ:** Python 3.9+<br>• **Thư viện AI/ML & Thống kê:** `scikit-learn`, `scipy`, `statsmodels`, `numpy`, `pandas`, `nltk`<br>• **Phần cứng:** CPU tiêu chuẩn (Core i5/Ryzen 5), RAM 8GB–16GB, không bắt buộc cần GPU. |
| **Thời gian tái lập dự kiến** | • **Chạy các Baseline Thống kê (Median, Mean, TF-IDF):** ~15 – 30 phút.<br>• **Chạy Kiểm định thống kê (Wilcoxon, A12):** ~1 giờ.<br>• **Tổng thời gian hoàn thiện & xuất bảng biểu:** **1 ngày làm việc**. |
| **Độ thuận lợi (Dễ)** | Mã nguồn cực kỳ sạch sẽ, tài liệu hướng dẫn (README) chi tiết, không gặp lỗi phụ thuộc GPU phức tạp. |
| **Thách thức (Khó)** | Đòi hỏi nắm vững lý thuyết thống kê phi tham số (Non-parametric testing) và chuẩn hóa dữ liệu chặt chẽ theo dòng thời gian. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
