# 📖 BẢNG TRA CỨU THUẬT NGỮ CHUYÊN SÂU (GLOSSARY) - BÀI BÁO GPT2SP & ƯỚC LƯỢNG STORY POINT TRONG AGILE

Tài liệu này cung cấp định nghĩa chuẩn xác, giải thích ngữ cảnh học thuật và đối chiếu Anh - Việt cho toàn bộ các khái niệm, mô hình, thang đo và thuật toán xuất hiện trong công trình:
> **Fu, M., & Tantithamthavorn, C. (2023). "GPT2SP: A Transformer-Based Agile Story Point Estimation Approach."** *IEEE Transactions on Software Engineering (TSE)*, 49(5), 3169–3185. DOI: [10.1109/TSE.2023.3241517](https://doi.org/10.1109/TSE.2023.3241517).

---

## 📑 MỤC LỤC TRA CỨU NHANH

1. [Quy Trình Quản Trị Agile & Ước Lượng Nỗ Lực (Agile & Effort Estimation)](#1-quy-trình-quản-trị-agile--ước-lượng-nỗ-lực)
2. [Xử Lý Ngôn Ngữ Tự Nhiên & Tokenization (NLP & Tokenization)](#2-xử-lý-ngôn-ngữ-tự-nhiên--tokenization)
3. [Kiến Trúc Học Sâu & Transformers (Deep Learning & Transformers)](#3-kiến-trúc-học-sâu--transformers)
4. [Kịch Bản Thực Nghiệm & Mô Hình Đối Chứng (Scenarios & Baselines)](#4-kịch-bản-thực-nghiệm--mô-hình-đối-chứng)
5. [Thang Đo Đánh Giá & Kiểm Định Thống Kê (Evaluation Metrics & Statistics)](#5-thang-đo-đánh-giá--kiểm-định-thống-kê)
6. [Trí Tuệ Nhân Tạo Có Thể Giải Thích (Explainable AI - XAI)](#6-trí-tuệ-nhân-tạo-có-thể-giải-thích-explainable-ai---xai)
7. [Tính Toàn Vẹn Thực Nghiệm & Rò Rỉ Dữ Liệu (Scientific Rigor & Leakage Control)](#7-tính-toàn-vẹn-thực-nghiệm--rò-rỉ-dữ-liệu)

---

## 1. Quy Trình Quản Trị Agile & Ước Lượng Nỗ Lực

### 🔹 Story Point (SP - Điểm Câu Chuyện)
* **Định nghĩa:** Đơn vị đo lường tương đối (relative metric) thể hiện tổng nỗ lực (overall effort) cần thiết để hoàn thành trọn vẹn một hạng mục công việc (Product Backlog Item / Issue).
* **Bản chất:** Story Point không đại diện đơn thuần cho số giờ công (person-hours), mà là sự tổng hòa của 4 yếu tố:
  1. **Khối lượng công việc (Amount of work):** Độ dài và quy mô tác vụ.
  2. **Độ phức tạp kỹ thuật (Technical complexity):** Mức độ phức tạp của logic nghiệp vụ và kiến trúc hệ thống.
  3. **Rủi ro (Risk):** Nguy cơ phát sinh lỗi, phụ thuộc thư viện bên ngoài.
  4. **Độ bất định (Uncertainty):** Mức độ chưa rõ ràng của yêu cầu người dùng.
* **Quy ước giá trị:** Thường sử dụng dãy số Fibonacci điều chỉnh: $1, 2, 3, 5, 8, 13, 20, 40, 100$.

### 🔹 Product Backlog Item (PBI) / Issue
* **Định nghĩa:** Hạng mục công việc được ghi nhận trong hệ thống quản lý Jira (User Story, Task, Bug, Epic, Improvement). Trong bài báo GPT2SP, mỗi issue được biểu diễn qua hai trường thông tin văn bản chính: **Title** (tiêu đề tóm tắt) và **Description** (mô tả chi tiết yêu cầu).

### 🔹 Sprint Planning & Backlog Refinement
* **Backlog Refinement (Tinh gọn Backlog):** Buổi họp định kỳ giữa Product Owner và Development Team nhằm rà soát, phân rã các yêu cầu lớn (Epic) thành các User Story nhỏ hơn và ước lượng sơ bộ.
* **Sprint Planning (Lập kế hoạch Sprint):** Đội ngũ cam kết số lượng Story Point đưa vào Sprint Backlog dựa trên vận tốc lịch sử (historical velocity) của nhóm.

### 🔹 Planning Poker
* **Định nghĩa:** Phương pháp ước lượng nỗ lực dựa trên sự đồng thuận của nhóm (consensus-based). Các thành viên giấu bài, đồng loạt lật thẻ điểm để tránh hiện tượng "neo mỏ neo tâm lý" (anchoring bias), sau đó thảo luận về các mức điểm quá lệch để đi đến thống nhất.
* **Hạn chế trong bài báo:** Mang nặng tính chủ quan của chuyên gia, dễ bị ảnh hưởng bởi áp lực thời gian và động lực nhóm, dẫn đến ước lượng sai lệch (overestimate hoặc underestimate).

---

## 2. Xử Lý Ngôn Ngữ Tự Nhiên & Tokenization

### 🔹 Subword Tokenization (Phân tách từ cấp độ từ con)
* **Khái niệm:** Kỹ thuật chia văn bản thành các đơn vị trung gian giữa từ hoàn chỉnh (word) và ký tự đơn lẻ (character).
* **Vấn đề của Deep-SE:** Deep-SE dùng Word-level Tokenization, tạo ra kho từ vựng khổng lồ (185.625 từ duy nhất), gây bùng nổ chiều không gian ma trận và không thể biểu diễn các từ mới xuất hiện ngoài tập huấn luyện (Out-of-Vocabulary - OOV).
* **Giải pháp của GPT2SP:** Dùng thuật toán **Byte-Pair Encoding (BPE)**. Các từ thông dụng được giữ nguyên vẹn (ví dụ: `database`, `test`), trong khi các từ hiếm gặp hoặc thuật ngữ chuyên ngành lạ được phân rã thành các mẩu subword thông dụng (ví dụ: `Unstoppable` $\rightarrow$ `Un` + `stoppable`).

### 🔹 Out-of-Vocabulary (OOV)
* **Hiện tượng:** Mô hình gặp các từ vựng mới trong tập kiểm thử (Test Set) mà chưa từng thấy trong tập huấn luyện (Train Set). Mô hình dùng Word-level Tokenization buộc phải thay thế bằng token lạ `<UNK>`, làm mất hoàn toàn thông tin ngữ nghĩa. BPE giải quyết triệt để vấn đề này.

### 🔹 Word & Positional Encoding
* **Word Encoding ($W_{te}$):** Ánh xạ chỉ số token vào không gian vector ngữ nghĩa $d=768$.
* **Positional Encoding ($W_{pe}$):** Vì Transformer xử lý song song toàn bộ chuỗi chứ không duyệt tuần tự như RNN/LSTM, vector vị trí được cộng trực tiếp vào vector từ để mô hình nắm bắt thứ tự xuất hiện của từ trong câu:
  $$\mathbf{e}_i = \mathbf{w}_i + \mathbf{p}_i$$

---

## 3. Kiến Trúc Học Sâu & Transformers

### 🔹 Foundation Model & Pre-trained Language Model (PLM)
* **Định nghĩa:** Mô hình ngôn ngữ quy mô lớn được tiền huấn luyện không giám sát (unsupervised pre-training) trên kho văn bản khổng lồ (GPT-2 được huấn luyện trên tập WebText gồm 40GB văn bản từ 8 triệu trang web), sau đó tinh chỉnh (fine-tuning) cho tác vụ chuyên biệt hạ nguồn.

### 🔹 GPT-2 (Generative Pre-trained Transformer 2)
* **Kiến trúc:** Decoder-only Transformer gồm các khối xếp chồng (Stack of Decoder Blocks). Trong bài báo GPT2SP, nhóm tác giả sử dụng biến thể **GPT-2 Small**:
  * Số tầng (Layers/Blocks): $L = 12$
  * Chiều ẩn (Hidden Dimension): $d = 768$
  * Số đầu chú ý (Attention Heads): $H = 12$
  * Tổng tham số: $\approx 117$ triệu tham số ($117\text{M}$).
  * Chiều mỗi đầu chú ý: $d_{kv} = 768 / 12 = 64$.

### 🔹 Masked Multi-Head Self-Attention
* **Cơ chế:** Tính toán mối liên hệ phụ thuộc ngữ cảnh giữa mọi cặp từ trong câu bằng công thức Scaled Dot-Product Attention:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
* **Masked:** Đảm bảo quá trình xử lý không nhìn trước thông tin tương lai trong chuỗi sinh sinh, bảo toàn tính nhân quả (causality).

### 🔹 MLP Regressor & L1 Loss (Head Hồi Quy)
* **Regression Head:** Lớp Perceptron đa tầng (Multi-Layer Perceptron) nhận vector trạng thái ẩn từ token cuối cùng của khối Transformer thứ 12 để ánh xạ thành một giá trị thực vô hướng (Scalar Value) đại diện cho Story Point ước lượng.
* **L1 Loss (Mean Absolute Error Loss):**
  $$\mathcal{L}_{L1}(\theta) = \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
  Hàm mất mát L1 giúp mô hình kháng lại các giá trị ngoại lai (outliers) tốt hơn đáng kể so với MSE ($L_2$).

### 🔹 AdamW Optimizer
* Thuật toán tối ưu hóa kết hợp giữa thuật toán thích nghi độ dốc (Adam) và kỹ thuật suy giảm trọng số tách rời (Decoupled Weight Decay), giúp mô hình tổng quát hóa tốt hơn và tránh hiện tượng quá khớp (overfitting) trên dữ liệu phần mềm. Tác giả sử dụng learning rate $\text{LR} = 5 \times 10^{-4}$.

---

## 4. Kịch Bản Thực Nghiệm & Mô Hình Đối Chứng

### 🔹 Within-Project Estimation (Ước lượng Nội dự án - RQ1)
* Mô hình được huấn luyện và kiểm thử trên **cùng một dự án** phần mềm (sử dụng tỷ lệ phân chia tuần tự hoặc ngẫu nhiên $60\%$ Train, $20\%$ Validation, $20\%$ Test).

### 🔹 Cross-Project Estimation (Ước lượng Liên dự án - RQ2)
* Mô hình được huấn luyện trên một **dự án nguồn (Source Project)** và mang đi dự đoán trực tiếp trên một **dự án đích (Target Project)** hoàn toàn xa lạ mà không được huấn luyện lại.
  * **Within-Repository:** Dự án nguồn và đích cùng một tổ chức (ví dụ: `Apache Mesos` $\rightarrow$ `Apache Usergrid`).
  * **Cross-Repository:** Dự án nguồn và đích thuộc hai tổ chức khác biệt hoàn toàn (ví dụ: `Talend Data Quality` $\rightarrow$ `Appcelerator Studio`).

### 🔹 Deep-SE (Choetkiertikul et al., 2019)
* Phương pháp SOTA trước GPT2SP: Kết hợp Word2Vec + Long Short-Term Memory (LSTM) + Recurrent Highway Network (RHWN). Hạn chế: Phải tự tiền huấn luyện Word2Vec cho từng dự án (mất 2-7 giờ/dự án), phụ thuộc ngữ cảnh cục bộ của LSTM và không thể giải thích.

### 🔹 ABE0 (Analogy-Based Estimation)
* Phương pháp ước lượng dựa trên tương đồng kinh điển: Tìm kiếm các issue trong quá khứ có độ tương đồng văn bản cao nhất (dùng khoảng cách Euclidean/Cosine) và lấy Story Point tương ứng làm giá trị ước lượng.

### 🔹 Baseline Thống Kê Cơ Sở (Mean / Median Baseline)
* **Mean Effort:** Dự đoán Story Point bằng trung bình cộng của toàn bộ các issue trong tập huấn luyện.
* **Median Effort:** Dự đoán Story Point bằng trung vị của tập huấn luyện. Đây là baseline tối quan trọng để kiểm tra xem một mô hình học máy phức tạp có thực sự học được tri thức hữu ích hay chỉ đoán quanh giá trị trung tâm.

---

## 5. Thang Đo Đánh Giá & Kiểm Định Thống Kê

### 🔹 Mean Absolute Error (MAE - Sai Số Tuyệt Đối Trung Bình)
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$
Thang đo chính được bài báo GPT2SP và Deep-SE sử dụng để đo lường độ lệch trung bình giữa điểm ước lượng và điểm thực tế.

### 🔹 Median Absolute Error (MdAE - Sai Số Tuyệt Đối Trung Vị)
$$\text{MdAE} = \text{median}\left(\{|y_1 - \hat{y}_1|, |y_2 - \hat{y}_2|, \dots, |y_N - \hat{y}_N|\}\right)$$
Độ đo trung vị của sai số tuyệt đối, không bị lệch bởi các giá trị ngoại lai cực đoan (outliers).

### 🔹 Standardised Accuracy (SA - Độ Chính Xác Chuẩn Hóa)
$$\text{SA} = \left(1 - \frac{\text{MAE}_{\text{model}}}{\text{MAE}_{\text{random}}}\right) \times 100\%$$
Đo lường mức độ cải thiện của mô hình so với việc đoán ngẫu nhiên (Random Guessing). Giá trị $\text{SA} > 0$ chứng minh mô hình hoạt động tốt hơn đoán mò; $\text{SA} \le 0$ đồng nghĩa mô hình vô giá trị.

### 🔹 Wilcoxon Signed-Rank Test
* Kiểm định thống kê phi tham số (non-parametric test) dành cho dữ liệu bắt cặp (paired data), kiểm tra xem sự khác biệt về sai số giữa GPT2SP và mô hình đối chứng có ý nghĩa thống kê thực sự hay chỉ do ngẫu nhiên ($p$-value $< 0.05$).

### 🔹 Cliff's Delta ($\delta$ - Kích Thước Hiệu Ứng)
* Độ đo phi tham số định lượng mức độ vượt trội giữa hai phân phối sai số:
  * $|\delta| < 0.147$: Không đáng kể (Negligible).
  * $0.147 \le |\delta| < 0.33$: Nhỏ (Small).
  * $0.33 \le |\delta| < 0.474$: Trung bình (Medium).
  * $|\delta| \ge 0.474$: Lớn (Large).

### 🔹 Scott-Knott ESD (Effect Size Difference)
* Thuật toán phân cụm thống kê thứ bậc kết hợp kiểm định giả thuyết và kích thước hiệu ứng Cliff's Delta, giúp nhóm các mô hình có hiệu năng tương đương vào cùng một Rank (Rank-1, Rank-2...) mà không bị trùng lặp phân cụm.

---

## 6. Trí Tuệ Nhân Tạo Có Thể Giải Thích (Explainable AI - XAI)

### 🔹 Self-Attention Weights (Trọng Số Chú Ý)
* Ma trận trọng số chú ý được trích xuất từ các đầu chú ý của Transformer, thể hiện mức độ một từ tập trung sự chú ý vào các từ khác trong câu khi đưa ra dự đoán.

### 🔹 Integrated Gradients (Gradient Tích Phân)
* Phương pháp gán thuộc tính đặc trưng theo nguyên lý tiên đề (axiomatic feature attribution method). Thuật toán tính tích phân các đạo hàm riêng của hàm dự đoán theo đường thẳng nối từ một vector cơ sở (baseline/zero embedding) tới vector đầu vào thực tế, đảm bảo hai nguyên lý: **Completeness** (tổng đóng góp bằng sai khác dự đoán) và **Implementation Invariance**.

### 🔹 Word Attribution Score (Điểm Đóng Góp Của Từ)
* Điểm số định lượng đo lường mức độ một từ ngữ cụ thể (ví dụ: `memory leak`, `crash`, `refactor`) đóng góp tích cực hay tiêu cực vào quyết định nâng hoặc hạ Story Point của issue.

### 🔹 Supporting Examples (Ví Dụ Minh Chứng Lịch Sử)
* Cơ chế của công cụ GPT2SP XAI: Khi đưa ra ước lượng cho một issue mới, mô hình truy xuất ngược lại từ tập huấn luyện quá khứ các issue có chứa cùng từ khóa quan trọng và có cùng mức Story Point tương ứng nhằm thuyết phục lập trình viên tin tưởng quyết định của AI.

---

## 7. Tính Toàn Vẹn Thực Nghiệm & Rò Rỉ Dữ Liệu

> [!CAUTION]
> **Đây là trọng tâm phân tích phản biện khoa học của Đề tài Nghiên cứu Nhóm 3 (NCKH Johnny Snowflake), vượt trên các giả định ngây thơ của bài báo gốc GPT2SP.**

### 🔹 Temporal Leakage (Rò Rỉ Thời Gian)
* **Khái niệm:** Lỗi phương pháp luận nghiêm trọng khi đưa các thông tin chỉ xuất hiện **SAU** thời điểm ước lượng (`SP_Estimation_Date`) vào làm đầu vào dự đoán mô hình.
* **Lỗ hổng trong GPT2SP:** Bài báo GPT2SP lấy toàn bộ Text mô tả tĩnh từ file CSV kết xuất lúc kết thúc dự án. Nhiều mô tả này đã được lập trình viên chỉnh sửa, bổ sung nguyên nhân gốc rễ (root cause) hoặc bản vá (patch details) trong quá trình sửa lỗi, làm mô hình ước lượng "dễ hơn thực tế" một cách phi thực tế.

### 🔹 Data Leakage do Phân Chia Ngẫu Nhiên (Random Split Leakage)
* **Khái niệm:** Phân chia tập Train/Test ngẫu nhiên thay vì phân chia theo dòng thời gian (Time-based Split / Chronological Split). Mô hình được huấn luyện trên dữ liệu tương lai (ví dụ: issue năm 2016) để dự đoán dữ liệu quá khứ (issue năm 2014), phá vỡ bản chất nhân quả của quy trình Agile trong thực tế.

### 🔹 Planning-Time Estimation
* **Nguyên tắc cốt lõi của Đề tài Nhóm 3:** Mọi vector đặc trưng (Title, Description, Metadata, Dependency Graph) phải được **tái dựng lịch sử (Historical State Reconstruction)** quay ngược về đúng thời khắc `SP_Estimation_Date` thông qua bảng `CHANGE_LOG` của CSDL TAWOS v1.1.
