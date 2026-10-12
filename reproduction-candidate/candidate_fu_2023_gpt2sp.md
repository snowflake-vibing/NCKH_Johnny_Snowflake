# BÁO CÁO TÁI LẬP (REPRODUCTION CANDIDATE) — GPT2SP
> **Paper:** GPT2SP: A Transformer-Based Agile Story Point Estimation Approach (IEEE TSE 2023)

---

## 📌 1. Phải xác định chính xác cái gì của paper để tái lập?
* **Mục tiêu tái lập:** Tái lập thực nghiệm mô hình học sâu **GPT2SP** (kiến trúc tiền huấn luyện GPT-2 kết hợp Regressor) trên dự án mã nguồn mở **Spring XD** nhằm kiểm chứng độ chính xác ước lượng Story Point và đối chiếu sai lệch thực tế so với bài báo gốc.
* **Câu hỏi nghiên cứu kiểm chứng:** Liệu việc fine-tune GPT-2 trên text tĩnh của issue có đạt được kết quả như công bố khi chạy trong môi trường PyTorch/Transformers hiện đại, và mô hình có bị ảnh hưởng bởi hiện tượng rò rỉ thông tin tương lai (Future-Information Leakage) hay không?

---

## 📑 2. Thông tin bài báo & Tác giả (Paper & Metadata)
* **Tên bài báo:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach*
* **Tác giả:** Michael Fu and Chakkrit Tantithamthavorn
* **Nơi xuất bản:** *IEEE Transactions on Software Engineering (TSE)*, Vol. 49, No. 4, 2023
* **DOI:** [10.1109/TSE.2022.3158252](https://doi.org/10.1109/TSE.2022.3158252)
* **Xếp hạng học thuật (Tier):** **Tier 1 (A*)** — Tạp chí đầu ngành Software Engineering (Q1 Scopus, CCF-A).
* **Điểm đánh giá tái lập:** **98 / 100 điểm** (Ưu tiên số 1).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Uy tín & Tiên phong:** Là công trình tiên phong chuyển dịch bài toán Agile Story Point từ mạng học sâu truyền thống (Deep-SE) sang kiến trúc **Pre-trained Transformer/LLM (GPT-2)**, đăng trên tạp chí uy tín nhất ngành (IEEE TSE).
2. **Khả năng tiếp cận Artifacts:** Tác giả công bố checkpoint mô hình và notebook mẫu trên HuggingFace (`MickyMike/0-GPT2SP-springxd`), giúp việc tải và kiểm chứng có cơ sở thực tế vững chắc.
3. **Mối liên hệ sống còn với đề tài Nhóm 3:**
   * GPT2SP huấn luyện trên snapshot tĩnh sau khi task hoàn thành (Final Snapshot), không kiểm soát rò rỉ thời gian.
   * Tái lập GPT2SP là cơ sở đối chứng cốt lõi (**Core Baseline**) để nhóm chứng minh luận điểm: *"Khi loại bỏ rò rỉ thông tin tương lai, hiệu năng thực tế của các mô hình LLM tại thời điểm Sprint Planning sẽ thay đổi như thế nào?"*.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset:** 
  * Dự án mã nguồn mở **Spring XD** (thuộc tập Choetkiertikul / TAWOS).
  * Quy mô: **3.526 issues**.
* **Target / Ground Truth:** 
  * Giá trị Story Point (SP) thực tế ghi nhận trong hệ thống Jira của Spring XD.
* **Baseline / Model:**
  * **Model tái lập chính:** **GPT2SP** (GPT-2 pre-trained + Token Representation Pooling + Linear Regression Head).
  * **Baselines đối chứng:** Median Effort, Mean Effort, Random Guessing, TF-IDF + Ridge Regression.
* **Data Split:**
  * **Chronological Split** (chia theo trục thời gian tạo issue theo tỷ lệ 60/20/20):
    * **Train set:** 2.115 issues (60%)
    * **Validation set:** 705 issues (20%)
    * **Test set:** 706 issues (20%)
* **Metrics đánh giá:**
  * **MAE** (Mean Absolute Error): Thước đo sai số tuyệt đối trung bình.
  * **MdAE** (Median Absolute Error): Sai số tuyệt đối trung vị (giảm độ nhạy với outlier).
  * **SA** (Standardized Accuracy): Tỷ lệ cải thiện độ chính xác chuẩn hóa so với đoán ngẫu nhiên.

---

## 📊 5. Kết quả cụ thể muốn tái lập (Targeted Results)
* **Phạm vi tái lập:** Tập trung tái lập sâu trên dự án **Spring XD** (dự án lớn nhất và có sẵn checkpoint công khai của tác giả).
* **Kết quả trong bài báo công bố:**
  * MAE công bố: **~0.96** (cải thiện ~44.2% so với Median Baseline là 1.72).
* **Kết quả Partial Reproduction thực tế của Nhóm 3:**
  * MAE đạt được: **1.7330**
  * MdAE đạt được: **1.2994**
  * Median Baseline: **1.7153**
* **Nguyên nhân phát hiện sai lệch khoa học (Scientific Discrepancy):**
  1. *Khác biệt đầu vào:* Bài báo mô tả kết hợp cả `Title + Description`, nhưng artifact/code thực tế của tác giả chỉ chạy riêng trên `Title` với `max_length = 20`.
  2. *Môi trường thư viện:* Thay đổi phiên bản Transformers và PyTorch ảnh hưởng đến pooling/padding representation.

---

## 🛠️ 6. Khả năng tái lập: Code / Data & Dự kiến Khó / Dễ

| Tiêu chí | Hiện trạng | Đánh giá & Giải pháp |
| :--- | :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn** | Có sẵn trong CSDL TAWOS v1.1 local và bộ dữ liệu Choetkiertikul. |
| **Mã nguồn (Code)** | **Có sẵn** | Checkpoint HuggingFace `MickyMike/0-GPT2SP-springxd` và notebook Google Colab. |
| **Điểm thuận lợi (Dễ)** | Thực thi linh hoạt | Chạy tốt trên Google Colab GPU (Tesla T4) với chi phí tài nguyên tính toán vừa phải. |
| **Điểm khó khăn (Khó)** | Lệch phiên bản & Rò rỉ | Cần xử lý tương thích giữa các phiên bản thư viện; phát hiện và phân tích bản chất rò rỉ dữ liệu (Future-Information Leakage) trong tập test. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
