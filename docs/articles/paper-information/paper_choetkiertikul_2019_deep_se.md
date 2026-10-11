# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** A Deep Learning Model for Estimating Story Points (Deep-SE)  
> **Nguồn công bố:** IEEE Transactions on Software Engineering (TSE), Vol. 45, No. 7, 2019

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | A Deep Learning Model for Estimating Story Points |
| **2**  | **Cite Key**             | `choetkiertikul2019deep` |
| **3**  | **Authors**              | Morakot Choetkiertikul, Hoa Khanh Dam, Truyen Tran, Trang Pham, Aditya Ghose, Tim Menzies |
| **4**  | **Year**                 | 2019 |
| **5**  | **Venue**                | IEEE Transactions on Software Engineering (TSE) |
| **6**  | **Files & media**        | [docs/articles/paper_deep-learning.pdf](docs/articles/paper_deep-learning.pdf) \| [DOI: 10.1109/TSE.2017.2787834](https://doi.org/10.1109/TSE.2017.2787834) |
| **7**  | **Venue Type**           | Journal |
| **8**  | **SJR Quartile**         | Q1 |
| **9**  | **CORE Rank**            | N/A (Journal) |
| **10** | **Rank**                 | Q1 (Top Journal in Software Engineering) |
| **11** | **Problem**              | Tự động hóa ước lượng Story Point cho các User Story trong quy trình Agile bằng cách khai thác thông tin ngữ nghĩa (Title + Description) và tương quan phụ thuộc giữa các issue thay vì dựa vào cảm tính chủ quan của con người. |
| **12** | **Dataset**              | 16 dự án mã nguồn mở từ 9 kho lưu trữ Jira công khai (tổng cộng 23.313 issues có gắn Story Point). |
| **13** | **Ground Truth**         | Giá trị Story Point (SP) số thực ghi nhận trong trường Story Point của Jira issue (Final Snapshot). |
| **14** | **Method**               | **Deep-SE**: Kiến trúc Deep Learning kết hợp nhúng từ Word2Vec + Recurrent Highway Network (RHWN) + Long Short-Term Memory (LSTM) + Dense Regressor. |
| **15** | **Baseline**             | Random Guessing (RG), Mean Effort, Median Effort, TF-IDF + Ridge Regression. |
| **16** | **Split**                | Random 10-Fold Cross-Validation và Chronological Split (60% Train / 20% Val / 20% Test theo mốc tạo issue). |
| **17** | **Metrics**              | MAE (Mean Absolute Error), MdAE (Median Absolute Error), SA (Standardized Accuracy). |
| **18** | **Main Result**          | Deep-SE đạt độ chính xác vượt trội so với các baseline truyền thống; chỉ số SA cải thiện đáng kể trên hầu hết 16 dự án, khẳng định tiềm năng của Deep Learning trong SE. |
| **19** | **Critical Notes**       | 1. **Temporal Leakage nghiêm trọng:** Dữ liệu trích xuất ở trạng thái issue đã đóng (Final Snapshot), nhìn thấy text đã sửa đổi sau planning.<br>2. **Bẫy tiền xử lý (Outlier Capping):** Cắt tỉa outlier ở phân vị 90% (90th percentile) trên toàn bộ dữ liệu trước khi phân chia tập train/test, gây sai số giảm nhân tạo. |
| **20** | **Takeaways**            | 1. Kế thừa nguyên lý biểu diễn ngữ nghĩa của User Story phục vụ bài toán hồi quy nỗ lực.<br>2. Tránh bẫy outlier capping trên tập kiểm thử.<br>3. Bắt buộc phải áp dụng quy trình kiểm soát rò rỉ dữ liệu theo thời gian (Temporal Leakage Control). |
| **21** | **Relevance to Topic**   | Đóng vai trò là mô hình nền tảng đối chứng (Baseline Model) kinh điển trong đề tài để đối chiếu hiệu năng giữa Final Snapshot và Planning-Time Snapshot. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Vấn đề thực tiễn:** Trong phương pháp luận Agile, việc ước lượng Story Point thường diễn ra trong các buổi họp Planning Poker bằng kinh nghiệm chuyên gia, dễ phát sinh sai lệch, thiếu nhất quán và tốn thời gian của đội ngũ phát triển.
- **Mục tiêu khoa học:** Tác giả đặt mục tiêu xây dựng một mô hình học sâu end-to-end có khả năng tự động học biểu diễn đặc trưng ngữ nghĩa từ tóm tắt (title) và mô tả (description) của User Story để dự báo nỗ lực phát triển phần mềm mà không cần kỹ nghệ đặc trưng thủ công (manual feature engineering).

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)
- **Nguồn dữ liệu:** Thu thập từ 16 dự án phần mềm nguồn mở lớn (Apache, Appcelerator, DuraSpace, Atlassian, v.v.) với 23.313 issues có gán điểm Story Point.
- **Đặc trưng đầu vào:** Kết hợp chuỗi văn bản gồm Title và Description của issue; bổ sung đồ thị liên kết phụ thuộc giữa các task.
- **Mốc thời gian lấy dữ liệu:** Toàn bộ dữ liệu được trích xuất tĩnh dạng **Final Snapshot** sau khi vòng đời của issue đã kết thúc.

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)
- **Kiến trúc mô hình:**
  - Lớp nhúng từ (Word Embedding): Sử dụng pre-trained Word2Vec để chuyển đổi từng token thành vector ngữ nghĩa.
  - Lớp trích xuất đặc trưng chuỗi: Mạng Recurrent Highway Network (RHWN) kết hợp LSTM cho phép truyền gradient qua nhiều tầng nơ-ron sâu mà không bị suy hao.
  - Lớp hồi quy (Regression Head): Fully Connected Layers tính toán giá trị Story Point dự báo dạng liên tục.
