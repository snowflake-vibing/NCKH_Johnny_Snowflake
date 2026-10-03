# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** A Deep Learning Model for Estimating Story Points (IEEE TSE 2019 / Deep-SE)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Choetkiertikul et al.** (*IEEE TSE*) | 2019 | Tự động hóa ước lượng Story Point trong Agile bằng kiến trúc Deep Learning kết hợp phân tích văn bản và siêu dữ liệu issue. | 16 dự án mã nguồn mở từ 9 Jira Repositories (23.313 issues có Story Point). | Final Story Point trong Jira issue. | **Deep-SE**: Kết hợp Word2Vec Embeddings + LSTM + Recurrent Highway Network (RHWN) + Regressor. | Random Guessing, Mean Effort, Median Effort, TF-IDF + Ridge Regression. | Random 10-Fold Cross Validation và Chronological Split (60/20/20). | MAE, MdAE, SA. | Đưa ra mô hình SOTA đầu tiên áp dụng Deep Learning cho bài toán Agile effort estimation. | 1. Áp dụng Transformation capping (bóp nốt outlier ở 90th percentile) lên toàn bộ dataset trước khi split, gây sai số bị giảm nhân tạo.<br>2. Bị rò rỉ dữ liệu tương lai (Future-Information Leakage) do dùng dữ liệu sau khi issue đã closed. | 1. Hiểu rõ kiến trúc Deep-SE cổ điển làm baseline tham chiếu.<br>2. Nhận diện các bẫy Data Leakage trong thiết kế thực nghiệm ban đầu. | 1. Làm mô hình nền tảng đối chứng (Baseline) khi so sánh hiệu quả giữa Final Snapshot và Planning-Time Snapshot. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 A Deep Learning Model for Estimating Story Points (Deep-SE)

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Morakot Choetkiertikul, Hoa Khanh Dam, Truyen Tran, Trang Pham, Aditya Ghose, and Tim Menzies, *"A deep learning model for estimating story points"*, IEEE Transactions on Software Engineering (TSE), 2019.
* **Year:** 2019.

#### 2. Đặt bài toán & Phương pháp (Problem & Methodology)
* **Problem:** Ước lượng effort tự động cho các User Story trong Agile bằng mạng Nơ-ron sâu.
* **Architecture:** Word2Vec embedding biểu diễn văn bản Title + Description, đi qua lớp Recurrent Highway Network (RHWN) và lớp kết nối đầy đủ (Dense Regressor).

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
