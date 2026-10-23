# 🔬 CASE STUDY CHUYÊN SÂU 04: HÌNH DUNG TOÀN DIỆN PHA HUẤN LUYỆN (TRAINING PHASE) CỦA GPT2SP

> **Mục tiêu tài liệu:**  
> Giải thích chi tiết, trực quan bằng ngôn ngữ dễ hiểu và số liệu thực tế về cách một mô hình AI học cách ước lượng Story Point từ các issue Jira cũ, **hoàn toàn không dùng sơ đồ khối trừu tượng**.  
> **Dữ liệu thực tế:** Dự án Spring XD — Khảo sát trực tiếp trên User Story lịch sử `XD-3751` ($y = 3.0$ Story Points).

---

## 🎯 1. BỨC TRANH TỔNG THỂ: HUẤN LUYỆN (TRAINING) THỰC CHẤT LÀ LÀM GÌ?

Để hình dung pha huấn luyện, bạn hãy tưởng tượng một câu chuyện rất đời thường:

Công ty bạn tuyển một **cậu thực tập sinh tài năng** (đại diện cho mô hình nền tảng **GPT-2**). Cậu này học tiếng Anh rất giỏi, đọc hàng triệu trang sách báo trên mạng nên câu cú ngữ pháp cái gì cũng biết, **nhưng cậu chưa từng đi làm phần mềm một ngày nào**. Cậu hoàn toàn không biết một lỗi *"ExpressionExecutionException"* hay một module *"DataWeave"* thì sửa mất bao nhiêu ngày công, đáng bao nhiêu Story Point.

Để đào tạo cậu thực tập sinh này thành một **chuyên gia ước lượng**, công ty làm như sau:
1. Đưa cho cậu một tập hồ sơ gồm hàng ngàn User Story mà các đàn anh kỳ cựu đã làm xong trong 3 năm qua (Dữ liệu Jira lịch sử).
2. Ở mỗi User Story, công ty **tạm thời lấy tay che đi mức điểm thật** (ví dụ che con số $3.0$ Story Points đi), chỉ đưa cho cậu đọc tiêu đề và mô tả.
3. Cậu thực tập sinh đọc xong và **đoán thử một con số** (ví dụ cậu đoán bừa là $2.45$ SP).
4. Công ty mở tay ra, chỉ vào đáp án thật: *"Sai rồi! Điểm thật là 3.0 cơ, cậu đoán non mất 0.55 điểm!"*.
5. Căn cứ vào mức độ đoán sai đó (hàm phạt $L_1$ Loss), công ty bắt cậu phải **tự kiểm điểm và chỉnh lại các nếp nhăn suy nghĩ trong đầu** (thuật toán lan truyền ngược Backpropagation).
6. Quy trình này lặp đi lặp lại hàng chục lần trên toàn bộ hàng ngàn User Story. Càng về sau, cậu đoán càng sát đáp án thật, cho đến khi sai số trung bình giảm xuống dưới 1 điểm thì công ty công nhận cậu đã "tốt nghiệp"!

Dưới đây là chi tiết từng bước mà cỗ máy tính toán thực sự trải qua khi huấn luyện trên một User Story cụ thể.

---

## 📋 2. BƯỚC 1: CHUẨN BỊ "ĐỀ THI" TỪ JIRA & NGUYÊN TẮC KHÔNG GIAN LẬN

Công ty trích xuất từ cơ sở dữ liệu Jira một User Story cũ có mã số `XD-3751` của dự án Spring XD:

* **Mặt trước tờ giấy thi (Phần đưa cho máy đọc):**  
  > Tiêu đề: `"ExpressionExecutionException when element that expects a DW starts with space"`  
  > Mô tả: Trình thông dịch biểu thức bị văng lỗi ngoại lệ khi phần tử luồng dữ liệu DataWeave (DW) bắt đầu bằng ký tự khoảng trắng.
* **Mặt sau tờ giấy thi (Đáp án thật - Ground Truth, giấu kín):**  
  > Điểm số thực tế do đội ngũ lập trình viên đã làm trong quá khứ: **$y = 3.0$ Story Points**.

