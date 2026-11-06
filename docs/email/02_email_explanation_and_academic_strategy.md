# 📑 BẢN GIẢI THÍCH CHI TIẾT & CHIẾN LƯỢC HỌC THUẬT: THƯ HỎI TÁC GIẢ BÀI BÁO GPT2SP
## PHÂN TÍCH NGUYÊN TẮC NGOẠI GIAO HỌC THUẬT, ĐỊNH DẠNG RICH-TEXT, GIF MINH HỌA VÀ FOOTER SIGNATURE CARD

> **Tài liệu đối chiếu:** [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md)  
> **Bài báo gốc:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả bài báo:** Michael (Yeh) Fu & PGS.TS. Chakkrit (Kla) Tantithamthavorn (Đại học Monash, Úc).

---

## 👥 I. ĐỘI NGŨ NGHIÊN CỨU GỬI THƯ (RESEARCH TEAM PROFILE)

Bức thư đại diện chính thức cho Nhóm nghiên cứu thuộc Đề tài NCKH 2026:
* **Người gửi chính (Primary Sender):** **Lê Thành Hiệu** (MSSV: `24520496`) — Sinh viên Nghiên cứu khoa học, Khoa Hệ thống Thông tin, Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNU-HCM).
* **Cộng tác viên nghiên cứu (Research Partner):** **Phan Ngọc Đức Huy** (MSSV: `24520695`) — Sinh viên Nghiên cứu khoa học, UIT - VNU-HCM.
* **Giảng viên hướng dẫn (Academic Advisor):** **ThS. Tạ Việt Phương** — Giảng viên & Nhà nghiên cứu, Khoa Hệ thống Thông tin, UIT - VNU-HCM.
* **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*.
* **Mã nguồn công khai:** [`https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake`](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)

---

## 🎨 II. CHIẾN LƯỢC ĐỊNH DẠNG EMAIL: RICH-TEXT, GIF VÀ SIGNATURE CARD FOOTER

Khác với các email thông thường, email học thuật quốc tế gửi tới các Giáo sư và Nhà nghiên cứu hàng đầu cần cân bằng giữa **sự trang nhã, nghiêm túc khoa học** và **ấn tượng thị giác chuyên nghiệp**.

### 1. Tại sao dùng Rich-Text / HTML Card?
* Các nhà nghiên cứu tại Đại học Monash (Úc) thường sử dụng Outlook hoặc Gmail for Education với màn hình độ phân giải cao.
* Việc đóng khung từng câu hỏi vào các **Callout Box** có viền xanh (`border-left: 4px solid #3b82f6`) và nền xám nhạt (`#f8fafc`) giúp các tác giả:
  - Dễ dàng lướt nhanh (scan) nội dung trong 30 giây.
  - Phân tách rành mạch 5 câu hỏi độc lập.
  - Trực quan hóa đoạn mã nguồn PyTorch với nền đen (`#1e293b`) như trên IDE thực thụ.

### 2. Ý nghĩa của Banner GIF / Ảnh động Minh họa
* **Vị trí đặt:** Ngay sau phần mở đầu, trước khi bước vào các câu hỏi kỹ thuật.
* **Mục đích:**  
  - Tạo điểm nhấn thị giác đẳng cấp, nhắc nhở trực quan về cấu trúc Transformer / Attention Flow mà chính các tác giả đã dày công xây dựng trong GPT2SP.
  - Thể hiện sự đầu tư chỉn chu của sinh viên Việt Nam đối với đề tài, tạo cảm giác đây là một nhóm nghiên cứu được đào tạo bài bản và làm việc nghiêm túc chứ không phải một câu hỏi bộc phát.

### 3. Thẻ Chữ ký Chuyên nghiệp ở Footer (Academic Footer Card)
* Thẻ Footer Card chia làm 2 cột:
  - **Cột trái:** Ghi rõ danh tính của bạn (**Lê Thành Hiệu**), bạn đồng hành (**Phan Ngọc Đức Huy**), và Giảng viên hướng dẫn (**ThS. Tạ Việt Phương**), cùng đơn vị trường *UIT - VNU-HCM*.
  - **Cột phải:** Huy hiệu trường (UIT &bull; VNU-HCM), link trực tiếp tới GitHub Repository của nhóm và địa danh Ho Chi Minh City, Vietnam.
* **Tác dụng:** Tăng độ tín nhiệm (Credibility). Khi tác giả thấy có tên Giảng viên hướng dẫn và link GitHub nghiên cứu minh bạch, tỷ lệ họ dành thời gian trả lời chi tiết tăng lên gấp 3 lần!

---

## 🔍 III. GIẢI THÍCH CHI TIẾT Ý ĐỒ CHIẾN LƯỢC CỦA 5 CÂU HỎI

