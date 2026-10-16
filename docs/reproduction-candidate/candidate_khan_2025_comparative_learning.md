# BÁO CÁO TÁI LẬP (REPRODUCTION CANDIDATE) — KHAN 2025
> **Paper:** Efficient Story Point Estimation With Comparative Learning (arXiv:2507.14642 [cs.SE])

---

## 📌 1. Phải xác định chính xác cái gì của paper để tái lập?
* **Mục tiêu tái lập:** Tái lập thực nghiệm mô hình học máy theo khung tiếp cận **Học so sánh cặp (Pairwise Comparative Learning Framework)** đối với các User Story trong Agile, nhằm so sánh độ tương quan thứ hạng nỗ lực thay vì dự đoán giá trị điểm số tuyệt đối.
* **Câu hỏi nghiên cứu kiểm chứng:** Liệu việc chuyển bài toán ước lượng Story Point từ dạng hồi quy điểm số tuyệt đối (Absolute Direct Rating) sang so sánh cặp đôi (Relative Pairwise Judgments) có giúp cải thiện độ tin cậy và đạt tương quan thứ hạng cao hơn các mô hình hồi quy truyền thống trên tập dữ liệu chuẩn hay không?

---

## 📑 2. Thông tin bài báo & Tác giả (Paper & Metadata)
* **Tên bài báo:** *Efficient Story Point Estimation With Comparative Learning*
* **Tác giả:** Monoshiz Mahbub Khan, Xiaoyin Xi, Andrew Meneely, Yiming Tang, and Zhe Yu (RIT & UMBC)
* **Nơi xuất bản:** *arXiv preprint arXiv:2507.14642 [cs.SE]* (Công bố 07/2025; Đang nộp tại các hội thảo hàng đầu về Kỹ nghệ phần mềm ESEM / SANER)
* **Preprint / Link:** [arXiv:2507.14642](https://arxiv.org/abs/2507.14642)
* **Xếp hạng học thuật (Tier):** **Tier 2 (A)** — Nghiên cứu mới hướng đến hội thảo Rank A (CORE Rank A: ESEM / SANER).
* **Điểm đánh giá tái lập:** **89 / 100 điểm** (Ứng viên ưu tiên số 3 - Ý tưởng mới đột phá ngoài repo).

---

## 🎯 3. Tại sao chọn bài báo này? (Rationale)
1. **Bài báo nằm ngoài repo GitHub hiện tại của nhóm:** Đây là hướng nghiên cứu hoàn toàn mới, mang tính mở rộng xuất sắc cho danh mục tài liệu nghiên cứu của nhóm.
2. **Khắc phục nhược điểm cốt lõi của Story Point:** Trong thực tế Agile, lập trình viên thường bất đồng về giá trị tuyệt đối (1 task là 3 hay 5 SP), nhưng rất dễ đồng thuận rằng: *"Task A phức tạp hơn Task B"*. Phương pháp Comparative Learning mô phỏng chính xác tâm lý này.
3. **Mã nguồn hoàn chỉnh & Dữ liệu tương thích 100%:** Tác giả cung cấp toàn bộ code trên GitHub và thực nghiệm trực tiếp trên 16 dự án Choetkiertikul — hoàn toàn trùng khớp với dữ liệu TAWOS mà nhóm đang có.
4. **Mở ra hướng nghiên cứu mới:** Nếu kết hợp Comparative Learning với cơ chế kiểm soát rò rỉ thời gian (Planning-Time Snapshot của Nhóm 3), đây sẽ là một đóng góp rất sáng tạo cho đề tài.

---

## 🔍 4. Thiết lập bài toán tái lập (Task Reproduced)
* **Dataset & Đường dẫn dữ liệu (Data Links):** 
  * 16 dự án mã nguồn mở (tập Choetkiertikul / TAWOS) với **23.313 issues** có Story Point.
  * **Link Dữ liệu Gốc GitHub:** [morakotch/datasets (GitHub)](https://github.com/morakotch/datasets) | [SOLAR-group/TAWOS (GitHub)](https://github.com/SOLAR-group/TAWOS)
  * **Link HuggingFace Mirror:** [giseldo/deep-se (HuggingFace Datasets)](https://huggingface.co/datasets/giseldo/deep-se)
* **Mã nguồn & Replication Package (Code Links):**
  * **GitHub Official Package:** [hil-se/EfficientSPEComparativeLearning (GitHub)](https://github.com/hil-se/EfficientSPEComparativeLearning)
* **Target / Ground Truth:** 
  * Phán đoán thứ tự ưu tiên nỗ lực giữa 2 User Story: $Story_A \succ Story_B$ (Story A tốn nhiều effort hơn Story B).
* **Baseline / Model:**
  * **Model tái lập:** **Comparative Learning Classifier** (biểu diễn cặp văn bản qua text embeddings, đưa qua mô hình phân loại nhị phân cặp để suy ra thứ hạng nỗ lực).
  * **Baselines đối chứng:** Standard Regression Models (Direct Rating: Ridge Regression, Random Forest, SBERT Regressor).
* **Data Split:**
  * Tạo các cặp $(Story_i, Story_j)$ từ tập Train và Test được chia theo Chronological Split để đảm bảo tính thực tế.
* **Metrics đánh giá:**
  * **Spearman's Rank Correlation Coefficient ($\rho$):** Đo mức độ tương quan thứ hạng giữa nỗ lực dự báo và nỗ lực thực tế.
  * **Pairwise Classification Accuracy:** Tỷ lệ đoán đúng cặp task nào tốn nhiều effort hơn.

---

## 📊 5. Kết quả cụ thể muốn tái lập & Kỳ vọng khoa học (Targeted Results & Expectations)
* **Phạm vi tái lập cụ thể:** Chạy tái lập pipeline huấn luyện mô hình so sánh cặp trên 2 dự án tiêu biểu (**Spring XD** và **Mesos**) để lấy chỉ số tương quan thứ hạng.
* **Kết quả chính trong bài báo công bố:**
  * Mô hình huấn luyện bằng Comparative Judgments đạt **Spearman's correlation trung bình là 0.34**, ngang ngửa hoặc vượt qua các mô hình hồi quy trực tiếp trên điểm tuyệt đối.
  * Giảm đáng kể thời gian gán nhãn và tăng mức độ đồng thuận của đội ngũ phát triển.
* **Mục tiêu nhóm cần tái lập:** Chạy mã nguồn của tác giả để tái tạo lại hệ số tương quan Spearman và kiểm tra xem khi áp dụng lọc dữ liệu trước mốc planning thì hiệu năng so sánh cặp thay đổi ra sao.
* **🎯 Kỳ vọng đạt được nếu tái lập & mở rộng thành công:**
  * **Xếp hạng hội nghị / Tạp chí kỳ vọng:** 
    * **Hội thảo Quốc tế:** **ACM/IEEE International Conference on Software Engineering (ICSE - CORE Rank A* / Poster/Artifact Track)** hoặc **IEEE/ACM ESEM (CORE Rank A)**.
    * **Tạp chí Quốc tế:** **Journal of Systems and Software (JSS - Q1/Tier 2)**.
  * **Giá trị đóng góp đề tài:** Tạo ra một hướng tiếp cận đột phá khi tích hợp: *Học so sánh cặp (Comparative Learning)* + *Kiểm soát rò rỉ thời gian (Temporal Leakage Control)*, nâng cao tính khả thi của mô hình khi triển khai vào các buổi họp Sprint Planning thực tế.

---

## 🛠️ 6. Khả năng tái lập: Công cụ, Thời gian & Dự kiến Khó / Dễ

| Tiêu chí | Chi tiết đánh giá |
| :--- | :--- |
| **Dữ liệu (Data)** | **Có sẵn 100% trực tuyến:** Dùng chung 16 dự án Choetkiertikul/TAWOS có sẵn link GitHub và local DB. |
| **Mã nguồn (Code)** | **Có sẵn 100% trực tuyến:** Repo GitHub `hil-se/EfficientSPEComparativeLearning` cung cấp đầy đủ script. |
| **Công cụ & Môi trường cần thiết** | • **Ngôn ngữ:** Python 3.9+<br>• **Thư viện AI/ML:** `scikit-learn`, `sentence-transformers`, `torch`, `scipy`, `pandas`, `numpy`<br>• **Phần cứng:** Google Colab GPU (Tesla T4) hoặc Máy tính cá nhân (16GB RAM + CPU đa nhân). |
| **Thời gian tái lập dự kiến** | • **Sinh tập cặp dữ liệu (Pair Generation):** ~1 – 2 giờ.<br>• **Huấn luyện & Đánh giá Spearman Correlation:** ~2 – 4 giờ.<br>• **Tổng thời gian hoàn thiện:** **2 – 3 ngày làm việc**. |
| **Độ thuận lợi (Dễ)** | Code viết bằng thư viện Machine Learning và PyTorch chuẩn mực, cấu trúc module rõ ràng. |
| **Thách thức (Khó)** | Độ phức tạp số lượng cặp $O(N^2)$ có thể gây tràn bộ nhớ (RAM) nếu không áp dụng kỹ thuật Pair Subsampling hợp lý. |

---

## 🔄 7. Quy trình Thực hiện Tái lập (End-to-End Workflow: Từ Input đến Output)

Quy trình tái lập mô hình Học so sánh cặp (Comparative Learning) theo Khan et al. (2025) được tổ chức theo 5 bước logic:

```
[Input: Tập User Stories có nhãn Story Point]
                       │
                       ▼
[Bước 1: Chia tập theo thời gian & Sinh cặp so sánh (Pair Generation)]
                       │
                       ▼
[Bước 2: Trích xuất Text Embedding (SBERT / Sentence-Transformers)]
                       │
                       ▼
[Bước 3: Huấn luyện Mô hình Phân loại Cặp đôi (Pairwise Classifier)]
                       │
                       ▼
[Bước 4: Suy luận Thứ hạng Toàn cục (Global Rank Inference)]
                       │
                       ▼
[Output: Đánh giá Tương quan Spearman & Bảng So sánh Baselines]
```

### 🔹 Bước 1: Tiếp nhận Input, Phân chia & Sinh Cặp So sánh (Pair Sampling)
* **Đầu vào (Input):** Danh sách các issues từ tập Spring XD / Choetkiertikul (văn bản `title + description` và giá trị nhãn Story Point $y_i$).
* **Thao tác thực hiện:**
  1. Phân chia Train / Test theo Chronological Split (60% Train / 40% Test hoặc 60/20/20).
  2. **Sinh cặp so sánh nỗ lực (Pairwise Sampling):** Với 2 issues bất kỳ $(Story_i, Story_j)$:
     * Nếu $y_i > y_j \rightarrow$ Nhãn cặp $z_{ij} = 1$ ($Story_i$ tốn nhiều công sức hơn $Story_j$).
     * Nếu $y_i < y_j \rightarrow$ Nhãn cặp $z_{ij} = 0$ ($Story_i$ tốn ít công sức hơn $Story_j$).
     * Nếu $y_i = y_j \rightarrow$ Có thể loại bỏ (tie filtering) hoặc gán nhãn trung lập.
  3. Để tránh bùng nổ tổ hợp $O(N^2)$ mẫu làm tràn bộ nhớ, áp dụng kỹ thuật **Random Pair Subsampling** (lấy mẫu ngẫu nhiên $K$ cặp cho mỗi issue, thường $K \approx 10 - 20$).
* **Đầu ra bước 1:** Tập dữ liệu các cặp so sánh $D_{pair} = \{ (Story_i, Story_j, z_{ij}) \}$.

### 🔹 Bước 2: Mã hóa Ngữ nghĩa Văn bản (Text Embedding)
* **Đầu vào:** Văn bản của từng cặp $(Story_i, Story_j)$.
* **Thao tác thực hiện:**
  1. Sử dụng mô hình tiền huấn luyện **Sentence-BERT (`all-MiniLM-L6-v2` hoặc `all-mpnet-base-v2`)**.
  2. Biểu diễn mỗi User Story thành vector nhúng ngữ nghĩa chiều cố định:
     $v_i = \text{SBERT}(Story_i) \in \mathbb{R}^d$ và $v_j = \text{SBERT}(Story_j) \in \mathbb{R}^d$.
  3. Tạo vector đặc trưng biểu diễn quan hệ giữa 2 task:
     $$x_{ij} = [v_i, v_j, v_i - v_j, v_i \odot v_j]$$
     (kết hợp nối vector, vector hiệu và tích phần tử Hadamard).
* **Đầu ra bước 2:** Ma trận đặc trưng cặp $X_{pair}$ và nhãn nhị phân $Z_{pair}$.

### 🔹 Bước 3: Huấn luyện Bộ Phân loại Cặp đôi (Pairwise Classifier)
* **Đầu vào:** Tập đặc trưng $(X_{pair}, Z_{pair})$ trên tập Train.
* **Thao tác thực hiện:**
  1. Huấn luyện bộ phân loại nhị phân (Binary Classifier: Logistic Regression, LightGBM, hoặc Mạng Nơ-ron MLP 2 lớp) để dự đoán xác suất:
     $P(Story_i \succ Story_j) = \sigma(f(x_{ij}))$.
  2. Sử dụng hàm mất mát Binary Cross-Entropy (BCE Loss).
* **Đầu ra bước 3:** Mô hình so sánh cặp đã được tối ưu hóa trọng số.

### 🔹 Bước 4: Suy luận Thứ hạng Toàn cục (Global Effort Ranking)
* **Đầu vào:** Toàn bộ các issues trong tập Test.
* **Thao tác thực hiện:**
  1. Với mỗi issue $k$ trong tập Test, cho mô hình so sánh cặp với một tập các mốc tham chiếu (anchors) hoặc so sánh chéo từng cặp trong tập Test.
  2. Tính điểm số nỗ lực tương đối (Win-rate hoặc Borda Count Score):
     $$Score_k = \frac{1}{|Test| - 1} \sum_{m \neq k} P(Story_k \succ Story_m)$$
  3. Sắp xếp thứ tự các User Story trong tập Test dựa trên $Score_k$ từ cao xuống thấp để nhận được vector thứ hạng dự báo $\hat{R}_{test}$.
* **Đầu ra bước 4:** Vector thứ hạng dự báo $\hat{R}_{test}$ và thứ hạng thực tế $R_{test}$ (xếp theo Ground Truth Story Point).

### 🔹 Bước 5: Đánh giá Tương quan & Xuất Output Báo cáo
* **Đầu vào:** Vector thứ hạng $\hat{R}_{test}$ và $R_{test}$.
* **Thao tác thực hiện:**
  1. Tính **Hệ số tương quan thứ hạng Spearman ($\rho$)**:
     $$\rho = 1 - \frac{6 \sum d_k^2}{N(N^2 - 1)}$$
     (trong đó $d_k$ là chênh lệch thứ hạng của issue thứ $k$).
  2. Đo độ chính xác phân loại cặp (Pairwise Accuracy): Tỷ lệ đoán đúng quan hệ thứ tự $Story_i \succ Story_j$.
* **Đầu ra cuối cùng (Final Output):**
  1. Bảng đối chiếu hệ số Spearman $\rho$ giữa *Comparative Learning Model* và các *Mô hình Hồi quy Tuyệt đối truyền thống (Direct Regression)*.
  2. Biểu đồ xếp hạng nỗ lực (Rank Correlation Scatter Plot).
  3. Báo cáo đánh giá mức độ giảm tải thời gian estimate trong quy trình Sprint Planning thực tế.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
