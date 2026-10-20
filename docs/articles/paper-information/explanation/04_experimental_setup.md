# 📖 CHƯƠNG 4: THIẾT LẬP THỰC NGHIỆM (EXPERIMENTAL SETUP)

> **Tài liệu gốc:** Trang 5 – 7, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả:** Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).

---

## ❓ 1. BA CÂU HỎI NGHIÊN CỨU (4.1 RESEARCH QUESTIONS)

Để kiểm chứng tính ưu việt của kiến trúc đề xuất so với các phương pháp hiện hành, nhóm tác giả xây dựng 3 câu hỏi nghiên cứu định lượng rõ ràng:

* **(RQ1) Liệu GPT2SP có vượt trội hơn Deep-SE và các mô hình baseline trong kịch bản ước lượng nội dự án (Within-Project Estimation)?**  
  * *Mục tiêu:* Kiểm tra khả năng học nỗ lực của GPT2SP khi được huấn luyện và kiểm thử trên cùng một dự án phần mềm, so sánh với 9 mô hình baseline (gồm Deep-SE, các mô hình học máy truyền thống và baseline thống kê).
* **(RQ2) Liệu GPT2SP có vượt trội hơn Deep-SE trong kịch bản ước lượng liên dự án (Cross-Project Estimation)?**  
  * *Mục tiêu:* Đánh giá khả năng chuyển giao tri thức (transferability) sang một dự án mới hoàn toàn chưa có dữ liệu lịch sử hoặc rất ít dữ liệu, chia thành hai tình huống: liên dự án trong cùng tổ chức (*Within-Repository*) và liên dự án giữa các tổ chức khác nhau (*Cross-Repository*).
* **(RQ3) Mức độ đóng góp của từng thành phần cấu tạo nên GPT2SP là bao nhiêu (Ablation Study)?**  
  * *Mục tiêu:* Bóc tách rành mạch xem bước nhảy vọt hiệu năng đến từ thuật toán phân tách từ con (**BPE Tokenization**) hay đến từ các khối giải mã chú ý (**Transformer Decoders**).

---

## 📊 2. TẬP DỮ LIỆU THỰC NGHIỆM (4.2 STUDIED DATASETS)

### Nguồn gốc & Tiêu chí thu thập
Nhóm tác giả sử dụng bộ dữ liệu chuẩn mực được công bố bởi **Choetkiertikul et al. (2019)** [7]. Dữ liệu được trích xuất thông qua Jira REST API đến mốc thời gian ngày **8 tháng 8 năm 2016**.
* Tập dữ liệu bao gồm **16 dự án mã nguồn mở lớn** thuộc **9 kho lưu trữ (repositories)** nổi tiếng trong cộng đồng phần mềm thế giới.
* **Quy tắc tiền xử lý và lọc sạch của Choetkiertikul:**
  * Loại bỏ các issue được gán Story Point bằng $0$ (thường là các bug không tái lập được hoặc không tốn nỗ lực xử lý).
  * Loại bỏ các issue có Story Point âm hoặc lớn bất thường một cách phi thực tế (ví dụ: $\text{SP} > 100$).

### Bảng 1: Thống kê mô tả chi tiết của 16 bộ dữ liệu dự án (Table 1 trong bài báo)

