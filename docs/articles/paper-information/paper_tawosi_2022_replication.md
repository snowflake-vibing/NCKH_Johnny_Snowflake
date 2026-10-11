# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study  
> **Nguồn công bố:** IEEE Transactions on Software Engineering (TSE), Vol. 49, No. 4, 2022

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study |
| **2**  | **Cite Key**             | `tawosi2022agile` |
| **3**  | **Authors**              | Vali Tawosi, Rebecca Moussa, Federica Sarro |
| **4**  | **Year**                 | 2022 |
| **5**  | **Venue**                | IEEE Transactions on Software Engineering (TSE) |
| **6**  | **Files & media**        | [docs/articles/2201.05401v2.pdf](docs/articles/2201.05401v2.pdf) \| [DOI: 10.1109/TSE.2022.3204902](https://doi.org/10.1109/TSE.2022.3204902) |
| **7**  | **Venue Type**           | Journal |
| **8**  | **SJR Quartile**         | Q1 |
| **9**  | **CORE Rank**            | N/A (Journal) |
| **10** | **Rank**                 | Q1 (Top Journal in Software Engineering) |
| **11** | **Problem**              | Tái lập và thẩm định độc lập (Close Replication & Extension) mô hình Deep-SE để trả lời câu hỏi cốt lõi: Liệu sự tương đồng ngữ nghĩa (Semantic Similarity) giữa các User Story có thực sự đủ để dự báo Story Point, hay độ chính xác cao trước đây chỉ là ảo ảnh do bẫy thiết kế thực nghiệm? |
| **12** | **Dataset**              | 3 bộ dữ liệu: Choetkiertikul (16 dự án, 23.313 issues), Porru (8 dự án, 4.904 issues), và tập mở rộng TAWOS (26 dự án, 31.960 issues). |
| **13** | **Ground Truth**         | Giá trị Story Point (SP) số thực ghi nhận trong Jira issue (Final Snapshot). |
| **14** | **Method**               | Nghiên cứu tái lập & mở rộng: Đánh giá lại Deep-SE (Word2Vec + LSTM + RHWN), so sánh với TF-IDF + SVM, thử nghiệm Data Augmentation và Cross-project learning. |
| **15** | **Baseline**             | Random Guessing (RG), Mean Effort, Median Effort Baseline. |
| **16** | **Split**                | Chronological Split (60% Train / 20% Val / 20% Test theo mốc tạo issue) cho within-project và Strict Chronological Split cho cross-project. |
| **17** | **Metrics**              | MAE (chính), MdAE, SA (Standardized Accuracy), Wilcoxon Rank-Sum Test (Bonferroni correction), Vargha-Delaney $\hat{A}_{12}$ Effect Size. |
| **18** | **Main Result**          | Deep-SE **KHÔNG** vượt trội hơn Median baseline ở 58% số dự án; chỉ hơn TF-IDF + SVM ở 19% dự án; thất bại hoàn toàn ở Cross-project; Pre-training 47h không cải thiện độ chính xác. |
| **19** | **Critical Notes**       | 1. Chỉ ra bẫy **Outlier Capping** (cắt 90th percentile trước khi split) của nghiên cứu trước làm sai số giảm nhân tạo.<br>2. Phát hiện 19.11% issues chứa code/stack trace làm nhiễu NLP.<br>3. Semantic similarity không đồng nhất với Effort nỗ lực.<br>4. Vẫn sử dụng Final Snapshot, chưa xử lý triệt để việc sửa đổi issue sau planning. |
| **20** | **Takeaways**            | 1. Bắt buộc dùng Chronological Split và Median Baseline.<br>2. Tuyệt đối không can thiệp biến đổi/cắt tỉa trên tập test.<br>3. Cần làm sạch rác kỹ thuật (code/stack trace).<br>4. Cần bổ sung các đặc trưng nỗ lực ngoài văn bản thuần túy. |
| **21** | **Relevance to Topic**   | Cung cấp nguồn dữ liệu nền tảng (TAWOS Dataset v1.1), bộ khung kiểm định thống kê chuẩn mực và lập luận phản biện sắc bén chống lại các tuyên bố phóng đại về Deep Learning trong ước lượng phần mềm. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Vấn đề thực tiễn:** Sau khi Choetkiertikul et al. (2019) công bố mô hình Deep-SE với kết quả vượt trội, cộng đồng học thuật đặt ra câu hỏi lớn về tính tái lập và giá trị thực tế của việc áp dụng mạng nơ-ron sâu trong môi trường dự án Agile thực tiễn.
- **Mục tiêu khoa học:** Tác giả tiến hành một nghiên cứu tái lập quy mô lớn nhất từ trước đến nay để xác minh liệu Deep-SE có thực sự vượt qua các baseline đơn giản và có thể tổng quát hóa sang các dự án chưa từng thấy hay không.

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)
- **Nguồn dữ liệu:** Kiểm thử toàn diện trên 50 dự án nguồn mở thông qua 3 nguồn dữ liệu lớn, sau đó tổng hợp và phát triển thành tập dữ liệu chuẩn **TAWOS Dataset** (SOLAR Group - UCL).
- **Đặc trưng đầu vào:** Chuỗi văn bản Title + Description, giới hạn ở 100 token đầu tiên của mỗi issue.
- **Mốc thời gian lấy dữ liệu:** Áp dụng chặt chẽ mốc thời gian tạo issue (`Created Date`) để chia tập train/val/test theo trình tự thời gian, nhưng dữ liệu văn bản vẫn nằm ở trạng thái tĩnh khi issue đã đóng (Final Snapshot).

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)
- **Thiết lập tái lập:**
  - Cài đặt lại chính xác kiến trúc Deep-SE nguyên bản bằng Keras/TensorFlow.
  - Xây dựng mô hình máy học cổ điển đối chứng: TF-IDF kết hợp Support Vector Machine (SVM).
  - Đánh giá vai trò của Pre-training Embedding trên kho ngữ liệu khổng lồ (~47 giờ huấn luyện GPU).
  - Thử nghiệm kỹ thuật tăng cường dữ liệu văn bản (Data Augmentation bằng hoán đổi từ đồng nghĩa).

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)
- **Hiệu năng Within-Project:** Deep-SE chỉ đánh bại Median baseline ở 42% dự án (tức kém hơn Median ở 58% dự án còn lại). Sự khác biệt có ý nghĩa thống kê với kích thước ảnh hưởng ($\hat{A}_{12}$) là rất khiêm tốn.
- **Hiệu năng Cross-Project:** Cả Deep-SE và TF-IDF-SVM đều không thể dự đoán tốt hơn phương pháp đoán ngẫu nhiên khi áp dụng chéo giữa các dự án.
- **Pre-training & Augmentation:** Không mang lại lợi ích rõ rệt, thậm chí làm suy giảm độ chính xác ở 67% dự án.

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)
- **Bóc trần hiện tượng Data Leakage trong nghiên cứu cũ:**
  - Bài báo vạch trần việc Choetkiertikul et al. cắt bỏ ngoại lai ở ngưỡng 90th percentile trên toàn bộ dataset trước khi chia split, vô tình để lộ phân phối của tập test vào quá trình chuẩn bị dữ liệu. Khi loại bỏ thao tác này, hiệu năng của Deep-SE giảm mạnh.
- **Hạn chế còn tồn đọng về Temporal Leakage:**
  - Mặc dù Tawosi et al. rất cẩn trọng trong việc chia tập dữ liệu theo thời gian, họ vẫn chưa truy xuất ngược lịch sử `CHANGELOG` để lấy đúng văn bản tại thời điểm `SP_Estimation_Date`. Đây chính là khoảng trống nghiên cứu (Research Gap) mà đề tài của Nhóm 3 tập trung giải quyết.

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)
- **Kế thừa thiết kế thực nghiệm:** Nhóm 3 sử dụng tập dữ liệu **TAWOS v1.1**, tuân thủ nghiêm ngặt nguyên tắc Chronological Split, lấy Median Effort làm baseline chuẩn, và sử dụng cặp kiểm định Wilcoxon + Vargha-Delaney $\hat{A}_{12}$ cho mọi đánh giá.
- **Đóng góp phát triển:** Điểm mới của Nhóm 3 so với Tawosi (2022) là giải quyết triệt để vấn đề rò rỉ thông tin tương lai trong nội dung văn bản (Future-Information / Temporal Leakage) bằng cách phục hồi trạng thái issue tại buổi họp Sprint Planning.
