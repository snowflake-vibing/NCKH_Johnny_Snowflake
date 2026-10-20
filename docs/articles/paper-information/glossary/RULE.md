# QUY CHUẨN XÂY DỰNG TỪ ĐIỂN THUẬT NGỮ (GLOSSARY RULES)

> **QUY TẮC BẮT BUỘC**:  
> Trước khi khởi tạo hoặc chỉnh sửa bất kỳ thuật ngữ nào trong thư mục `doc/glossary/`, **BẮT BUỘC PHẢI ĐỌC KỸ VÀ TUÂN THỦ TUYỆT ĐỐI** các quy chuẩn trong file `RULE.md` này.

---

## 1. Triết Lý Cốt Lõi: Kỹ Thuật Feynman (The Feynman Technique)

Mục đích của `doc/glossary/` không phải là sao chép lại các định nghĩa hàn lâm khô khan, mà là giúp người đọc **thấu hiểu bản chất trực giác sâu sắc** của từng khái niệm kỹ thuật trong bài toán dự báo chuỗi thời gian và mô hình TiDE.

> *"Nếu bạn không thể giải thích một khái niệm phức tạp bằng ngôn từ đơn giản cho một đứa trẻ 10 tuổi hiểu, thì chính bạn cũng chưa thực sự hiểu nó."*  
> — **Richard Feynman** (Giải Nobel Vật lý 1965)

### 4 Nguyên Tắc Feynman:
1. **Đơn giản hóa tuyệt đối ở bước khởi đầu**: Dùng câu chuyện đời thường, ví dụ quen thuộc (bán kem, đi chợ, dự báo thời tiết, giao thông hàng ngày) để giới thiệu khái niệm trước khi đưa ra bất kỳ công thức toán học nào.
2. **Không dùng biệt ngữ để giải thích biệt ngữ**: Tuyệt đối tránh việc dùng một thuật ngữ chuyên ngành khó hiểu khác để định nghĩa thuật ngữ hiện tại.
3. **Bóc tách tận gốc từ ngữ (Deconstruction)**: Giải thích chiết tự vì sao thuật ngữ đó lại được gọi tên như vậy (gốc tiếng Anh, nghĩa tiếng Việt, hàm ý logic).
4. **Trực quan hóa và phản biện**: Sử dụng bảng biểu so sánh, ma trận dữ liệu và sơ đồ luồng tư duy để người đọc có khoảnh khắc bừng sáng (*"Aha! Moment"*).

---

## 2. Cấu Trúc Khung Chuẩn Của Một Bài Thuật Ngữ (6 Phần Bắt Buộc)

Mỗi file thuật ngữ trong `doc/glossary/` (ví dụ: `dynamic_covariates.md`, `channel_independence.md`, `residual_block.md`...) **phải tuân thủ đúng khung 6 phần sau**:

### Phần 1: Giải Thích Cho Đứa Trẻ 10 Tuổi (The 10-Year-Old Explanation)
- Kể một câu chuyện đời thực có nhân vật, tình huống cụ thể (ví dụ: Bác Ba bán kem, chú bảo vệ trông xe, người nông dân dự báo mùa vụ...).
- Đặt ra bài toán và chỉ ra vai trò tự nhiên của thuật ngữ trong câu chuyện.
- Đúc kết một câu định nghĩa ngắn gọn, dễ nhớ bằng ngôn ngữ bình dân.

### Phần 2: Bóc Tách Từng Từ Ngữ Chuyên Ngành (Deconstructing the Jargon)
- Bóc tách từng thành tố cấu thành tên thuật ngữ (ví dụ: *Dynamic* là gì, *Co-* là gì, *Variates* là gì).
- Lập bảng phân tích: Gốc từ, nghĩa thông thường, ý nghĩa trong Machine Learning, và các khái niệm đối lập (Antonyms).

### Phần 3: Trực Quan Hóa Bằng Bảng Dữ Liệu (The "Aha!" Moment)
- Vẽ bảng dữ liệu mẫu mô phỏng (dạng bảng Excel/DataFrame) phân chia ranh giới rõ ràng giữa **Quá khứ ($t \le L$)** và **Tương lai ($t > L$)**.
- Làm nổi bật sự khác biệt mấu chốt giữa biến mục tiêu (bị ẩn trong tương lai) và biến ngoại sinh (đã biết trước).