| STT | Jira Repository | Dự án (Project) | Mã Key | Số lượng (#Issues) | $\text{SP}_{\min}$ | $\text{SP}_{\max}$ | $\text{SP}_{\text{mean}}$ | $\text{SP}_{\text{median}}$ | $\text{SP}_{\text{var}}$ | $\text{SP}_{\text{std}}$ |
| :-: | :--- | :--- | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | **Apache** | Mesos | `MESOS` | 1.680 | 1 | 40 | 3,09 | 3 | 5,87 | 2,42 |
| 2 | **Apache** | Usergrid | `USERGRID` | 482 | 1 | 8 | 2,85 | 3 | 1,97 | 1,40 |
| 3 | **Appcelerator** | Appcelerator Studio | `TISTUD` | 2.919 | 1 | 40 | 5,64 | 5 | 11,07 | 3,33 |
| 4 | **Appcelerator** | Aptana Studio | `APSTUD` | 829 | 1 | 40 | 8,02 | 8 | 35,46 | 5,95 |
| 5 | **Appcelerator** | Titanium SDK / CLI | `TIMOB` | 2.251 | 1 | 34 | 6,32 | 5 | 25,97 | 5,10 |
| 6 | **Dura Space** | DuraCloud | `DURACLOUD`| 666 | 1 | 16 | 2,13 | 1 | 4,12 | 2,03 |
| 7 | **Atlassian** | Bamboo | `BAM` | 521 | 1 | 20 | 2,42 | 2 | 4,60 | 2,14 |
| 8 | **Atlassian** | Clover | `CLOV` | 384 | 1 | 40 | 4,59 | 2 | 42,95 | 6,55 |
| 9 | **Atlassian** | JIRA Software | `JSWSERVER`| 352 | 1 | 20 | 4,43 | 3 | 12,35 | 3,51 |
| 10 | **Moodle** | Moodle | `MDL` | 1.166 | 1 | 100 | 15,54 | 8 | 468,53 | 21,65 |
| 11 | **Lsstcorp** | Data Management | `DM` | 4.667 | 1 | 100 | 9,57 | 4 | 275,71 | 16,61 |
| 12 | **Mulesoft** | Mule | `MULE` | 889 | 1 | 21 | 5,08 | 5 | 12,24 | 3,50 |
| 13 | **Mulesoft** | Mule Studio | `MULSTUD` | 732 | 1 | 34 | 6,40 | 5 | 29,01 | 5,39 |
| 14 | **Spring** | Spring XD | `XD` | **3.526** | 1 | 40 | 3,70 | 3 | 10,42 | 3,23 |
| 15 | **Talendforge** | Talend Data Quality | `TDQ` | 1.381 | 1 | 40 | 5,92 | 5 | 26,96 | 5,19 |
| 16 | **Talendforge** | Talend ESB | `TESB` | 868 | 1 | 13 | 2,16 | 2 | 2,24 | 1,50 |
| **-** | **TỔNG CỘNG** | **16 Dự án** | **-** | **23.313** | **1** | **100** | **-** | **-** | **-** | **-** |

### Chiến lược phân chia tập dữ liệu (Dataset Splitting)
Tác giả chia dữ liệu của mỗi dự án thành 3 tập con theo tỷ lệ kinh điển:
* **Tập Huấn luyện (Training set):** $60\%$ dùng để tối ưu hóa trọng số mô hình.
* **Tập Xác thực (Validation set):** $20\%$ dùng để chọn tập siêu tham số tối ưu và dừng sớm (early stopping) tránh overfitting.
* **Tập Kiểm thử (Testing set):** $20\%$ độc lập hoàn toàn, dùng để đánh giá và báo cáo hiệu năng cuối cùng.

---

## 💻 3. MÔI TRƯỜNG TRIỂN KHAI & CẤU HÌNH SIÊU THAM SỐ (4.3 & 4.4)

### Hạ tầng kỹ thuật & Thư viện
* **Môi trường phần mềm:** Viết bằng Python sử dụng hai thư viện chủ đạo:
  * **Hugging Face Transformers** [56]: Khai thác kiến trúc GPT-2 và BPE Tokenizer.
  * **PyTorch** [30]: Quản lý đồ thị tính toán, tính toán tensor và lan truyền ngược.
* **Hạ tầng phần cứng:** Sử dụng duy nhất 01 card đồ họa **NVIDIA RTX 3090** (24GB VRAM).
* **Thời gian huấn luyện:** Cực kỳ nhanh, chỉ dao động từ **3 giây đến 39 giây** cho mỗi dự án (trung bình 14 giây/dự án), vượt trội hoàn toàn so với Deep-SE vốn mất 2 đến 7 giờ/dự án!

### Bảng cấu hình siêu tham số mô hình (Hyper-parameter Settings)

| Siêu tham số | Giá trị cấu hình | Giải thích ý nghĩa |
| :--- | :---: | :--- |
| **Kiến trúc nền** | **GPT-2 Small** | Phiên bản gọn nhẹ nhất của GPT-2, gồm 117 triệu tham số ($117\text{M}$). |
| **Số tầng Transformer** | $12$ | 12 khối Transformer Decoder xếp chồng liên tiếp. |
| **Chiều ẩn ($d$)** | $768$ | Độ dài vector biểu diễn trạng thái ẩn của mỗi token. |
| **Số đầu chú ý ($H$)** | $12$ | 12 cơ chế Multi-Head Attention song song. |
| **Chiều mỗi đầu ($d_{kv}$)** | $64$ | $768 / 12 = 64$, kích thước ma trận Query/Key/Value. |
| **Kích thước từ điển ($|V|$)** | $50.257$ | Số lượng subword tokens được tiền huấn luyện sẵn của GPT-2. |
| **Chiều dài ngữ cảnh tối đa ($c$)** | $1024$ | Số token tối đa mà mô hình tiếp nhận cho một issue. |
| **Hàm mất mát** | **L1 Loss** | Sai số tuyệt đối $\sum \|y_{\text{true}} - \hat{y}_{\text{pred}}\|$. |
| **Bộ tối ưu hóa** | **AdamW** | Adam với Decoupled Weight Decay. |
| **Tốc độ học (Learning Rate)** | $5 \times 10^{-4}$ | Learning rate chuẩn cho bước tinh chỉnh. |

> [!TIP]
> **Nhận định về biên dưới hiệu năng (Lower Bound Performance):**  
> Việc chọn phiên bản GPT-2 Small gọn nhất đồng nghĩa với việc kết quả đạt được trong nghiên cứu này chỉ là **biên dưới (lower bound)** về năng lực của các mô hình Transformer. Nếu dùng các phiên bản lớn hơn (Medium 345M, Large 774M, XL 1.5B), độ chính xác có thể còn cao hơn nữa (sẽ được kiểm chứng ở Phần Phụ lục 13).

---

## 📐 4. THANG ĐO ĐÁNH GIÁ (4.5 EVALUATION MEASURE)

Thang đo chính được lựa chọn để đánh giá là **Sai số Tuyệt đối Trung bình (Mean Absolute Error - MAE)**:
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
Trong đó $y_i$ là Story Point thực tế của issue thứ $i$, và $\hat{y}_i$ là giá trị do mô hình dự đoán.

### Vì sao bài báo chỉ chọn MAE mà loại bỏ các thang đo khác?
Tác giả giải thích rất rành mạch lý do khoa học của việc không sử dụng các thước đo khác:
1. **Loại bỏ MdAE (Median Absolute Error):** Mặc dù MdAE không bị ảnh hưởng bởi giá trị ngoại lai, nhưng nó lại **bỏ qua hoàn toàn các sai số cực đoan**. Trong quản lý phần mềm, một dự đoán sai lệch nghiêm trọng (ví dụ task 40 điểm bị đoán thành 1 điểm) gây thảm họa lớn cho Sprint, do đó MAE phản ánh rủi ro này tốt hơn.
2. **Loại bỏ MMRE (Mean Magnitude of Relative Error):** Nghiên cứu kinh điển của Shepperd & MacDonell [43] đã chứng minh MMRE bị thiên lệch nặng nề về phía dự đoán non (under-estimation penalty).
3. **Loại bỏ SA (Standardised Accuracy):** SA đo lường mức độ cải thiện so với việc đoán ngẫu nhiên (*Random Guessing*). Mục tiêu tối thượng của bài báo là **vượt qua đỉnh cao SOTA của Deep-SE**, chứ không phải so kè với đoán mò ngẫu nhiên.

---

## 📈 5. PHƯƠNG PHÁP KIỂM ĐỊNH THỐNG KÊ (4.6 STATISTICAL ANALYSIS)

Để đảm bảo kết quả vượt trội không phải do ngẫu nhiên may rủi, nghiên cứu sử dụng chuỗi kiểm định phi tham số nghiêm ngặt:

### 1. Kiểm định dấu hạng Wilcoxon (Wilcoxon Signed-Rank Test)
* Kiểm định phi tham số dành cho dữ liệu bắt cặp (paired), không đòi hỏi phân phối chuẩn.
* Kiểm tra giả thuyết không ($H_0$): Không có sự khác biệt giữa phân phối sai số của GPT2SP và mô hình đối chứng.
* Bác bỏ $H_0$ khi giá trị xác suất $p$-value $< 0.05$.

### 2. Kích thước hiệu ứng Cliff's Delta ($\delta$)
* Đo lường mức độ thực chất của sự khác biệt giữa hai phân phối mẫu:
  $$\delta = \frac{\# (x_i > y_j) - \# (x_i < y_j)}{m \times n}$$
* Phân loại ngưỡng định lượng của Romano et al. [41]:
  * $|\delta| < 0.147$: Không đáng kể (**Negligible**).
  * $0.147 \le |\delta| < 0.33$: Nhỏ (**Small**).
  * $0.33 \le |\delta| < 0.474$: Trung bình (**Medium**).
  * $|\delta| \ge 0.474$: Lớn (**Large**).

### 3. Phân cụm xếp hạng Scott-Knott ESD
* Thuật toán phân cụm thống kê thứ bậc dựa trên kích thước hiệu ứng và phân tích phương sai, giúp gom các mô hình có hiệu năng tương đương về mặt thống kê vào cùng một nhóm thứ hạng (Rank-1, Rank-2, Rank-3...) mà không gặp hiện tượng trùng lặp nhóm như kiểm định post-hoc Bonferroni thông thường.
