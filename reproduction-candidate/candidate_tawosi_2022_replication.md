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

## 🔄 7. Quy trình Thực hiện Tái lập (End-to-End Workflow: Từ Input đến Output)

Quy trình tái lập thực nghiệm theo chuẩn mực của Tawosi et al. (2022) gồm 5 bước bài bản:

```
[Input: TAWOS / Choetkiertikul Issues Dataset]
                       │
                       ▼
[Bước 1: Lọc Dữ liệu Sạch & Chronological Split (60/20/20)]
                       │
                       ▼
[Bước 2: Xây dựng Đường cơ sở Thống kê (Mean, Median Baseline)]
                       │
                       ▼
[Bước 3: Huấn luyện Baseline Học máy (TF-IDF + SVM / Ridge)]
                       │
                       ▼
[Bước 4: Kiểm định Thống kê Nghiêm ngặt (Wilcoxon Test & Vargha-Delaney A12)]
                       │
                       ▼
[Output: Bảng Tổng hợp Hiệu năng & Kết luận Ý nghĩa Thống kê]
```

### 🔹 Bước 1: Tiếp nhận Input & Phân chia Dữ liệu Chuẩn
* **Đầu vào (Input):** Bảng dữ liệu issues từ CSDL TAWOS (gồm các trường: `issue_key`, `created`, `summary`, `description`, `storypoint`).
* **Thao tác thực hiện:**
  1. Loại bỏ các issues không có Story Point hoặc Story Point $\le 0$.
  2. Sắp xếp các issue theo thứ tự tăng dần của trường mốc thời gian tạo (`created`).
  3. Chia dữ liệu theo mốc thời gian: 60% Train / 20% Validation / 20% Test (cho từng dự án).
  4. **Quy tắc vàng chống Data Leakage:** Tuyệt đối không áp dụng kỹ thuật bóp outlier (ví dụ: gọt 90th percentile) lên toàn bộ dữ liệu trước khi chia, mà chỉ được tính toán ngưỡng trên tập Train.
* **Đầu ra bước 1:** Bộ dữ liệu Train, Validation, Test chuẩn hóa không bị rò rỉ dữ liệu.

### 🔹 Bước 2: Thiết lập Đường cơ sở Thống kê (Statistical Baselines)
* **Đầu vào:** Cột nhãn Story Point của tập Train $Y_{train}$.
* **Thao tác thực hiện:**
  1. **Median Baseline:** Tính trung vị của tập Train: $\hat{y}_{median} = \text{median}(Y_{train})$. Gán giá trị hằng số này làm dự đoán cho toàn bộ tập Test.
  2. **Mean Baseline:** Tính trung bình cộng của tập Train: $\hat{y}_{mean} = \text{mean}(Y_{train})$.
  3. **Random Guessing (RG):** Sinh số ngẫu nhiên đều trong khoảng $[ \min(Y_{train}), \max(Y_{train}) ]$.
* **Đầu ra bước 2:** Các mảng kết quả dự báo cơ sở $\hat{Y}_{median}, \hat{Y}_{mean}, \hat{Y}_{RG}$ trên tập Test.

### 🔹 Bước 3: Huấn luyện Mô hình Học máy Cổ điển (TF-IDF + SVM)
* **Đầu vào:** Văn bản `summary + description` và nhãn Story Point tập Train.
* **Thao tác thực hiện:**
  1. Trích xuất đặc trưng văn bản bằng **TF-IDF Vectorizer** (giới hạn số lượng từ vựng phổ biến `max_features = 1000` đến `5000`).
  2. Huấn luyện mô hình hồi quy Support Vector Machine (SVR với Linear Kernel hoặc RBF Kernel) hoặc Ridge Regression.
  3. Tối ưu siêu tham số ($C, \epsilon, \alpha$) trên tập Validation.
  4. Dự đoán Story Point trên tập Test.
* **Đầu ra bước 3:** Vector dự đoán $\hat{Y}_{SVM}$ trên tập Test.

### 🔹 Bước 4: Kiểm định Thống kê Phi tham số (Statistical Significance & Effect Size)
* **Đầu vào:** Các vector sai số tuyệt đối của từng mô hình trên tập Test: $E_{model} = [e_1, ..., e_N]$ và $E_{median} = [e'_1, ..., e'_N]$.
* **Thao tác thực hiện:**
  1. **Kiểm định Wilcoxon Signed-Rank Test:** Kiểm tra giả thuyết $H_0$ (sai số giữa mô hình và Median baseline không có sự khác biệt có ý nghĩa thống kê) với ngưỡng ý nghĩa $\alpha = 0.05$.
  2. **Đo kích thước hiệu ứng Vargha-Delaney $\hat{A}_{12}$:**
     * $\hat{A}_{12} > 0.5$: Mô hình tốt hơn Median baseline.
     * $\hat{A}_{12} = 0.5$: Không có sự khác biệt.
     * $\hat{A}_{12} < 0.5$: Mô hình kém hơn Median baseline.
* **Đầu ra bước 4:** Giá trị $p$-value và chỉ số $\hat{A}_{12}$ effect size định lượng chính xác.

### 🔹 Bước 5: Xuất Báo cáo Kết quả (Output)
* **Đầu ra cuối cùng (Final Output):**
  1. Bảng so sánh đa chỉ số: MAE, MdAE, SA của từng mô hình trên các dự án (Spring XD, Mule,...).
  2. Kết luận kiểm định thống kê: Xác định mô hình có thực sự đánh bại Median Baseline hay chỉ là biến thiên ngẫu nhiên.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
