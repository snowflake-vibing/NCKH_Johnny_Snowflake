# Literature Review: Khan et al. (2025)

- **Title:** Efficient Story Point Estimation With Comparative Learning
- **Cite Key:** Khan2025Comparative
- **Authors:** Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, Zhe Yu
- **Year:** 2025
- **Venue:** arXiv preprint arXiv:2507.14642 [cs.SE] (Submitting to Top SE Conference ESEM / SANER)
- **Venue Type:** Preprint / Conference (CORE Rank A candidate)
- **DOI:** https://arxiv.org/abs/2507.14642 (Replication repo: https://github.com/hil-se/EfficientSPEComparativeLearning)
- **Problem:** Ước lượng Story Point truyền thống yêu cầu gán điểm số tuyệt đối cho từng backlog item (Direct Rating), thường gây tranh cãi, tốn nhiều thời gian và các mô hình hồi quy (Regression) đòi hỏi dữ liệu lịch sử dự án rất lớn. Bài báo đặt vấn đề: Con người đánh giá tương đối (Task A tốn nhiều effort hơn Task B) dễ dàng và chính xác hơn nhiều so với việc chỉ định một con số tuyệt đối.
- **Dataset:** 16 dự án mã nguồn mở từ tập Choetkiertikul / TAWOS với 23.313 issues có Story Point được ước lượng thủ công bởi các đội ngũ phát triển thực tế.
- **Ground Truth:** Phán đoán thứ tự ưu tiên nỗ lực tương đối giữa 2 User Story: $Story_A \succ Story_B$ (nghĩa là Story A tốn nhiều công sức hơn Story B) được suy ra từ nhãn Story Point thực tế trong Jira.
- **Method:** Đề xuất khung tiếp cận **Comparative Learning Framework**:
  1. Thay vì hồi quy điểm số, mô hình chuyển đổi bài toán sang học phân loại nhị phân trên từng cặp User Story $(Story_i, Story_j)$.
  2. Sử dụng mô hình Sentence-BERT (SBERT) để trích xuất vector nhúng ngữ nghĩa chiều cao cho từng issue text.
  3. Xây dựng vector quan hệ cặp $x_{ij} = [v_i, v_j, v_i - v_j, v_i \odot v_j]$ và huấn luyện bộ phân loại nhị phân (Pairwise Classifier) để dự đoán xác suất nhiệm vụ nào phức tạp hơn.
  4. Áp dụng thuật toán tổng hợp thứ hạng toàn cục (Global Ranking / Borda Count) để xếp hạng mức độ nỗ lực của toàn bộ backlog.
- **Baseline:** Các mô hình hồi quy điểm số tuyệt đối truyền thống (Direct Rating Regression): Ridge Regression, Random Forest, và SBERT Regression.
- **Split:** Phân chia theo dòng thời gian (Chronological Split) tạo cặp từ tập Train và đánh giá trên tập Test để bảo đảm tính thực tế.
- **Metrics:** Hệ số tương quan thứ hạng Spearman (Spearman's Rank Correlation Coefficient $\rho$) và độ chính xác phân loại cặp (Pairwise Classification Accuracy).
- **Main Result:**
  1. Mô hình huấn luyện trên phán đoán so sánh cặp đạt hệ số tương quan thứ hạng Spearman trung bình là **0.34** trên 16 dự án, tương đương hoặc vượt trội hơn các mô hình hồi quy trực tiếp trên nhãn tuyệt đối.
  2. Thử nghiệm trên người dùng thực tế (human-subject study) chứng minh rằng phương pháp so sánh cặp giúp **giảm đáng kể thời gian gán nhãn**, mang lại **độ tin cậy cao hơn** cho lập trình viên và duy trì sự đồng thuận tương đương với phương pháp Planning Poker truyền thống.
- **Critical Notes:**
  1. *Độ phức tạp tổ hợp sinh cặp:* Việc tạo cặp giữa các issues làm tăng số lượng mẫu huấn luyện theo cấp số nhân ($O(N^2)$), đòi hỏi phải có chiến lược lấy mẫu ngẫu nhiên (Pair Subsampling) để tránh bùng nổ tài nguyên tính toán và bộ nhớ RAM.
  2. *Vấn đề rò rỉ dữ liệu gốc:* Giống như các nghiên cứu trước, tập dữ liệu đầu vào vẫn lấy từ snapshot cuối cùng của issue sau khi đã hoàn thành, chưa áp dụng cơ chế khôi phục trạng thái tại thời điểm planning.
- **Takeaways:**
  1. Hướng tiếp cận học so sánh tương đối (Relative / Comparative Learning) phù hợp với bản chất nhận thức của con người trong quy trình Agile hơn là hồi quy số tuyệt đối.
  2. Sentence-BERT kết hợp vector quan hệ cặp đôi là một kiến trúc trích xuất đặc trưng gọn nhẹ, hiệu quả và có khả năng khái quát hóa cao.
- **Relevance to Topic:**
  1. Là nghiên cứu mới nhất (2025) nằm ngoài các tài liệu ban đầu, cung cấp một góc nhìn đột phá để nhóm làm đa dạng hóa danh mục mô hình nghiên cứu.
  2. Có thể kết hợp ý tưởng **Comparative Learning** với cơ chế **Kiểm soát rò rỉ thời gian (Temporal Leakage Control)** của Nhóm 3 để tạo ra một hướng đóng góp nghiên cứu rất mới lạ và có giá trị xuất bản cao.