### ⚠️ Nguyên tắc sống còn: Tuyệt đối không gian lận thời gian (Temporal Leakage Free)
Khi đưa "đề thi" cho mô hình học, bạn chỉ được phép đưa những câu chữ được viết **vào đúng ngày họp Sprint Planning**.  
Bạn tuyệt đối không được để lộ những thông tin sinh ra sau đó, ví dụ: *"Task này lập trình viên Nam làm mất 4 ngày mới xong"* hay *"Code sửa ở file parser.java dòng 120"*. Nếu để lộ những thông tin của tương lai này, mô hình sẽ "học vẹt" đáp án chứ không học được cách tư duy từ bản mô tả ban đầu!

---

## 🔤 3. BƯỚC 2: MÁY TÍNH "CẮT CHỮ" ĐỔI THÀNH CÁC CON SỐ (TOKENIZATION)

Máy tính không có mắt để đọc chữ cái như con người, nó chỉ hiểu các con số. Vì vậy, câu văn phải trải qua 2 khâu chế biến:

### 1. Bẻ nhỏ từ ghép thành các mẩu Lego quen thuộc (BPE Tokenization)
Trong câu trên có một từ rất dài và kỳ dị: `ExpressionExecutionException`.  
Nếu là các mô hình cũ như Deep-SE, khi gặp từ dài này nó sẽ "bó tay" vì chưa từng thấy trong từ điển, và nó coi như một ký tự vô danh `<UNK>`.

Nhưng GPT-2 dùng thuật toán bẻ chữ thông minh: nó bẻ từ dài ngoằng đó thành 5 mẩu Lego quen thuộc:  
`Exp` + `ression` + `Exec` + `ution` + `Exception`.

Toàn bộ câu văn 15 từ được bẻ thành 15 mẩu Lego:  
`["Exp", "ression", "Exec", "ution", "Exception", "when", "element", "that", "expects", "a", "D", "W", "starts", "with", "space"]`.

### 2. Dán nhãn tọa độ ý nghĩa và thẻ số thứ tự (Word & Positional Embedding)
* **Tọa độ ý nghĩa:** Mỗi mẩu Lego được tra vào một cuốn từ điển khổng lồ gồm 50.257 trang để đổi thành một dãy **768 con số tọa độ**. Dãy số này cho biết từ này có liên quan gì đến kỹ thuật, đến lập trình hay lỗi lầm hay không.
* **Thẻ số thứ tự:** Từ `Exp` đứng ở vị trí số 1 được cộng thêm một dãy 768 con số mang ý nghĩa *"tôi đứng đầu hàng"*. Từ `space` đứng ở vị trí số 15 được cộng thêm một dãy 768 con số mang ý nghĩa *"tôi đứng cuối hàng"*.

👉 **Hình dung kết quả:** Lúc này trên bàn máy tính là một tập hồ sơ gồm **15 tờ phiếu**, mỗi tờ phiếu ghi chi chít **768 con số thực**, xếp ngay ngắn theo thứ tự từ 1 đến 15.

---

## 🧠 4. BƯỚC 3: CUỘC HỌP 12 TẦNG SUY NGẪM (12 KHỐI TRANSFORMER DECODERS)

Tập hồ sơ 15 tờ phiếu này được chuyển qua **12 phòng ban làm việc liên tiếp** (tương ứng với 12 khối Transformer Decoder):

### 1. Trong mỗi phòng ban: Các từ "trao đổi thông tin" với nhau (Self-Attention)
Ở mỗi phòng ban, 15 tờ phiếu không nằm im lìm mà liên tục trao đổi dữ liệu:
* Tờ phiếu mang chữ `"Exception"` (lỗi) sẽ chủ động "nói chuyện" với tờ phiếu `"ExpressionExecution"` để hiểu rằng đây là lỗi của bộ thông dịch biểu thức.
* Tờ phiếu `"starts with"` sẽ kết nối với `"space"` để biết lỗi này xảy ra khi có khoảng trắng.
* **Quy tắc bịt mắt nghiêm ngặt (Masked):** Khi tờ phiếu số 5 đang suy ngẫm, nó chỉ được phép nghe ngóng các tờ phiếu từ 1 đến 5. Nó tuyệt đối không được nhìn lén các tờ phiếu từ 6 đến 15 ở phía sau. Nhờ vậy, dòng suy nghĩ luôn chảy xuôi tự nhiên theo câu chữ.

#### 🎯 Kết quả thu được sau khi các tờ phiếu trao đổi thông tin xong:

Sau cuộc thảo luận đa chiều (Self-Attention), điều kỳ diệu xảy ra trên bàn làm việc: **15 tờ phiếu ban đầu đã hoàn toàn "lột xác"**:

