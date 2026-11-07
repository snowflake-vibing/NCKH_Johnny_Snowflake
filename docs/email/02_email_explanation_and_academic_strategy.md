# 📑 BẢN GIẢI THÍCH CHI TIẾT & CHIẾN LƯỢC HỌC THUẬT: THƯ HỎI TÁC GIẢ BÀI BÁO GPT2SP
## PHÂN TÍCH NGUYÊN TẮC NGOẠI GIAO HỌC THUẬT, BÓC TÁCH CHI TIẾT 5 CÂU HỎI KỸ THUẬT, 3 KỊCH BẢN PHẢN HỒI VÀ THIẾT KẾ EMAIL SIGNATURE

> **Tài liệu đối chiếu:** [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md)  
> **Bài báo gốc:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả bài báo:** Michael (Yeh) Fu & PGS.TS. Chakkrit (Kla) Tantithamthavorn (Đại học Monash, Úc).

---

## 👥 I. ĐỘI NGŨ NGHIÊN CỨU GỬI THƯ (RESEARCH TEAM PROFILE)

Bức thư đại diện chính thức cho Nhóm nghiên cứu thuộc Đề tài NCKH 2026:
* **Người gửi chính (Primary Sender):** **Lê Thành Hiệu** (MSSV: `24520496`) — Sinh viên Nghiên cứu khoa học, Khoa Hệ thống Thông tin, Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNU-HCM).
* **Cộng sự cùng thực hiện (Co-Investigator / Partner):** **Phan Ngọc Đức Huy** (MSSV: `24520695`) — Sinh viên Nghiên cứu khoa học, UIT - VNU-HCM.
* **Giảng viên hướng dẫn (Academic Advisor):** **ThS. Tạ Việt Phương** — Giảng viên & Nhà nghiên cứu, Khoa Hệ thống Thông tin, UIT - VNU-HCM.
* **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*.
* **Mã nguồn công khai:** [`https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake`](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)

---

## 🧭 II. TỔNG QUAN & MỤC ĐÍCH CỦA BỨC THƯ

Trong cộng đồng nghiên cứu Kỹ nghệ Phần mềm đỉnh cao (IEEE TSE, ACM TOSEM, ICSE, FSE, MSR), việc liên hệ với tác giả bài báo gốc để làm rõ chi tiết thực nghiệm khi tái tạo (replication) là một **thực hành học thuật chuẩn mực** (Standard Academic Practice).

Việc gửi thư này phục vụ 3 mục tiêu chiến lược cho đề tài **NCKH_3**:
1. **Xác nhận tính trung thực khoa học (Scientific Rigor):** Làm rõ khoảng cách giữa bài báo lý thuyết (IEEE TSE) và mã nguồn/checkpoint công khai trên GitHub/Hugging Face mà không mang giọng điệu quy kết hay bắt bẻ.
2. **Thiết lập kênh liên lạc học thuật (Academic Networking):** Giới thiệu nhóm nghiên cứu của chúng ta với nhóm tác giả hàng đầu thế giới về SE/AI (nhóm AWSM của PGS. Chakkrit Tantithamthavorn tại Đại học Monash).
3. **Mở đường cho đóng góp học thuật mới (Novel Contribution):** Bằng việc khéo léo đề cập đến vấn đề *Intra-issue Revision History* (lịch sử sửa đổi issue sau thời điểm planning), chúng ta đặt nền móng chứng minh rằng đề tài NCKH_3 không chỉ tái tạo bài báo của họ, mà còn **phát hiện và khắc phục rủi ro rò rỉ dữ liệu theo thời gian (Temporal Leakage)** mà nghiên cứu gốc chưa xử lý.

---

## 🔍 III. BÓC TÁCH CHI TIẾT TỪNG PHẦN CỦA BỨC THƯ (ACADEMIC STRATEGY BREAKDOWN)

### 1. Phần Mở đầu (Salutation & Rapport Building)
* **Nội dung:** Gửi lời chào lịch sự, giới thiệu nhóm nghiên cứu sinh viên đại học (Lê Thành Hiệu, Phan Ngọc Đức Huy, ThS. Tạ Việt Phương tại UIT - VNU-HCM) đang thực hiện đề tài về Agile Estimation, và **dành lời khen ngợi chân thành** cho đóng góp tiên phong của bài báo GPT2SP.
* **Chiến lược học thuật:** Tuyệt đối không nhảy bổ vào hỏi lỗi ngay lập tức. Các nhà nghiên cứu rất tự hào về công trình IEEE TSE của họ. Việc công nhận bài báo của họ là "seminal paper" và "groundbreaking milestone" tạo tâm lý cởi mở, thiện chí và tôn trọng.

---

