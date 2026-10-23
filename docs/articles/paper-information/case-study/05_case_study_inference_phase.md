# 🔬 CASE STUDY CHUYÊN SÂU 05: HÌNH DUNG TOÀN DIỆN PHA SUY LUẬN (INFERENCE PHASE) CỦA GPT2SP

> **Mục tiêu tài liệu:**  
> Giải thích chi tiết, trực quan bằng ngôn ngữ đời thường và số liệu thực tế về cách mô hình AI vận hành trong thực tế để ước lượng một User Story mới tinh, **hoàn toàn không dùng sơ đồ khối trừu tượng**.  
> **Dự án thực tế:** Dự án Spring XD — Khảo sát trực tiếp buổi họp Sprint Planning cho User Story hoàn toàn mới `XD-4012` (chưa từng có điểm Story Point).

---

## 🎯 1. BỨC TRANH TỔNG THỂ: SUY LUẬN (INFERENCE) THỰC CHẤT LÀ LÀM GÌ?

Nếu như ở **Pha Huấn luyện (Training Phase)**, mô hình giống như một cậu thực tập sinh phải ngày đêm giải hàng ngàn bài tập Jira cũ để học hỏi từ các lỗi sai, thì ở **Pha Suy luận (Inference Phase)**:

> **Cậu thực tập sinh ngày nào nay đã "tốt nghiệp loại xuất sắc", được cấp chứng chỉ chuyên gia và chính thức bước vào phòng họp Sprint Planning cùng toàn thể đội ngũ kỹ sư phần mềm!**

Hãy hình dung một buổi sáng thứ Hai tại công ty:
1. Toàn bộ đội ngũ Scrum (Product Owner, Scrum Master, các lập trình viên Senior, Junior và Tester) ngồi quanh bàn tròn để chuẩn bị cho Sprint mới.
2. Product Owner đưa lên màn hình một User Story hoàn toàn mới tinh mang mã số `XD-4012`.
3. Task này **hoàn toàn chưa có điểm Story Point nào cả**. Cả nhóm chuẩn bị rút bộ bài Planning Poker ra để chấm điểm xem task này tốn bao nhiêu công sức.
4. Thay vì để các lập trình viên tranh cãi nảy lửa theo cảm tính, **mô hình AI (lúc này đóng vai trò một Chuyên gia Cố vấn Độc lập)** được mời đọc bản mô tả task và đưa ra ý kiến tư vấn ngay tại chỗ.

Chỉ trong vòng **chưa đầy một cái chớp mắt (khoảng 20 phần nghìn giây)**, AI không chỉ nói một con số, mà còn đưa ra đầy đủ bằng chứng thuyết phục để cả phòng họp cùng gật đầu đồng ý.

Dưới đây là chi tiết từng bước mà cỗ máy thực hiện trong tích tắc đó.

---

## 📋 2. BƯỚC 1: TIẾP NHẬN USER STORY MỚI TINH (`XD-4012`)

Product Owner chiếu bản yêu cầu công việc mới vừa được tạo trên hệ thống Jira:

* **Mã số Issue:** `XD-4012`.
* **Dự án:** Spring XD.
* **Tiêu đề công việc:**  
  > `"NullPointerException in ExpressionExecution when parsing complex DataWeave header"`  
  > *(Lỗi con trỏ rỗng NullPointerException trong bộ thực thi biểu thức khi phân tích cú pháp tiêu đề DataWeave phức tạp)*.
* **Mô tả chi tiết:** Luồng dữ liệu bị sập hoàn toàn khi người dùng truyền vào gói tin có cấu trúc header lồng nhau nhiều cấp mà module DataWeave chưa xử lý kịp.
* **Điểm Story Point hiện tại:** **`Chưa xác định (None)`** — Đây chính là ẩn số mà cả nhóm cần tìm lời giải.

### ⚠️ Nguyên tắc thời gian thực (Không rò rỉ dữ liệu tương lai)
Tại thời điểm buổi họp diễn ra, phần mềm chưa được viết một dòng code sửa lỗi nào, chưa ai biết ai sẽ nhận làm task này và task này sẽ tốn bao nhiêu ngày công thực tế. Mô hình AI cũng tuyệt đối chỉ được phép đọc đúng những câu chữ ban đầu này, bảo đảm sự công tâm tuyệt đối.

