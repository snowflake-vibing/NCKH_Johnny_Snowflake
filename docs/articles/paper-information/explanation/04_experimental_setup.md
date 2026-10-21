# 📖 CHƯƠNG 4: THIẾT LẬP THỰC NGHIỆM (EXPERIMENTAL SETUP)

> **Tài liệu gốc:** Mục 4 (EXPERIMENTAL SETUP), Trang 5 – 7, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả:** Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).

---

## ❓ 1. BA CÂU HỎI NGHIÊN CỨU (4.1 RESEARCH QUESTIONS)

> 📍 **Vị trí bài báo gốc:** Mục 4.1 (Research Questions), Trang 5, Cột 2 (Dòng 10 – 35) – Trang 6, Cột 1 (Dòng 1 – 25).

Để đánh giá toàn diện năng lực của kiến trúc GPT2SP, nhóm tác giả xây dựng 3 câu hỏi nghiên cứu (Research Questions - RQ) định lượng có tính mục tiêu rõ rệt:

### 1.1. RQ1: Đánh giá trong nội bộ dự án (Within-Project Scenarios)
> 📍 **Vị trí bài báo gốc:** Trang 5, Cột 2, Dòng 14 – 35.
* **Câu hỏi:** *(RQ1) Does our GPT2SP outperform Deep-SE for within-project scenarios?* (Liệu GPT2SP có vượt trội hơn Deep-SE trong kịch bản ước lượng nội bộ dự án?)
* **Động cơ khoa học:** Ước lượng Story Point mang tính đặc thù cao theo từng đội ngũ và từng dự án. Dù Choetkiertikul et al. [7] đã đề xuất Deep-SE là mô hình học sâu SOTA, độ chính xác của nó vẫn còn hạn chế. RQ1 nhằm kiểm chứng xem GPT2SP có vượt trội hơn Deep-SE và 9 mô hình baseline khác khi được huấn luyện và kiểm thử trên cùng một dự án phần mềm hay không.

### 1.2. RQ2: Đánh giá liên dự án (Cross-Project Scenarios)
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 1, Dòng 1 – 15.
* **Câu hỏi:** *(RQ2) Does our GPT2SP outperform Deep-SE for cross-project scenarios?* (Liệu GPT2SP có vượt trội hơn Deep-SE trong kịch bản ước lượng liên dự án?)
* **Động cơ khoa học:** Khi bắt đầu một dự án Agile mới, các lập trình viên thường thiếu tri thức lịch sử để ước lượng; các mô hình AI/ML cũng thiếu dữ liệu huấn luyện cục bộ. Giải pháp phổ biến là ước lượng liên dự án (huấn luyện trên dự án nguồn và dự đoán cho dự án đích). RQ2 đánh giá khả năng chuyển giao tri thức (transferability) của GPT2SP so với Deep-SE và phương pháp ABE0 trên hai tình huống: liên dự án trong cùng tổ chức (*within-repository*) và giữa các tổ chức khác biệt (*cross-repository*).

### 1.3. RQ3: Đóng góp của từng cấu phần kiến trúc (Ablation Study)
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 1, Dòng 16 – 25.
* **Câu hỏi:** *(RQ3) What are the contributions of the components of GPT2SP?* (Đóng góp thực sự của từng thành phần trong GPT2SP là gì?)
* **Động cơ khoa học:** Kiến trúc GPT2SP gồm hai thành phần chủ chốt: bộ phân tách từ con **$\text{BPE}_{\text{GPT2}}$** và các khối giải mã **$\text{GPT-2}$ Transformer**, khác biệt hoàn toàn với bộ ba $\text{WordEmb} + \text{LSTM} + \text{RHWN}$ của Deep-SE. RQ3 nhằm bóc tách thực nghiệm xem bước nhảy vọt về độ chính xác bắt nguồn chủ yếu từ thuật toán BPE hay từ các khối giải mã Transformer.

---

## 📊 2. TẬP DỮ LIỆU NGHIÊN CỨU (4.2 STUDIED DATASETS)

> 📍 **Vị trí bài báo gốc:** Mục 4.2 (Studied Datasets), Trang 6, Cột 1 (Dòng 26 – 40) – Cột 2 (Dòng 1 – 5) & **Bảng 1 (Table 1, Trang 6)**.

