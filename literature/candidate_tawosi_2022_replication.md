# Literature Review: Tawosi et al. (2022)

- **Title:** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study
- **Cite Key:** Tawosi2022Agile
- **Authors:** Vali Tawosi, Rebecca Moussa, Federica Sarro
- **Year:** 2022
- **Venue:** IEEE Transactions on Software Engineering (TSE), Vol. 49, No. 4, pp. 2673-2691 (Preprint arXiv:2201.05401)
- **Venue Type:** Journal (CORE Rank A*, Q1 Scopus, CCF-A)
- **DOI:** https://doi.org/10.1109/TSE.2022.3204902
- **Problem:** Kiểm chứng lại tính đúng đắn và độ tin cậy của các tuyên bố nghiên cứu trước đây (đặc biệt là Deep-SE của Choetkiertikul et al., IEEE TSE 2019) cho rằng học sâu đã giải quyết tốt bài toán ước lượng Story Point. Đặt câu hỏi khoa học: Liệu sự tương đồng ngữ nghĩa thuần túy (semantic similarity) giữa các User Story có thực sự đủ để phân biệt và dự đoán chính xác độ phức tạp công việc hay không?
- **Dataset:** 3 bộ dữ liệu lớn với tổng cộng hơn 60.000 issues:
  1. Tập Choetkiertikul (16 dự án, 23.313 issues có Story Point).
  2. Tập Porru (8 dự án, 4.904 issues).
  3. Tập Tawosi mở rộng (26 dự án, 31.960 issues bổ sung).
- **Ground Truth:** Giá trị Story Point (SP) thực tế ghi nhận trong hệ thống Jira của từng dự án.
- **Method:** Tiến hành nghiên cứu tái lập nghiêm ngặt (Strict Replication) và mở rộng (Extension):
  1. Tái lập mô hình học sâu Deep-SE (Word2Vec + LSTM + Recurrent Highway Network + Dense Regressor).
  2. Xây dựng mô hình học máy truyền thống: TF-IDF + Support Vector Machine (SVM) / Ridge Regression.
  3. Xây dựng các đường cơ sở thống kê giản đơn (Median, Mean, Random Guessing) làm chuẩn đối chứng tối thiểu.
- **Baseline:** Random Guessing (RG), Mean Effort, Median Effort (đường cơ sở trung vị của tập Train).
- **Split:** Phân chia nghiêm ngặt theo thời gian (Chronological Split: 60% Train / 20% Val / 20% Test) cho thiết lập nội bộ dự án (Within-project) và Strict Chronological Split cho thiết lập liên dự án (Cross-project).
- **Metrics:** Mean Absolute Error (MAE), Median Absolute Error (MdAE), Standardized Accuracy (SA), kiểm định phi tham số Wilcoxon Signed-Rank Test ($\alpha = 0.05$ kèm hiệu chỉnh Bonferroni) và kích thước hiệu ứng Vargha-Delaney $\hat{A}_{12}$ Effect Size.
- **Main Result:**
  1. Mô hình học sâu Deep-SE **không vượt trội hơn Median baseline** ở 58% các dự án thử nghiệm (within-project).
  2. Trong kịch bản liên dự án (cross-project), Deep-SE bị Median baseline đánh bại hoàn toàn.
  3. Kỹ thuật tăng cường dữ liệu (Data Augmentation) làm giảm hiệu năng ở 67% các dự án.
  4. Quá trình tiền huấn luyện (Pre-training kéo dài ~47 giờ) không giúp cải thiện độ chính xác hay tốc độ hội tụ so với khởi tạo ngẫu nhiên.
- **Critical Notes:**
  1. *Phát hiện bẫy Data Leakage trong nghiên cứu cũ:* Nghiên cứu Choetkiertikul et al. (2019) đã áp dụng kỹ thuật bóp chặn outlier (capping 90th percentile) lên toàn bộ tập dữ liệu trước khi chia train/test, làm sai số MAE trên tập test bị giảm nhân tạo.
  2. *Nhiễu dữ liệu văn bản:* 19.11% issues chứa đoạn code, traceback lỗi, log rác làm sai lệch biểu diễn ngữ nghĩa của các mô hình NLP.
  3. *Hạn chế của Semantic Similarity:* Ngữ nghĩa văn bản giống nhau không đồng nghĩa với khối lượng công việc thực tế giống nhau.
- **Takeaways:**
  1. Bắt buộc phải sử dụng **Median Baseline** làm ngưỡng chặn dưới (lower bound) cho mọi mô hình AI trong bài toán Story Point.
  2. Tuyệt đối không tính toán thống kê (như chuẩn hóa, lọc outlier) trên Test set trước khi chia tập dữ liệu.
  3. Cần sử dụng kiểm định thống kê phi tham số (Wilcoxon Test và Vargha-Delaney $\hat{A}_{12}$) thay vì chỉ so sánh điểm MAE trung bình.
- **Relevance to Topic:**
  1. Cung cấp nền tảng phương pháp luận thực nghiệm chuẩn mực nhất (Replication Framework) cho đề tài NCKH của Nhóm 3.
  2. Cung cấp nguồn CSDL TAWOS v1.1 phục vụ toàn bộ các thử nghiệm phân tích EDA và huấn luyện mô hình của nhóm.
  3. Là cơ sở lý luận vững chắc giúp nhóm chứng minh rủi ro của Data Leakage và tầm quan trọng của việc kiểm soát rò rỉ thông tin tương lai.