---

## 🔒 3. BƯỚC 2: CHUYỂN SANG CHẾ ĐỘ "ĐI LÀM THỰC TẾ" (INFERENCE MODE)

Khi đi làm thực tế, cỗ máy AI hoạt động khác hẳn so với lúc còn đi học trong phòng huấn luyện:

### 1. Khóa chặt toàn bộ nếp nhăn tư duy (`model.eval()`)
Toàn bộ $117$ triệu trọng số (các thông số tri thức đã học được ở 12 tầng Transformer và đầu hồi quy MLP) được đóng băng hoàn toàn. Cỗ máy không học thêm, không thay đổi nếp nghĩ để đảm bảo tính ổn định và khách quan.

### 2. "Vứt bỏ cuốn sổ nháp" (`torch.no_grad()`)
Khi còn đi học, sau mỗi bước tính toán, máy phải cặm cụi ghi lại toàn bộ các con số trung gian vào "sổ nháp" (đồ thị đạo hàm tính toán) để lát nữa còn tính đạo hàm ngược mà sửa sai.  
Nhưng khi đi làm thực tế, máy **không cần sửa sai nữa nên vứt bỏ toàn bộ sổ nháp**:
* **Tiết kiệm hơn 70% bộ nhớ GPU (VRAM):** Máy chạy nhẹ tênh.
* **Tốc độ cực nhanh:** Thời gian tính toán cho một User Story chỉ mất từ **$15$ đến $30$ mili-giây** ($0.02$ giây), nhanh gấp hàng trăm lần tốc độ người kịp bấm chuột!

### 3. Tắt trò chơi "đố vui ngẫu nhiên" (Tắt Dropout $p = 0$)
Khi huấn luyện, người ta cố tình tắt ngẫu nhiên một số nơ-ron (Dropout) để ép máy không được học vẹt.  
Khi đi làm thực tế, trò chơi này bị tắt hoàn toàn. **100% nơ-ron cùng tập trung làm việc**. Nhờ đó, nếu bạn hỏi máy 10 lần cùng một câu hỏi, máy sẽ trả lời ra **đúng 1 con số duy nhất**, không bao giờ có chuyện lúc đoán thế này lúc đoán thế khác.

---

## 🔤 4. BƯỚC 3: MÁY ĐỌC VĂN BẢN VỚI BỘ TỪ ĐIỂN ĐÃ THUỘC LÒNG

Tiêu đề của task `XD-4012` được đưa vào cỗ máy. Máy sử dụng cuốn từ điển $50.257$ từ quen thuộc (đã học từ trước) để bẻ câu văn thành $18$ mẩu Lego:

`["Null", "Pointer", "Exception", "in", "Exp", "ression", "Exec", "ution", "when", "parsing", "complex", "Data", "We", "ave", "header"]`

* Mỗi mẩu chữ được gán một tọa độ ý nghĩa $768$ chiều và một thẻ vị trí từ $1$ đến $18$.
* Kết quả là một tập hồ sơ gồm **18 tờ phiếu**, mỗi tờ phiếu chứa $768$ con số đặc trưng xếp ngay ngắn từ đầu đến cuối câu.

---

## 🧠 5. BƯỚC 4: DÒNG SUY NGHĨ MỘT CHIỀU (FORWARD PASS ONLY)

Tập hồ sơ 18 tờ phiếu này đi qua **12 phòng ban suy ngẫm liên tiếp** (12 khối Transformer Decoders):

1. **Các từ kết nối ý nghĩa với nhau:**  
   * Tờ phiếu mang chữ `"NullPointerException"` (lỗi sập nghiêm trọng) lập tức liên kết mật thiết với `"ExpressionExecution"` (module lõi xử lý biểu thức).
   * Tờ phiếu `"complex"` (phức tạp) chú ý đặc biệt đến cụm từ `"DataWeave"` và `"header"`.
2. **Quy tắc dòng chảy một chiều:**  
   Toàn bộ thông tin đi một mạch từ Khối 1 đến Khối 12. Không có bước quay ngược trở lại, không có tính toán sai số, không có cập nhật trọng số.