### 2. Câu hỏi 1: Biểu diễn Dữ liệu Đầu vào (`Title` vs. `Title + Description`)
* **Vị trí bài báo gốc:** Section 3.1 (*Context Extraction*, trang 3) và Section 4.1 (*Experimental Setup*, trang 7).
* **Nội dung đối chiếu mã nguồn:**
  Trong văn bản bài báo, tác giả khẳng định mô hình khai thác cả `Title` (tiêu đề) lẫn `Description` (mô tả chi tiết) để giữ trọn ngữ nghĩa kỹ thuật của issue. Tuy nhiên, khi kiểm tra notebook chính thức (`model_training_notebook.ipynb`, hàm `prepare_dataframe`):
  ```python
  d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
  ```
  Dữ liệu đưa vào huấn luyện thực tế **chỉ lấy duy nhất trường `title`**!
* **Ý đồ chiến lược:**
  - Trong thực tế, trường `description` trong Jira thường rất dài và chứa nhiều thông tin cập nhật muộn (post-planning comments, bug logs).
  - Nếu tác giả chỉ chạy trên `title`, thì độ phức tạp và khả năng rò rỉ dữ liệu thấp hơn, nhưng kết quả bài báo lại khẳng định dùng cả hai.
  - Câu hỏi này giúp nhóm xác định chính xác cấu hình thực nghiệm thực tế mà tác giả đã dùng để ra được Bảng 4.

---

### 3. Câu hỏi 2: Ngưỡng Cắt ngắn Độ dài Chuỗi (`SEQUENCE_LEN = 20`)
* **Vị trí bài báo gốc:** Section 4.1 (*Experimental Setup*, trang 7) và file `model_training_notebook.ipynb`.
* **Nội dung đối chiếu mã nguồn:**
  Mô hình gốc GPT-2 có cửa sổ ngữ cảnh lên tới 1.024 tokens. Tuy nhiên, trong notebook huấn luyện, tác giả lại cố định cứng:
  ```python
  SEQUENCE_LEN = 20
  ```
* **Ý đồ chiến lược:**
  - Ngưỡng 20 token là cực kỳ ngắn (chỉ tương đương khoảng 12 – 15 từ tiếng Anh), đồng nghĩa với việc hầu hết các câu mô tả yêu cầu phần mềm đều bị cắt cụt phần đuôi.
  - Câu hỏi này lịch sự chỉ ra điểm thắt cổ chai lớn nhất của code public mà không mang tính chỉ trích: hỏi xem đây là tối ưu hóa có chủ đích để tiết kiệm GPU khi chạy 16 dự án hay tác giả đã từng thử nghiệm với các độ dài lớn hơn (128, 512).

---

### 4. Câu hỏi 3: Kiến trúc Đầu MLP Head (`dense1`, `dense2`, `score`) & Thiếu Hàm Phi Tuyến GELU
* **Vị trí bài báo gốc:** Section 3.3 (*Story Point Regression*, trang 4).
* **Nội dung đối chiếu mã nguồn:**
  Bài báo mô tả đầu hồi quy MLP Regressor Head có tích hợp hàm kích hoạt phi tuyến GELU giữa các tầng ẩn. Tuy nhiên, trong file `GPT2SP.py`:
  ```python
  hidden_states = self.dense1(hidden_states)
  hidden_states = self.dense2(hidden_states)
  logits = self.score(hidden_states)
  ```
  Tensor chảy qua 3 tầng Linear liên tiếp mà **hoàn toàn không có hàm kích hoạt phi tuyến nào** (`F.gelu()`).
* **Ý đồ chiến lược:**
  - Về mặt toán học mạng nơ-ron: Tích của 3 phép biến đổi tuyến tính liên tiếp tương đương với **1 phép biến đổi tuyến tính duy nhất** ($W_{\text{eff}} = W_1 \times W_2 \times W_3$), làm triệt tiêu khả năng học quan hệ phi tuyến phức tạp của mạng sâu!
  - Việc hỏi câu này chứng minh nhóm nghiên cứu của chúng ta đã **đọc code ở cấp độ giải tích toán học vi mô**, tạo sự nể trọng học thuật rất lớn từ phía Michael Fu và PGS. Chakkrit.

---

### 5. Câu hỏi 4: Kết quả Chạy Thực nghiệm Đối chứng Checkpoint Spring XD (MAE 3.3090 vs. 0.96)
* **Vị trí bài báo gốc:** Table 4 (*Comparison of MAE on Within-project Estimation*, trang 8).
* **Nội dung đối chiếu thực nghiệm thực tế:**
  - Khi nhóm chúng ta tải đúng checkpoint chính thức của tác giả trên Hugging Face (`MickyMike/0-GPT2SP-springxd`) và chạy inference trên 706 issue của tập Test dự án Spring XD trên Kaggle GPU:
    - **Median Effort Baseline (Trung vị):** $\text{MAE} = 1.7153$
    - **GPT2SP (Checkpoint MickyMike trên Kaggle):** $\text{MAE} = 3.3090$ (hoặc $\sim 1.7330$ nếu tiền xử lý chặt chẽ).
    - **Wilcoxon Signed-Rank Test:** $p = 1.48 \times 10^{-84}$ (sai khác có ý nghĩa thống kê áp đảo).
  - Trong khi đó, **Bảng 4 trong bài báo IEEE TSE 2023** lại tuyên bố con số kỷ lục: $\text{MAE} = 0.96$!
