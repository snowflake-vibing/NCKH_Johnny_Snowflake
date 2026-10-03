# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study (arXiv:2201.05401v2)

---

## 📋 THƯỚC ĐO 13 CỘT TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tawosi et al.** (*IEEE TSE / arXiv:2201.05401v2*) | 2022 | Kiểm chứng (Replication & Extension) hiệu quả của mô hình Deep Learning (Deep-SE) trong ước lượng Agile Effort (Story Points) ở mức task; xác minh liệu tương đồng ngữ nghĩa có đủ để dự đoán effort. | 3 bộ dữ liệu: Choetkiertikul (16 dự án, 23.313 issues), Porru (8 dự án, 4.904 issues), và Tawosi (26 dự án, 31.960 issues mở rộng). | Story Point (SP) thực tế ghi nhận trong hệ thống Jira. | Replication & Extension study: Đánh giá Deep-SE (Word Embedding + LSTM + RHWN + Regressor) & TF/IDF-SVM. | Random Guessing (RG), Mean Effort, Median Effort. | Within-project: Chronological split (60% train / 20% val / 20% test). Cross-project: Strict Chronological split theo mốc thời gian tạo issue. | MAE (chính), MdAE, SA, Wilcoxon Rank-Sum test ($\alpha = 0.05$ & Bonferroni $0.025$), Vargha-Delaney $\hat{A}_{12}$ effect size. | Deep-SE **KHÔNG** vượt trội hơn Median baseline ở 58% dự án (within-project); chỉ hơn TF/IDF-SVM ở 19% dự án (tệ hơn ở 15%); Cross-project tệ hơn Within-project; Augmentation làm kém đi 67% dự án; Pre-training (~47h) không tăng độ chính xác hay tốc độ hội tụ. | 1. Nguy cơ rò rỉ dữ liệu (Future-Information Leakage) khi cap outlier 90th percentile lên cả test set và dùng data tương lai trong cross-project.<br>2. 19.11% issue chứa code/stack trace làm nhiễu NLP.<br>3. Semantic similarity không phân biệt được nỗ lực thực tế.<br>4. Ground truth SP mang tính cảm quan chủ quan.<br>5. Giới hạn 100 token đầu của issue text. | 1. Bắt buộc dùng **Chronological Split**.<br>2. Không transform/cap outlier trên test set.<br>3. Bỏ qua bước pre-training đắt đỏ.<br>4. Tiền xử lý tách biệt code/stack trace khỏi natural text.<br>5. Bổ sung các đặc trưng effort drivers khác ngoài ngữ nghĩa thuần túy. | 1. Cung cấp căn cứ sắc bén phản biện việc lạm dụng NLP/LLM embedding cho bài toán ước lượng effort.<br>2. Cung cấp chuẩn mực thiết kế thực nghiệm (Chronological split, Median baseline, kiểm định Wilcoxon & $\hat{A}_{12}$).<br>3. Giúp nhóm lập luận né tránh Future-Information Leakage khi bảo vệ đề tài. |

---

## 📑 CẤU TRÚC PHẢN HỒI CHUẨN (DETAILED LITERATURE NOTE TEMPLATE)