### Phần 4: Thách Thức Kỹ Thuật & Vì Sao Các Phương Pháp Khác Bị Hạn Chế?
- Giải thích vì sao các mô hình truyền thống (ARIMA, Linear/DLinear, Transformer cổ điển, PatchTST) lại gặp khó khăn hoặc bó tay trước khái niệm này.
- Nêu rõ nguyên nhân kỹ thuật (bùng nổ số chiều, trôi phân phối, cơ chế attention không tương thích...).

### Phần 5: Mô Hình TiDE Giải Quyết Vấn Đề Này Như Thế Nào?
- Chỉ rõ thành phần kiến trúc cụ thể trong TiDE phụ trách khái niệm này (Feature Projection, Temporal Decoder, Global Skip...).
- Dùng ẩn dụ kỹ thuật trực quan (ví dụ: "máy nén hành lý", "đường cao tốc").

### Phần 6: Tổng Kết 30 Giây (The Elevator Pitch)
- 3 gạch đầu dòng đúc kết tinh hoa nhất để người đọc có thể nhớ và nhắc lại trong 30 giây khi được phỏng vấn.

---

## 3. Quy Chuẩn Về Ngôn Ngữ & Sơ Đồ (Diagram & Language Rules)

> [!IMPORTANT]
> **ĐẶC BIỆT CHÚ Ý VỀ TIẾNG VIỆT CÓ DẤU TRONG SƠ ĐỒ:**

1. **Tiếng Việt có dấu 100% trong toàn bộ bài viết**:
   - Tất cả văn bản giải thích, tiêu đề, bảng biểu và **toàn bộ nội dung trong các sơ đồ Mermaid** PHẢI viết bằng **Tiếng Việt CÓ DẤU đầy đủ và chuẩn xác chính tả**.
   - Tuyệt đối KHÔNG viết tiếng Việt không dấu (ví dụ: viết *"Giá trị thay đổi theo thời gian"*, KHÔNG ĐƯỢC viết *"Gia tri thay doi theo thoi gian"*).

2. **Quy chuẩn kỹ thuật khi viết sơ đồ Mermaid trên GitHub**:
   - **Luôn bao bọc nhãn node bằng cặp dấu ngoặc kép**: `NodeID["Nội dung tiếng Việt có dấu"]`.
   - **Tuyệt đối không lồng ngoặc vuông hoặc dấu chấm phẩy bên trong nhãn**: Tránh viết `Node["Ghép [a ; b]"]` vì cú pháp `[` và `]` sẽ làm bộ phân tích Mermaid của GitHub báo lỗi `Error parsing Mermaid diagram`. Thay vào đó, viết `Node["Ghép vector a và vector b"]`.
   - **Không nối trực tiếp ID của Subgraph**: Luôn nối giữa các Node con bên trong Subgraph với nhau hoặc với Node ngoài.
   - **Sử dụng sơ đồ trực quan, mạch lạc**: Sử dụng `flowchart TD` (trên xuống dưới) hoặc `flowchart LR` (trái sang phải) với cấu trúc dễ theo dõi.

3. **Quy chuẩn công thức toán học (LaTeX/KaTeX)**:
   - Các công thức toán hiển thị (display equations) phải đặt trong khối riêng biệt với cặp `$$`:
     ```markdown
     $$
     \hat{y}_{L+1:L+H} = f_\Theta(y_{1:L}, x_{1:L+H}, a)
     $$
     ```
   - Không đặt dấu `$$` thụt đầu dòng bên trong danh sách dấu gạch đầu dòng để tránh lỗi render trên GitHub.

---

## 4. Danh Sách Thuật Ngữ Mục Tiêu Dự Kiến

Mỗi thuật ngữ sau đây khi được tạo mới đều phải tuân thủ chuẩn `RULE.md`:
1. `dynamic_covariates.md`: Biến ngoại sinh động theo thời gian (Đã hoàn thiện mẫu).
2. `static_attributes.md`: Thuộc tính ngoại sinh tĩnh.
3. `channel_independence.md`: Chiến lược xử lý độc lập từng kênh chuỗi thời gian.
4. `feature_projection.md`: Kỹ thuật chiếu giảm chiều đặc trưng theo bước thời gian.
5. `temporal_decoder.md`: Bộ giải mã theo thời gian & cơ chế đường cao tốc (Covariate Highway).
6. `residual_block.md`: Khối nơ-ron phần dư dày đặc trong kiến trúc MLP.
7. `revin.md`: Chuẩn hóa thực thể đảo nghịch (Reversible Instance Normalization).
