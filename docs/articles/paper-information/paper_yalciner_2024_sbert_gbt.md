# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** Enhancing Agile Story Point Estimation: Integrating Deep Learning, Machine Learning, and Natural Language Processing with SBERT and Gradient Boosted Trees  
> **Nguồn công bố:** Applied Sciences (MDPI), Vol. 14, No. 16, 2024

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | Enhancing Agile Story Point Estimation: Integrating Deep Learning, Machine Learning, and Natural Language Processing with SBERT and Gradient Boosted Trees |
| **2**  | **Cite Key**             | `yalciner2024sbert` |
| **3**  | **Authors**              | Berkay Yalçıner, Kıvanç Dinçer, Ali Görkem Karaçor, Mehmet Önder Efe |
| **4**  | **Year**                 | 2024 |
| **5**  | **Venue**                | Applied Sciences (MDPI) |
| **6**  | **Files & media**        | [docs/articles/paper_SBERT&GPT.pdf](docs/articles/paper_SBERT&GPT.pdf) \| [DOI: 10.3390/app14167305](https://doi.org/10.3390/app14167305) |
| **7**  | **Venue Type**           | Journal |
| **8**  | **SJR Quartile**         | Q2 |
| **9**  | **CORE Rank**            | N/A (Journal) |
| **10** | **Rank**                 | Q2 (Applied Sciences / Computer Science Applications) |
| **11** | **Problem**              | Khắc phục tính chất hộp đen (black-box), khó giải thích và hiệu năng chưa ổn định của các mô hình Deep Learning tuần tự cổ điển bằng cách kết hợp Sentence-BERT (SBERT) với Gradient Boosted Trees (GBT), đồng thời kết hợp linh hoạt giữa văn bản và siêu dữ liệu dự án. |
| **12** | **Dataset**              | Dữ liệu tổng hợp từ các kho Jira mã nguồn mở (Apache, Spring, v.v.) và các dự án phát triển phần mềm doanh nghiệp thực tế. |
| **13** | **Ground Truth**         | Giá trị Story Point (SP) số thực ghi nhận trong Jira issue (Final Snapshot). |
| **14** | **Method**               | **SBERT + GBT**: Trích xuất nhúng ngữ nghĩa cấp câu bằng Sentence-BERT, kết hợp các đặc trưng phân loại/bảng (tabular issue metadata) và huấn luyện trên các mô hình cây tăng cường gradient (LightGBM, XGBoost, CatBoost). |
| **15** | **Baseline**             | Deep-SE (LSTM), TF-IDF + Ridge Regression, Random Forest thuần túy, Linear Regression. |
| **16** | **Split**                | Chronological Split và Train/Test Split (80% Train / 20% Test). |
| **17** | **Metrics**              | MAE (Mean Absolute Error), MdAE (Median Absolute Error), RMSE, $R^2$ Score, MAPE. |
| **18** | **Main Result**          | Mô hình SBERT + CatBoost/LightGBM vượt trội rõ rệt so với Deep-SE và các baseline truyền thống; giảm MAE đáng kể và cung cấp khả năng diễn giải tầm quan trọng đặc trưng (Feature Importance). |
| **19** | **Critical Notes**       | 1. **Chưa xử lý Temporal Leakage:** Dữ liệu văn bản và siêu dữ liệu vẫn được lấy ở trạng thái tĩnh sau khi đóng issue.<br>2. Cần cẩn trọng với các trường siêu dữ liệu động (Comments, Assignee, Resolution) có thể phát sinh sau mốc planning nếu không được chốt mốc thời gian nghiêm ngặt. |
| **20** | **Takeaways**            | 1. SBERT tạo ra vector ngữ nghĩa có độ kết dính ngữ cảnh cao hơn nhiều so với Word2Vec hoặc BERT thông thường.<br>2. Kiến trúc GBT kết hợp đặc trưng bảng và NLP mang lại độ ổn định cao và khả năng giải thích (XAI) tốt cho người dùng Agile. |
| **21** | **Relevance to Topic**   | Được Nhóm 3 lựa chọn làm mô hình nâng cao hiện đại (Advanced SOTA Model) để huấn luyện và so sánh trong quy trình kiểm soát Temporal Leakage của đề tài. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Vấn đề thực tiễn:** Các mô hình học sâu như Deep-SE hoặc Transformer thuần túy thường coi nhẹ các đặc trưng phi văn bản (như Issue Type, Priority, Component) và hoạt động như một "hộp đen" khiến các lập trình viên trong Sprint Planning khó tin tưởng vào kết quả dự báo.
- **Mục tiêu khoa học:** Xây dựng một phương pháp tiếp cận dung hòa giữa khả năng hiểu văn bản sâu sắc của NLP hiện đại và tính hiệu quả, minh bạch trong phân loại/hồi quy đặc trưng bảng của Gradient Boosted Trees.

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)
- **Nguồn dữ liệu:** Khai thác các bộ dữ liệu Jira công khai quy mô lớn, làm sạch các thẻ HTML, markdown và các ký tự đặc biệt.
- **Đặc trưng đầu vào:**
  - *Đặc trưng văn bản (Textual Features):* Title và Description được nhúng thành vector 384/768 chiều bằng SBERT (Sentence-BERT).
  - *Đặc trưng bảng (Tabular Features):* Issue Type, Priority, Reporter, Component được mã hóa (One-Hot Encoding hoặc Target Encoding).
