# 📑 Literature Review: GPT2SP (Fu & Tantithamthavorn, 2023)

> **Tổng quan nhanh:** Công trình tiên phong đưa mô hình ngôn ngữ lớn tiền huấn luyện (Pre-trained LLM - GPT-2) vào bài toán dự đoán Story Point trong Agile, đóng vai trò là mô hình cốt lõi (Core Baseline) trong đề tài của Nhóm 3.

---

- 📌 **Title (Tiêu đề):** GPT2SP: A Transformer-Based Agile Story Point Estimation Approach
- 🔑 **Cite Key (Khóa trích dẫn BibTeX):** `Fu2023GPT2SP`
- 👥 **Authors (Tác giả):** Michael Fu và Chakkrit Tantithamthavorn (Đại học Monash, Úc)
- 📅 **Year (Năm xuất bản):** 2023
- 🏛️ **Venue (Nơi công bố):** IEEE Transactions on Software Engineering (TSE), Volume 49, Issue 4, Trang 2450–2464
- 🏷️ **Venue Type (Loại hình công bố):** Tạp chí Khoa học Quốc tế (Journal) — **CORE Rank A\***, Scopus Q1, CCF-A (Tạp chí số 1 thế giới về Kỹ nghệ Phần mềm)
- 🔗 **DOI / Link (Đường dẫn bài báo):** 
  - Bài báo chính thức: https://doi.org/10.1109/TSE.2022.3158252
  - Mã nguồn GitHub: https://github.com/awsm-research/gpt2sp
  - Checkpoint mô hình trên Hugging Face: https://huggingface.co/MickyMike/0-GPT2SP-springxd
- 🎯 **Problem (Bài toán & Thách thức):**
  - Trong quy trình Agile Scrum, việc ước lượng Story Point thủ công (như họp Planning Poker) thường bị chi phối bởi cảm tính chủ quan, tốn nhiều thời gian và gây mệt mỏi cho đội ngũ phát triển.
  - Các mô hình học sâu trước đây (tiêu biểu là Deep-SE dùng LSTM + Word2Vec) chỉ học từ vựng cố định, không hiểu được ngữ cảnh sâu của câu từ kỹ thuật, và không thể chuyển giao tri thức (non-transferable/non-pre-trained) giữa các dự án khác nhau.
  - Thách thức: Làm sao tận dụng tri thức ngôn ngữ khổng lồ từ các mô hình Transformer tiền huấn luyện (Pre-trained LLMs) để tự động hóa việc chấm điểm Story Point chính xác từ văn bản của User Story?
- 📊 **Dataset (Bộ dữ liệu thực nghiệm):**
  - Sử dụng **16 dự án phần mềm mã nguồn mở** lớn từ bộ dữ liệu Choetkiertikul (như Spring XD, Mule, Appcelerator, Mesos, Apache,...) kết hợp với 3 dự án Jira công nghiệp mở rộng, tổng cộng lên đến hàng chục nghìn issues có gán điểm.
  - Dự án tiêu biểu nhất được kiểm chứng sâu: **Spring XD (3.526 issues)**.
- 🎯 **Ground Truth (Nhãn mục tiêu thực tế):**
  - Giá trị Story Point (SP) số nguyên/số thực dương thực tế được ghi nhận chính thức trên hệ thống Jira bởi các lập trình viên sau buổi họp Sprint Planning.
- 🧠 **Method (Phương pháp & Kiến trúc đề xuất):**
  - Đề xuất kiến trúc **GPT2SP**:
    1. **Tokenization:** Sử dụng bộ tách từ Byte-Pair Encoding (BPE Tokenizer) của GPT-2 để phân rã tiêu đề/mô tả của issue mà không bị lỗi từ ngoài từ điển (Out-Of-Vocabulary).
    2. **Transformer Backbone:** Sử dụng mô hình nền tảng GPT-2 tiền huấn luyện gồm 12 tầng Transformer Blocks để trích xuất vector biểu diễn ngữ cảnh sâu (Contextual Representation).
    3. **Pooling Layer:** Gom các vector token đại diện (hoặc lấy token cuối cùng) để tạo thành vector tóm tắt toàn bộ User Story (kích thước 768 chiều).
    4. **Regression Head:** Đưa qua một tầng tuyến tính Dense Linear Layer (`Linear(768, 1)`) để thực hiện tác vụ Hồi quy (Regression), dự đoán trực tiếp ra giá trị Story Point liên tục $\hat{y}$.
    5. **Tối ưu hóa:** Huấn luyện tinh chỉnh (Fine-tuning) toàn bộ mạng với hàm mất mát MSE/L1 Loss bằng thuật toán tối ưu AdamW.