* **Ý đồ chiến lược:**
  - Đây là **bằng chứng thực nghiệm thép** (hard empirical evidence). Nhóm không hề nói "kết quả bài báo sai", mà trình bày: *"Khi chạy đúng checkpoint và đúng dataset công khai, chúng tôi quan sát thấy khoảng cách từ 1.73 – 3.31 so với 0.96, kính mong tác giả chia sẻ script đánh giá chuẩn xác để nhóm có thể tái hiện được con số 0.96"*.
  - Cách hành văn này biến vấn đề từ "nghi ngờ số liệu" thành "mong muốn học hỏi cách tái tạo chuẩn mực".

---

### 6. Câu hỏi 5: Lịch sử Sửa đổi Issue & Động thái Thời gian (Temporal Dynamics & Leakage)
* **Nội dung hỏi:** Khi khai thác dữ liệu Jira kết thúc dự án, các trường issue thường đã bị sửa chữa sau buổi họp Sprint Planning (bổ sung stack trace, bug report, lời giải). Nhóm tác giả có cân nhắc đến việc trích xuất snapshot tại thời điểm planning không?
* **Ý đồ chiến lược:**
  - **Đây là "nước cờ quyết định" nâng tầm toàn bộ bức thư!**
  - Nó báo hiệu rằng nhóm nghiên cứu của chúng ta không chỉ dừng lại ở việc replicate, mà đang thực hiện một công trình khoa học vượt lên trên (beyond) GPT2SP: **Kiểm soát rò rỉ dữ liệu theo thời gian (Temporal & Data Leakage Control)**.
  - Nếu tác giả hồi đáp đồng tình, đây sẽ là trích dẫn đắt giá nhất để đưa vào bài báo NCKH của nhóm: *"Như tác giả bài báo gốc đã xác nhận trong trao đổi học thuật cá nhân..."*.

---

## 🎭 IV. BA KỊCH BẢN PHẢN HỒI VÀ HƯỚNG XỬ LÝ CỦA NHÓM

| Kịch bản | Khả năng | Phản ứng dự kiến của tác giả | Hướng xử lý khoa học của Nhóm 3 |
| :--- | :---: | :--- | :--- |
| **Kịch bản A: Hợp tác tích cực** | ~35% | Tác giả trả lời chi tiết, gửi bổ sung evaluation script chuẩn, giải thích lý do cắt 20 token và hoan nghênh hướng nghiên cứu về Temporal Leakage của nhóm. | • Cảm ơn tác giả trang trọng.<br>• Chạy kiểm chứng lại với script bổ sung.<br>• Đưa nhóm AWSM (Monash) vào mục *Acknowledgments* trong bài báo NCKH của chúng ta. |
| **Kịch bản B: Thừa nhận mã nguồn tinh giản** | ~40% | Tác giả thừa nhận mã nguồn/checkpoint trên GitHub & Hugging Face là bản rút gọn/demo phục vụ công bố, còn bản chạy ra Bảng 4 nằm trên cluster nội bộ của lab. | • Đây là tình huống cực kỳ phổ biến trong Computer Science.<br>• Nhóm ghi nhận đây là minh chứng vững chắc cho báo cáo NCKH: kết quả công bố có độ nhạy cảm cao và replication package công khai chưa đủ để tái tạo hoàn toàn. |
| **Kịch bản C: Không hồi âm sau 2-3 tuần** | ~25% | Các giáo sư lớn thường nhận hàng trăm email mỗi ngày nên có thể bị trôi thư hoặc không còn lưu trữ môi trường chạy của bài báo cũ (2022-2023). | • Sau 14 ngày, gửi một email nhắc nhở nhẹ nhàng (gentle follow-up).<br>• Nếu vẫn không có phản hồi, nhóm vẫn hoàn toàn có quyền học thuật để khẳng định: *"Dựa trên replication package công khai chính thức tại thời điểm thực nghiệm..."*. |

---

## 🎨 V. Ý NGHĨA THIẾT KẾ: GIF "HAVE A NICE DAY" VÀ FOOTER SIGNATURE CARD 3 CỘT

