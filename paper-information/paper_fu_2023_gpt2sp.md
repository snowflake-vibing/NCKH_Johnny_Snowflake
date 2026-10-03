# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** GPT2SP: A Transformer-Based Agile Story Point Estimation Approach (IEEE TSE 2023)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Fu & Tantithamthavorn** (*IEEE TSE*) | 2023 | Ước lượng Story Point tự động bằng Transformer (GPT-2 fine-tuning), khắc phục hạn chế không truyền giao (non-transferable) và độ chính xác thấp của Deep-SE. | 16 dự án từ Choetkiertikul dataset và 3 dự án Jira mở rộng (tổng số hàng chục nghìn issues). | Initial / Final Story Point ghi nhận trong Jira. | **GPT2SP**: Fine-tuning mô hình GPT-2 pre-trained với kiến trúc Regressor chuyển đổi output token representation sang giá trị Story Point. | Random Guessing, Mean Effort, Median Effort, Deep-SE, TF-IDF + Ridge. | Chronological Split (60% Train / 20% Val / 20% Test) theo thứ tự tạo issue. | MAE (Mean Absolute Error), MdAE, SA (Standardized Accuracy), Wilcoxon Signed-Rank Test. | GPT2SP đạt MAE trung vị ~0.96 trên dự án Spring XD, cải thiện khoảng 44.2% so với Median baseline trong báo cáo gốc của bài báo. | 1. Artifact notebook công khai của tác giả chỉ trích xuất `Title` (`max_length=20`) thay vì kết hợp `Title + Description` như mô tả.<br>2. Chạy lại (Replication) trên PyTorch/Transformers mới cho MAE = 1.73 (thấp hơn kỳ vọng).<br>3. Chưa kiểm soát Future-Information Leakage khi issue bị sửa đổi sau estimation. | 1. Kế thừa ý tưởng sử dụng LLM Representation (GPT-2, RoBERTa, SBERT) làm Feature Extractor.<br>2. Lưu ý bẫy khác biệt giữa mô tả bài báo và mã nguồn thực tế (Title vs Title+Description). | 1. Là đối chứng chính cho mô hình thử nghiệm tái lập trong Báo cáo NCKH Lần 2 của Nhóm 3.<br>2. Giúp nhóm chứng minh nguyên nhân Partial Reproduction và đề xuất pipeline chống leakage. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 GPT2SP: A Transformer-Based Agile Story Point Estimation Approach

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Michael Fu and Chakkrit Tantithamthavorn, *"GPT2SP: A Transformer-Based Agile Story Point Estimation Approach"*, IEEE Transactions on Software Engineering (TSE), 2023.
* **Year:** 2023.
* **DOI / Link:** [10.1109/TSE.2022.3158252](https://doi.org/10.1109/TSE.2022.3158252)

#### 2. Đặt bài toán & Mục tiêu nghiên cứu (Problem & Goal)
* **Problem:** Các mô hình học sâu trước đó như Deep-SE gặp khó khăn khi trích xuất ngữ nghĩa sâu từ User Story và không thể chuyển giao kiến thức (transfer learning).
* **Approach:** Áp dụng mô hình ngôn ngữ lớn pre-trained GPT-2 để fine-tuning cho bài toán regression dự báo Story Point.

#### 3. Dữ liệu & Phương pháp thực nghiệm (Dataset & Methodology)
* **Dataset:** 16 dự án từ Choetkiertikul dataset (Spring XD, Mule, Appcelerator, etc.).
* **Method:** Fine-tuning GPT-2 với pooling layer và Dense Regression head.
* **Split:** Chronological Split (60/20/20).

#### 4. Đóng góp & Kết quả Tái lập của Nhóm 3
* Nhóm 3 đã tái lập lại kết quả trên dự án **Spring XD** (3.526 issues). Kết quả chạy lại thực tế ghi nhận **Partial Reproduction** (MAE = 1.7330 so với 0.96 trong bài báo), tiền đề để Nhóm 3 đóng góp pipeline kiểm soát Temporal Leakage.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
