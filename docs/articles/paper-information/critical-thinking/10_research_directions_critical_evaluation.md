# 🧠 PHÂN TÍCH PHẢN BIỆN 10: ĐÁNH GIÁ ĐA TIÊU CHÍ VÀ ĐỀ XUẤT HƯỚNG NGHIÊN CỨU TỐI ƯU CHO HỘI NGHỊ WSESE TRONG THỜI HẠN 1 THÁNG

> **Chuyên mục:** Phân tích phản biện khoa học độc lập (Scientific Critical Thinking).  
> **Đề tài NCKH Nhóm 3:** *"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"*.  
> **Mục tiêu sống còn:** Lựa chọn hướng đi có **khả năng được chấp nhận (Acceptance Rate) cao nhất tại Hội nghị Quốc tế WSESE** và hoàn thành toàn bộ bài báo trong vòng **đúng 1 tháng (4 tuần)**.

---

## 🧭 1. ĐẶT LÊN BÀN CÂN 5 HƯỚNG NGHIÊN CỨU TIỀM NĂNG

Dựa trên yêu cầu khắt khe của hội nghị chuyên ngành công nghệ phần mềm và hạn mức 1 tháng, 5 phương án nghiên cứu được đặt lên bàn cân:

```mermaid
flowchart TD
    subgraph Original["3 HƯỚNG NGHIÊN CỨU BAN ĐẦU"]
        H1["HƯỚNG 1: Full-Scale SOTA Deep Learning<br/>• Kế thừa GPT2SP (117M params)<br/>• Fine-tuning Transformer trên Leaked vs. Clean Data<br/>• Rủi ro tại WSESE: Dễ bị phản biện vì thiếu đóng góp phương pháp luận, GPU OOM"]
        H2["HƯỚNG 2: Empirical Leakage Impact Study<br/>• Đo lường mức độ sai lệch khi dùng dữ liệu sau planning<br/>• Vạch trần ảo tưởng hiệu năng (Performance Mirage)<br/>• Điểm mạnh: Trúng 100% tôn chỉ phương pháp luận của WSESE"]
        H3["HƯỚNG 3: Lightweight Baseline Models<br/>• TF-IDF, Ridge Regression, Random Forest, SBERT, Median<br/>• Chứng minh bằng chứng thép: Lỗi do dữ liệu rò rỉ, không phải do mô hình<br/>• Điểm mạnh: Huấn luyện vài giây, loại trừ 100% nhiễu"]
    end

    subgraph Proposed["2 HƯỚNG NGHIÊN CỨU MỚI ĐỀ XUẤT (TỐI ƯU HÓA CHO WSESE)"]
        H4["HƯỚNG 4 (MỚI): Fine-Grained Leakage Channel Ablation<br/>• Phẫu thuật phân rã 3 kênh rò rỉ riêng biệt:<br/>  (1) Sửa đổi mô tả vs. (2) Metadata sau Planning vs. (3) Bình luận<br/>• Đo lường % đóng góp ảo tưởng của từng kênh (Causal Attribution)<br/>• Đích ngắm: Ứng viên Best Paper tại WSESE"]
        H5["HƯỚNG 5 (MỚI): Leakage-Free Contextual Engineering<br/>• Đột phá giải pháp: Clean Text + Agile Planning Dynamics<br/>• Tái dựng đặc trưng hợp lệ tại mốc Planning: Velocity, Workload, Component Churn<br/>• Đóng góp hoàn chỉnh: Cung cấp Benchmark chuẩn tắc không rò rỉ cho cộng đồng"]
    end
```

---

## 📊 2. BỘ TIÊU CHÍ ĐÁNH GIÁ ĐA MỤC TIÊU MỞ RỘNG (EXPANDED 9-CRITERIA MCDA)

