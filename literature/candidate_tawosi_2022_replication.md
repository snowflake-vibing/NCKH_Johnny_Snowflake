# 📑 Literature Review: Tawosi et al. (2022)

> **Tổng quan nhanh:** Công trình nghiên cứu tái lập (Replication Study) mẫu mực và quy mô lớn nhất trong ngành Kỹ nghệ phần mềm về ước lượng Story Point. Tác giả cũng chính là nhóm xây dựng bộ CSDL TAWOS mà đề tài đang sử dụng.

---

- 📌 **Title (Tiêu đề):** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study
- 🔑 **Cite Key (Khóa trích dẫn BibTeX):** `Tawosi2022Agile`
- 👥 **Authors (Tác giả):** Vali Tawosi, Rebecca Moussa, và Federica Sarro (SOLAR Research Group, University College London - UCL, Vương Quốc Anh)
- 📅 **Year (Năm xuất bản):** 2022 (Công bố chính thức trên TSE 2022, bản thảo hoàn thiện 12/2022)
- 🏛️ **Venue (Nơi công bố):** IEEE Transactions on Software Engineering (TSE), Volume 49, Issue 4, Trang 2673–2691
- 🏷️ **Venue Type (Loại hình công bố):** Tạp chí Khoa học Quốc tế (Journal) — **CORE Rank A\***, Scopus Q1, CCF-A
- 🔗 **DOI / Link (Đường dẫn bài báo):** 
  - Bài báo IEEE: https://doi.org/10.1109/TSE.2022.3204902
  - Bản Preprint mở: https://arxiv.org/abs/2201.05401
  - Replication Package chính thức trên GitHub: https://github.com/SOLAR-group/AgileEffortEstimation
  - CSDL TAWOS Dataset v1.1: https://github.com/SOLAR-group/TAWOS
- 🎯 **Problem (Bài toán & Thách thức):**
  - Năm 2019, bài báo nổi tiếng Deep-SE (Choetkiertikul et al., IEEE TSE 2019) tuyên bố mạng học sâu đã giải quyết xuất sắc bài toán ước lượng Story Point tự động. Tuy nhiên, kết quả này có thực sự khái quát hóa được trên các dự án phần mềm thực tế khác hay không?
  - Nghiên cứu đặt ra câu hỏi phản biện cốt lõi: *"Liệu sự tương đồng ngữ nghĩa (Semantic Similarity) giữa các câu chữ trong User Story có thực sự tương quan và đủ để dự đoán độ phức tạp công việc thực tế hay chưa?"*.
  - Kiểm tra xem các bẫy rò rỉ dữ liệu và phương pháp đánh giá thiếu chuẩn mực có đang làm thổi phồng hiệu năng của Deep Learning trong ngành phần mềm hay không.
- 📊 **Dataset (Bộ dữ liệu thực nghiệm):**
  - Sử dụng **3 bộ dữ liệu lớn với tổng cộng hơn 60.000 issues** có nhãn Story Point từ hệ thống Jira:
    1. Tập Choetkiertikul (16 dự án, 23.313 issues có SP).
    2. Tập Porru (8 dự án, 4.904 issues).
    3. Tập Tawosi mở rộng (26 dự án, 31.960 issues bổ sung từ kho TAWOS).
- 🎯 **Ground Truth (Nhãn mục tiêu thực tế):**
  - Giá trị Story Point (SP) số nguyên/số thực dương thực tế được ghi nhận trong Jira của từng issue.
- 🧠 **Method (Phương pháp & Kiến trúc đề xuất):**
  - Thực hiện một quy trình nghiên cứu tái lập nghiêm ngặt (Strict Close Replication) và nghiên cứu mở rộng (Extension):
    1. **Tái lập Deep-SE:** Xây dựng lại kiến trúc mạng nơ-ron sâu kết hợp biểu diễn từ Word2Vec, qua tầng bộ nhớ ngắn hạn dài hạn LSTM, tầng mạng cao tốc lặp (Recurrent Highway Network - RHWN), và tầng hồi quy Dense Layer.
    2. **Xây dựng ML Baselines:** Kết hợp trích xuất tần suất từ nghịch đảo văn bản TF-IDF với thuật toán Support Vector Machine (SVM) và Ridge Regression.
    3. **Chuẩn hóa quy trình kiểm định:** Triệt tiêu hoàn toàn việc rò rỉ dữ liệu giữa tập Train và Test bằng cách cô lập toàn bộ các bước tiền xử lý.
- ⚖️ **Baseline (Đường cơ sở đối chứng):**
  - **Random Guessing (RG):** Sinh điểm số ngẫu nhiên đều trong khoảng giá trị nhỏ nhất và lớn nhất của tập Train.
  - **Mean Effort:** Dự đoán một giá trị hằng số bằng trung bình cộng nhãn của tập Train.
  - **Median Effort:** Dự đoán một giá trị hằng số bằng **trung vị (Median)** của tập Train — Đây là đường cơ sở tối thiểu quan trọng nhất mà bất kỳ mô hình AI nào cũng bắt buộc phải vượt qua.
