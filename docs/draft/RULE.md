# 📏 BỘ QUY TẮC CHUẨN HÓA QUY TRÌNH XỬ LÝ DỮ LIỆU & VIẾT BÁO CÁO (RULEBOOK CHO CÁC DỰ ÁN TIẾP THEO)

> **Mục đích tài liệu:** Ghi nhận đầy đủ các quy tắc kỹ thuật và quy tắc trình bày rút ra từ quá trình làm sạch dự án **Spring XD (`XD`)**, nhằm đảm bảo khi nhân rộng sang **15 dự án chuẩn tiếp theo** (như `MESOS`, `TIMOB`, `MULE`, `DURACLOUD`, `USERGRID`...) **không bao giờ lặp lại các sai lầm về rò rỉ dữ liệu hay gây rối mạch tài liệu**.

---

## 🧭 PHẦN A. QUY TẮC TỔ CHỨC TÀI LIỆU ĐỂ KHÔNG BỊ RỐI (DOCUMENTATION RULES)

Khi phân tích bất kỳ dự án mới nào từ CSDL TAWOS v1.1, bộ tài liệu báo cáo luôn được chia thành **4 phần độc lập theo trình tự thời gian xử lý** và tuân thủ nghiêm ngặt 5 quy tắc sau:

### Quy tắc A1 — Không liệt kê dàn trải các bảng phụ không sử dụng ở Phần 1
- **Sai lầm cần tránh:** Liệt kê cả 11–12 bảng của CSDL (`Version`, `Fix_Version`, `Affected_Version`, `Repository`...) ở Phần 1 nhưng đến phần ví dụ mẫu chỉ chiếu ra 2 bảng, làm người đọc không biết bảng nào mới là bảng đang dùng.
- **Quy tắc bắt buộc:** Ở Phần 1 chỉ tập trung giải thích rõ **2 bảng cốt lõi**:
  1. **Bảng `Issue`:** Lưu trạng thái cuối cùng (*Final Snapshot*) của mỗi công việc (gồm 30 cột).
  2. **Bảng `Change_Log`:** Lưu lịch sử chỉnh sửa của từng công việc trong bảng `Issue`, nối với nhau qua khóa `Issue.ID = Change_Log.Issue_ID`.
- Luôn đi kèm **5 dòng dữ liệu mẫu của bảng `Issue`** và **5 dòng lịch sử tương ứng của chính công việc đó trong bảng `Change_Log`**.

### Quy tắc A2 — Chỉ phân tích trên tập có nhãn `Story_Point > 0`
- **Sai lầm cần tránh:** Đưa cả cột thống kê của các công việc không có điểm (`Story_Point = 0` hoặc `NULL`) vào chung bảng phân tích ở Phần 2 gây loãng số liệu.
- **Quy tắc bắt buộc:** Ngay từ cuối Phần 1, lọc cô lập tập công việc có `Story_Point > 0` (`N` hợp lệ). Bước sang Phần 2, **100% các bảng thống kê chỉ tính trên tập `N` công việc có Story Point này**.

### Quy tắc A3 — Tuyệt đối không trộn dữ liệu đã làm sạch (`Clean_*`) vào Phần 2
- **Sai lầm cần tránh:** Đưa các cột mới tạo sau khi làm sạch (`Clean_Type`, `Clean_Priority`, `Initial_Story_Point`, `Has_Clean_Description`) vào ngay các bảng của Phần 2 trong khi đến Phần 3 mới giải thích điểm bất thường và cách xử lý.
- **Quy tắc bắt buộc:**
  - **Phần 2** chỉ mô tả **100% dữ liệu gốc (Raw Data)** trong CSDL để người đọc hiểu nguyên trạng dữ liệu trước khi can thiệp.
  - Không để cột `Tỷ lệ khuyết (%)` dư thừa trong bảng liệt kê 30 cột của bảng `Issue` (chỉ để `Số dòng có dữ liệu` và `Số dòng bị trống`).
  - Ghi rõ tiêu đề là *"Danh sách 30 cột thuộc tính của bảng `Issue`"* (không gọi là "bảng dữ liệu thứ 3" để tránh nhầm với một table trong CSDL).

