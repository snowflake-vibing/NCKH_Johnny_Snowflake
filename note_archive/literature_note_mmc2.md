# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Leakage and the reproducibility crisis in machine-learning-based science (Patterns, 2023 / mmc2.pdf)

---

## 📋 THƯỚC ĐO 13 CỘT TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kapoor & Narayanan** (*Patterns / Cell Press*) | 2023 | Khủng hoảng khả năng tái lặp (Reproducibility crisis) trong nghiên cứu khoa học ứng dụng ML do hiện tượng Rò rỉ dữ liệu (Data Leakage); xây dựng taxonomy và bộ công cụ kiểm soát leakage pre-publication. | Meta-review 22 bài báo khảo sát từ 17 ngành khoa học (ảnh hưởng 294 bài báo); Case study 124 bài báo dự đoán nội chiến (12 bài full code/data, 4 bài công bố ML vượt trội). | Nhãn sự kiện theo từng lĩnh vực (Ví dụ: Khởi phát nội chiến Civil War Onset, Chẩn đoán y khoa, Đột biến gen...). | Survey phân tích 17 ngành; Xây dựng Taxonomy 8 loại Leakage; Đề xuất Model Info Sheets (21 câu hỏi); Re-analysis thực nghiệm sửa lỗi leakage trên Civil War Prediction. | Mô hình thống kê cổ điển Logistic Regression (LR) vốn dùng để diễn giải (explanatory) chứ không tối ưu cho dự đoán. | Train-Test split phân chia theo mốc thời gian (Strict Temporal split) hoặc cụm độc lập (Block CV); loại bỏ hoàn toàn leakage trong pre-processing/feature selection. | AUC (Area Under ROC), Accuracy, Z-test so sánh ROC (Robin et al.), Bootstrap 95% Confidence Interval. | Data Leakage ảnh hưởng 294 bài báo ở 17 lĩnh vực; Khi sửa hết lỗi Leakage ở case study dự đoán nội chiến, các mô hình ML phức tạp (Random Forest, AdaBoost) **KHÔNG CÒN VƯỢT TRỘI HƠN** mô hình Logistic Regression cổ điển (AUC chênh lệch từ 0.14 giảm về 0.01). | 1. Taxonomy 8 loại Data Leakage thuộc 3 nhóm L1, L2, L3.<br>2. 9/12 bài báo không thực hiện kiểm định thống kê hay tính khoảng tin cậy.<br>3. Bẫy Hype và Publication bias ủng hộ các kết quả lạc quan giả tạo.<br>4. Không thể áp dụng thẳng quy trình chống leakage từ các cuộc thi (Kaggle) hay engineering sang ML-based science. | 1. Sử dụng **Taxonomy 8 loại Leakage** để tự rà soát pipeline.<br>2. Điền **Model Info Sheets (21 câu hỏi)** kiểm tra trước khi công bố.<br>3. Luôn chạy kiểm định thống kê Z-test/Bootstrap CI khi so sánh ML với Baseline.<br>4. Cảnh giác với kết quả nhảy vọt bất thường của ML phức tạp. | 1. Cung cấp luận cứ khoa học cao nhất (Patterns - Cell Press) khẳng định tính nguy hại của Data Leakage.<br>2. Là cơ sở để nhóm xây dựng thiết kế thực nghiệm sạch (không rò rỉ dữ liệu) để bảo vệ trước các hội đồng NCKH khắt khe.<br>3. Trích dẫn taxonomy leakage cho phần phương pháp luận. |

---

## 📑 CẤU TRÚC PHẢN HỒI CHUẨN (DETAILED LITERATURE NOTE TEMPLATE)

