# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Enhancing Story Point Estimation in Software Projects Using Transformer-Based Embeddings and Ensemble Regression Models (2024)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Wijaya et al.** (*BINUS Univ*) | 2024 | Cải thiện độ chính xác ước lượng Story Point bằng cách trích xuất ngữ nghĩa từ văn bản bằng Transformer Embeddings kết hợp các thuật toán Ensemble Regression. | Dữ liệu Jira công khai từ tập TAWOS/Choetkiertikul. | Story Point ghi nhận trong Jira issue. | **TBE + ERM**: Trích xuất nhúng biểu diễn văn bản bằng RoBERTa/BERT, sau đó đưa vào các mô hình học kết hợp (Ensemble Regressors: Random Forest, Extra Trees, Gradient Boosting). | Linear Regression, Single Tree Regressors. | Train/Test Split theo tỉ lệ cố định. | MAE, MdAE, $R^2$. | Việc kết hợp Transformer Embeddings với Ensemble Regression mang lại sai số nhỏ hơn hẳn so với các mô hình hồi quy tuyến tính cổ điển. | Nghiên cứu chủ yếu tập trung trên dữ liệu tĩnh và chưa tính đến các yếu tố thay đổi thông tin theo thời gian (Temporal Leakage). | Kỹ thuật trích xuất ngữ nghĩa bằng Transformer + Ensemble Regressor để so sánh trên 2 bối cảnh Final vs Planning-time. | Làm tài liệu tham khảo cho các kiến trúc mô hình thử nghiệm mở rộng của nhóm. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Enhancing Story Point Estimation Using Transformer-Based Embeddings and Ensemble Regression Models

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Darren Cornelius Citra Wijaya, Auryn Larissa Sabrina, Meiliana, *"Enhancing Story Point Estimation in Software Projects Using Transformer-Based Embeddings and Ensemble Regression Models"*, Bina Nusantara University, 2024.
* **Year:** 2024.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
