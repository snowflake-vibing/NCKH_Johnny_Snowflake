# 📑 BẢN GIẢI THÍCH CHI TIẾT & CHIẾN LƯỢC HỌC THUẬT: THƯ HỎI TÁC GIẢ BÀI BÁO GPT2SP
## PHÂN TÍCH NGUYÊN TẮC NGOẠI GIAO HỌC THUẬT, MỤC ĐÍCH TỪNG CÂU HỎI VÀ CÁC KỊCH BẢN PHẢN HỒI

> **Tài liệu đối chiếu:** [01_inquiry_letter_to_gpt2sp_authors.md](01_inquiry_letter_to_gpt2sp_authors.md)  
> **Bài báo gốc:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả bài báo:** Michael (Yeh) Fu & PGS.TS. Chakkrit (Kla) Tantithamthavorn (Đại học Monash, Úc).

---

## 🧭 I. TỔNG QUAN & MỤC ĐÍCH CỦA BỨC THƯ

Trong cộng đồng nghiên cứu Kỹ nghệ Phần mềm đỉnh cao (IEEE TSE, ACM TOSEM, ICSE, FSE, MSR), việc liên hệ với tác giả bài báo gốc để làm rõ chi tiết thực nghiệm khi tái tạo (replication) là một **thực hành học thuật chuẩn mực** (Standard Academic Practice).

Việc gửi thư này phục vụ 3 mục tiêu chiến lược cho đề tài **NCKH_3**:
1. **Xác nhận tính trung thực khoa học (Scientific Rigor):** Làm rõ khoảng cách giữa bài báo lý thuyết (IEEE TSE) và mã nguồn công khai trên GitHub/Hugging Face mà không mang giọng điệu quy kết hay bắt bẻ.
2. **Thiết lập kênh liên lạc học thuật (Academic Networking):** Giới thiệu nhóm nghiên cứu của chúng ta với nhóm tác giả hàng đầu thế giới về SE/AI (nhóm AWSM của PGS. Chakkrit Tantithamthavorn).
3. **Mở đường cho đóng góp học thuật mới (Novel Contribution):** Bằng việc khéo léo đề cập đến vấn đề *Intra-issue Revision History* (lịch sử sửa đổi issue sau thời điểm planning), chúng ta đặt nền móng chứng minh rằng đề tài NCKH_3 không chỉ tái tạo bài báo của họ, mà còn **phát hiện và khắc phục rủi ro rò rỉ dữ liệu theo thời gian (Temporal Leakage)** mà nghiên cứu gốc chưa xử lý.

---

## 👥 II. ĐỐI TƯỢNG NHẬN THƯ & BỐI CẢNH TÁC GIẢ

* **Michael (Yeh) Fu** (`yeh.fu@monash.edu`):  
  - Tác giả thứ nhất (Lead Author), nghiên cứu sinh tiến sĩ (PhD Candidate) trực tiếp viết code, chạy thực nghiệm và upload checkpoint lên Hugging Face Hub (`MickyMike`).  
  - Là người nắm chi tiết kỹ thuật từng dòng code PyTorch và file notebook.
* **PGS.TS. Chakkrit (Kla) Tantithamthavorn** (`chakkrit@monash.edu`):  
  - Tác giả liên hệ (Corresponding Author), Phó Giáo sư (Associate Professor) tại Đại học Monash, một trong những nhà nghiên cứu AI4SE (AI for Software Engineering) có ảnh hưởng nhất thế giới với hàng trăm bài báo Q1/A*.  
  - Là người định hướng phương pháp luận, duyệt bản thảo và giám sát tính liêm chính học thuật của dự án.

---

## 🔍 III. GIẢI THÍCH CHI TIẾT TỪNG PHẦN CỦA BỨC THƯ (ACADEMIC STRATEGY BREAKDOWN)

### 1. Phần Mở đầu (Salutation & Rapport Building)
* **Nội dung:** Gửi lời chào lịch sự, giới thiệu nhóm nghiên cứu sinh viên đại học đang thực hiện đề tài về Agile Estimation, và **dành lời khen ngợi chân thành** cho đóng góp tiên phong của bài báo GPT2SP.
* **Chiến lược học thuật:** Tuyệt đối không nhảy bổ vào hỏi lỗi ngay lập tức. Các nhà nghiên cứu rất tự hào về công trình IEEE TSE của họ. Việc công nhận bài báo của họ là "seminal paper" và "groundbreaking milestone" tạo tâm lý cởi mở, thiện chí và tôn trọng.