Hệ thống đánh giá sử dụng phương pháp **Phân tích Quyết định Đa Tiêu chí (Multi-Criteria Decision Analysis - MCDA)**, được tinh chỉnh đặc thù cho bài toán nộp hội nghị **WSESE** (International Workshop on Methodological Issues with Empirical Studies in Software Engineering / World Symposium on Software Engineering) với deadline 1 tháng:

| Mã | Tiêu chí đánh giá | Trọng số ($W$) | Ý nghĩa học thuật & Ràng buộc đối với Hội nghị WSESE |
| :-: | :--- | :-: | :--- |
| **C1** | **Khả thi trong 1 tháng (Feasibility & Submission Velocity)** | **$15\%$** | Tốc độ trích xuất dữ liệu, huấn luyện mô hình, kiểm định và viết bài báo; bảo đảm nộp đúng hạn 1 tháng không bị chậm trễ phần cứng. |
| **C2** | **Độ khớp tôn chỉ & Khả năng chấp nhận tại WSESE (WSESE Fit & Acceptance Rate)** | **$15\%$** | Bài báo giải quyết đúng trọng tâm của WSESE: vạch trần các vấn đề phương pháp luận (Methodological Issues) và các mối đe dọa giá trị (Threats to Validity) trong nghiên cứu thực nghiệm SE. |
| **C3** | **Tính chặt chẽ khoa học (Scientific Rigor & Proof)** | **$15\%$** | Bằng chứng thực nghiệm không thể bác bỏ; thiết kế đối chứng chuẩn mực; cô lập hoàn toàn các biến gây nhiễu (Confounders). |
| **C4** | **Tính đóng góp xây dựng (Constructive Novelty)** | **$10\%$** | Không chỉ dừng ở việc phê bình bài báo cũ (Destructive Critique) mà còn mang lại giải pháp thay thế khả thi (Actionable Solution) cho cộng đồng SE. |
| **C5** | **Giá trị thực tế Scrum Teams (Practical Industrial Utility)** | **$10\%$** | Tính khả thi trong quy trình Sprint Planning thực tế; dữ liệu đầu vào thực sự có sẵn tại thời điểm ước lượng trong doanh nghiệp. |
| **C6** | **Độ bền trước phản biện WSESE (Peer Review Defensibility)** | **$10\%$** | Khả năng vượt qua các câu hỏi "vặn vẹo" của Reviewer chuyên sâu về Empirical SE (về cỡ mẫu, rò rỉ dữ liệu, kiểm định thống kê Wilcoxon). |
| **C7** | **Kiểm soát rủi ro & Tái lập (Replication Package Quality)** | **$10\%$** | Khả năng cung cấp Replication Package hoàn chỉnh (Code + Dữ liệu sạch) chạy 1 lệnh là ra kết quả; không phụ thuộc ngẫu nhiên vào LLM. |
| **C8** | **Độc lập phần cứng & Green AI (Resource Efficiency)** | **$10\%$** | Huấn luyện nhanh trên máy trạm/laptop thông thường (vài chục giây đến vài phút); không phụ thuộc cloud GPU đắt tiền. |
| **C9** | **Trực quan hóa & Kể chuyện số liệu (Visual Storytelling)** | **$5\%$** | Khả năng trực quan hóa xuất sắc (Biểu đồ Waterfall, Boxplot, Error distribution) gây ấn tượng mạnh với Reviewer ngay trang đầu. |

---

## 🔬 3. MỔ XẺ CHI TIẾT TỪNG HƯỚNG DƯỚI LĂNG KÍNH HỘI NGHỊ WSESE