### 2.1. Nguồn gốc & Tiêu chí thu thập dữ liệu
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 1, Dòng 26 – 40.
Nhằm đảm bảo tính so sánh công bằng và khách quan với mô hình SOTA Deep-SE, nhóm tác giả sử dụng lại bộ dữ liệu chuẩn mực được công bố bởi **Choetkiertikul et al. (2019)** [7]:
* Dữ liệu được trích xuất từ hệ thống theo dõi lỗi **JIRA** (thông qua JIRA Agile plugin) bằng JIRA REST API tính đến mốc thời gian ngày **8 tháng 8 năm 2016**.
* Tập dữ liệu bao gồm **$23.313$ issues** từ **16 dự án mã nguồn mở lớn** thuộc **9 kho lưu trữ (repositories)** nổi tiếng.
* Thông tin trích xuất của mỗi issue gồm: Mã định danh (`Issue ID`), Tiêu đề (`Title`), Mô tả kỹ thuật (`Description`) và điểm nỗ lực thực tế (`Story Point`).

### 2.2. Bảng 1: Thống kê mô tả chi tiết của 16 bộ dữ liệu dự án
> 📍 **Vị trí bài báo gốc:** Bảng 1 (TABLE 1: The descriptive statistics of the story point datasets provided by Choetkiertikul et al. [7], Trang 6).