### 📄 Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Vali Tawosi, Rebecca Moussa, and Federica Sarro, *"Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study"*, IEEE Transactions on Software Engineering (TSE), 2022.
* **Year:** 2022 (arXiv:2201.05401v2, Dec 2022).
* **DOI / Link:** [arXiv:2201.05401v2](https://arxiv.org/abs/2201.05401) | Rep package: [GitHub SOLAR-group/AgileEffortEstimation](https://github.com/SOLAR-group/AgileEffortEstimation)

---

#### 2. Đặt bài toán & Mục tiêu nghiên cứu (Problem & Goal)
* **Problem:** 
  * Ước lượng nỗ lực (Effort Estimation) trong các dự án Agile thường được thực hiện ở mức công việc (task-level) thông qua **Story Point (SP)** dựa trên đánh giá cảm quan của chuyên gia (expert judgement), dẫn đến sự thiếu nhất quán và chủ quan giữa các sprint.
  * Bài báo tiến hành một nghiên cứu tái lặp nghiêm ngặt (close replication) và mở rộng (extension) đối với công trình nền tảng Deep-SE (Choetkiertikul et al., IEEE TSE 2019) – mô hình Deep Learning được coi là State-of-the-Art (SOTA) trong ước lượng Story Point.
  * Nghiên cứu nhằm trả lời câu hỏi cốt lõi: *"Liệu sự tương đồng ngữ nghĩa (semantic similarity) giữa các User Story có đủ để phân biệt và dự đoán chính xác Story Point hay chưa?"*
* **Ground truth:** 
  * Giá trị **Story Point (SP)** thực tế được ghi nhận bởi các đội ngũ phát triển trên hệ thống quản lý Jira (thường thuộc dãy Fibonacci: 1, 2, 3, 5, 8, 13, 20, 40,...).

---

#### 3. Dữ liệu & Phương pháp thực nghiệm (Dataset & Methodology)
* **Dataset:** Nghiên cứu sử dụng 3 bộ dữ liệu lớn từ các dự án mã nguồn mở:
  1. **Choetkiertikul Dataset (Choet):** 16 dự án từ 9 kho lưu trữ (Jira repositories), tổng cộng 23,313 issues.
  2. **Porru Dataset:** 8 dự án từ 6 repositories, tổng cộng 4,904 issues (đã áp dụng các bộ lọc khắt khe hơn).
  3. **Tawosi Dataset (Mở rộng mới):** 26 dự án từ 13 repositories với tổng cộng **31,960 issues** (mỗi dự án > 200 issues), áp dụng quy trình lọc dữ liệu khắt khe của Porru et al. để loại bỏ nhiễu.
* **Method:**
  * **Deep-SE (Replication & Extension):** Kiến trúc kết hợp Word Embedding + Long Short-Term Memory (LSTM) + Recurrent Highway Network (RHWN) + Differentiable Regressor.
  * **TF/IDF-SVM:** Trích xuất đặc trưng TF-IDF từ title/description kết hợp với loại issue (type) và thành phần (component), đưa vào mô hình Support Vector Classifier.
* **Baseline:**
  * **Random Guessing (RG):** Lấy ngẫu nhiên giá trị SP từ tập lịch sử.
  * **Mean Effort:** Dự đoán bằng giá trị trung bình cộng (Mean) SP của các issue trong quá khứ.
  * **Median Effort:** Dự đoán bằng giá trị trung vị (Median) SP của các issue trong quá khứ.
* **Split:**
  * **Within-project:** Sắp xếp dữ liệu theo thứ tự thời gian khởi tạo (Chronological order) – 60% cũ nhất làm tập Train, 20% tiếp theo làm tập Validation, 20% mới nhất làm tập Test.
  * **Cross-project (Thực tế - Extension RQ3.2 & RQ4):** Phân chia nghiêm ngặt theo mốc thời gian (*Strict Chronological Split*). Tất cả các issue trong tập Train/Validation cross-project phải được tạo trước ngày tạo issue đầu tiên của tập Test trong target project nhằm triệt tiêu hoàn toàn **Future-Information Leakage**.
* **Metrics:**
  * **MAE (Mean Absolute Error):** Độ đo sai số tuyệt đối trung bình (chính).
  * **MdAE (Median Absolute Error):** Sai số tuyệt đối trung vị.
  * **SA (Standardized Accuracy):** Tỷ lệ cải thiện độ chính xác so với Random Guessing.
  * **Wilcoxon Rank-Sum Test (Mann-Whitney U Test):** Kiểm định ý nghĩa thống kê 1 phía ($\alpha = 0.05$ và hiệu chỉnh Bonferroni $\alpha = 0.025$).
  * **Vargha-Delaney $\hat{A}_{12}$ Effect Size:** Đánh giá mức độ khác biệt thực tiễn giữa các mô hình (negligible `<0.6`, small `0.6-0.7`, medium `0.7-0.8`, large `≥0.8`).

---

#### 4. Kết quả & Đóng góp chính (Results & Takeaways)
* **Main result:**
  1. **RQ1 (Sanity Check - Within-project):** Deep-SE **KHÔNG** vượt qua được bài kiểm tra Sanity Check cơ bản. Deep-SE chỉ vượt trội hơn Median baseline có ý nghĩa thống kê ở **42% trường hợp** (8/16 dự án Choet, 4/26 dự án Tawosi). Ở 58% trường hợp còn lại, Median baseline đơn giản cho kết quả tương đương hoặc tốt hơn Deep-SE.
  2. **RQ2 (Deep-SE vs. TF/IDF-SVM):** Deep-SE chỉ vượt trội hơn TF/IDF-SVM có ý nghĩa thống kê ở **19% trường hợp** (5/26 dự án Tawosi), trong khi ở **15% trường hợp** Deep-SE lại cho kết quả tệ hơn TF/IDF-SVM.
  3. **RQ3 (Cross-project Estimation):** Khả năng ước lượng cross-project của Deep-SE rất kém so với within-project. Khi đưa vào ngữ cảnh thời gian thực tế (RQ3.2), Deep-SE hoàn toàn thất bại và bị Median baseline đánh bại ở toàn bộ các dự án.
  4. **RQ4 (Augmented Training Set):** Việc bổ sung thêm dữ liệu từ các dự án khác trong cùng công ty/repository không mang lại cải thiện ổn định (chỉ tốt lên ở 5/18 dự án, nhưng lại làm kết quả tệ đi ở 12/18 dự án - 67%).
  5. **RQ5 (Pre-Training Effectiveness):** Bước Pre-training đắt đỏ (tốn ~47 giờ tính toán trên 50,000 issues) đối với tầng Embedding và LSTM **KHÔNG** giúp tăng độ chính xác ước lượng và **KHÔNG** làm tăng tốc độ hội tụ (convergence speed) của Deep-SE. Do đó, bước này hoàn toàn có thể bỏ qua.

* **Điểm cần lưu ý:**
  1. **Nguy cơ rò rỉ dữ liệu tương lai (Future-Information Leakage):**
     * **Transformation Leakage trong bài báo gốc (Choetkiertikul et al., 2019):** Bài gốc áp dụng hàm cap outlier ở bách phân vị 90 lên **TOÀN BỘ dataset trước khi chia tập test**, dẫn đến sai số tuyệt đối bị bóp nhỏ giả tạo trên tập test (tạo ra kết quả lạc quan giả tạo không thể áp dụng thực tế).
     * **Temporal Leakage trong Cross-project:** Trong bài gốc, 11/16 thực nghiệm cross-project có hơn 97% issue ở tập Train được tạo *sau* ngày bắt đầu của target project (dùng dữ liệu tương lai để dự đoán quá khứ). Khi bài báo này sửa lại đúng thứ tự thời gian (Strict Chronological Split), độ chính xác của Deep-SE giảm sút mạnh.
  2. **Lỗi tính toán Baseline trong nghiên cứu trước:** Bài báo gốc đã **cộng thêm 1.0** vào kết quả dự đoán của Mean và Median baseline một cách không có giải thích hay căn cứ lý thuyết, làm thổi phồng sai số của baseline một cách bất hợp lý.
  3. **Hạn chế cốt lõi của Semantic Similarity:** Độ tương đồng ngữ nghĩa giữa các văn bản tiêu đề/mô tả không tỉ lệ thuận với nỗ lực triển khai thực tế. Nhiều user story cùng đề cập đến một chủ đề (như *"Kafka message bus"*) nhưng lại yêu cầu mức nỗ lực rất khác nhau (từ 1, 2, 3 đến 8 SP tùy thuộc vào là sửa lỗi nhỏ hay thêm tính năng phức tạp).
  4. **Nhiễu dữ liệu văn bản (Unprocessed Text Noise):** Có **19.11% issue** (6,107/31,960 issues) trong bộ dữ liệu chứa mã nguồn (code snippets) hoặc vết lỗi (stack traces). Việc không tiền xử lý loại bỏ code snippets/links ảnh hưởng tiêu cực đến khả năng học của các tầng NLP.
  5. **Sự không đồng nhất của dữ liệu (Data Heterogeneity):** Tập dữ liệu huấn luyện gộp chung nhiều loại issue khác nhau (Bug, Story, Improvement, Task, Epic...) có cấu trúc và độ dài văn bản khác biệt rất lớn (độ dài Bug và Story chênh lệch có ý nghĩa thống kê với $p < 2.2 \times 10^{-16}$), gây trở ngại cho mô hình học tổng quát.
  6. **Mối đe dọa giá trị thực nghiệm (Threats to Validity):**
     * **Ground truth subjectivity:** Nhãn Story Point dựa trên đánh giá cảm quan của con người (expert estimation) nên có thể chứa nhiễu và sự thiếu nhất quán.
     * **External validity:** Dữ liệu chỉ thu thập từ các dự án mã nguồn mở (Open-source); môi trường doanh nghiệp thương mại có quy trình viết văn bản cohesive và Disciplined hơn nên cần thêm kiểm chứng độc lập.
     * **Input Truncation:** Cả Deep-SE và nghiên cứu tái lặp chỉ cắt lấy **100 token đầu tiên** của tiêu đề + mô tả issue, có nguy cơ bỏ sót các thông tin nỗ lực quan trọng nằm ở đoạn sau.

---

#### 5. Giá trị thực tiễn cho Đề tài NCKH của Nhóm (Team Application)

* **Nhóm có thể học/kế thừa gì?:**
  1. **Quy trình phân chia dữ liệu chuẩn mực (Chronological Split):** Đối với dữ liệu quản lý dự án / issue history, tuyệt đối không sử dụng Random K-Fold Cross-Validation mà phải chia theo thứ tự thời gian thực tế để tránh *Future-Information Leakage*.
  2. **Tránh bẫy biến đổi dữ liệu (Data Pre-processing Trap):** Mọi thao tác chuẩn hóa, xử lý outlier (capping, normalization) chỉ được tính toán và áp dụng dựa trên tập Train, sau đó áp dụng sang tập Validation/Test; tuyệt đối không được fit transformer trên toàn bộ dataset.
  3. **Tách biệt thông tin tự nhiên và mã nguồn:** 19.11% issue chứa code snippets hoặc stack traces. Việc trích xuất và xử lý riêng biệt các đoạn mã/dấu vết kỹ thuật khỏi văn bản tự nhiên là cực kỳ cần thiết để tránh làm nhiễu mô hình NLP.
  4. **Tiết kiệm tài nguyên thực nghiệm:** Không nhất thiết phải tốn chi phí tính toán khổng lồ cho các bước Pre-training ngôn ngữ tự nhiên khi áp dụng vào bài toán ước lượng Story Point.
  5. **Hạn chế của Semantic Similarity thuần túy:** Bài báo đã minh chứng rõ ràng rằng các user story có ngữ nghĩa rất giống nhau (cùng bàn về *"Kafka message bus"*) nhưng lại có Story Point chênh lệch từ 1, 2, 3 đến 8 SP. Do đó, nếu chỉ dựa vào văn bản tiêu đề/mô tả (NLP/LLM embedding) thì mô hình không thể phân biệt được độ phức tạp thực sự.

* **Liên quan/giúp gì cho đề tài nhóm?:**
  1. **Căn cứ lý thuyết vững chắc để phản biện lạm dụng LLM/NLP:** Cung cấp luận điểm sắc bén và bằng chứng thực nghiệm để giải thích vì sao các mô hình NLP/LLM thuần túy không đạt hiệu quả cao trong ước lượng nỗ lực phần mềm nếu thiếu đi các đặc trưng kỹ thuật và ngữ cảnh (effort drivers).
  2. **Thiết lập bộ Baseline & Kiểm định thống kê chuẩn mực:** Cung cấp khung đánh giá chuẩn mực cho đề tài của nhóm: Benchmark bắt buộc phải bao gồm *Median baseline*, áp dụng kiểm định thống kê phi tham số *Wilcoxon Rank-Sum test* kết hợp *Vargha-Delaney $\hat{A}_{12}$ effect size*.
  3. **Bảo vệ phương pháp luận trước hội đồng phản biện:** Giúp nhóm tự tin bảo vệ lựa chọn phương pháp chia dữ liệu Chronological Split và quy trình tiền xử lý chống Data Leakage khi viết bài báo khoa học hoặc bảo vệ đề tài NCKH.
