# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** GPT2SP: A Transformer-Based Agile Story Point Estimation Approach  
> **Nguồn công bố:** IEEE Transactions on Software Engineering (TSE), Vol. 49, No. 2, 2023

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | GPT2SP: A Transformer-Based Agile Story Point Estimation Approach |
| **2**  | **Cite Key**             | `fu2023gpt2sp` |
| **3**  | **Authors**              | Michael Fu, Chakkrit Tantithamthavorn |
| **4**  | **Year**                 | 2023 |
| **5**  | **Venue**                | IEEE Transactions on Software Engineering (TSE) |
| **6**  | **Files & media**        | [docs/articles/paper_gpt2sp.pdf](docs/articles/paper_gpt2sp.pdf) \| [DOI: 10.1109/TSE.2022.3158252](https://doi.org/10.1109/TSE.2022.3158252) |
| **7**  | **Venue Type**           | Journal |
| **8**  | **SJR Quartile**         | Q1 |
| **9**  | **CORE Rank**            | N/A (Journal) |
| **10** | **Rank**                 | Q1 (Top Journal in Software Engineering) |
| **11** | **Problem**              | Giải quyết hạn chế không thể chuyển giao tri thức (non-transferable), phụ thuộc từ vựng đóng và hiệu năng thấp của các mô hình Deep Learning trước đó (Deep-SE) bằng mô hình ngôn ngữ lớn tiền huấn luyện (Pre-trained LLM). |
| **12** | **Dataset**              | 16 dự án từ tập dữ liệu Choetkiertikul và 3 dự án Jira công khai mở rộng (trong đó Spring XD có 3.526 issues). |
| **13** | **Ground Truth**         | Giá trị Story Point (SP) số thực ghi nhận trong Jira issue (Final Snapshot). |
| **14** | **Method**               | **GPT2SP**: Tinh chỉnh (fine-tuning) mô hình Transformer tiền huấn luyện GPT-2 kết hợp lớp Last Token Pooling và Dense Regressor. |
| **15** | **Baseline**             | Random Guessing (RG), Mean Effort, Median Effort, Deep-SE, TF-IDF + Ridge Regression. |
| **16** | **Split**                | Chronological Split (60% Train / 20% Val / 20% Test theo thứ tự thời gian tạo issue). |
| **17** | **Metrics**              | MAE (Mean Absolute Error), MdAE (Median Absolute Error), SA (Standardized Accuracy), Wilcoxon Signed-Rank Test, Cliff's Delta. |
| **18** | **Main Result**          | Báo cáo MAE trung vị đạt 0.96 trên dự án Spring XD, cải thiện khoảng 44.2% so với Median baseline (1.72); vượt trội hơn hẳn Deep-SE. |
| **19** | **Critical Notes**       | 1. **Sai lệch mã nguồn & bài báo:** Bài báo mô tả dùng `Title + Description`, nhưng notebook công khai của tác giả chỉ chạy trên riêng `Title` (`max_length=20`).<br>2. **Tái lập một phần (Partial Reproduction):** Nhóm 3 chạy lại checkpoint công khai chỉ đạt MAE = 1.7330 (kém hơn Median baseline 1.7153).<br>3. **Chưa xử lý Temporal Leakage:** Dữ liệu text vẫn lấy sau khi issue đóng. |
| **20** | **Takeaways**            | 1. Kế thừa kiến trúc Fine-tuning Pre-trained Transformers cho bài toán ước lượng phần mềm.<br>2. Cần cẩn trọng kiểm chứng đối chiếu artifact công khai với tài liệu mô tả.<br>3. Bắt buộc xây dựng đường ống dữ liệu tái dựng trạng thái tại thời điểm Planning. |
| **21** | **Relevance to Topic**   | Đối tượng tái lập thực nghiệm cốt lõi (Primary Reproduction Target) trong Báo cáo NCKH Lần 2 của Nhóm 3 và là mô hình so sánh trung tâm khi đánh giá tác động của Temporal Leakage. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Vấn đề thực tiễn:** Các kỹ thuật ước lượng nỗ lực truyền thống dựa vào Word2Vec hoặc Bag-of-Words (như Deep-SE) chỉ học được từ vựng cụ thể trong từng dự án riêng lẻ, không thể tận dụng vốn tri thức ngôn ngữ phong phú từ các kho mã nguồn khổng lồ.
- **Mục tiêu khoa học:** Khám phá khả năng của kiến trúc Transformer và mô hình sinh ngôn ngữ tự hồi quy (Autoregressive LLM - GPT-2) trong việc nắm bắt ngữ cảnh dài và ngữ nghĩa trừu tượng của User Story để dự báo điểm Story Point.

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)
- **Nguồn dữ liệu:** Kiểm thử trên tập dữ liệu chuẩn từ Choetkiertikul (16 dự án) kết hợp bổ sung các dự án Spring XD, Mule, Appcelerator.
- **Đặc trưng đầu vào:** Bài báo mô tả kết hợp Title và Description của issue được token hóa bằng Byte-Pair Encoding (BPE) của GPT-2.
- **Mốc thời gian lấy dữ liệu:** Mặc dù áp dụng phân chia tập train/val/test theo thời gian tạo issue (Chronological Split), nhưng nội dung văn bản lại được trích xuất ở thời điểm **Final Snapshot** sau khi công việc đã kết thúc.

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)
- **Kiến trúc mô hình:**
  - Khởi tạo từ trọng số pre-trained `gpt2` (124M tham số).
  - Trích xuất trạng thái ẩn của token cuối cùng (Last Token Hidden State) làm vector đại diện ngữ nghĩa cho toàn bộ văn bản issue.
  - Bổ sung một Linear Regression Head chuyển đổi vector trạng thái thành một giá trị điểm Story Point liên tục.
