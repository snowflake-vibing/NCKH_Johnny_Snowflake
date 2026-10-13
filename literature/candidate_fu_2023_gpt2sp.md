# Literature Review: GPT2SP

- **Title:** GPT2SP: A Transformer-Based Agile Story Point Estimation Approach
- **Cite Key:** Fu2023GPT2SP
- **Authors:** Michael Fu, Chakkrit Tantithamthavorn
- **Year:** 2023
- **Venue:** IEEE Transactions on Software Engineering (TSE), Vol. 49, No. 4, pp. 2450-2464
- **Venue Type:** Journal (CORE Rank A*, Q1 Scopus, CCF-A)
- **DOI:** https://doi.org/10.1109/TSE.2022.3158252
- **Problem:** Ước lượng Story Point trong Agile thường mang tính chủ quan và tốn thời gian. Các mô hình học sâu trước đó (như Deep-SE) sử dụng Word2Vec/LSTM bị hạn chế về khả năng học ngữ cảnh sâu (contextual understanding), không thể truyền giao tri thức (non-transferable/non-pre-trained) và có độ chính xác ước lượng còn hạn chế.
- **Dataset:** 16 dự án mã nguồn mở từ tập dữ liệu Choetkiertikul (gồm Spring XD, Mule, Appcelerator, Mesos, Apache,...) và 3 dự án Jira công nghiệp mở rộng, với tổng cộng hàng chục nghìn issues.
- **Ground Truth:** Giá trị Story Point (SP) được đội ngũ phát triển ghi nhận trong hệ thống Jira của từng issue.
- **Method:** Đề xuất **GPT2SP** — Mô hình tiền huấn luyện GPT-2 (Generative Pre-trained Transformer 2) được tinh chỉnh (fine-tuning) cho bài toán hồi quy (Regression). Mô hình sử dụng GPT-2 Tokenizer (BPE), qua các tầng Transformer blocks để biểu diễn ngữ cảnh văn bản của issue, sau đó đưa qua pooling layer và một Dense Linear Layer (Regression Head) để dự đoán giá trị Story Point liên tục.
- **Baseline:** Random Guessing (RG), Mean Effort, Median Effort, TF-IDF + Ridge Regression, và mô hình học sâu Deep-SE (LSTM + Highway Network).
- **Split:** Phân chia theo dòng thời gian tạo issue (Chronological Split) với tỷ lệ 60% Train / 20% Validation / 20% Test theo từng dự án (Within-project).
- **Metrics:** Mean Absolute Error (MAE), Median Absolute Error (MdAE), Standardized Accuracy (SA), và kiểm định thống kê Wilcoxon Signed-Rank Test.
- **Main Result:** Bài báo công bố GPT2SP vượt trội hơn tất cả các baselines trên 16 dự án. Cụ thể trên dự án Spring XD, GPT2SP đạt MAE trung vị ~0.96, cải thiện khoảng 44.2% so với Median baseline (MAE = 1.72) và đạt độ chính xác chuẩn hóa SA cao nhất.
- **Critical Notes:**
  1. *Mâu thuẫn giữa bài báo và artifact công khai:* Bài báo mô tả kết hợp `Title + Description` để ước lượng, nhưng trong Notebook/Checkpoint công khai của tác giả (`MickyMike/0-GPT2SP-springxd`) chỉ sử dụng riêng trường `Title` và cắt ngắn `max_length = 20`.
  2. *Rò rỉ dữ liệu tương lai (Future-Information Leakage):* Mô hình sử dụng dữ liệu tĩnh (Final Snapshot) được thu thập sau khi issue đã hoàn thành/đóng lại, khiến văn bản chứa các sửa đổi kỹ thuật hậu kỳ mà tại thời điểm Sprint Planning nhóm chưa hề có.
  3. *Hiện tượng Partial Reproduction:* Khi tái lập lại bằng checkpoint của tác giả trên môi trường Transformers mới, MAE đạt được thực tế là 1.7330 (kém hơn Median baseline 1.7153), cho thấy tính nhạy cảm môi trường cao.
- **Takeaways:**
  1. Mô hình ngôn ngữ tiền huấn luyện (Pre-trained Transformer) có khả năng trích xuất đặc trưng ngữ nghĩa tốt hơn Word2Vec/LSTM truyền thống.
  2. Khi tái lập nghiên cứu khoa học, cần kiểm tra đối chiếu trực tiếp giữa mã nguồn artifact thực tế và phần mô tả trong bài báo.
  3. Cần kiểm soát nghiêm ngặt thời điểm trích xuất dữ liệu để tránh đánh giá độ chính xác tăng ảo (overoptimistic results).
- **Relevance to Topic:**
  1. Là mô hình học sâu / Transformer cốt lõi đóng vai trò Core Baseline trong đề tài NCKH của Nhóm 3.
  2. Kết quả phân tích sai lệch và tái lập GPT2SP là cơ sở thực nghiệm thuyết phục để nhóm đề xuất pipeline tái tạo dữ liệu tại thời điểm lập kế hoạch (Planning-Time Historical State Reconstruction) nhằm kiểm soát Temporal Leakage.