---

### 2. Câu hỏi 1: Biểu diễn Dữ liệu Đầu vào (`Title` vs `Title + Description`)
* **Nội dung hỏi:** Bài báo nói dùng cả `Title + Description`, nhưng file `model_training_notebook.ipynb` chỉ trích `data['title']`. Kết quả trong Bảng 4 là dựa trên `title` hay có script nối thêm `description`?
* **Ý đồ chiến lược:**  
  - Trong thực tế, trường `description` trong Jira thường rất dài và chứa nhiều thông tin cập nhật muộn (post-planning comments, bug logs).  
  - Nếu tác giả chỉ chạy trên `title`, thì độ phức tạp và khả năng rò rỉ dữ liệu thấp hơn, nhưng kết quả bài báo lại khẳng định dùng cả 2.  
  - Câu hỏi này giúp ta biết chính xác input thực tế để tái tạo công bằng.

---

### 3. Câu hỏi 2: Ngưỡng Cắt ngắn Độ dài Chuỗi (`SEQUENCE_LEN = 20`)
* **Nội dung hỏi:** Tại sao notebook lại đặt `SEQUENCE_LEN = 20` trong khi GPT-2 hỗ trợ tới 1.024 tokens? Đây là lựa chọn vì giới hạn GPU/thời gian chạy trên 16 dự án hay đã có thực nghiệm chứng minh độ dài 20 là tối ưu?
* **Ý đồ chiến lược:**  
  - Độ dài 20 token là cực kỳ ngắn (chỉ khoảng 12-15 từ tiếng Anh), hầu như cắt vụn phần lớn mô tả yêu cầu phần mềm.  
  - Câu hỏi này lịch sự chỉ ra điểm thắt cổ chai lớn nhất của code public mà không chỉ trích, tạo cơ hội cho tác giả giải thích về tài nguyên phần cứng.

---

### 4. Câu hỏi 3: Kiến trúc Đầu MLP Head (`dense1`, `dense2`, `score`)
* **Nội dung hỏi:** Bài báo mô tả MLP có hàm kích hoạt phi tuyến GELU, nhưng code trong `GPT2SP.py` lại là 3 lớp `Linear` tuyến tính nối tiếp nhau liên tục:
  $$\text{hidden\_states} = \text{dense1}(\text{hidden\_states}) \rightarrow \text{dense2} \rightarrow \text{score}$$
* **Ý đồ chiến lược:**  
  - Về mặt toán học mạng nơ-ron: Tích của 3 phép biến đổi tuyến tính liên tiếp tương đương với **1 phép biến đổi tuyến tính duy nhất** ($W_{\text{eff}} = W_1 \times W_2 \times W_3$), làm mất đi tính biểu diễn phi tuyến của mạng nơ-ron sâu!
  - Việc hỏi câu này chứng minh nhóm chúng ta đã **đọc code ở mức độ vi mô cực kỳ cẩn thận**, tạo sự nể trọng học thuật từ phía tác giả.

---

### 5. Câu hỏi 4: Kết quả Chạy Thực nghiệm trên Checkpoint Spring XD
* **Nội dung hỏi:** Khi nhóm tải đúng checkpoint tác giả public trên Hugging Face (`MickyMike/0-GPT2SP-springxd`) và chạy inference trên tập test của Spring XD, kết quả MAE đo được là **1.7330**, trong khi Bảng 4 của bài báo ghi **MAE = 0.96**. Có cấu hình inference hoặc tiền xử lý đặc biệt nào khác biệt không?
* **Ý đồ chiến lược:**  
  - Đây là bằng chứng thực nghiệm thép (hard empirical evidence). Nhóm không nói "kết quả bài báo sai", mà trình bày: *"Khi chạy đúng checkpoint và đúng dataset công khai, chúng tôi quan sát thấy khoảng cách 1.73 vs 0.96, kính mong tác giả hướng dẫn cách cấu hình để đạt được con số 0.96"*.
  - Cách hành văn này biến vấn đề từ "nghi ngờ sai số" thành "mong muốn học hỏi cách tái tạo chuẩn xác".