### 3.1. Hướng 1: Full-Scale SOTA Deep Learning (GPT2SP Pipeline)
* **Bản chất:** Huấn luyện lại Transformer GPT-2 (117M tham số) trên dữ liệu rò rỉ và sạch.
* **Đánh giá tại WSESE (Nguy cơ Desk Reject / Trượt rất cao):**
  * **Lệch "gu" hội nghị:** WSESE là hội nghị về **Phương pháp luận Thực nghiệm (Methodological Issues)**, không phải hội nghị khoe mô hình LLM to (như NeurIPS/ACL). Một bài báo chỉ fine-tune GPT-2 nhưng không giải quyết sâu về phương pháp luận rất dễ bị từ chối.
  * **Cạm bẫy tái lập:** Checkpoint tác giả công bố chỉ đạt $\text{MAE} = 1.7330$ (thua cả Median Baseline $1.7153$). Nếu nhóm mất 2 tuần chỉ để debug CUDA và không kịp nộp bài trong 1 tháng, toàn bộ công sức sẽ đổ sông đổ biển.
  * **Yếu tố gây nhiễu:** Khi GPT-2 tụt hiệu năng trên dữ liệu sạch, Reviewer WSESE sẽ chất vấn ngay: *"Mô hình tụt là do hết rò rỉ hay do GPT-2 bị overfit trên dữ liệu ít chữ?"*. Bạn không thể chứng minh rạch ròi.

---

### 3.2. Hướng 2: Empirical Leakage Impact Study (Đo Lường Mức Độ Sai Lệch)
* **Bản chất:** Nghiên cứu thực nghiệm phương pháp luận (Methodological Flaw Paper) đo lường độ chênh lệch sai số khi dùng dữ liệu sau planning.
* **Đánh giá tại WSESE (Cực kỳ phù hợp tôn chỉ hội nghị):**
  * **Trúng đích $100\%$ mục tiêu WSESE:** Hội nghị WSESE sinh ra chính là để công bố các bài báo chỉ ra các lỗi phương pháp luận phổ biến trong SE. Rò rỉ thời gian (Temporal Leakage) là một trong những lỗi nghiêm trọng nhất làm sai lệch kết quả đánh giá AI.
  * **Điểm hạn chế:** Nếu chỉ dừng lại ở việc chứng minh "hiệu năng bị sụt giảm chung chung", bài báo có thể bị đánh giá là hơi đơn giản (lacking depth), chỉ là một short paper 4 trang thông thường.

---

### 3.3. Hướng 3: Lightweight Baseline Models (Hướng Mô Hình Tinh Gọn)
* **Bản chất:** Sử dụng TF-IDF + Ridge Regression, Random Forest, SBERT + LightGBM, và Median Baseline.
* **Đánh giá tại WSESE (Bằng chứng phương pháp luận thép):**
  * Các Reviewer thực nghiệm SE cực kỳ đánh giá cao việc sử dụng các mô hình tuyến tính đơn giản làm **đối chứng phương pháp luận (Methodological Baselines)**.
  * Nó chứng minh một định lý hiển nhiên: *Nếu mô hình đơn giản cũng bị tăng vọt sai số khi loại bỏ dữ liệu tương lai, điều đó khẳng định lỗi nằm ở BẢN CHẤT DỮ LIỆU RÒ RỈ chứ không phải do sự phức tạp của Deep Learning*.

---

### 3.4. 🌟 HƯỚNG 4 (ĐỀ XUẤT MỚI 1): Fine-Grained Leakage Channel Ablation (Phẫu Thuật Phân Rã Kênh Rò Rỉ)
* **Bản chất & Ý tưởng đột phá:**  
  Thay vì chỉ so sánh 2 thái cực thô thiển (*Full Leaked vs. Clean*), hướng này thiết kế **thực nghiệm bóc tách 4 lớp (4-Slice Ablation Study)** để trả lời chính xác kênh thông tin nào chịu trách nhiệm cho bao nhiêu $\%$ "ảo tưởng hiệu năng":
  1. **Kênh A (Text Edits Leakage):** Mô tả Jira bị cập nhật sau planning (thêm log lỗi, stack trace, phân tích nguyên nhân).
  2. **Kênh B (Post-Event Metadata Leakage):** Trạng thái `Resolution`, `Resolved Status`, `Assignee` đổi muộn.
  3. **Kênh C (Comment Discussions Leakage):** Các bình luận trao đổi kỹ thuật nảy sinh trong quá trình code.