Khác với email thông thường, email học thuật gửi tới các giáo sư quốc tế cần cân bằng giữa **sự trang nhã khoa học** và **ấn tượng thị giác chuyên nghiệp**.

### 1. Vị trí & Tác dụng của GIF "Have a nice day!"
* **Vị trí đặt:** Đặt ở **dưới cùng của nội dung email**, ngay trước lời chào kết (*Warmest regards*).
* **Nội dung:** Ảnh động nhẹ nhàng mang thông điệp *"Have a nice day! Wishing you a wonderful & inspiring day ahead!"* cùng biểu tượng mặt trời tỏa nắng thân thiện.
* **Tác dụng:**
  - Làm dịu đi tính kỹ thuật căng thẳng của 5 câu hỏi phản biện phía trên.
  - Mang lại nụ cười và năng lượng tích cực cho 2 tác giả khi mở thư vào buổi sáng, thể hiện sự kính trọng và tính nhân văn của sinh viên Việt Nam.
  - File GIF chỉ nặng **15.8 KB**, được lưu trữ trực tiếp trên GitHub repository của nhóm nên tốc độ tải tức thì, không làm chậm email và không bị bộ lọc spam chặn.

### 2. Thiết kế Thẻ Chữ ký Chuyên nghiệp ở Footer (3 Phân Vùng)
Bảng chữ ký footer được thiết kế bằng bảng HTML tương thích tuyệt đối với mọi ứng dụng email (Gmail, Outlook, Apple Mail):

```text
┌─────────────────┬──────────────────────────────────────┬─────────────────┐
│                 │  Le Thanh Hieu                       │ CONNECT WITH US │
│    [LOGO UIT]   │  Undergraduate Student Researcher    │  🐙 GitHub Repo │
│   UIT • VNU-HCM │  Partner: Phan Ngoc Duc Huy          │  💼 LinkedIn    │
│                 │  Advisor: Mr. Ta Viet Phuong         │  👥 Facebook    │
│                 │  Faculty of Information Systems      │                 │
└─────────────────┴──────────────────────────────────────┴─────────────────┘
```

1. **Cột bên trái — Logo UIT:**  
   - Logo chính thức của Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (`uit_logo.png`), viền nét trong suốt.
   - Thể hiện tính chính danh và danh tiếng học thuật của nhà trường.
2. **Cột ở giữa — Thông tin chi tiết của Nhóm:**  
   - Tên người gửi chính (**Lê Thành Hiệu** - MSSV: `24520496`).
   - Tên bạn đồng hành (**Phan Ngọc Đức Huy** - MSSV: `24520695`).
   - Tên Giảng viên hướng dẫn (**ThS. Tạ Việt Phương**), Khoa Hệ thống Thông tin.
3. **Cột bên phải — Menu Mạng Xã hội & Nghiên cứu (Connect with us):**  
   - **GitHub Repo:** Link thẳng tới repository nghiên cứu mở NCKH_Johnny_Snowflake (`https://github.com/snowflake-vibing`).
   - **LinkedIn:** Link trực tiếp tới trang LinkedIn cá nhân của Lê Thành Hiệu (`https://www.linkedin.com/in/thành-hiệu-84b99634b/`).
   - **Facebook:** Link kết nối mạng xã hội.

---

## 📮 VI. HƯỚNG DẪN THỰC HÀNH CÁCH GỬI EMAIL TRÊN GMAIL / OUTLOOK

### 1. Cách dán vào Gmail / Outlook (Bản Rich-Text đẹp nhất)
1. Mở file [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md) ở chế độ Preview (Markdown preview).
2. Dùng chuột bôi đen toàn bộ vùng khung **BẢN 1** (từ chữ *Dear Michael...* đến hết thẻ *Footer Card*).
3. Nhấn `Ctrl + C` $\rightarrow$ mở khung soạn thư mới của Gmail hoặc Outlook $\rightarrow$ nhấn `Ctrl + V`. Toàn bộ định dạng bảng, màu sắc, font chữ, code block, GIF và thẻ footer sẽ được giữ nguyên vẹn 100%!

### 2. Thông tin địa chỉ & thời điểm gửi tối ưu
* **To:** `yeh.fu@monash.edu`
* **Cc:** `chakkrit@monash.edu`, [Email của ThS. Tạ Việt Phương]
* **Subject:** `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`
* **Thời điểm gửi lý tưởng:**
  - Ngày: Thứ Ba hoặc Thứ Tư (tránh thứ Hai họp hành và thứ Sáu chuẩn bị nghỉ cuối tuần).
  - Giờ: **04:30 – 05:30 sáng giờ Việt Nam** (tương đương **08:30 – 09:30 sáng giờ Melbourne, GMT+11**). Thư sẽ nằm ngay đầu hòm thư của 2 tác giả khi họ vừa mở máy tính bắt đầu ngày làm việc mới!
