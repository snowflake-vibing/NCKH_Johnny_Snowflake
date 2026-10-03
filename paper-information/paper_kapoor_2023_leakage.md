# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Leakage and the Reproducibility Crisis in Machine-Learning-Based Science (Patterns, 2023 / Cell Press)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kapoor & Narayanan** (*Patterns / Cell Press*) | 2023 | Khủng hoảng khả năng tái lặp (Reproducibility crisis) trong nghiên cứu khoa học ứng dụng ML do hiện tượng Rò rỉ dữ liệu (Data Leakage); xây dựng taxonomy và bộ công cụ kiểm soát leakage pre-publication. | Meta-review 22 bài báo khảo sát từ 17 ngành khoa học (ảnh hưởng 294 bài báo); Case study 124 bài báo dự đoán nội chiến (12 bài full code/data, 4 bài công bố ML vượt trội). | Nhãn sự kiện theo từng lĩnh vực (Ví dụ: Khởi phát nội chiến Civil War Onset, Chẩn đoán y khoa, Đột biến gen...). | Mô hình thống kê cổ điển Logistic Regression (LR) vốn dùng để diễn giải (explanatory) chứ không tối ưu cho dự đoán. | Survey phân tích 17 ngành; Xây dựng Taxonomy 8 loại Leakage; Đề xuất Model Info Sheets (21 câu hỏi); Re-analysis thực nghiệm sửa lỗi leakage trên Civil War Prediction. | Strict Temporal split hoặc Block CV; loại bỏ hoàn toàn leakage trong pre-processing/feature selection. | AUC (Area Under ROC), Accuracy, Z-test so sánh ROC, Bootstrap 95% Confidence Interval. | Data Leakage ảnh hưởng 294 bài báo ở 17 lĩnh vực; Khi sửa hết lỗi Leakage ở case study dự đoán nội chiến, các mô hình ML phức tạp (Random Forest, AdaBoost) **KHÔNG CÒN VƯỢT TRỘI HƠN** mô hình Logistic Regression cổ điển (AUC chênh lệch từ 0.14 giảm về 0.01). | 1. Taxonomy 8 loại Data Leakage thuộc 3 nhóm L1, L2, L3.<br>2. 9/12 bài báo không thực hiện kiểm định thống kê hay tính khoảng tin cậy.<br>3. Bẫy Hype và Publication bias ủng hộ các kết quả lạc quan giả tạo. | 1. Sử dụng **Taxonomy 8 loại Leakage** để tự rà soát pipeline.<br>2. Điền **Model Info Sheets (21 câu hỏi)** kiểm tra trước khi công bố.<br>3. Luôn chạy kiểm định thống kê Z-test/Bootstrap CI khi so sánh ML với Baseline.<br>4. Cảnh giác với kết quả nhảy vọt bất thường của ML phức tạp. | 1. Cung cấp luận cứ khoa học cao nhất (Patterns - Cell Press) khẳng định tính nguy hại của Data Leakage.<br>2. Là cơ sở để nhóm xây dựng thiết kế thực nghiệm sạch (không rò rỉ dữ liệu) để bảo vệ trước các hội đồng NCKH khắt khe.<br>3. Trích dẫn taxonomy leakage cho phần phương pháp luận. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Leakage and the Reproducibility Crisis in Machine-Learning-Based Science

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Sayash Kapoor and Arvind Narayanan, *"Leakage and the reproducibility crisis in machine-learning-based science"*, Patterns, Volume 4, Issue 9, 100804, Cell Press, September 8, 2023.
* **Year:** 2023.
* **DOI:** [10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804)

#### 2. Đóng góp Cốt lõi & Taxonomy 8 loại Data Leakage
1. **[L1] Lack of clean separation between train and test sets:** `L1.1` No test set, `L1.2` Pre-processing on whole dataset, `L1.3` Feature selection on whole dataset, `L1.4` Duplicates.
2. **[L2] Illegitimate Features:** Dùng biến đại diện (proxy) của mục tiêu.
3. **[L3] Test set not drawn from target distribution:** `L3.1` Temporal Leakage, `L3.2` Non-independence, `L3.3` Selection Bias.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