- **Quá trình huấn luyện:** Tối ưu hóa hàm mất mát MAE Loss với learning rate nhỏ để fine-tune toàn bộ trọng số của Transformer.

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)
- **Kết quả công bố trong bài báo:** Trên dự án Spring XD (3.526 issues), GPT2SP đạt MAE = 0.96, vượt trội hoàn toàn so với Median baseline (MAE = 1.72) và Deep-SE (MAE = 2.13).
- **Kết quả tái lập của Nhóm 3 (Artifact Reproduction):**
  - Số dòng dữ liệu: 3.526 issues (khớp 100%).
  - Tỉ lệ phân chia 60/20/20: 2.115 train / 705 val / 706 test (khớp 100%).
  - Median baseline MAE: 1.7153 (khớp với 1.72 sau làm tròn).
  - GPT2SP Checkpoint công khai: Đạt MAE = 1.7330 (không khớp với công bố 0.96 và kém hơn Median baseline 1.03%).

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)
- **Nguy cơ rò rỉ dữ liệu tương lai (Temporal Leakage):**
  - Khoảng 19% số issues trong thực tế bị chỉnh sửa nội dung văn bản sau ngày họp ước lượng. GPT2SP học trên dữ liệu Final Snapshot nên có nguy cơ nhìn thấy trước các giải pháp kỹ thuật sinh ra sau buổi họp planning.
- **Sai lệch giữa văn bản và Artifact:**
  - File notebook thực tế `0-GPT2SP.ipynb` do tác giả cung cấp chỉ nạp trường `Title` và giới hạn cứng `max_length=20`, mâu thuẫn trực tiếp với phần mô tả phương pháp trong bài báo (khẳng định dùng cả Title và Description).

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)
- **Bài học kinh nghiệm:** Minh chứng rõ ràng rằng việc công bố kết quả học máy trong SE cần phải đi kèm với quy trình kiểm chứng nghiêm ngặt và tái lập độc lập.
- **Ứng dụng cho đề tài:** Nhóm 3 sử dụng GPT2SP làm mô hình mục tiêu chính để đánh giá: Liệu sự vượt trội của Transformer có còn được duy trì khi chúng ta tái dựng lại trạng thái trung thực tại `SP_Estimation_Date` (Planning-Time Snapshot) hay không?