- ⚖️ **Baseline (Đường cơ sở đối chứng):**
  - **Nhóm Thống kê cơ sở:** Random Guessing (Đoán ngẫu nhiên), Mean Effort (Dự đoán trung bình cộng), **Median Effort (Dự đoán trung vị)**.
  - **Nhóm Học máy cổ điển:** TF-IDF kết hợp mô hình hồi quy Ridge Regression.
  - **Nhóm Học sâu trước đó:** Mô hình Deep-SE (Word2Vec + LSTM + Recurrent Highway Network).
- ✂️ **Split (Chiến lược phân chia dữ liệu):**
  - Áp dụng **Chronological Split (Phân chia theo dòng thời gian tạo issue)** với tỷ lệ **60% Train / 20% Validation / 20% Test** theo từng dự án:
    - Train: 2.115 issues đầu tiên theo thời gian.
    - Val: 705 issues kế tiếp để chọn checkpoint tốt nhất.
    - Test: 706 issues sau cùng để đánh giá khách quan.
  - *Lý do:* Giữ đúng trật tự thời gian thực tế trong doanh nghiệp, tránh việc lấy issue của tương lai dự đoán cho quá khứ.
- 📏 **Metrics (Thước đo đánh giá):**
  - **MAE (Mean Absolute Error):** Sai số tuyệt đối trung bình giữa giá trị dự đoán và Story Point thực tế.
  - **MdAE (Median Absolute Error):** Sai số tuyệt đối trung vị (giúp tránh bị sai lệch bởi các giá trị dị biệt/outliers).
  - **SA (Standardized Accuracy):** Tỷ lệ cải thiện độ chính xác chuẩn hóa so với phương pháp đoán ngẫu nhiên: $SA = 1 - \frac{MAE_{model}}{MAE_{random\_guessing}}$.
  - **Kiểm định Wilcoxon Signed-Rank Test:** Đo ý nghĩa thống kê của mức độ cải thiện so với baseline.
- 🏆 **Main Result (Kết quả cốt lõi):**
  - Bài báo công bố GPT2SP vượt trội hơn tất cả các baselines trên cả 16 dự án.
  - Trên dự án Spring XD, bài báo báo cáo GPT2SP đạt **MAE trung vị ~0.96**, cải thiện khoảng **44.2%** so với Median baseline (MAE = 1.72), và đạt giá trị SA cao nhất.
- ⚠️ **Critical Notes (Phản biện & Điểm lưu ý quan trọng):**
  - 💥 **Mâu thuẫn nghiêm trọng giữa bài báo và code thực tế:** Trong bài báo, tác giả tuyên bố mô hình sử dụng kết hợp cả `Title + Description`. Tuy nhiên, khi kiểm tra mã nguồn và notebook chính thức của tác giả, mô hình **chỉ lấy riêng trường `Title` và bị cắt ngắn cứng ở `max_length = 20`** tokens!
  - ⏳ **Bẫy Rò rỉ Dữ liệu Tương lai (Future-Information Leakage):** Nghiên cứu thu thập dữ liệu dạng *Final Snapshot* (sau khi issue đã đóng). Trong thực tế, lập trình viên thường sửa tiêu đề/mô tả sau buổi planning để thêm log lỗi, giải pháp kỹ thuật, khiến mô hình nhìn thấy trước tương lai $\rightarrow$ Kết quả trên bài báo bị tăng ảo (overoptimistic).
  - 📉 **Thực tế Tái lập (Partial Reproduction của Nhóm 3):** Khi tải checkpoint gốc của tác giả (`MickyMike/0-GPT2SP-springxd`) chạy trên tập Test chuẩn với môi trường Transformers hiện tại, kết quả thực tế đạt **MAE = 1.7330**, **MdAE = 1.2994** $\rightarrow$ Kém hơn cả Median Baseline (1.7153).
- 💡 **Takeaways (Bài học rút ra):**
  - Mô hình Transformer/LLM biểu diễn ngữ nghĩa vượt trội hơn mô hình chuỗi thời gian LSTM cổ điển, nhưng rất nhạy cảm với việc xử lý văn bản đầu vào.
  - Khi đọc bài báo khoa học, bắt buộc phải kiểm tra đối chiếu trực tiếp giữa lời văn trong paper và mã nguồn thực tế (artifact audit).
  - Phải kiểm soát chặt chẽ mốc thời gian lấy dữ liệu tại thời điểm lập kế hoạch (`SP_Estimation_Date`) để tránh bẫy rò rỉ dữ liệu.
- 🚀 **Relevance to Topic (Đóng góp cho Đề tài Nhóm):**
  - Là **Core Baseline** số 1 để nhóm tái lập, so sánh và chứng minh luận điểm nghiên cứu: Khi loại bỏ thông tin rò rỉ (Planning-Time Snapshot), hiệu năng của GPT2SP sẽ thay đổi như thế nào?
  - Cung cấp bằng chứng thực nghiệm rõ ràng để nhóm bảo vệ tính cấp thiết của đề tài trước hội đồng NCKH.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