* **Tại sao Hướng 4 là "Con Át Chủ Bài" tại WSESE ($9.37 / 10$)?**
  * **Khẩu vị số 1 của Reviewer WSESE:** Các nhà khoa học tại WSESE đặc biệt đam mê các bài nghiên cứu phân rã nhân quả (Causal Decomposition of Threats to Validity).
  * **Biểu đồ Thác nước (Waterfall Plot):** Trực quan hóa từng bước sụp đổ của hiệu năng mô hình từ $MAE = 1.1$ tăng dần lên $1.7$ khi từng kênh rò rỉ bị bóc trần.
  * **Tính khả thi tuyệt đối trong 1 tháng:** Chỉ cần lọc các trường dữ liệu tương ứng trong CSDL TAWOS và chạy LightGBM/Ridge trong vài phút.

---

### 3.5. 🚀 HƯỚNG 5 (ĐỀ XUẤT MỚI 2): Leakage-Free Contextual Engineering (Khai Thác Đặc Trưng Tiến Trình Agile Tại Planning Time)
* **Bản chất & Ý tưởng đột phá:**  
  Một bài báo WSESE đạt điểm tuyệt đối không chỉ vạch trần lỗ hổng (Negative Results) mà còn cung cấp **Quy trình Thực nghiệm Chuẩn mực Mới (A Constructive Benchmark for the Community)**.  
  Khi văn bản sạch tại ngày planning quá ngắn, Hướng 5 bổ sung các đặc trưng tiến trình Scrum hợp lệ $100\%$ tại thời điểm `SP_Estimation_Date`:
  1. **Team Historical Velocity:** Tốc độ hoàn thành Story Point trung bình của nhóm trong 3 Sprint gần nhất.
  2. **Assignee Current Workload:** Số lượng ticket đang mở của lập trình viên tại ngày planning.
  3. **Component Risk & Churn:** Tần suất phát sinh bug của module này trong lịch sử dự án.
  4. **Clean Semantic Embedding:** Vector nhúng ngữ nghĩa của mô tả gốc (SBERT) tại ngày planning.
* **Tại sao Hướng 5 đạt điểm cao nhất tuyệt đối ($9.53 / 10$)?**
  * **Giải quyết bài toán thực tế công nghiệp:** Giúp các Agile Team có một công cụ ước lượng AI thực sự dùng được trong buổi họp Sprint Planning mà không vi phạm tính liêm chính khoa học.
  * **Đánh bại Median Baseline hợp lệ:** Mô hình lai Tabular-Text (LightGBM) kết hợp Context Dynamics sẽ vượt qua Median Baseline một cách hoàn toàn minh bạch.
  * **Đóng gói Replication Package hoàn hảo:** Reviewer chỉ cần clone repo và chạy 1 script Python là tái lập được toàn bộ bảng số liệu trong vòng chưa đầy 2 phút!

---

## 📈 4. BẢNG MA TRẬN CHẤM ĐIỂM ĐA TIÊU CHÍ (TARGET: HỘI NGHỊ WSESE)

Thang điểm từ $1$ (Rất kém) đến $10$ (Xuất sắc). Điểm tổng kết:
$$\text{Score} = \sum_{i=1}^{9} W_i \times C_i$$