- **Hàm mất mát & Tối ưu:** Mean Squared Error (MSE) kết hợp thuật toán tối ưu hóa Adam.

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)
- **Hiệu năng:** Deep-SE vượt trội rõ rệt so với Random Guessing, Mean baseline và mô hình TF-IDF + Ridge Regression trên cả 16 dự án mã nguồn mở.
- **Kiểm định:** Sử dụng Standardized Accuracy (SA) để chứng minh mô hình hoạt động thực chất hơn phương pháp đoán ngẫu nhiên.

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)
- **Temporal / Future-Information Leakage:**
  - Bài báo hoàn toàn chưa kiểm soát hiện tượng lập trình viên cập nhật, chỉnh sửa Title/Description trong quá trình sửa lỗi (sau buổi họp Sprint Planning). Dữ liệu văn bản chứa thông tin nguyên nhân lỗi và giải pháp kỹ thuật cụ thể sinh ra trong tương lai.
  - Không phân biệt giữa thời điểm ước lượng (`SP_Estimation_Date`) và thời điểm hoàn thành issue.
- **Tính minh bạch & Khả năng tái lập:**
  - Quy trình xử lý ngoại lai (capping tại 90th percentile) thực hiện trước khi chia tập dữ liệu tạo ra rò rỉ phân phối (Data Leakage), khiến kết quả báo cáo khả quan hơn nhiều so với thực tế triển khai.

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)
- **Ý tưởng kế thừa:** Tham khảo cách thức ghép nối ngữ nghĩa từ Title và Description làm vector đầu vào.
- **Đóng góp của nhóm:** Sử dụng Deep-SE làm mô hình mốc so sánh (Baseline). Nhóm sẽ chạy Deep-SE trên 2 thiết lập độc lập: (1) Final Snapshot (như bài báo) và (2) Planning-Time Snapshot (sau khi dựng lại trạng thái lịch sử qua CHANGELOG) để đo lường định lượng mức độ suy giảm do loại bỏ Temporal Leakage.