1. **Từ các con số tĩnh biến thành "Tri thức ngữ cảnh sống động" (Contextualized Representation):**  
   Trước khi vào phòng, mỗi tờ phiếu chỉ mang ý nghĩa từ điển cô độc. Sau khi trao đổi xong, mỗi tờ phiếu đều được ghi chép bổ sung thêm thông tin ngữ cảnh đắt giá từ các tờ phiếu khác:

| Tờ phiếu (Token) | Trước khi trao đổi (Nghĩa từ điển tĩnh) | Sau khi trao đổi Self-Attention (Đã làm giàu ngữ cảnh) |
| :--- | :--- | :--- |
| **`"Exception"`** (vị trí 5) | Chỉ biết chung chung: *"Tôi là một lỗi ngoại lệ nào đó"*. | Biết chính xác: *"Tôi là lỗi runtime nghiêm trọng của bộ thông dịch biểu thức SpEL (liên kết với `ExpressionExecution`), không phải lỗi mạng hay database"*. |
| **`"expects"`** (vị trí 9) | Chỉ biết: *"Tôi là hành động kỳ vọng / đòi hỏi"*. | Biết chính xác: *"Tôi đang kiểm tra ràng buộc cấu hình luồng dữ liệu DataWeave (`DW`)"*. |
| **`"space"`** (vị trí 15, cuối câu) | Chỉ biết: *"Tôi là một ký tự khoảng trắng vô tri"*. | **Trở thành tờ phiếu quyền lực nhất:** Nhờ quy tắc bịt mắt cho phép nhìn hết 14 từ trước, nó thấu suốt toàn bộ câu chuyện: *"Tôi là ký tự khoảng trắng đứng ở đầu chuỗi (starts with), và chính tôi là thủ phạm kích hoạt lỗi ExpressionExecutionException trong module DW!"*. |

2. **Bản chất toán học của kết quả trao đổi:**  
   Toàn bộ sự trao đổi này biến ma trận 15 tờ phiếu ban đầu thành một ma trận biểu diễn mới:

$$\mathbf{z} = \text{Attention}(Q, K, V) \in \mathbb{R}^{15 \times 768}$$

3. **Cộng bù tờ phiếu cũ (Residual Connection) & Chuẩn hóa (LayerNorm):**  
   Để các từ ngữ không bị "say sưa" thông tin mới mà quên mất ý nghĩa nguyên bản của chính mình, máy tính lấy tờ phiếu mới cộng trực tiếp với tờ phiếu ban đầu:

$$\mathbf{x}_{\text{mid}} = \text{LayerNorm}(\mathbf{x} + \mathbf{z}) \in \mathbb{R}^{15 \times 768}$$

👉 **Đầu ra hoàn tất của khâu 1:** Ta thu được một tập hồ sơ gồm **15 tờ phiếu mới toanh**, vừa giữ trọn vẹn bản sắc từ gốc, vừa thấm nhuần ngữ cảnh của cả User Story, sẵn sàng bước sang căn phòng tiếp theo để kiểm tra kho tri thức chuyên sâu!

### 2. Phòng lưu trữ tri thức chuyên sâu (Mạng truyền thẳng FFN)
Sau khi các từ trao đổi với nhau, từng tờ phiếu được đưa vào một căn phòng phóng đại đặc trưng rộng gấp 4 lần (**từ 768 chiều phóng to lên 3072 chiều**).  
Tại đây, các nơ-ron nhận diện mẫu sẽ sáng bừng lên:
* Nơ-ron chuyên phát hiện lỗi cú pháp Java kêu lên: *"Có mẫu lỗi văng ngoại lệ kìa!"*.
* Nơ-ron chuyên về module DataWeave kêu lên: *"Có công nghệ xử lý dữ liệu phức tạp kìa!"*.
* Sau đó, thông tin được nén gọn gàng trở lại 768 con số và chuyển sang phòng ban tiếp theo.

### 3. Lấy tờ phiếu của Token cuối cùng làm "Bản đúc kết" (Last Token Pooling)
Sau khi đi qua hết 12 phòng ban, ta có 15 tờ phiếu đã được làm giàu ngữ nghĩa ở mức cao nhất.  
Lúc này, ta **bỏ qua 14 tờ phiếu đầu tiên**, chỉ cầm duy nhất **tờ phiếu số 15 (từ `"space"`)**!