| STT | Jira Repository | Dự án (Project) | Mã Key | Số lượng (#Issues) | $\text{SP}_{\min}$ | $\text{SP}_{\max}$ | $\text{SP}_{\text{mean}}$ | $\text{SP}_{\text{median}}$ | $\text{SP}_{\text{var}}$ | $\text{SP}_{\text{std}}$ |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Apache** | Mesos | `MESOS` | 1.680 | 1 | 40 | 3,09 | 3 | 5,87 | 2,42 |
| 2 | **Apache** | Usergrid | `USERGRID` | 482 | 1 | 8 | 2,85 | 3 | 1,97 | 1,40 |
| 3 | **Appcelerator** | Appcelerator Studio | `TISTUD` | 2.919 | 1 | 40 | 5,64 | 5 | 11,07 | 3,33 |
| 4 | **Appcelerator** | Aptana Studio | `APSTUD` | 829 | 1 | 40 | 8,02 | 8 | 35,46 | 5,95 |
| 5 | **Appcelerator** | Titanium SDK / CLI | `TIMOB` | 2.251 | 1 | 34 | 6,32 | 5 | 25,97 | 5,10 |
| 6 | **Dura Space** | DuraCloud | `DURACLOUD` | 666 | 1 | 16 | 2,13 | 1 | 4,12 | 2,03 |
| 7 | **Atlassian** | Bamboo | `BAM` | 521 | 1 | 20 | 2,42 | 2 | 4,60 | 2,14 |
| 8 | **Atlassian** | Clover | `CLOV` | 384 | 1 | 40 | 4,59 | 2 | 42,95 | 6,55 |
| 9 | **Atlassian** | JIRA Software | `JSWSERVER` | 352 | 1 | 20 | 4,43 | 3 | 12,35 | 3,51 |
| 10 | **Moodle** | Moodle | `MDL` | 1.166 | 1 | 100 | 15,54 | 8 | 468,53 | 21,65 |
| 11 | **Lsstcorp** | Data Management | `DM` | 4.667 | 1 | 100 | 9,57 | 4 | 275,71 | 16,61 |
| 12 | **Mulesoft** | Mule | `MULE` | 889 | 1 | 21 | 5,08 | 5 | 12,24 | 3,50 |
| 13 | **Mulesoft** | Mule Studio | `MULSTUD` | 732 | 1 | 34 | 6,40 | 5 | 29,01 | 5,39 |
| 14 | **Spring** | Spring XD | `XD` | **3.526** | 1 | 40 | 3,70 | 3 | 10,42 | 3,23 |
| 15 | **Talendforge** | Talend Data Quality | `TDQ` | 1.381 | 1 | 40 | 5,92 | 5 | 26,96 | 5,19 |
| 16 | **Talendforge** | Talend ESB | `TESB` | 868 | 1 | 13 | 2,16 | 2 | 2,24 | 1,50 |
| **-** | **TỔNG CỘNG** | **16 Dự án** | **-** | **23.313** | **1** | **100** | **-** | **-** | **-** | **-** |

### 2.3. Quy tắc phân chia dữ liệu theo dòng thời gian (Temporal Data Split)
> 📍 **Vị trí bài báo gốc:** Mục 5 (Approach of RQ1), Trang 7, Cột 2, Dòng 10 – 25.
Để phản ánh đúng thực tế vận hành phần mềm và ngăn chặn triệt để hiện tượng rò rỉ dữ liệu tương lai (temporal validation bias):
* Toàn bộ dữ liệu của từng dự án được **sắp xếp theo thứ tự thời gian tạo lập (chronological order)**.
* Phân chia thành 3 tập con:
  * **Tập Huấn luyện (Training set - $60\%$):** Các issue xuất hiện sớm nhất trong lịch sử dự án.
  * **Tập Xác thực (Validation set - $20\%$):** Dùng để tinh chỉnh siêu tham số và tính toán hàm mất mát $\mathcal{L}(\theta)$.
  * **Tập Kiểm thử (Testing set - $20\%$):** Các issue mới nhất, độc lập tuyệt đối, dùng để tính sai số MAE đánh giá cuối cùng.

---

## 💻 3. TRIỂN KHAI MÔ HÌNH (4.3 MODEL IMPLEMENTATION)

> 📍 **Vị trí bài báo gốc:** Mục 4.3 (Model Implementation), Trang 6, Cột 2, Dòng 6 – 32.

### 3.1. Thư viện phần mềm & Hạ tầng phần cứng
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 2, Dòng 6 – 16.
* **Thư viện chủ đạo:**
  * **Transformers (Hugging Face) [56]:** Cung cấp API truy cập kiến trúc mô hình Transformer và bộ phân tách từ con BPE Tokenizer dựa trên kho ngữ liệu GPT-2.
  * **PyTorch [30]:** Quản lý đồ thị tính toán tự động, tính toán tensor và lan truyền ngược (back-propagation).
* **Hạ tầng phần cứng:** Huấn luyện trên duy nhất **01 card đồ họa NVIDIA RTX 3090** (24GB VRAM).
* **Thời gian huấn luyện đột phá:** Thời gian fine-tune mỗi dự án chỉ mất từ **$3$ giây đến $39$ giây** (trung bình $14$ giây/dự án, xem Bảng 4 ở Phụ lục), nhanh gấp hàng trăm lần so với Deep-SE (vốn tốn $2$ đến $7$ giờ cho mỗi dự án).

### 3.2. Hàm mất mát L1 Loss (Mean Absolute Error Loss)
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 2, Dòng 17 – 25.
Quá trình huấn luyện tìm kiếm tập tham số $\theta$ tối ưu nhằm cực tiểu hóa hàm mất mát trên **tập xác thực (validation set)**:

$$\mathcal{L}(\theta) = \sum_{i=1}^{n} |y_{\text{true}, i} - y_{\text{predicted}, i}|$$

Hàm mất mát sai số tuyệt đối $L_1$ được lựa chọn vì nó có đạo hàm ổn định, không bị khuếch đại gradient bởi các điểm dữ liệu ngoại lai cực lớn (outliers như $40, 100$ SP) thường gặp trong phân phối Story Point bị lệch phải.

### 3.3. Bộ tối ưu hóa AdamW & Tốc độ học (Learning Rate)
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 2, Dòng 25 – 32.
* Sử dụng bộ tối ưu hóa **AdamW** [26] với tốc độ học được thiết lập cố định:

$$\text{LR} = 5 \times 10^{-4}$$

* AdamW là phiên bản nâng tiến của Adam [21], tích hợp cơ chế phân rã trọng số độc lập (weight decay regularization), giúp tối ưu hóa hiệu quả bộ nhớ và chống quá khớp (overfitting) vượt trội.
* Thuật toán lan truyền ngược (**Back-propagation**) thực thi quy tắc chuỗi đạo hàm riêng để cập nhật đồng thời toàn bộ trọng số của các khối Transformer và đầu hồi quy MLP.

---

## ⚙️ 4. CẤU HÌNH SIÊU THAM SỐ (4.4 HYPER-PARAMETER SETTINGS)

> 📍 **Vị trí bài báo gốc:** Mục 4.4 (Hyper-Parameter Settings), Trang 6, Cột 2 (Dòng 33) – Trang 7, Cột 1 (Dòng 1 – 25).

### 4.1. Bốn biến thể GPT-2 & Lựa chọn GPT-2 Small
> 📍 **Vị trí bài báo gốc:** Trang 6, Cột 2 (Dòng 33 – 45) – Trang 7, Cột 1 (Dòng 1 – 8).
OpenAI đề xuất 4 biến thể GPT-2 khác nhau về quy mô tham số:
1. **GPT-2 Small:** 117 triệu tham số ($117\text{M}$).
2. **GPT-2 Medium:** 345 triệu tham số ($345\text{M}$).
3. **GPT-2 Large:** 774 triệu tham số ($774\text{M}$).
4. **GPT-2 XL:** 1,5 tỷ tham số ($1.5\text{B}$).

Nhóm tác giả quyết định chọn **GPT-2 Small** làm cấu hình mặc định nhằm tránh bùng nổ chi phí tính toán và ngăn ngừa nguy cơ quá khớp trên tập dữ liệu phần mềm.

> [!TIP]
> **Khái niệm Biên dưới Hiệu năng (Lower Bound Performance):**  
> Việc chọn phiên bản GPT-2 Small gọn nhất đồng nghĩa với việc kết quả đạt được trong nghiên cứu này đóng vai trò là **biên dưới (lower bound)** về năng lực của các mô hình Transformer. Khi chuyển sang các biến thể lớn hơn, độ chính xác có thể còn được nâng cao hơn nữa (được kiểm chứng tại Phụ lục Mục 13).

### 4.2. Bảng tổng hợp siêu tham số kiến trúc GPT2SP
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 1, Dòng 8 – 25.

| Siêu tham số | Ký hiệu / Giá trị | Ý nghĩa kỹ thuật trong mô hình |
| :--- | :---: | :--- |
| **Kiến trúc mô hình** | **GPT-2 Small** | Biến thể decoder-only gọn nhẹ nhất với $117\text{M}$ tham số. |
| **Số tầng Decoder** | $12$ | 12 khối Transformer Decoder xếp chồng liên tiếp. |
| **Số chiều ẩn** | $d = 768$ | Độ dài vector nhúng từ và vector trạng thái ẩn của mỗi token. |
| **Số đầu chú ý** | $H = 12$ | 12 cơ chế Multi-Head Attention song song trong mỗi khối. |
| **Chiều mỗi đầu chú ý** | $d_{kv} = 64$ | Kích thước ma trận $Q, K, V$ ($768 / 12 = 64$). |
| **Kích thước từ vựng** | $\|V\| = 50.257$ | Số lượng subword tokens trong từ điển tiền huấn luyện BPE. |
| **Độ dài ngữ cảnh tối đa** | $c = 1024$ | Số token tối đa mà mô hình tiếp nhận cho một issue. |
| **Kích thước vector ghép nối** | $768$ | Sau khi ghép nối 12 đầu chú ý ($64 \times 12 = 768$). |
| **Tầng mạng truyền thẳng** | **FFN (Linear + GELU)** | Tầng nơ-ron truyền thẳng biến đổi đặc trưng sâu. |
| **Đầu hồi quy** | **3-layer MLP** | Mạng Perceptron đa tầng ánh xạ vector $\mathbf{h}_{\text{last}}$ thành điểm $\hat{y}$. |

---

## 📐 5. THANG ĐO ĐÁNH GIÁ (4.5 EVALUATION MEASURE)

> 📍 **Vị trí bài báo gốc:** Mục 4.5 (Evaluation Measure), Trang 7, Cột 1, Dòng 26 – 45.

### 5.1. Sai số Tuyệt đối Trung bình (Mean Absolute Error - MAE)
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 1, Dòng 26 – 32.
Thang đo chính được lựa chọn cho cả hai kịch bản trong nội bộ dự án (within-project) và liên dự án (cross-project) là **MAE** (đồng nhất với thước đo đánh giá Deep-SE của Choetkiertikul et al. [7]):

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

Trong đó $y_i$ là Story Point thực tế của issue thứ $i$, $\hat{y}_i$ là điểm Story Point do mô hình dự đoán, và $n$ là tổng số issue trong tập kiểm thử. MAE đo lường độ lớn trung bình của sai số mà không xét đến chiều sai lệch (âm hay dương).

### 5.2. Luận cứ khoa học bác bỏ các thang đo khác (MdAE, MMRE, SA)
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 1, Dòng 33 – 45.
Mục tiêu cốt lõi của bài báo là **vượt qua đỉnh cao SOTA của Deep-SE** (chứ không phải so kè với việc đoán ngẫu nhiên). Tác giả giải trình chi tiết lý do loại bỏ 3 thang đo phổ biến khác:
1. **Loại bỏ MdAE (Median Absolute Error):** Dù trung vị MdAE không bị kéo lệch bởi các giá trị ngoại lai, nhưng nó lại **bỏ qua hoàn toàn các sai số ước lượng cực đoan**. Trong quản lý phần mềm, một task lớn bị đoán non nghiêm trọng (under-estimation) gây vỡ toàn bộ kế hoạch phát hành, do đó MAE phản ánh rủi ro này trung thực hơn.
2. **Loại bỏ MMRE (Mean Magnitude of Relative Error):** Nghiên cứu kinh điển của Shepperd & MacDonell [43] đã chứng minh bằng toán học rằng MMRE bị thiên lệch nặng nề (thiên vị việc đoán thấp để giảm tỷ lệ sai số tương đối).
3. **Loại bỏ SA (Standardised Accuracy):** SA là thang đo tương đối so với đoán mò ngẫu nhiên (*Random Guessing*), không phản ánh sát sao năng lực cạnh tranh giữa các mô hình học sâu hiện đại.

---

## 📈 6. PHƯƠNG PHÁP KIỂM ĐỊNH THỐNG KÊ (4.6 STATISTICAL ANALYSIS)

> 📍 **Vị trí bài báo gốc:** Mục 4.6 (Statistical Analysis), Trang 7, Cột 1 (Dòng 46) – Cột 2 (Dòng 1 – 45).

Để xác định xem sự cải thiện độ chính xác của GPT2SP so với các baseline có mang ý nghĩa thống kê thực chất hay không, nghiên cứu áp dụng quy trình kiểm định phi tham số **Non-Parametric ScottKnott ESD (NPSK)** [47] thay cho kiểm định ANOVA truyền thống.

### 6.1. Ưu thế vượt trội của Non-Parametric ScottKnott ESD
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 1 (Dòng 50) – Cột 2 (Dòng 1 – 15).
Kiểm định Scott-Knott ESD truyền thống đòi hỏi 3 giả định khắt khe của mô hình ANOVA:
* Dữ liệu phải tuân theo phân phối chuẩn (normality).
* Phương sai giữa các nhóm phải đồng nhất (homogeneity of variances).
* Cỡ mẫu tối thiểu phải đủ lớn.

Phân phối sai số Story Point trong thực tế vi phạm hoàn toàn các giả định trên. Do đó, kiểm định **Non-Parametric ScottKnott ESD** là lựa chọn chuẩn mực vì nó hoàn toàn phi tham số, không đòi hỏi phân phối chuẩn và kích cỡ mẫu đồng đều.

### 6.2. Hai bước thực thi của thuật toán NPSK
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 2, Dòng 16 – 35.

Quy trình phân cụm thứ bậc của NPSK gồm 2 bước:
1. **Bước 1 — Tìm điểm phân tách tối đa hóa trung vị (Kruskal Chisq Test):** Sắp xếp các kỹ thuật theo giá trị trung vị sai số. Sử dụng thống kê phi tham số **Kruskal-Wallis Chi-Square** để tìm điểm phân chia tối ưu sao cho sự khác biệt giữa các cụm là lớn nhất.
2. **Bước 2 — Phân tách hoặc Gộp nhóm dựa trên Kích thước Hiệu ứng Cliff's $|\delta|$:**
   * Tính toán kích thước hiệu ứng Cliff's Delta giữa từng cặp trung vị của hai nhóm.
   * Nếu tồn tại dù chỉ một cặp có kích thước hiệu ứng khác biệt thực chất (non-negligible, $|\delta| \ge 0.147$), thuật toán sẽ **tách thành 2 nhóm riêng biệt**.
   * Ngược lại, nếu mọi cặp đều có độ khác biệt không đáng kể (negligible, $|\delta| < 0.147$), hai nhóm được **gộp chung làm một nhóm thứ hạng duy nhất**.

### 6.3. Bảng phân ngưỡng kích thước hiệu ứng Cliff's Delta ($\delta$)
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 2, Dòng 30 – 35 (trích dẫn Romano et al. [41]).

$$\delta = \frac{\# (x_i > y_j) - \# (x_i < y_j)}{m \times n}$$

| Ngưỡng giá trị Cliff's Delta ($\lvert \delta \rvert$) | Mức độ hiệu ứng (Effect Size) | Kết luận thống kê |
| :---: | :---: | :--- |
| $\lvert \delta \rvert < 0.147$ | **Negligible** | Khác biệt không đáng kể (được gộp chung thứ hạng). |
| $0.147 \le \lvert \delta \rvert < 0.330$ | **Small** | Mức độ khác biệt nhỏ. |
| $0.330 \le \lvert \delta \rvert < 0.474$ | **Medium** | Mức độ khác biệt trung bình. |
| $\lvert \delta \rvert \ge 0.474$ | **Large** | Mức độ khác biệt lớn, có ý nghĩa khoa học mạnh. |

### 6.4. Công cụ thực thi gói phần mềm R
> 📍 **Vị trí bài báo gốc:** Trang 7, Cột 2, Dòng 36 – 40.
Toàn bộ quá trình kiểm định phân nhóm thống kê được thực thi bằng gói phần mềm chính thức:
* Gói thư viện: **ScottKnott ESD R package (Version 3.0)** do chính nhóm tác giả phát triển và công bố công khai trên CRAN.