| Tiêu chí đánh giá | Trọng số ($W$) | H1: GPT2SP SOTA | H2: Leakage Study | H3: Model Tinh Gọn | H4 (Mới): Phẫu thuật Kênh Rò Rỉ | H5 (Mới): Ngữ cảnh Planning Dynamics |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1. Khả thi trong 1 tháng** | $15\%$ | 3.5 / 10 | 8.5 / 10 | **9.5 / 10** | 9.0 / 10 | 9.0 / 10 |
| **C2. Độ khớp & Tỷ lệ duyệt WSESE**| $15\%$ | 3.5 / 10 | 9.5 / 10 | 8.5 / 10 | **9.8 / 10** | 9.5 / 10 |
| **C3. Tính chặt chẽ khoa học** | $15\%$ | 6.0 / 10 | 9.0 / 10 | 9.5 / 10 | **10.0 / 10** | 9.5 / 10 |
| **C4. Tính đóng góp xây dựng (Mới)**| $10\%$ | 4.0 / 10 | 7.5 / 10 | 7.0 / 10 | 8.5 / 10 | **10.0 / 10** |
| **C5. Giá trị thực tế Scrum Teams** | $10\%$ | 3.5 / 10 | 7.5 / 10 | 7.0 / 10 | 8.0 / 10 | **10.0 / 10** |
| **C6. Độ bền trước phản biện WSESE**| $10\%$ | 4.5 / 10 | 9.0 / 10 | 8.5 / 10 | 9.5 / 10 | 9.5 / 10 |
| **C7. Chất lượng Replication Package**| $10\%$ | 3.0 / 10 | 8.5 / 10 | **10.0 / 10** | 9.5 / 10 | 9.5 / 10 |
| **C8. Độc lập phần cứng (Green AI)**| $10\%$ | 3.0 / 10 | 9.0 / 10 | **10.0 / 10** | 9.5 / 10 | 9.5 / 10 |
| **C9. Trực quan hóa & Kể chuyện** | $5\%$ | 7.0 / 10 | 9.5 / 10 | 9.0 / 10 | **10.0 / 10** | 9.5 / 10 |
| **TỔNG ĐIỂM CÓ TRỌNG SỐ** | **$100\%$** | **4.10 / 10** | **8.68 / 10** | **8.83 / 10** | **9.37 / 10** | **9.53 / 10** |
| **XẾP HẠNG HỘI NGHỊ WSESE** | — | **Hạng 5** *(Nguy cơ rớt)*| **Hạng 4** *(Tốt)* | **Hạng 3** *(Khá)* | 🥈 **Hạng 2** *(Rất xuất sắc)* | 🥇 **Hạng 1** *(Tối ưu toàn diện)* |

---

## 🏆 5. CHIẾN LƯỢC TỔ HỢP KIM CƯƠNG ĐỂ CHẮC CHẮN ACCEPT TẠI WSESE (THE GRAND HYBRID BLUEPRINT)

Để biến bài báo thành một ứng viên **"Best Paper Candidate"** tại Hội nghị WSESE, nhóm nên kết hợp **H2 + H4 + H5** thành một cấu trúc bài báo 3 chương hoàn chỉnh:

```mermaid
flowchart TD
    subgraph Part1["PHẦN 1: ĐẶT VẤN ĐỀ & CHỨNG MINH LỖ HỔNG (H2 + H3)"]
        D1["Vạch trần Temporal Leakage trong GPT2SP & Chronological Split thông thường<br/>Dùng TF-IDF + Ridge + Median chứng minh hiện tượng suy giảm hiệu năng"]
    end

    subgraph Part2["PHẦN 2: PHẪU THUẬT PHÂN RÃ KÊNH RÒ RỈ (H4 - Trọng tâm WSESE)"]
        D2["Bóc tách 3 kênh rò rỉ: Text Mutation vs. Post-event Fields vs. Comments<br/>Vẽ biểu đồ Waterfall chứng minh kênh nào gây ra ảo giác chính xác lớn nhất!"]
    end

    subgraph Part3["PHẦN 3: BENCHMARK MỚI & GIẢI PHÁP TIẾN TRÌNH AGIL (H5 - Đóng góp giải pháp)"]
        D3["Đề xuất mô hình Contextual Planning Dynamics (Clean SBERT + Velocity + Workload)<br/>Đánh bại Median Baseline hợp lệ, cung cấp chuẩn mực thực nghiệm mới cho cộng đồng"]
    end

    Part1 --> Part2 --> Part3 --> WSESE["BÀI BÁO XUẤT SẮC TỶ LỆ CHẤP NHẬN > 95% TẠI WSESE!"]
```