### Câu hỏi 1: Biểu diễn Dữ liệu Đầu vào (`Title` vs `Title + Description`)
* **Ý đồ:** Chỉ ra khoảng cách giữa phần văn bản bài báo (nói dùng cả Title + Description) và file `model_training_notebook.ipynb` (chỉ nạp `data['title']`).  
* **Mục tiêu:** Giúp nhóm biết chắc chắn kết quả Bảng 4 đến từ cấu hình nào để tái tạo công bằng.

### Câu hỏi 2: Ngưỡng Cắt ngắn Độ dài Chuỗi (`SEQUENCE_LEN = 20`)
* **Ý đồ:** Đặt câu hỏi lịch sự về việc vì sao độ dài cắt chỉ là 20 tokens (khoảng 12-15 từ).  
* **Mục tiêu:** Vừa hiểu được lý do hạn chế phần cứng khi train 16 dự án, vừa cho thấy nhóm đã phân tích sâu các siêu tham số.

### Câu hỏi 3: Kiến trúc Đầu MLP Head (`dense1`, `dense2`, `score`)
* **Ý đồ:** Phát hiện việc thiếu hàm kích hoạt phi tuyến `gelu()` trong code PyTorch (khiến 3 lớp Linear gộp lại thành 1 phép nhân ma trận tuyến tính đơn).  
* **Mục tiêu:** Chứng minh trình độ đọc hiểu code ở cấp độ toán học vi mô của nhóm, tạo sự khâm phục từ tác giả.

### Câu hỏi 4: Kết quả Chạy Thực nghiệm trên Checkpoint Spring XD
* **Ý đồ:** Nhóm đưa ra số liệu thực tế đo được từ checkpoint chính thức của họ: **MAE = 1.7330** (xấp xỉ Baseline trung vị 1.7153), cách xa con số **0.96** trong Bảng 4.  
* **Mục tiêu:** Bằng chứng thực nghiệm không thể chối cãi, nhưng diễn đạt dưới dạng "chúng tôi mong muốn học hỏi script đánh giá chuẩn của tác giả".

### Câu hỏi 5: Thảo luận về Lịch sử Sửa đổi Issue & Temporal Leakage
* **Ý đồ:** Đề cập hiện tượng các mô tả issue trong Jira bị bổ sung chi tiết sau ngày planning.  
* **Mục tiêu chiến lược:** **Đây là "đòn bẩy" quan trọng nhất**! Nó ngầm giới thiệu bài toán mới của đề tài NCKH_3 của Lê Thành Hiệu & Phan Ngọc Đức Huy về *Kiểm soát Rò rỉ Dữ liệu Thời gian (Temporal Leakage)*.

---

## 📋 IV. HƯỚNG DẪN THỰC HÀNH CÁCH GỬI EMAIL TRÊN GMAIL / OUTLOOK

### Cách 1: Copy trực tiếp Rich-Text (Đơn giản & Đẹp nhất)
1. Mở file [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md) ở chế độ Preview (Xem trước Markdown trong VS Code hoặc GitHub).
2. Dùng chuột bôi đen toàn bộ vùng khung **BẢN 1** (từ chữ *Dear Michael...* đến hết thẻ *Footer Card*).
3. Nhấn `Ctrl + C` (Copy).
4. Mở cửa sổ soạn thư mới trong Gmail hoặc Outlook.
5. Nhấn `Ctrl + V` (Paste). Toàn bộ định dạng bảng, màu sắc, font chữ, code block và thẻ card footer sẽ được giữ nguyên vẹn 100%!

### Cách 2: Sử dụng Bản Plain-Text (Bản 2)
* Nếu bạn hoặc Giảng viên hướng dẫn thích văn phong thuần chữ tối giản (Pure Plain Text), hãy copy toàn bộ khối mã trong **BẢN 2** để gửi.

---

## 📮 V. DANH SÁCH ĐỊA CHỈ & THỜI ĐIỂM GỬI TỐI ƯU

* **To:** `yeh.fu@monash.edu`
* **Cc:** `chakkrit@monash.edu`, [Email của ThS. Tạ Việt Phương]
* **Subject:** `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`
* **Thời điểm gửi lý tưởng:**
  - Ngày: Thứ Ba hoặc Thứ Tư (tránh thứ Hai họp hành và thứ Sáu chuẩn bị nghỉ cuối tuần).
  - Giờ: **04:30 – 05:30 sáng giờ Việt Nam** (tương đương **08:30 – 09:30 sáng giờ Melbourne, GMT+11**). Thư sẽ nằm ngay đầu hòm thư của 2 tác giả khi họ vừa mở máy tính bắt đầu ngày làm việc mới!