- **Mốc thời gian lấy dữ liệu:** Trích xuất dạng tĩnh (Final Snapshot) sau khi issue đã hoàn tất.

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)
- **Trích xuất nhúng Sentence-BERT (SBERT):** Sử dụng mô hình siamese/triplet network đã được tinh chỉnh cho bài toán tương đồng câu (Semantic Textual Similarity - STS) để thu được vector biểu diễn cô đọng cho toàn bộ đoạn văn bản User Story.
- **Mô hình hồi quy Gradient Boosted Trees:**
  - Nối vector SBERT cùng các đặc trưng bảng thành một vector đặc trưng duy nhất.
  - Huấn luyện với các thuật toán GBT hàng đầu: LightGBM, XGBoost và CatBoost.
  - Tối ưu hóa siêu tham số bằng kỹ thuật Bayesian Optimization / Optuna.
- **Khả năng diễn giải mô hình (Explainability):** Sử dụng SHAP values và Gain Feature Importance để phân tích đặc trưng nào đóng góp lớn nhất vào quyết định chấm điểm Story Point.

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)
- **Hiệu năng vượt trội:** SBERT + GBT vượt qua Deep-SE với mức giảm sai số MAE khoảng 15-25% trên nhiều dự án kiểm thử.
- **Thời gian huấn luyện:** Nhanh hơn gấp hàng chục lần so với việc fine-tune toàn bộ mô hình ngôn ngữ lớn (như GPT2SP), đồng thời ít bị ảnh hưởng bởi vấn đề thiếu hụt dữ liệu huấn luyện.

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)
- **Nguy cơ Temporal Leakage tiềm ẩn:**
  - Giống như hầu hết các bài báo cùng thời kỳ, nghiên cứu sử dụng dữ liệu tĩnh sau khi issue đã đóng.
  - Đặc biệt khi kết hợp nhiều trường siêu dữ liệu (Metadata), nếu không có cơ chế lọc bỏ theo mốc `SP_Estimation_Date`, mô hình có thể vô tình học từ các trường được cập nhật muộn (như Component được sửa đổi khi dev nhận ra phạm vi ảnh hưởng của bug).

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)
- **Mô hình đại diện cho nhánh Hybrid:** Nhóm 3 kế thừa kiến trúc SBERT + GBT (cụ thể là Sentence-Transformers + LightGBM/CatBoost) làm mô hình thử nghiệm nâng cao trong Roadmap nghiên cứu.
- **Kiểm chứng tính bền vững:** Nhóm sẽ chứng minh liệu kiến trúc SBERT + GBT có giữ vững được độ chính xác khi đưa vào môi trường Planning-Time Snapshot (loại bỏ hoàn toàn rò rỉ dữ liệu) hay không.
