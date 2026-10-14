# 📑 Literature Review: Khan et al. (2025)

> **Tổng quan nhanh:** Công trình mới nhất (2025) mở ra một hướng tiếp cận hoàn toàn mới: Chuyển đổi bài toán từ "dự đoán điểm số tuyệt đối" sang "học so sánh tương đối giữa từng cặp User Story" (Pairwise Comparative Learning), mô phỏng chính xác tâm lý con người trong quy trình Agile.

---

- 📌 **Title (Tiêu đề):** Efficient Story Point Estimation With Comparative Learning
- 🔑 **Cite Key (Khóa trích dẫn BibTeX):** `Khan2025Comparative`
- 👥 **Authors (Tác giả):** Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, và Zhe Yu (Học viện Công nghệ Rochester - RIT và Đại học Maryland Quận Baltimore - UMBC, Hoa Kỳ)
- 📅 **Year (Năm xuất bản):** 2025 (Bản preprint công bố tháng 07/2025, đang trong quy trình bình duyệt tại các hội thảo hàng đầu về Kỹ nghệ Phần mềm)
- 🏛️ **Venue (Nơi công bố):** arXiv preprint arXiv:2507.14642 [cs.SE] (Mục tiêu hội thảo ESEM / SANER)
- 🏷️ **Venue Type (Loại hình công bố):** Bản thảo Tiền xuất bản / Kỷ yếu Hội thảo Khoa học Quốc tế (Preprint / Conference) — Ứng viên **CORE Rank A**
- 🔗 **DOI / Link (Đường dẫn bài báo):** 
  - Bản Preprint: https://arxiv.org/abs/2507.14642
  - Mã nguồn thực nghiệm chính thức trên GitHub: https://github.com/hil-se/EfficientSPEComparativeLearning
- 🎯 **Problem (Bài toán & Thách thức):**
  - **Nghịch lý của con số tuyệt đối trong Agile:** Trong các buổi họp Planning Poker thực tế, các lập trình viên thường xuyên tranh cãi gay gắt về việc một User Story là 3 điểm hay 5 điểm. Việc gán một con số Story Point tuyệt đối (Direct Rating) là rất khó khăn, mang tính cảm quan cao và tốn thời gian.
  - Tuy nhiên, con người lại rất giỏi và đồng thuận cực kỳ nhanh khi so sánh tương đối: *"Task A chắc chắn phức tạp và mất nhiều công sức hơn Task B"*.
  - Các mô hình học máy truyền thống thường cố gắng hồi quy một con số tuyệt đối (Regression), đòi hỏi lượng dữ liệu lịch sử rất lớn và thường xuyên dự đoán chệch do phân phối nhãn bị lệch mạnh.
  - Thách thức: Làm sao huấn luyện mô hình AI học theo cơ chế so sánh cặp tương đối của con người để xếp hạng nỗ lực chính xác hơn và giảm tải thời gian cho lập trình viên?
- 📊 **Dataset (Bộ dữ liệu thực nghiệm):**
  - Sử dụng **16 dự án mã nguồn mở** từ tập dữ liệu chuẩn Choetkiertikul / TAWOS với **23.313 issues** đã được ước lượng Story Point thực tế bởi các nhóm phát triển.
- 🎯 **Ground Truth (Nhãn mục tiêu thực tế):**
  - Mối quan hệ thứ tự ưu tiên nỗ lực giữa 2 User Story bất kỳ: $Story_A \succ Story_B$ (nghĩa là Story A tốn nhiều nỗ lực hơn Story B), được suy ra từ việc so sánh giá trị Story Point gốc ghi nhận trong Jira.
- 🧠 **Method (Phương pháp & Kiến trúc đề xuất):**
  - Đề xuất khung kiến trúc **Học so sánh cặp (Comparative Learning Framework)** gồm 4 giai đoạn logic:
    1. **Ghép cặp User Story (Pair Generation):** Với mỗi cặp công việc $(Story_i, Story_j)$, mô hình gán nhãn nhị phân $z_{ij} = 1$ nếu $Story_i$ tốn nhiều điểm hơn $Story_j$, và $z_{ij} = 0$ nếu ngược lại.
    2. **Mã hóa ngữ nghĩa văn bản bằng SBERT:** Sử dụng mô hình Sentence-BERT tiền huấn luyện (`all-MiniLM-L6-v2` hoặc `all-mpnet-base-v2`) để biến đổi đoạn văn bản của mỗi Story thành một vector ngữ nghĩa chiều cố định $v_i, v_j$.
    3. **Vector hóa quan hệ cặp đôi:** Tạo vector đặc trưng tổng hợp biểu diễn sự tương tác và chênh lệch giữa hai công việc:
       $$x_{ij} = [v_i, v_j, v_i - v_j, v_i \odot v_j]$$
       (kết hợp phép ghép nối, phép trừ vector và tích phần tử Hadamard).
    4. **Bộ phân loại nhị phân cặp (Pairwise Binary Classifier):** Huấn luyện mô hình phân loại (Logistic Regression, LightGBM hoặc MLP) với hàm mất mát Binary Cross-Entropy để dự đoán xác suất $P(Story_i \succ Story_j)$.
    5. **Tổng hợp Thứ hạng Toàn cục (Global Rank Inference):** Cho mỗi issue trong tập kiểm thử thi đấu so sánh chéo để tính điểm thắng cuộc (Borda Count Score), từ đó suy ra thứ hạng nỗ lực của toàn bộ backlog từ dễ đến khó.