3. **Lấy tờ phiếu cuối cùng số 18 làm bản đúc kết (Last Token Pooling):**  
   Sau khi đi qua Khối 12, máy bỏ qua 17 tờ phiếu đầu và chỉ cầm duy nhất **tờ phiếu số 18 (từ `"header"`)**.  
   Như ta đã biết, nhờ quy tắc bịt mắt nhìn xuôi, tờ phiếu cuối cùng này là nơi duy nhất đã lắng nghe toàn bộ 17 từ phía trước và tích lũy trọn vẹn bức tranh độ khó của toàn bộ task.
4. **Bác Thẩm Định Viên (MLP Regressor Head) chấm điểm:**  
   Bác thẩm định nhận tờ phiếu 768 con số, nén lại thành 256 tiêu chí quản lý dự án, rồi chốt ra một con số thực:
   $$\hat{y} = \mathbf{4.82\text{ Story Points}}$$

---

## ⚡ 6. BƯỚC 5: BƯỚC ĐỘT PHÁ HAI LUỒNG SONG SONG (DUAL-OUTPUT STREAM)

Nếu cỗ máy AI chỉ bước vào phòng họp và buông một câu cộc lốc: *"Task này 4.82 điểm!"*, chuyện gì sẽ xảy ra?

Các lập trình viên kỳ cựu chắc chắn sẽ khoanh tay nghi ngờ:
> *"Máy móc thì biết cái gì! Tại sao lại là 4.82 mà không phải là 2 hay 8? Dựa vào đâu mà bảo task này khó ngang đó?"*

Chính vì vậy, điểm sáng tạo xuất sắc nhất của nhóm tác giả bài báo GPT2SP (IEEE TSE 2023) là **không bao giờ để AI phán bừa như một chiếc hộp đen**, mà kích hoạt đồng thời **Hai Luồng Thông Tin Song Song**:

---

### 🟢 LUỒNG 1: QUY ĐỔI SANG THANG ĐIỂM THỰC TẾ AGILE (STORY POINT ESTIMATION)

* Máy tính ra con số toán học là: $\hat{y} = \mathbf{4.82}$.
* Nhưng trong thực tế, các đội Scrum không bao giờ chấm số lẻ như $4.82$ điểm. Họ dùng **dãy số Fibonacci**: $1, 2, 3, 5, 8, 13$.
* Hệ thống tự động so khớp và làm tròn con số $4.82$ về nấc thang gần nhất:  
  👉 **Khuyến nghị chính thức cho buổi họp: $5.0$ Story Points!**

---

### 🔍 LUỒNG 2: BẰNG CHỨNG MINH BẠCH GIẢI THÍCH CHO CON NGƯỜI (MODEL INSPECTION & XAI)

Đồng thời với con số 5 điểm, hệ thống lập tức trưng ra hai bằng chứng không thể chối cãi:

#### Bằng chứng 1: Kính lúp soi từ khóa (Tô sáng từ vựng chi phối qua Integrated Gradients)
Hệ thống dùng thuật toán toán học để "hỏi" cỗ máy: *"Những chữ nào trong câu đã khiến mày quyết định nâng điểm lên cao như vậy?"*. Kết quả được tô màu trực tiếp trên màn hình chiếu:

* 🟥 **`NullPointerException` (Đóng góp $+0.42$ điểm):** Đây là lỗi sập nghiêm trọng nhất trong thế giới Java, khiến điểm nỗ lực bị kéo vọt lên.
* 🟧 **`ExpressionExecution` (Đóng góp $+0.35$ điểm):** Đây là module lõi rất nhạy cảm của hệ thống, đụng vào là phải viết rất nhiều bài test.
* 🟨 **`DataWeave` (Đóng góp $+0.28$ điểm):** Công nghệ biến đổi dữ liệu phức tạp của bên thứ ba, tiềm ẩn nhiều rủi ro không tương thích.
* 🟦 **`complex` (Đóng góp $+0.18$ điểm):** Từ ngữ báo hiệu cấu trúc dữ liệu nhiều tầng lồng nhau.
* ⬜ **`when parsing` (Đóng góp $+0.04$ điểm):** Từ ngữ ngữ pháp thông thường, hầu như không làm tăng điểm.