---

### 6. Câu hỏi 5: Lịch sử Sửa đổi Issue & Động thái Thời gian (Temporal Dynamics)
* **Nội dung hỏi:** Khi khai thác dữ liệu Jira kết thúc dự án, các trường issue thường đã bị sửa chữa sau buổi họp Sprint Planning. Nhóm có cân nhắc đến việc trích xuất snapshot tại thời điểm planning không?
* **Ý đồ chiến lược:**  
  - Đây là **"nước cờ quyết định"** nâng tầm bức thư.  
  - Nó báo hiệu rằng nhóm nghiên cứu của chúng ta đang thực hiện một công trình khoa học vượt lên trên (beyond) GPT2SP: kiểm soát rò rỉ dữ liệu theo thời gian (*Temporal & Data Leakage Control*).  
  - Nếu tác giả đồng tình, đây sẽ là trích dẫn lý tưởng để đưa vào bài báo NCKH của chúng ta: *"Như tác giả bài báo gốc đã xác nhận trong trao đổi học thuật cá nhân..."*.

---

## 🎭 IV. BA KỊCH BẢN PHẢN HỒI VÀ HƯỚNG XỬ LÝ CỦA NHÓM

| Kịch bản | Khả năng | Phản ứng của tác giả | Hướng xử lý của Nhóm 3 |
| :--- | :---: | :--- | :--- |
| **Kịch bản A: Hợp tác tích cực** | ~35% | Tác giả trả lời chi tiết, gửi bổ sung script mới, giải thích lý do cắt 20 token và hoan nghênh hướng nghiên cứu về Temporal Leakage. | • Cảm ơn tác giả trang trọng.<br>• Sử dụng dữ liệu giải thích làm căn cứ thực nghiệm.<br>• Đưa nhóm AWSM vào mục *Acknowledgments* trong bài báo NCKH. |
| **Kịch bản B: Thừa nhận mã nguồn tinh giản** | ~40% | Tác giả thừa nhận mã nguồn trên GitHub là bản rút gọn/demo phục vụ công bố, còn bản chạy ra Bảng 4 nằm trên cluster riêng của lab và có thể khó tái tạo 100%. | • Đây là tình huống rất phổ biến trong Computer Science.<br>• Ta ghi nhận đây là minh chứng vững chắc cho báo cáo NCKH: công bố kết quả của bài báo gốc có độ nhạy cảm cao với môi trường tái tạo. |
| **Kịch bản C: Không hồi âm sau 2-3 tuần** | ~25% | Các giáo sư lớn thường nhận hàng trăm email mỗi ngày nên có thể bị trôi thư hoặc không có thời gian xử lý các chi tiết kỹ thuật cũ (bài báo 2022-2023). | • Sau 14 ngày, gửi một email nhắc nhở nhẹ nhàng (gentle reminder).<br>• Nếu vẫn không có phản hồi, nhóm vẫn hoàn toàn có quyền học thuật để trích dẫn: *"Dựa trên replication package công khai chính thức tại thời điểm thực nghiệm..."*. |

---

## 📮 V. HƯỚNG DẪN THỰC TẾ KHI GỬI EMAIL

1. **Địa chỉ gửi:**
   - **To:** `yeh.fu@monash.edu`
   - **Cc:** `chakkrit@monash.edu`, [Email của Giảng viên Hướng dẫn NCKH của bạn]
2. **Tiêu đề email (Subject Line):**  
   `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`  
   *(Giữ nguyên tiêu đề chuẩn xác này để email không bị rơi vào hòm thư rác Spam)*.
3. **Thời điểm gửi tối ưu:**  
   - Thứ Ba hoặc Thứ Tư, vào khoảng **08:30 – 09:30 sáng giờ Melbourne (GMT+11)**, tức khoảng **04:30 – 05:30 sáng giờ Việt Nam**. Tránh gửi vào tối thứ Sáu hoặc cuối tuần vì thư sẽ bị vùi lấp vào sáng thứ Hai.
4. **Thay thế thông tin cá nhân:**  
   - Thay `[Your Name]`, `[Your University / Institution]`, `[Advisor's Name]` trong file bản thảo bằng thông tin thực tế trước khi bấm gửi.
