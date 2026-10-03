# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Enhancing Agile Story Point Estimation: Integrating Deep Learning, Machine Learning, and Natural Language Processing with SBERT and Gradient Boosted Trees (Applied Sciences 2024)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Yalçıner et al.** (*Appl. Sci. 2024*) | 2024 | Nâng cao độ chính xác ước lượng Story Point bằng cách kết hợp Sentence-BERT (SBERT) embeddings với Gradient Boosted Trees (GBT). | Dữ liệu từ các dự án mã nguồn mở Jira và các doanh nghiệp phát triển phần mềm. | Story Point thực tế của User Story. | **SBERT + GBT**: Trích xuất ngữ nghĩa đoạn văn bản bằng SBERT, kết hợp các đặc trưng bảng (tabular features) đưa vào mô hình LightGBM / XGBoost / CatBoost. | Deep-SE, TF-IDF + Ridge, Random Forest thuần túy. | Chronological Split và Train/Test Split. | MAE, MdAE, RMSE, $R^2$. | Sự kết hợp giữa Sentence Embeddings và Gradient Boosted Trees cho kết quả chính xác vượt trội hơn các mô hình chuỗi thời gian thuần túy (LSTM) trên nhiều tập dữ liệu. | Dữ liệu đầu vào vẫn sử dụng snapshot văn bản tĩnh thu thập sau khi issue đã hoàn thành (chưa kiểm soát Temporal Leakage). | Phương pháp trích xuất SBERT embeddings kết hợp GBT regressor là một baseline hiện đại mạnh mẽ để nhóm đưa vào thử nghiệm. | Là một trong các mô hình nâng cao (Advanced Model) được Nhóm 3 thử nghiệm và so sánh trên pipeline kiểm soát Temporal Leakage. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Enhancing Agile Story Point Estimation with SBERT and GBT

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** B. Yalçıner, K. Dinçer, A.G. Karaçor, M.Ö. Efe, *"Enhancing Agile Story Point Estimation: Integrating Deep Learning, Machine Learning, and Natural Language Processing with SBERT and Gradient Boosted Trees"*, Applied Sciences, 14(16), 7305, 2024.
* **Year:** 2024.
* **DOI:** [10.3390/app14167305](https://doi.org/10.3390/app14167305)

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