### Quy tắc A4 — Trình bày Phần 3 theo cấu trúc cặp `1 Điểm bất thường -> 1 Cách giải quyết`
- **Sai lầm cần tránh:** Tách rời hoàn toàn danh sách các điểm bất thường ở một mục và danh sách các bước làm sạch ở một mục khác khiến người đọc phải tự dò xem bước làm sạch nào giải quyết điểm bất thường nào.
- **Quy tắc bắt buộc:** Ở Phần 3, với mỗi điểm bất thường phát hiện được, phải trình bày theo đúng 2 mục con liền kề nhau:
  - `🔴 Phát hiện điểm bất thường` (nêu con số thực tế và hậu quả nếu không sửa).
  - `✅ Cách giải quyết đã áp dụng` (nêu rõ thuật toán xử lý để ra cột sạch).

### Quy tắc A5 — Đặt bảng đối chiếu `Trước xử lý vs. Sau xử lý` ở Phần 4
- **Quy tắc bắt buộc:** Mọi sự so sánh giữa dữ liệu gốc (Bảng `Issue`) và dữ liệu sạch (`cleaned_dataset.csv`), kiểm định `0% Data Leakage`, và kiểm định ranh giới thời gian `Chronological_Split` (`train` / `val` / `test`) đều phải đặt tại **Phần 4 (Thẩm định Clean Data)**.

---

## 🛠️ PHẦN B. QUY TẮC KỸ THUẬT BẮT BUỘC KHI TẠO `cleaned_dataset.csv` CHO CÁC DỰ ÁN KHÁC

Khi chạy script hoặc Jupyter Notebook để xuất file `<project>_cleaned_dataset.csv` cho bất kỳ dự án nào trong TAWOS v1.1, **bắt buộc phải thực hiện đủ 6 bước kiểm tra và xử lý kỹ thuật sau**:

```mermaid
flowchart TD
    R1["Bước 1: Lọc Story_Point > 0\n(Cấm impute Median cho mẫu thiếu SP)"] --> R2["Bước 2: Chạy strip_sql_quotes()\nGỡ bỏ ký tự bọc \\\" và \\\"\\\"\\\" ở bảng Issue"]
    R2 --> R3["Bước 3: Xác định Real_Estimation_Date & Initial_SP\nLọc bỏ điểm nháp (0, NULL, 999999, 10^10...)"]
    R3 --> R4["Bước 4: Truy vết Change_Log (Creation_Date > Real_Est_Date)\nKhôi phục Clean_Title, Clean_Desc, Clean_Type, Clean_Priority, Clean_Components"]
    R4 --> R5["Bước 5: Xóa 12 cột rò rỉ tương lai\n(Status, Resolution, Timespent, PR_URL, Assignee, Sprint...)"]
    R5 --> R6["Bước 6: Sắp xếp theo Real_Estimation_Date\nChia Chronological_Split (60% Train / 20% Val / 20% Test)"]
```

### Quy tắc B1 — Bắt buộc gỡ bỏ ký tự nháy kép bọc chuỗi (`\"` và `\"\"\"`) từ SQL Dump
- **Lý do:** Trong CSDL `tawos_eda.db`, các cột văn bản của bảng `Issue` (`Title`, `Description`, `Description_Text`) bị bọc trong dấu `\"...\"` hoặc `\"\"\"...\"\"\"`, trong khi `From_String` của bảng `Change_Log` không có dấu bọc này.
- **Quy tắc code:** Luôn chạy hàm `strip_sql_quotes()` cho toàn bộ các trường văn bản của cả 2 bảng trước khi so sánh hoặc gộp chuỗi để ngăn chặn *Synthetic Format Leakage*.