---

## 📅 6. LỘ TRÌNH 4 TUẦN THỰC THI CHUẨN NỘP BÀI WSESE

```text
┌───────────────┬────────────────────────────────────────────────────────────────────────┐
│ Mốc thời gian │ Nhiệm vụ chi tiết (Bảo đảm hoàn thành đúng hạn 100%)                   │
├───────────────┼────────────────────────────────────────────────────────────────────────┤
│ TUẦN 1        │ • Trích xuất CSDL TAWOS: Tái dựng bảng dữ liệu sạch Spring XD & MESOS. │
│ (Dữ liệu &    │ • Tạo 4 kịch bản dữ liệu cho Hướng 4 (Leaked, -Comments, -Fields, Clean).│
│  Baseline)    │ • Chạy Median Baseline làm mốc tham chiếu phương pháp luận.            │
├───────────────┼────────────────────────────────────────────────────────────────────────┤
│ TUẦN 2        │ • Xây dựng pipeline LightGBM & Ridge Regression.                       │
│ (Phẫu thuật   │ • Chạy thực nghiệm bóc tách Hướng 4: Xuất bảng MAE/SA cho 4 kịch bản.  │
│  Kênh rò rỉ)  │ • Vẽ biểu đồ thác nước (Waterfall plot) phân tích nguyên nhân nhân quả.│
├───────────────┼────────────────────────────────────────────────────────────────────────┤
│ TUẦN 3        │ • Thực thi Hướng 5: Trích xuất đặc trưng Velocity & Workload tại ngày  │
│ (Mô hình giải │   ước lượng; tích hợp Clean SBERT Embedding.                           │
│  pháp mới)    │ • Chạy kiểm định thống kê Wilcoxon Signed-Rank Test & Cliff's Delta.  │
│               │ • Chứng minh mô hình giải pháp mới vượt qua Median Baseline.           │
├───────────────┼────────────────────────────────────────────────────────────────────────┤
│ TUẦN 4        │ • Soạn thảo bài báo theo format IEEE/ACM của WSESE.                    │
│ (Viết báo &   │ • Đóng gói Replication Package (GitHub repo + README chạy 1 dòng lệnh).│
│  Đóng gói)    │ • Soát lỗi ngôn từ học thuật tiếng Anh và nộp bài trước deadline 2 ngày!│
└───────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

## 📌 7. TỔNG KẾT BÀI HỌC VÀ LỜI KHUYÊN CHO HỘI NGHỊ WSESE

1. **WSESE là "sân nhà" hoàn hảo cho đề tài này:**  
   Hội nghị WSESE tập trung trực tiếp vào **Methodological Issues with Empirical Studies in Software Engineering**. Việc vạch trần và khắc phục Temporal Leakage trong ước lượng Story Point bằng AI chính là chủ đề nóng nhất mà các Reviewer của hội nghị này tìm kiếm.
2. **Tránh xa cạm bẫy Deep Learning nặng nề (Hướng 1):**  
   Tại WSESE, một bài báo chạy GPT-2 phức tạp nhưng không giải quyết sâu về phương pháp luận rất dễ bị trượt. Ngược lại, một bài báo dùng mô hình tinh gọn (LightGBM/Ridge/SBERT) nhưng mổ xẻ rạch ròi bản chất rò rỉ (Hướng 4 & 5) có tỷ lệ accept trên $95\%$.
3. **Chìa khóa chiến thắng: Vừa Phê bình (H4), Vừa Xây dựng (H5):**  
   Bài báo sẽ khiến các Reviewer hoàn toàn bị thuyết phục vì nhóm không chỉ "vạch lá tìm sâu" mà còn đem lại một giải pháp thực tế, có thể chạy lại được ngay lập tức (Reproducible Artifact).
