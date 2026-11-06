# 📑 BẢN GIẢI THÍCH CHI TIẾT & CHIẾN LƯỢC HỌC THUẬT: THƯ HỎI TÁC GIẢ BÀI BÁO GPT2SP
## PHÂN TÍCH NGUYÊN TẮC NGOẠI GIAO HỌC THUẬT, THIẾT KẾ THẺ CHỮ KÝ 3 PHẦN VÀ GIF "HAVE A NICE DAY"

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

## 🎨 II. Ý NGHĨA THIẾT KẾ: GIF "HAVE A NICE DAY" VÀ FOOTER SIGNATURE CARD 3 CỘT

Việc gửi email học thuật đến các giáo sư quốc tế đòi hỏi sự chuẩn mực cao, song một chút tinh tế và thân thiện ở phần kết sẽ tạo cảm giác ấm áp, gần gũi và khác biệt hoàn toàn so với những bức thư khô khan thông thường.

### 1. Vị trí & Tác dụng của GIF "Have a nice day!"
* **Vị trí đặt:** Đặt ở **dưới cùng của nội dung email**, ngay trước lời chào kết (*Warmest regards*).
* **Nội dung:** Ảnh động nhẹ nhàng mang thông điệp *"Have a nice day! Wishing you a wonderful & inspiring day ahead!"* cùng biểu tượng mặt trời tỏa nắng thân thiện.
* **Tác dụng tâm lý học:**  
  - Làm dịu đi tính kỹ thuật căng thẳng của 5 câu hỏi phản biện phía trên.
  - Mang lại nụ cười và năng lượng tích cực cho 2 tác giả khi đọc thư vào buổi sáng, thể hiện sự kính trọng và tính nhân văn của sinh viên Việt Nam.
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
   - Tên người gửi chính (**Lê Thành Hiệu** - `24520496`).
   - Tên bạn đồng hành (**Phan Ngọc Đức Huy** - `24520695`).
   - Tên Giảng viên hướng dẫn (**ThS. Tạ Việt Phương**), Khoa Hệ thống Thông tin.
3. **Cột bên phải — Menu Mạng Xã hội & Nghiên cứu (Connect with us):**  
   - **GitHub Repo:** Link thẳng tới repository nghiên cứu mở NCKH_Johnny_Snowflake.
   - **LinkedIn & Facebook:** Giúp tác giả Michael Fu hoặc PGS. Chakkrit có thể dễ dàng bấm vào xem trang cá nhân, kết nối mạng lưới học thuật lâu dài.

---

## 🔍 III. Ý ĐỒ CHIẾN LƯỢC CỦA 5 CÂU HỎI KỸ THUẬT

1. **Câu 1 (`Title` vs `Title + Description`):** Làm rõ dữ liệu đầu vào thực sự dùng trong Bảng 4 của bài báo.
2. **Câu 2 (`SEQUENCE_LEN = 20`):** Đặt câu hỏi vì sao cắt ngắn chỉ 20 token để tìm hiểu về giới hạn GPU và tài nguyên.
3. **Câu 3 (Thiếu GELU trong MLP Head):** Chỉ ra việc 3 lớp Linear nối tiếp nhau bị triệt tiêu tính phi tuyến, chứng minh nhóm đọc hiểu code ở tầng toán học sâu sắc.
4. **Câu 4 (MAE 1.7330 vs 0.96 trên Spring XD):** Trình bày bằng chứng đối chứng thực nghiệm trên checkpoint chính thức của tác giả, hỏi về script đánh giá chuẩn.
5. **Câu 5 (Temporal Leakage & Intra-issue Revision):** **Bàn đạp chiến lược quan trọng nhất**, mở đường giới thiệu đề tài NCKH_3 về kiểm soát rò rỉ dữ liệu sau planning.

---

## 📋 IV. HƯỚNG DẪN THỰC HÀNH KHI GỬI THƯ

### 1. Cách thay link cá nhân (LinkedIn & Facebook) của bạn
Trong file [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md), bạn chỉ cần thay đường dẫn:
* `https://www.linkedin.com` $\rightarrow$ `https://www.linkedin.com/in/ten-linkedin-cua-hieu`
* `https://www.facebook.com` $\rightarrow$ `https://www.facebook.com/ten-facebook-cua-hieu`

### 2. Cách dán vào Gmail / Outlook
1. Mở file [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md) ở chế độ Preview.
2. Bôi đen từ đầu đến hết thẻ Footer Card của **BẢN 1**.
3. Nhấn `Ctrl + C` $\rightarrow$ mở khung soạn thư Gmail / Outlook $\rightarrow$ nhấn `Ctrl + V`.
4. Điền:
   - **To:** `yeh.fu@monash.edu`
   - **Cc:** `chakkrit@monash.edu`, [Email của ThS. Tạ Việt Phương]
   - **Subject:** `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`
5. Gửi vào sáng sớm thứ Ba hoặc thứ Tư (khoảng 04:30 – 05:30 sáng giờ Việt Nam, tức 08:30 – 09:30 sáng giờ Melbourne) để thư luôn nằm ở vị trí đầu tiên trong hòm thư của 2 tác giả!