- ✂️ **Split (Chiến lược phân chia dữ liệu):**
  - **Within-project (Nội bộ dự án):** Phân chia theo dòng thời gian tạo issue (**Chronological Split: 60% Train / 20% Val / 20% Test**).
  - **Cross-project (Liên dự án):** Phân chia theo dòng thời gian tuyệt đối toàn cục (**Strict Chronological Split**) giữa các dự án khác nhau để triệt tiêu mọi khả năng rò rỉ thông tin tương lai.
- 📏 **Metrics (Thước đo đánh giá):**
  - **Thước đo sai số:** MAE, MdAE, SA (Standardized Accuracy).
  - **Kiểm định phi tham số (Non-parametric Tests):**
    - **Wilcoxon Signed-Rank Test** (với mức ý nghĩa $\alpha = 0.05$ kèm hiệu chỉnh Bonferroni): Kiểm tra xem sự khác biệt sai số giữa mô hình và Median baseline có ý nghĩa thống kê thực sự hay chỉ do ngẫu nhiên.
    - **Vargha-Delaney $\hat{A}_{12}$ Effect Size:** Thước đo kích thước hiệu ứng đo lường xác suất một mô hình tạo ra dự đoán chính xác hơn mô hình đối chứng ($\hat{A}_{12} > 0.5$ là tốt hơn, $\hat{A}_{12} = 0.5$ là ngang nhau).
- 🏆 **Main Result (Kết quả cốt lõi):**
  - 💥 **Deep-SE không vượt trội hơn Median Baseline ở 58% các dự án** thử nghiệm trong kịch bản nội bộ (within-project). Chỉ cần dùng một con số trung vị đơn giản đã chiến thắng mô hình Deep Learning phức tạp ở hơn một nửa số dự án!
  - Trong kịch bản liên dự án (cross-project), Deep-SE hoàn toàn bị Median Baseline và TF-IDF đánh bại.
  - Kỹ thuật tăng cường dữ liệu (Data Augmentation) làm giảm độ chính xác ở **67%** các dự án.
  - Việc bỏ ra gần **47 giờ GPU để tiền huấn luyện (Pre-training)** không giúp mô hình cải thiện độ chính xác hay tốc độ hội tụ so với việc khởi tạo ngẫu nhiên.
- ⚠️ **Critical Notes (Phản biện & Điểm lưu ý quan trọng):**
  - 🚨 **Vạch trần lỗ hổng Data Leakage của Deep-SE (2019):** Nhóm tác giả phát hiện bài báo Deep-SE gốc đã áp dụng kỹ thuật gọt outlier (capping 90th percentile) lên **toàn bộ dữ liệu trước khi chia train/test**, khiến sai số MAE của tập test bị bóp nhỏ giả tạo!
  - 🧹 **Nhiễu văn bản (Noise):** Có tới **19.11%** các issues chứa log lỗi, stack trace, đoạn mã code nguồn dài dòng làm sai lệch nghiêm trọng các bộ trích xuất ngữ nghĩa NLP.
  - ❌ **Sự ngộ nhận về Semantic Similarity:** Tác giả kết luận đanh thép rằng hai công việc mô tả bằng câu chữ giống nhau hoàn toàn có thể đòi hỏi nỗ lực triển khai khác nhau hoàn toàn tùy thuộc vào cấu trúc codebase, kinh nghiệm lập trình viên và kiến trúc hệ thống.
- 💡 **Takeaways (Bài học rút ra):**
  - **Luôn kiểm tra với Median Baseline:** Một mô hình học máy dù hiện đại đến đâu nếu không vượt qua được Median Baseline và không có ý nghĩa thống kê qua kiểm định Wilcoxon thì đều không có giá trị thực tiễn.
  - Tuyệt đối không bao giờ thực hiện chuẩn hóa (Normalization), điền dữ liệu khuyết hay lọc outlier trên toàn bộ tập dữ liệu trước khi phân chia Train/Test.
  - Bắt buộc dùng kiểm định phi tham số (Wilcoxon Test & $\hat{A}_{12}$) thay vì chỉ nhìn vào điểm trung bình MAE để kết luận.
- 🚀 **Relevance to Topic (Đóng góp cho Đề tài Nhóm):**
  - Là **kim chỉ nam về phương pháp luận nghiên cứu (Methodological Benchmark)** cho đề tài của Nhóm 3.
  - Cung cấp toàn bộ công thức và chuẩn mực kiểm định thống kê giúp nhóm xây dựng pipeline đánh giá khách quan.
  - Cung cấp nguồn CSDL TAWOS v1.1 phục vụ toàn bộ các thử nghiệm của đề tài.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
