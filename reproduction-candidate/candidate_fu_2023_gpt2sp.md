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
* **Xếp hạng học thuật (Tier):** **Tier 1 (A*)** — Tạp chí đầu ngành Software Engineering thế giới (Q1 Scopus, CCF-A, H-index 180+).
* **Điểm đánh giá tái lập:** **98 / 100 điểm** (Ứng viên ưu tiên số 1).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Uy tín & Tiên phong:** Là công trình tiên phong chuyển dịch bài toán Agile Story Point từ mạng học sâu truyền thống (Deep-SE) sang kiến trúc **Pre-trained Transformer/LLM (GPT-2)**, đăng trên tạp chí uy tín nhất ngành (IEEE TSE).
2. **Khả năng tiếp cận Artifacts & Mã nguồn:** Tác giả công bố đầy đủ mã nguồn và checkpoint trên GitHub & HuggingFace, giúp việc kiểm chứng có cơ sở thực tế vững chắc.
3. **Mối liên hệ sống còn với đề tài Nhóm 3:**
   * GPT2SP huấn luyện trên snapshot tĩnh sau khi task hoàn thành (Final Snapshot), không kiểm soát rò rỉ thời gian.
   * Tái lập GPT2SP là cơ sở đối chứng cốt lõi (**Core Baseline**) để nhóm chứng minh luận điểm: *"Khi loại bỏ rò rỉ thông tin tương lai, hiệu năng thực tế của các mô hình LLM tại thời điểm Sprint Planning sẽ suy giảm đáng kể như thế nào?"*.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset & Đường dẫn dữ liệu (Data Links):** 
  * Dự án mã nguồn mở **Spring XD** (thuộc tập Choetkiertikul / TAWOS). Quy mô: **3.526 issues**.
  * **Link Dataset Repository:** [morakotch/datasets (GitHub)](https://github.com/morakotch/datasets) | [SOLAR-group/TAWOS (GitHub)](https://github.com/SOLAR-group/TAWOS)
  * **Link HuggingFace Mirror:** [giseldo/deep-se (HuggingFace Datasets)](https://huggingface.co/datasets/giseldo/deep-se)
* **Mã nguồn & Checkpoints (Code & Model Links):**
  * **GitHub Replication Package:** [awsm-research/gpt2sp (GitHub)](https://github.com/awsm-research/gpt2sp)
  * **HuggingFace Checkpoint Model:** [MickyMike/0-GPT2SP-springxd (HuggingFace Hub)](https://huggingface.co/MickyMike/0-GPT2SP-springxd)
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

## 📊 5. Kết quả cụ thể muốn tái lập & Kỳ vọng khoa học (Targeted Results & Expectations)
* **Phạm vi tái lập cụ thể:** Tái lập sâu trên dự án **Spring XD** (3.526 issues) với checkpoint có sẵn của tác giả.
* **Kết quả trong bài báo công bố:**
  * MAE công bố: **~0.96** (cải thiện ~44.2% so với Median Baseline là 1.72).
* **Kết quả Partial Reproduction thực tế của Nhóm 3:**
  * MAE đạt được: **1.7330** | MdAE: **1.2994** | Median Baseline: **1.7153**
* **Nguyên nhân sai lệch khoa học phát hiện được:**
  1. *Khác biệt Input:* Bài báo mô tả kết hợp cả `Title + Description`, nhưng artifact/code thực tế của tác giả chỉ chạy riêng trên `Title` với `max_length = 20`.
  2. *Môi trường thư viện:* Thay đổi phiên bản Transformers và PyTorch ảnh hưởng đến pooling/padding representation.
* **🎯 Kỳ vọng đạt được nếu tái lập & mở rộng thành công:**
  * **Xếp hạng hội nghị / Tạp chí kỳ vọng:** Báo cáo xuất sắc tại Hội nghị Sinh viên Nghiên cứu Khoa học cấp Trường (UIT); hướng đến công bố tại các hội thảo/tạp chí chuyên ngành uy tín:
    * **Hội thảo Quốc tế:** **IEEE/ACM MSR (Mining Software Repositories - CORE Rank A)** hoặc **IEEE SANER (CORE Rank A)** (nhánh Registered Reports / Replication Track).
    * **Tạp chí Quốc tế:** **Empirical Software Engineering (EMSE - Q1/Tier 2)** hoặc **Journal of Systems and Software (JSS - Q1/Tier 2)**.
  * **Giá trị đóng góp đề tài:** Cung cấp bằng chứng thực nghiệm vững chắc chứng minh hiện tượng **Overoptimistic Performance** trong các nghiên cứu LLM ước lượng Story Point trước đây do rò rỉ dữ liệu (Data/Temporal Leakage).

---

## 🛠️ 6. Khả năng tái lập: Công cụ, Thời gian & Dự kiến Khó / Dễ

| Tiêu chí | Chi tiết đánh giá |
| :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn trực tuyến:** Đã có link GitHub/HuggingFace và tích hợp sẵn trong CSDL TAWOS local. |
| **Mã nguồn (Code)** | **Có sẵn trực tuyến:** Đã có repo `awsm-research/gpt2sp` và checkpoint trên Hugging Face. |
| **Công cụ & Môi trường cần thiết** | • **Ngôn ngữ:** Python 3.9+<br>• **Thư viện AI/ML:** PyTorch (>=2.0), HuggingFace `transformers` (v4.39.3), `datasets`, `accelerate`, `scikit-learn`, `pandas`<br>• **Phần cứng:** Google Colab GPU (Nvidia Tesla T4 16GB VRAM) hoặc GPU cục bộ RTX 3060 trở lên. |
| **Thời gian tái lập dự kiến** | • **Chạy Inference từ Checkpoint:** ~0.5 – 1 giờ.<br>• **Fine-tuning lại từ đầu trên Spring XD:** ~3 – 5 giờ GPU.<br>• **Tổng thời gian hoàn thiện & phân tích sai số:** **1 – 2 ngày làm việc**. |
| **Độ thuận lợi (Dễ)** | Đã có sẵn checkpoint lưu trữ công khai, kiến trúc HuggingFace chuẩn hóa cao, dễ debug. |
| **Thách thức (Khó)** | Xử lý chênh lệch phiên bản thư viện; tái dựng pipeline cắt ngắn token (`max_length=20` vs full text) để giải thích sai lệch. |

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