> ❓ **Tại sao lại chỉ lấy tờ phiếu cuối cùng?**  
> Hãy nhớ lại quy tắc bịt mắt: Tờ phiếu số 1 chỉ biết mỗi chính nó. Tờ phiếu số 2 chỉ biết số 1 và 2. **Chỉ duy nhất tờ phiếu số 15 ở cuối câu là người duy nhất được phép lắng nghe toàn bộ câu chuyện từ đầu đến cuối!** Nó là bản tổng kết hoàn mỹ nhất chứa đựng toàn bộ độ khó của User Story.

---

## ⚖️ 5. BƯỚC 4: BÁC THẨM ĐỊNH CHỐT SỐ ĐOÁN (MLP REGRESSOR HEAD)

Tờ phiếu số 15 (gồm 768 con số ngữ nghĩa cô đọng) được chuyển sang bàn làm việc của **Bác Thẩm Định Viên (MLP Regressor Head)**:

1. **Rút gọn thành 256 tiêu chí nỗ lực:**  
   Bác thẩm định không nhìn dàn trải 768 con số nữa, bác dùng một phép biến đổi toán học để gom chúng lại thành **256 tiêu chí quản lý dự án**:
   * Tiêu chí 1: Lỗi này có làm sập hệ thống không?
   * Tiêu chí 2: Cần sửa bao nhiêu file mã nguồn?
   * Tiêu chí 3: Đội ngũ đã có kinh nghiệm với module DataWeave này chưa?
2. **Cân nhắc điều kiện (Hàm kích hoạt GELU):**  
   Bác suy xét: *"Lỗi này tuy là Exception nghe rất ghê gớm, nhưng nguyên nhân chỉ là do người dùng gõ thừa dấu khoảng trắng (starts with space), việc sửa chữa có lẽ không quá phức tạp đến mức 8 hay 13 điểm"*.
3. **Chốt con số dự đoán:**  
   Bác thẩm định bấm máy tính và đưa ra con số dự đoán của lượt này:  
   👉 **`Dự đoán: 2.45 Story Points`**.

---

## 📏 6. BƯỚC 5: SO SÁNH VỚI ĐÁP ÁN THẬT & CÂY ROI PHẠT ($L_1$ LOSS)

Bây giờ, người giám sát mở mặt sau của tờ giấy thi ra. Đáp án thực tế của các đàn anh năm xưa là: **`3.0 Story Points`**.

Cỗ máy đã đoán $2.45$, trong khi thực tế là $3.0$. Mức độ đoán sai lệch là:
$$\text{Sai số} = |3.0 - 2.45| = \mathbf{0.55\text{ điểm}}$$

Con số $0.55$ này chính là **Hàm Mất Mát $L_1$ Loss** (còn gọi là sai số tuyệt đối MAE).

### 💡 Tại sao lại phạt bằng sai số thẳng ($L_1$) mà không phạt bằng bình phương ($L_2$)?
Hãy hình dung trong dự án Jira, thỉnh thoảng có một vài task "khổng lồ" bất thường được chấm tới $40$ hoặc $100$ điểm:
* Nếu dùng phép phạt bình phương (**$L_2$ Loss - MSE**): Khi gặp một task 40 điểm mà mô hình đoán 10 điểm (lệch 30 điểm), mức phạt sẽ bị bình phương lên thành **$30^2 = 900$**! Mức phạt khổng lồ này như một cú đánh sấm sét, làm rung chuyển và phá hỏng toàn bộ các nếp nhăn suy nghĩ mà mô hình vừa học được từ các task bình thường.
* Nếu dùng mức phạt thẳng (**$L_1$ Loss - MAE**): Lệch 30 điểm thì phạt đúng 30 điểm. Lệch 0.55 điểm thì phạt đúng 0.55 điểm. Mức phạt luôn tăng đều đặn, công bằng, giúp mô hình **không bao giờ bị hoảng loạn trước những task dị biệt (Robust to Outliers)**.

---

## 🔄 7. BƯỚC 6: CUỘC RÚT KINH NGHIỆM LỘI NGƯỢC DÒNG (BACKPROPAGATION & ADAMW)

Biết mình bị phạt $0.55$ điểm, mô hình không dừng lại ở đó. Nó bắt đầu quá trình **sửa sai lội ngược dòng (Backpropagation)**:

1. **Từ kết quả đi lùi lại:**  
   Tín hiệu sai số $(-0.55)$ đi ngược từ con số $2.45$ quay trở lại Bác Thẩm Định: *"Bác đã đoán hơi non một chút rồi, cần phải tăng trọng số cho các lỗi liên quan đến trình thông dịch biểu thức lên!"*.