Nhìn vào màn hình tô màu, lập trình viên hiểu ngay: **AI không hề đoán mò, nó đã nhìn trúng 3 "ổ gà tử thần" nguy hiểm nhất của task này!**

#### Bằng chứng 2: Lục tìm hồ sơ tiền lệ trong quá khứ (Supporting Examples Retrieval)
Để tăng tính thuyết phục lên mức tuyệt đối, AI tự động quét ngược lại kho lưu trữ hàng ngàn User Story lịch sử của dự án Spring XD và rút ra **3 task cũ tương đồng nhất** mà chính các lập trình viên trong phòng đã từng làm:

1. **Hồ sơ tiền lệ 1 (`XD-2914`):**  
   * *Nội dung cũ:* Lỗi `NullPointerException` trong bộ phân tích cú pháp DataWeave khi gặp header lồng nhau.  
   * *Kết quả năm ngoái:* **Đội ngũ đã làm hết đúng $5.0$ Story Points**.
2. **Hồ sơ tiền lệ 2 (`XD-1882`):**  
   * *Nội dung cũ:* Lỗi sập trình thực thi biểu thức phức tạp trên tiêu đề luồng dữ liệu.  
   * *Kết quả năm ngoái:* **Đội ngũ đã làm hết đúng $5.0$ Story Points**.
3. **Hồ sơ tiền lệ 3 (`XD-3751`):**  
   * *Nội dung cũ:* Lỗi ngoại lệ `ExpressionExecutionException` nhưng ở trường hợp đơn giản hơn (do khoảng trắng đầu dòng).  
   * *Kết quả năm ngoái:* **Đội ngũ chỉ làm hết $3.0$ Story Points**.

---

## 👥 7. BƯỚC 6: DIỄN BIẾN PHÒNG HỌP PLANNING POKER ĐỔI THAY NHƯ THẾ NÀO?

Hãy xem màn hỗ trợ của AI đã làm thay đổi hoàn toàn cục diện buổi họp Sprint Planning như thế nào:

### Kịch bản quen thuộc khi CHƯA CÓ AI (Tranh cãi cảm tính & Mất thời gian)
* **Anh Senior (kỳ cựu):** Giơ thẻ bài **$2$ điểm** và nói: *"Lỗi này anh gặp hoài, vào thêm cái câu lệnh kiểm tra `if (header == null)` là xong trong nửa buổi, chấm 2 điểm thôi!"*.
* **Anh Junior (mới vào):** Giơ thẻ bài **$8$ điểm** và lo lắng: *"Em chưa rành module DataWeave này, nhỡ sửa xong nó gãy luôn cả luồng truyền tin thì sao? Em thấy phải 8 điểm mới an toàn"*.
* Hai bên ngồi tranh luận, bảo vệ quan điểm cá nhân, người thì sợ trễ deadline, người thì tự tin thái quá. **Cuộc cãi vã kéo dài 20–30 phút vẫn chưa chốt được điểm!**

### Kịch bản thực tế khi CÓ GPT2SP TRỢ GIÚP (Đồng thuận dựa trên dữ liệu xác thực)
Màn hình máy chiếu hiện lên:  
**Gợi ý: 5 Story Points | Từ khóa cảnh báo: NullPointerException, ExpressionExecution, DataWeave | Bằng chứng: Task tương tự XD-2914 năm ngoái mất đúng 5 SP.**

* Anh Senior nhìn thấy mã task `XD-2914` liền ồ lên: *"À nhớ rồi! Năm ngoái chính anh làm task XD-2914 này. Tưởng chỉ cần check null đơn giản, ai dè bộ parser của DataWeave nó chạy bất đồng bộ nên phải viết lại cả hàm đệ quy mất trọn 4 ngày. Đúng rồi, task này không thể 2 điểm được, phải 5 điểm mới chuẩn!"*.
* Anh Junior nhìn thấy điểm 5 và các task tiền lệ cũng thở phào nhẹ nhõm vì 5 điểm là đủ thời gian cho anh tìm hiểu mà không bị ép tiến độ vô lý.
* Scrum Master hô: *"Đếm 1, 2, 3 cùng lật bài!"*.  
  👉 **100% thành viên đều giơ thẻ 5 Story Points!**  
  👉 **Cuộc thảo luận kết thúc êm thấm chỉ sau đúng 2 phút!**