### Quy tắc B2 — Không bao giờ dùng trực tiếp cột `Issue.Estimation_Date`
- **Lý do:** Cột `Issue.Estimation_Date` trong TAWOS bị lỗi lệch múi giờ `-1.00 giờ` so với `Creation_Date` trên hàng nghìn bản ghi và không phản ánh thời điểm gán điểm thực tế trong `Change_Log`.
- **Quy tắc code:** Luôn tính lại **`Real_Estimation_Date`** từ bảng `Change_Log (Field = 'Story Points')` và đảm bảo bất đẳng thức `Real_Estimation_Date >= Creation_Date` đúng trên 100% số dòng.

### Quy tắc B3 — Kiểm tra miền giá trị hợp lệ trước khi lấy `From_String` làm `Initial_Story_Point`
- **Lý do:** Khi mới mở ticket, người dùng trên Jira đôi khi nhập các số giả định/placeholder (`0`, `-1`, `0.01`, `100`, `444`, `1000`, `999999`, `9999999`, `10000000000`) trước khi đội Scrum vào chấm điểm thật trong buổi họp Sprint Planning.
- **Quy tắc code:**
  1. Kiểm tra phân phối điểm chuẩn của dự án để xác định miền hợp lệ `[SP_min, SP_max]` (thông thường là `[0.5, 40.0]` hoặc `[0.5, 100.0]` tùy quy ước Planning Poker của dự án).
  2. Nếu `From_String` của lần đổi `Story Points` đầu tiên là `NULL`, `0`, hoặc nằm ngoài `[SP_min, SP_max]`, phải bỏ qua giá trị nháp đó và lấy `To_String` hợp lệ đầu tiên trong `Change_Log` làm `Initial_Story_Point` (đồng thời cập nhật `Real_Estimation_Date` theo thời điểm của bản ghi đó).
  3. Tạo cột cờ `Is_Valid_Scale_SP` (`0` / `1`) để đánh dấu các mẫu dị biệt (như Epic lớn hoặc lỗi nhập liệu) thay vì tự ý xóa ngầm.

### Quy tắc B4 — Không tin vào cột cờ `Description_Changed_After_Estimation` trong bảng `Issue`
- **Lý do:** Cột `Description_Changed_After_Estimation` trong bảng `Issue` của TAWOS bị lỗi ghi nhận bằng `0` trên toàn bộ CSDL, dù thực tế trong `Change_Log` có hàng trăm công việc bị sửa `description` sau ước lượng.
- **Quy tắc code:** Luôn truy vấn trực tiếp bảng `Change_Log` với điều kiện `LOWER(Field) IN ('summary', 'description', 'issuetype', 'priority', 'component')` và `Creation_Date > Real_Estimation_Date`, lấy `From_String` của bản ghi đầu tiên sau mốc ước lượng để khôi phục trạng thái quá khứ.

### Quy tắc B5 — Xóa 100% các cột phát sinh sau thời điểm ước lượng khỏi file CSV đầu ra
- **Danh sách các cột cấm xuất hiện trong `cleaned_dataset.csv`:**
  - `Status`, `Resolution`, `Resolution_Date`, `Last_Updated`
  - `Timespent`, `In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`
  - `Pull_Request_URL`, `Description_Code` (trích từ mô tả cuối)
  - `Assignee_ID`, `Sprint_ID`, `Story_Point` (nhãn cuối chưa khôi phục)

### Quy tắc B6 — Quy chuẩn viết file Jupyter Notebook (`.ipynb`)
- Kết nối CSDL ở chế độ chỉ đọc (`sqlite3.connect("file:C:/tawos/tawos_eda.db?mode=ro", uri=True)`).
- Truy vấn bảng `Change_Log` theo khoảng khóa chính `WHERE Issue_ID BETWEEN min_id AND max_id` để tận dụng chỉ mục (`idx_changelog_issue`), giúp tốc độ chạy dưới 2 giây cho mỗi dự án.
- **Cell văn bản (Markdown) trong `.ipynb`:** Chỉ viết duy nhất tiêu đề **Heading 3 (`### ...`)** và 1–2 câu mô tả ngắn gọn; mọi giải thích chi tiết đưa sang hệ thống 4 file `.md`.