2. **Chui ngược qua 12 phòng ban:**  
   Tín hiệu sai số tiếp tục lội ngược qua phòng ban 12, phòng ban 11... về tận phòng ban 1.  
   Nhờ có **hệ thống 24 đường tắt cao tốc (Residual Connections)** chạy dọc theo các phòng ban, dòng tín hiệu sửa sai này truyền thẳng tắp từ trên xuống dưới mà không bị suy hao hay tắc nghẽn giữa đường.
3. **Người quản giáo AdamW vặn lại các nút ốc:**  
   Thuật toán tối ưu hóa **AdamW** đứng ở từng nơ-ron:
   * Nó vặn nhẹ các con số trọng số một lượng vừa phải theo tốc độ học đã định sẵn ($\text{LR} = 5 \times 10^{-4}$): không vặn quá mạnh làm đảo lộn mọi thứ, nhưng đủ để lần sau không phạm phải sai lầm cũ.
   * Đồng thời, nó "gọt bớt" các trọng số đang có xu hướng bị phình to quá mức (cơ chế **Weight Decay**), ép mô hình luôn giữ sự khiêm tốn, không được thiên vị thái quá một từ ngữ cá biệt nào.

---

## 📈 8. BƯỚC 7: LẶP ĐI LẶP LẠI QUA NHIỀU VÒNG (EPOCHS) CHO ĐẾN KHI THÀNH TÀI

Mô hình không chỉ học một mình task `XD-3751`. Nó học hàng ngàn task khác nhau của dự án Spring XD:
* Mỗi lần nó bốc một nhóm gồm **64 task (Mini-batch)** ra học cùng lúc.
* Sau khi duyệt qua hết toàn bộ hàng ngàn task trong kho dữ liệu, ta gọi đó là hoàn thành **1 Vòng học (Epoch)**.

Hãy hình dung sự tiến bộ rõ rệt của mô hình qua từng vòng học:
* **Ở Vòng 1:** Mô hình đoán mò lung tung, sai số trung bình (MAE) lên tới **$2.5 - 3.0$ điểm**. Nó nhìn thấy task nào có chữ "Exception" cũng phán bừa 8 điểm.
* **Ở Vòng 5:** Mô hình bắt đầu biết phân biệt ngữ cảnh: nó biết lỗi văng ngoại lệ do khoảng trắng thì chỉ tốn khoảng 3 điểm, còn lỗi đứt kết nối mạng phân tán thì phải 5 hay 8 điểm. Sai số giảm xuống **$1.6$ điểm**.
* **Ở Vòng 15:** Các trọng số hội tụ ổn định, mô hình ước lượng cực kỳ nhạy bén và chuẩn xác. Trên dự án Spring XD, sai số trung bình giảm xuống mức kỷ lục: **$\mathbf{0.96\text{ điểm}}$** (vượt trội hoàn toàn so với mức $1.61$ điểm của Deep-SE).

Lúc này, công ty tuyên bố: **Quá trình huấn luyện kết thúc!**  
Toàn bộ 117 triệu tham số đã đạt độ chín muồi được lưu lại vào một file mô hình an toàn trên ổ cứng, sẵn sàng được "đóng băng" để chuyển sang phục vụ các buổi họp Sprint Planning thực tế.

---

## ⏱️ 9. ĐÚC KẾT BẢN CHẤT PHA HUẤN LUYỆN TRONG 3 CÂU

1. **Đầu vào và Mục tiêu:** Nhận vào câu chữ Jira cũ, tự tính toán qua 12 tầng Transformer và đầu hồi quy MLP để đoán điểm, sau đó so sánh với điểm thực tế do con người đã chấm.
2. **Cơ chế sửa sai:** Đo mức độ đoán lệch bằng hàm phạt tuyến tính $L_1$ Loss (chống nhiễu ngoại lai), rồi truyền ngược đạo hàm xuyên suốt toàn bộ mô hình để chỉ rõ từng nơ-ron cần phải chỉnh bao nhiêu.
3. **Kết quả đạt được:** Qua hàng ngàn lượt lặp với thuật toán AdamW, mô hình biến vốn tiếng Anh tổng quát ban đầu thành vốn tri thức định giá nỗ lực phần mềm chuyên nghiệp, đạt độ chính xác cao nhất trước khi bước vào phòng họp thực tế.