### 📄 Leakage and the reproducibility crisis in machine-learning-based science

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Sayash Kapoor and Arvind Narayanan, *"Leakage and the reproducibility crisis in machine-learning-based science"*, Patterns, Volume 4, Issue 9, 100804, Cell Press, September 8, 2023.
* **Year:** 2023 (Published: August 4, 2023).
* **DOI / Link:** [https://doi.org/10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804) | Replication capsule: [CodeOcean Capsule](https://doi.org/10.24433/CO.4899453.v1)

---

#### 2. Đặt bài toán & Mục tiêu nghiên cứu (Problem & Goal)
* **Problem:** 
  * Sự chuyển dịch sang sử dụng Machine Learning (ML) trong các ngành khoa học định lượng (ML-based science) đang phải đối mặt với một **cuộc khủng hoảng khả năng tái lặp (reproducibility crisis)** nghiêm trọng do cạm bẫy **Rò rỉ dữ liệu (Data Leakage)**.
  * Data Leakage tạo ra các mối tương quan giả tạo (spurious relationships) giữa biến độc lập và biến mục tiêu do lỗi trong khâu thu thập, chọn mẫu hoặc tiền xử lý dữ liệu, dẫn đến các kết quả đánh giá mô hình bị thổi phồng cực kỳ lạc quan (*wildly overoptimistic*).
  * Mục tiêu nghiên cứu:
    1. Tổng khảo sát mức độ ảnh hưởng của Data Leakage xuyên suốt các ngành khoa học.
    2. Xây dựng một **Hệ thống phân loại (Taxonomy)** chi tiết về các dạng Data Leakage.
    3. Đề xuất bộ công cụ **Model Info Sheets** (với 21 câu hỏi kiểm định) để ngăn ngừa leakage pre-publication.
    4. Tiến hành thực nghiệm kiểm chứng lại (Reproducibility case study) trong lĩnh vực dự đoán nội chiến (civil war prediction) nhằm đo lường tác động thực sự khi lỗi leakage được khắc phục.
* **Ground truth:** 
  * Các biến mục tiêu thực tế theo từng lĩnh vực khoa học (ví dụ: bùng phát nội chiến *Civil War Onset* [0/1], chẩn đoán bệnh ung thư, phát hiện biến đổi gen, dự đoán sự cố phần mềm...).

---

#### 3. Dữ liệu & Phương pháp thực nghiệm (Dataset & Methodology)
* **Dataset:** 
  * **Tập dữ liệu Khảo sát (Meta-review):** Tổng hợp 22 bài báo khảo sát tổng quan từ **17 lĩnh vực khoa học** (y sinh, tâm lý học, khoa học máy tính, xã hội học, tài chính, địa lý...), phát hiện Data Leakage ảnh hưởng trực tiếp tới **294 bài báo khoa học**.
  * **Tập dữ liệu Thực nghiệm Case Study (Dự đoán Nội chiến):** Khảo sát hệ thống 124 bài báo trong ngành Khoa học Chính trị -> Thu hẹp còn 12 bài báo tập trung dự đoán nội chiến có đầy đủ dữ liệu và mã nguồn -> Phân tích sâu 4 bài báo công bố trên các tạp chí Top-10 ngành khẳng định các mô hình ML phức tạp vượt trội hoàn toàn so với mô hình Logistic Regression cổ điển.
* **Method:**
  * **Meta-Analysis & Cross-Disciplinary Review:** Tổng hợp và hệ thống hóa các dạng lỗi từ 17 ngành khoa học.
  * **Taxonomy Construction:** Xây dựng hệ thống phân loại 8 dạng Leakage thuộc 3 nhóm nguyên nhân chính (L1, L2, L3).
  * **Model Info Sheets Protocol:** Xây dựng bảng 21 câu hỏi kiểm định tính minh bạch và sự phân tách sạch sẽ của dữ liệu.
  * **Re-analysis & Empirical Correction:** Chạy lại toàn bộ bộ mã nguồn của các nghiên cứu dự đoán nội chiến sau khi đã khắc phục triệt để các lỗi leakage (sửa lại quy trình Imputation, Feature Selection, Data Splitting).
* **Baseline:**
  * Mô hình **Logistic Regression (LR)** truyền thống (được xây dựng từ nhiều thập kỷ trước), vốn chỉ được thiết kế để diễn giải nguyên nhân lịch sử chứ không được tối ưu cho bài toán dự đoán tương lai.
* **Split:**
  * **Trong thực nghiệm sửa lỗi:** Sử dụng **Strict Temporal Split** (chia theo thời gian: tập train chỉ bao gồm các năm trước mốc thời gian của tập test) hoặc **Block Cross-Validation** (chia theo cụm bệnh nhân/thực thể độc lập) để đảm bảo không rò rỉ thông tin.
  * Đảm bảo mọi thao tác tiền xử lý (Imputation, Oversampling, Feature Selection) chỉ được `fit` trên tập Train.
* **Metrics:**
  * **AUC (Area Under the ROC Curve):** Diện tích dưới đường cong ROC (độ đo chính).
  * **Accuracy, Precision, Recall.**
  * **Z-test cho đường ROC (Robin et al.):** Kiểm định ý nghĩa thống kê về sự chênh lệch AUC giữa các mô hình.
  * **Bootstrapped 95% Confidence Intervals:** Ước lượng khoảng tin cậy 95% bằng kỹ thuật lấy mẫu lại Bootstrap.

---

#### 4. Kết quả & Đóng góp chính (Results & Takeaways)
* **Main result:**
  1. **Quy mô khủng hoảng toàn cầu:** Data Leakage xảy ra phổ biến ở cả 17 ngành khoa học được khảo sát, ảnh hưởng trực tiếp đến ít nhất **294 bài báo khoa học**. Các bài báo vi phạm leakage thường tạo ra headline rất kêu và được trích dẫn nhiều hơn hẳn các bài báo tái lặp chuẩn mực.
  2. **Kết quả sụp đổ của các mô hình ML phức tạp khi sửa lỗi Leakage (Case Study Dự đoán Nội chiến):**
     * Cả **4/4 bài báo** đăng trên các tạp chí top-10 ngành Khoa học Chính trị tuyên bố các mô hình ML phức tạp (Random Forests, AdaBoost, Gradient Boosted Trees) vượt trội hơn hẳn Logistic Regression **ĐỀU BỊ LỖI DATA LEAKAGE nghiêm trọng**.
     * Khi các lỗi leakage được sửa chữa: Các mô hình ML phức tạp **KHÔNG CÒN VƯỢT TRỘI HƠN** mô hình Logistic Regression (LR) truyền thống từ hàng thập kỷ trước.
     * Cụ thể: Trong nghiên cứu của Wang et al., chênh lệch AUC ban đầu báo cáo AdaBoost vượt trội hơn LR là **0.14** (AUC ~ 0.88 vs 0.74), nhưng sau khi sửa lỗi leakage, chênh lệch này **sụt giảm xuống chỉ còn 0.01** (AUC của cả hai mô hình đều xoay quanh ~0.75).
  3. **Đề xuất Hệ thống Phân loại 8 dạng Data Leakage (Taxonomy):**
     * **[L1] Không phân tách sạch tập Train và Test (Lack of clean separation):**
       * `L1.1` Không có tập test riêng (Overfitting giáo khoa - dùng chung dữ liệu cho train và test).
       * `L1.2` Tiền xử lý trên toàn bộ dataset (Thực hiện Imputation, Normalization, Oversampling/SMOTE trên cả Train + Test trước khi split).
       * `L1.3` Chọn đặc trưng (Feature Selection) trên toàn bộ dataset trước khi split.
       * `L1.4` Trùng lặp dữ liệu (Duplicates) tồn tại đồng thời ở cả tập Train và Test.
     * **[L2] Sử dụng đặc trưng không hợp lệ (Illegitimate Features):**
       * Mô hình sử dụng các biến đặc trưng thực chất là đại diện/hệ quả (proxy) của biến mục tiêu (ví dụ: dùng việc uống thuốc huyết áp để dự đoán bệnh cao huyết áp).
     * **[L3] Tập Test không đại diện cho phân phối khoa học quan tâm (Test set not drawn from target distribution):**
       * `L3.1` Temporal Leakage: Dùng dữ liệu tương lai trong tập Train để dự đoán sự kiện trong quá khứ ở tập Test.
       * `L3.2` Sự phụ thuộc giữa tập Train và Test (Non-independence): Đưa các quan sát từ cùng một bệnh nhân, cùng một họ protein, hoặc cùng một cụm vào cả tập Train và Test.
       * `L3.3` Bias trong chọn mẫu tập Test (Sampling/Selection Bias): Loại bỏ các trường hợp ranh giới (borderline cases) khó dự đoán khỏi tập Test hoặc chỉ test trên 1 bệnh viện nhưng kết luận cho toàn bộ dân số.
  4. **Giới thiệu công cụ Model Info Sheets:** Đề xuất bộ câu hỏi chuẩn hóa 21 mục giúp các tác giả và phản biện viên (reviewers) kiểm soát minh bạch toàn bộ pipeline ML trước khi công bố.

* **Điểm cần lưu ý:**
  1. **Sự khác biệt về bối cảnh chống Leakage (Science vs. Contests/Engineering):**
     * Trong các cuộc thi (Kaggle), tập Test được bên thứ 3 giữ kín hoàn toàn. Trong khi trong nghiên cứu khoa học (ML-based science), nhà nghiên cứu nắm toàn bộ dataset nên rất dễ vô tình/cố ý làm rò rỉ thông tin tập test vào quá trình huấn luyện.
     * Trong kỹ thuật sản phẩm (Engineering), việc deploy thử nghiệm thực tế có thể phát hiện leakage; nhưng trong ML-based science, các kết luận khoa học phụ thuộc hoàn toàn vào con số báo cáo trên tập test.
  2. **Thiếu kiểm định ý nghĩa thống kê (Lack of Significance Testing):** 9/12 bài báo trong case study không thực hiện bất kỳ kiểm định thống kê nào hoặc không tính khoảng tin cậy. Khi kích thước mẫu nhỏ (ví dụ chỉ có 11 vụ bùng phát nội chiến), khoảng tin cậy AUC rất rộng (0.66 - 0.95), khiến các tuyên bố "vượt trội" trở nên hoàn toàn không có ý nghĩa thống kê ($p > 0.14$).
  3. **Cạm bẫy Hype & Publication Bias:** Tâm lý sùng bái các mô hình ML phức tạp khiến các tạp chí ưu tiên đăng bài có kết quả "đột phá", vô tình tạo ra chu kỳ phản hồi thổi phồng (feedback loop of overoptimism) ủng hộ các kết quả kém tái lặp.

---

#### 5. Giá trị thực tiễn cho Đề tài NCKH của Nhóm (Team Application)

* **Nhóm có thể học/kế thừa gì?:**
  1. **Sử dụng Taxonomy 8 dạng Leakage làm bảng kiểm tra (Checklist):** Áp dụng trực tiếp bộ phân loại `L1.1` đến `L3.3` để rà soát toàn bộ code và pipeline thực nghiệm của nhóm, đảm bảo không mắc bất kỳ lỗi tiền xử lý hay chia dữ liệu nào.
  2. **Điền bảng Model Info Sheets (21 câu hỏi):** Đưa bảng trả lời Model Info Sheets vào phần Phụ lục (Supplementary Materials) của bài báo/báo cáo NCKH của nhóm để khẳng định tính minh bạch và minh chứng thực nghiệm "sạch".
  3. **Quy tắc vàng trong Pre-processing:** Tất cả các bước: `fit_transform` (Imputation, MinMaxScaler, StandardScaler), `Oversampling` (SMOTE), `Feature Selection` (PCA, RFE, SelectKBest) **BẮT BUỘC CHỈ ĐƯỢC THỰC HIỆN TRÊN TẬP TRAIN**, sau đó mới dùng tham số đó để `transform` trên tập Validation/Test.
  4. **Bắt buộc kiểm định thống kê và tính khoảng tin cậy (Confidence Interval):** Khi so sánh mô hình mới của nhóm với Baseline, không chỉ báo cáo con số trung bình mà phải kèm theo kiểm định thống kê (Wilcoxon, Z-test) và khoảng tin cậy 95% Bootstrap.

* **Liên quan/giúp gì cho đề tài nhóm?:**
  1. **Bằng chứng khoa học cấp cao nhất (Patterns - Cell Press 2023):** Cung cấp tài liệu tham khảo thẩm quyền nhất để dẫn chứng trong bài báo/đề tài về mối nguy của Data Leakage và lý do nhóm lựa chọn thiết kế thực nghiệm chặt chẽ.
  2. **Luận cứ bảo vệ thiết kế chia dữ liệu (Chronological & Block Split):** Giúp nhóm tự tin giải trình và bảo vệ trước Hội đồng NCKH lý do tại sao nhóm không dùng K-Fold Random CV hay SMOTE trên toàn bộ dataset mà bắt buộc tuân thủ thứ tự thời gian/cụm độc lập.
  3. **Bài học cảnh giác trước Baseline cổ điển:** Nhắc nhở nhóm luôn phải so sánh mô hình ML phức tạp với các Baseline đơn giản nhưng chuẩn mực (như Logistic Regression, Median baseline). Nếu mô hình ML phức tạp chỉ nhỉnh hơn không đáng kể ($p > 0.05$), cần thẳng thắn thừa nhận giới hạn dự đoán của bài toán.