- ⚖️ **Baseline (Đường cơ sở đối chứng):**
  - Các mô hình hồi quy điểm số tuyệt đối truyền thống (Direct Rating Regression):
    - Ridge Regression (Hồi quy Ridge với phạt L2).
    - Random Forest Regressor (Rừng ngẫu nhiên).
    - SBERT Regression (Trích xuất SBERT embedding đưa vào tầng hồi quy tuyến tính).
- ✂️ **Split (Chiến lược phân chia dữ liệu):**
  - Áp dụng **Chronological Split (Phân chia theo dòng thời gian tạo issue)**: Huấn luyện bộ so sánh trên các cặp được sinh ra từ các issues trong quá khứ (Train set) và kiểm thử khả năng xếp hạng trên các issues tương lai (Test set) để đảm bảo mô phỏng đúng môi trường thực tế.
- 📏 **Metrics (Thước đo đánh giá):**
  - **Hệ số tương quan thứ hạng Spearman ($\rho$):** Đo lường mức độ tương đồng giữa thứ hạng nỗ lực mà mô hình dự đoán và thứ hạng nỗ lực thực tế từ các chuyên gia (giá trị từ -1 đến 1, càng gần 1 càng tốt).
  - **Độ chính xác phân loại cặp (Pairwise Classification Accuracy):** Tỷ lệ phần trăm mô hình đoán đúng cặp task nào tốn nhiều effort hơn.
- 🏆 **Main Result (Kết quả cốt lõi):**
  - Mô hình học so sánh cặp đạt **hệ số tương quan thứ hạng Spearman trung bình là 0.34** trên toàn bộ 16 dự án, đạt độ tin cậy tương đương hoặc vượt trội hơn các mô hình hồi quy số tuyệt đối truyền thống.
  - **Thử nghiệm trên người dùng thực tế (Human-subject study):** Nghiên cứu chứng minh rằng phương pháp so sánh cặp giúp **giảm đáng kể thời gian gán nhãn**, mang lại **độ tự tin cao hơn** cho lập trình viên và duy trì sự đồng thuận tương đương với việc thảo luận Planning Poker truyền thống.
- ⚠️ **Critical Notes (Phản biện & Điểm lưu ý quan trọng):**
  - 💥 **Bùng nổ tổ hợp số lượng cặp ($O(N^2)$ Complexity):** Khi có $N$ issues, số lượng cặp khả dĩ là $\frac{N(N-1)}{2}$. Với 20.000 issues, số cặp lên tới hàng trăm triệu, gây nguy cơ tràn bộ nhớ RAM nghiêm trọng nếu không áp dụng kỹ thuật lấy mẫu con (Pair Subsampling, $K \approx 10-20$ cặp ngẫu nhiên cho mỗi task).
  - ⏳ **Vẫn sử dụng dữ liệu tĩnh (Final Snapshot):** Tác giả vẫn lấy văn bản sau khi hoàn thành task từ bộ Choetkiertikul gốc, nghĩa là mô hình của Khan et al. cũng đang vô tình chịu ảnh hưởng của hiện tượng **Future-Information Leakage**.
- 💡 **Takeaways (Bài học rút ra):**
  - Việc chuyển bài toán từ "dự đoán một con số cụ thể" sang "xếp hạng tương đối" (Ranking / Comparative Learning) là một hướng đi mang tính thực tiễn rất cao trong quy trình Agile.
  - Trích xuất đặc trưng bằng Sentence-BERT kết hợp vector sai phân ($v_i - v_j$) là giải pháp rất nhẹ, chạy nhanh và hiệu quả hơn nhiều so với việc fine-tuning toàn bộ mô hình LLM cồng kềnh như GPT-2.
- 🚀 **Relevance to Topic (Đóng góp cho Đề tài Nhóm):**
  - Là bài báo đại diện cho hướng nghiên cứu mới nhất (2025) nằm ngoài các tài liệu ban đầu của nhóm, mang lại góc nhìn học thuật đa dạng và sáng tạo.
  - **Ý tưởng đóng góp cho đề tài:** Nhóm có thể kết hợp phương pháp **Comparative Learning** này với cơ chế **Kiểm soát rò rỉ thời gian (Planning-Time Snapshot)** để đánh giá xem: *"Khi loại bỏ rò rỉ dữ liệu, độ chính xác xếp hạng nỗ lực của mô hình so sánh cặp có còn giữ vững được hệ số Spearman 0.34 hay không?"*. Đây là một câu hỏi nghiên cứu rất mới lạ, có tiềm năng công bố tại các hội thảo Rank A.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