### Con số biết nói từ bài báo gốc (Chương 6 - Khảo sát chuyên gia)
* Mức độ tin tưởng của các kỹ sư vào gợi ý của AI tăng vọt từ **$19\%$ lên $75\%$** khi có thêm luồng giải thích minh bạch (XAI) và các ví dụ tiền lệ.
* **$88\%$** các chuyên gia phần mềm thực tế khẳng định công cụ này loại bỏ sự thiên vị cá nhân, rút ngắn thời gian họp Sprint và giúp kế hoạch Sprint sát với năng lực thực tế hơn rất nhiều.

---

## 📊 8. BẢNG SO SÁNH TRỰC DIỆN: PHA HUẤN LUYỆN (TRAINING) VS. PHA SUY LUẬN (INFERENCE)

Để ghi nhớ bản chất, bạn chỉ cần nhớ bảng đối sánh đơn giản dưới đây:

| Tiêu chí so sánh | Pha Huấn luyện (Training Phase) | Pha Suy luận (Inference Phase) |
| :--- | :--- | :--- |
| **Bản chất đời thường** | Cậu học việc ngày đêm làm bài tập cũ để học nghề. | Chuyên gia đã tốt nghiệp đi làm cố vấn trong phòng họp. |
| **Dữ liệu đầu vào** | Issue cũ đã có sẵn đáp án thật ($y = 3.0$ SP). | Issue mới tinh chưa hề có điểm ($y = \text{None}$). |
| **Mục đích chính** | Điều chỉnh trọng số mô hình cho bớt sai số. | Đưa ra dự đoán nỗ lực và bảo vệ ý kiến bằng chứng cứ. |
| **Trạng thái mô hình** | Mở khóa toàn bộ nơ-ron, liên tục cập nhật trọng số. | Khóa cứng 100% trọng số (`model.eval()`). |
| **Sổ nháp tính toán** | Bắt buộc bật để tính đạo hàm ngược (`requires_grad`). | Vứt bỏ hoàn toàn sổ nháp (`torch.no_grad()`). |
| **Yếu tố ngẫu nhiên** | Bật Dropout để chống học vẹt. | Tắt Dropout ($p=0$) để kết quả 100% ổn định, nhất quán. |
| **Đường đi của dữ liệu** | Đi xuôi (Forward Pass) rồi đi ngược (Backprop). | Chỉ đi xuôi một chiều duy nhất (Forward Pass Only). |
| **Tài nguyên & Tốc độ** | Tốn rất nhiều VRAM, mất nhiều giờ/ngày để học xong. | Tiết kiệm 70% VRAM, tốc độ siêu nhanh ($15 - 30$ mili-giây). |
| **Kết quả đầu ra** | Hàm mất mát $L_1$ Loss (dùng để phạt và sửa sai). | **Hai luồng song song:** Gợi ý điểm Fibonacci + Bằng chứng XAI. |
| **Tác động thực tiễn** | Nằm trong phòng máy tính của nhà nghiên cứu. | Nằm trên màn hình phòng họp Sprint Planning của đội Scrum. |

---

## 💡 TỔNG KẾT BẢN CHẤT PHA SUY LUẬN

* **Pha Suy luận không phải là chiếc hộp đen bí ẩn**: Đó là quá trình đọc hiểu một User Story mới bằng toàn bộ vốn tri thức đã đóng băng, tính toán qua 12 tầng Transformer và nén về token cuối cùng để bác thẩm định chốt điểm.
* **Sức mạnh thực sự nằm ở sự minh bạch (Dual-Output Stream)**: Một con số dự đoán vô hồn ($4.82$) sẽ không có giá trị nếu thiếu đi những từ khóa rủi ro được tô sáng và 3 câu chuyện tiền lệ lịch sử đi kèm.
* **AI không thay thế con người**: GPT2SP không tự ý quyết định thay lập trình viên; nó đóng vai trò một người cố vấn công tâm, dùng dữ liệu quá khứ để dập tắt các tranh cãi cảm tính, giúp đội ngũ Agile chốt kế hoạch Sprint nhanh chóng và chuẩn xác.
