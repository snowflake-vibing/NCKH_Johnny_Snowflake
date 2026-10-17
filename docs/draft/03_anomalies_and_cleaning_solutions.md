# 🛠️ PHẦN 3. PHÁT HIỆN CÁC ĐIỂM BẤT THƯỜNG & GIẢI PHÁP XỬ LÝ TƯƠNG ỨNG ĐỂ TẠO CLEAN DATA

> **Nguyên tắc trình bày:** Với mỗi điểm bất thường (Anomaly) hoặc lỗ hổng rò rỉ dữ liệu (Data Leakage) phát hiện được trên tập **3,542 công việc của dự án Spring XD**, tài liệu này trình bày trực tiếp **bằng chứng định lượng** và **cách giải quyết triệt để** đã được hiện thực hóa trong [`EDA_SpringXD_Leakage_Free.ipynb`](EDA_SpringXD_Leakage_Free.ipynb) để tạo ra [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv).

---

## 1. Bất Thường 1: Ký Tự Nháy Kép Bọc Chuỗi Từ SQL Dump (`\"...\"` và `\"\"\"...\"\"\"`) Gây Rò Rỉ Định Dạng Nhân Tạo

### 🔴 Phát hiện điểm bất thường
- Khi kiểm tra chuỗi văn bản gốc trong bảng `Issue` của `C:/tawos/tawos_eda.db`, toàn bộ **3,542 / 3,542 dòng (`100%`)** ở cột `Title` đều bị bọc bởi cặp ký tự `\"...\"` (ví dụ: `\"How do I make a job restartable in spring xd\"`), cột `Description` bị bọc bởi `\"...\"`, và cột `Description_Text` bị bọc bởi 3 cặp `\"\"\"...\"\"\"`.
- Ngược lại, trong bảng `Change_Log`, các cột `From_String` và `To_String` lưu văn bản thuần túy **không hề có** các ký tự bọc `\"` này.
- **Tác hại nghiêm trọng:** Nếu ghép trực tiếp văn bản khôi phục từ `Change_Log` với văn bản giữ nguyên từ bảng `Issue`, các công việc từng bị chỉnh sửa sau ước lượng sẽ không có dấu `\"` ở đầu, còn các công việc không bị chỉnh sửa lại bắt đầu bằng `\"` hoặc `\"\"\"`. Các mô hình ngôn ngữ (như GPT-2, RoBERTa, TF-IDF) sẽ lập tức học vẹt dấu `\"` này như một đặc trưng rò rỉ nhân tạo (*Synthetic Format Leakage*).

### ✅ Cách giải quyết đã áp dụng
- Xây dựng hàm chuẩn hóa chuỗi `strip_sql_quotes(val)` quét và gỡ bỏ đệ quy toàn bộ các lớp ký tự bọc `\"\"\"`, `"""`, `\"` và `"` ở hai đầu chuỗi cho cả bảng `Issue` lẫn bảng `Change_Log` ngay trước khi thực hiện đối chiếu và khôi phục.
- **Kết quả:** 100% văn bản trong `Clean_Title`, `Clean_Description` và `Clean_Text` của `springxd_cleaned_dataset.csv` hoàn toàn sạch dấu bọc SQL (`0 / 3,542` dòng còn chứa `\"`).

---

## 2. Bất Thường 2: Cột `Issue.Estimation_Date` Bị Gán Cứng Theo `Creation_Date` Và Lệch Múi Giờ `-1.00 Giờ`

### 🔴 Phát hiện điểm bất thường
- Khi kiểm tra hiệu số thời gian `Issue.Estimation_Date - Issue.Creation_Date` trên 3,542 công việc của dự án Spring XD:
  1. Có tới **2,442 công việc (`68.94%`)** có `Estimation_Date` **sớm hơn `Creation_Date` đúng `-1.00 giờ`** (ví dụ: tạo lúc `13:41:25` nhưng `Estimation_Date` lại ghi `12:41:25`). Đây là lỗi lệch múi giờ mùa hè (DST/BST offset) khi nhóm tác giả TAWOS sinh cột `Estimation_Date` từ `Creation_Date`.
  2. Có **1,100 công việc (`31.06%`)** có `Estimation_Date == Creation_Date`.
  3. **Không có bất kỳ công việc nào (`0 dòng`)** trong bảng `Issue` của Spring XD có `Estimation_Date > Creation_Date`, mặc dù thực tế trong `Change_Log` có **89 công việc** lúc mới tạo chưa có điểm hợp lệ (`From_String = NULL`, `0` hoặc điểm nháp) và chỉ được chấm điểm nhiều giờ hoặc nhiều ngày sau khi tạo!

### ✅ Cách giải quyết đã áp dụng
- Không sử dụng cột `Issue.Estimation_Date` bị lỗi, mà tái thiết lập cột **`Real_Estimation_Date`** trực tiếp từ chuỗi sự kiện `Field = 'Story Points'` trong bảng `Change_Log`:
  - Nếu công việc được gán điểm hợp lệ ngay từ lúc tạo (không có log `Story Points`, hoặc lần đổi `Story Points` đầu tiên đã có `From_String` hợp lệ): Đặt `Real_Estimation_Date = Creation_Date` (triệt tiêu hoàn toàn độ lệch `-1.00 giờ` trên 2,442 công việc).
  - Nếu công việc lúc tạo chưa có điểm hợp lệ (`From_String` là `NULL`, `0`, hoặc ngoài thang đo) và được chấm điểm sau đó trong `Change_Log`: Đặt `Real_Estimation_Date` bằng đúng thời điểm `Creation_Date` của bản ghi `Change_Log` đầu tiên gán điểm Story Point hợp lệ.

---

## 3. Bất Thường 3: Điểm Giả Định / Placeholder (`10000000000`, `9999999`, `1000`, `444`, `100`, `0`) Khi Mở Ticket Và Nhãn Nhiễu Ngoài Thang Đo (`2567.0`)

### 🔴 Phát hiện điểm bất thường
- Khi kiểm tra giá trị `From_String` của lần thay đổi `Story Points` đầu tiên trong bảng `Change_Log` (trên 517 công việc có lịch sử đổi điểm):
  1. Có `23` công việc lúc tạo để trống (`From_String = NULL`) và `47` công việc lúc tạo điền `0` (`From_String = '0'`).
  2. Đặc biệt, có **19 công việc** lúc mới mở ticket bị người báo cáo điền các con số giả định khổng lồ hoặc ngoài thang đo để đánh dấu "chưa ước lượng / chờ họp Planning", sau đó đội Scrum mới vào thay bằng điểm thật (`1, 2, 3, 5, 8`):
     - `XD-3470`: `From_String = 10000000000` $\rightarrow$ đổi thành `To_String = 1`
     - `XD-3476`: `From_String = 9999999` $\rightarrow$ đổi thành `To_String = 1`
     - `XD-3474` & `XD-3475`: `From_String = 999999` $\rightarrow$ đổi thành `To_String = 1`
     - `XD-2731`: `From_String = 1000` $\rightarrow$ đổi thành `To_String = 5`
     - `XD-3710`: `From_String = 610` $\rightarrow$ đổi thành `To_String = 8`
     - `XD-2974`: `From_String = 444` $\rightarrow$ đổi thành `To_String = 2`
     - `XD-3713`: `From_String = 233` $\rightarrow$ đổi thành `To_String = 5`
     - `XD-3712`: `From_String = 111` $\rightarrow$ đổi thành `To_String = 1`
     - `XD-1584`, `XD-2578`, `XD-2371`, `XD-2355`: `From_String = 100` $\rightarrow$ đổi thành `To_String = 1, 2, 8`
     - `XD-2675`: `From_String = -1` $\rightarrow$ đổi thành `To_String = 3`
     - `XD-2580`: `From_String = 0.01` $\rightarrow$ đổi thành `To_String = 1`
     *(Nếu lấy mù quáng `From_String > 0` làm `Initial_Story_Point`, trung bình nhãn mục tiêu sẽ bị vọt lên tới **2,825,244.50 điểm**!).*
  3. Ngoài ra, có **6 công việc (`0.17%`)** giữ nguyên điểm vượt trần Planning Poker (`> 40.0`) đến tận lúc đóng: gồm `XD-2602` (`Story_Point = 2567.0`, đóng với lý do `Works as Designed`), `XD-3562` (`Story_Point = 100.0`, trạng thái `To Do`), và 4 Epic lớn (`XD-92`, `XD-836`, `XD-996`, `XD-1141` có điểm `50, 80, 100`).

### ✅ Cách giải quyết đã áp dụng
- Thiết lập miền thang đo Planning Poker hợp lệ của dự án Spring XD là **`[0.5, 40.0]`**:
  - Với **402 công việc** có `From_String` đầu tiên nằm trong `[0.5, 40.0]`: Khôi phục `Initial_Story_Point = float(From_String)`.
  - Với **89 công việc** có `From_String` là `NULL`, `0`, hoặc nằm ngoài `[0.5, 40.0]`: Loại bỏ con số giả định lúc tạo, lấy giá trị `To_String` hợp lệ đầu tiên trong `[0.5, 40.0]` làm `Initial_Story_Point` (nhờ đó khôi phục chính xác điểm thật `1, 2, 3, 5, 8` mà đội Scrum đã chấm, đưa `Mean(Initial_Story_Point)` về đúng **`3.1497`**, `Median = 3.0000`).
  - Với **6 công việc** ngoại lệ (`50, 80, 100, 2567`): Gắn cờ `Is_Valid_Scale_SP = 0` trong `springxd_cleaned_dataset.csv` để người dùng dễ dàng lọc giữ lại `3,536` mẫu chuẩn (`Is_Valid_Scale_SP = 1`) khi huấn luyện mô hình.

---

## 4. Bất Thường 4: Cột Cờ `Description_Changed_After_Estimation = 0` Báo Sai Và Rò Rỉ Văn Bản Sau Ước Lượng (`Title` & `Description`)

### 🔴 Phát hiện điểm bất thường
- Trong bảng `Issue`, cột `Description_Changed_After_Estimation` hiển thị giá trị `0` cho cả `3,542 / 3,542` công việc, khiến người dùng lầm tưởng rằng không có công việc nào bị sửa mô tả sau khi ước lượng.
- Tuy nhiên, khi kiểm toán trực tiếp bảng `Change_Log` đối chiếu với mốc `Real_Estimation_Date`:
  - Có **594 công việc (`16.77%`)** bị thay đổi nội dung `Title` (`Field = 'summary'`, với `802` lượt sửa) sau thời điểm ước lượng.
  - Có **576 công việc (`16.26%`)** bị thay đổi nội dung `Description` (`Field = 'description'`, với `886` lượt sửa) sau thời điểm ước lượng.
  - Tổng cộng có **969 công việc (`27.36%` toàn dự án Spring XD)** bị thay đổi `Title` hoặc `Description` (bổ sung nguyên nhân lỗi, stack trace, giải pháp kỹ thuật) sau khi đã chấm điểm Story Point!

### ✅ Cách giải quyết đã áp dụng
- Bỏ qua hoàn toàn các cột cờ có sẵn trong bảng `Issue` và thực thi thuật toán **Tái dựng trạng thái văn bản lịch sử (`Historical Text Reconstruction`)** từ bảng `Change_Log`:
  - Với mỗi công việc và mỗi trường văn bản (`summary`, `description`), lọc tất cả bản ghi `Change_Log` có `Creation_Date > Real_Estimation_Date` và sắp xếp tăng dần theo `(Creation_Date, ID)`.
  - Nếu tồn tại bản ghi thay đổi sau `Real_Estimation_Date`, giá trị văn bản tại đúng thời điểm ước lượng (`Clean_Title`, `Clean_Description`) chính là **`From_String` của bản ghi thay đổi đầu tiên xảy ra sau `Real_Estimation_Date`**.
  - Nếu không có bản ghi thay đổi nào sau `Real_Estimation_Date`, giữ nguyên văn bản đã làm sạch từ bảng `Issue`.
  - Sau đó ghép `Clean_Text = Clean_Title + " " + Clean_Description` và tính lại số từ sạch (`Clean_Title_Word_Count`, `Clean_Desc_Word_Count`, `Has_Clean_Description`).

---

## 5. Bất Thường 5: Biến Động Sau Ước Lượng Của Siêu Dữ Liệu (`Type`, `Priority`, `Component`) Và 12 Cột Rò Rỉ Tương Lai

### 🔴 Phát hiện điểm bất thường
- Kiểm toán `Change_Log` sau mốc `Real_Estimation_Date` cho thấy:
  1. **Nhóm siêu dữ liệu cấu trúc có sẵn lúc lập kế hoạch nhưng bị sửa đổi một phần về sau:** `Type` bị đổi trên **255 issues (`7.20%`)**, `Component` bị đổi trên **252 issues (`7.11%`)**, và `Priority` bị đổi trên **137 issues (`3.87%`)**.
  2. **Nhóm 12 thuộc tính bị rò rỉ tương lai nặng nề (chỉ hình thành trong hoặc sau khi làm task):** `Status` (`83.37%` đổi sau ước lượng), `Resolution` (`82.38%`), `Fix_Version` (`75.24%`), `Sprint_ID` (`63.55%`), `Assignee_ID` (`50.51%`), `Pull_Request_URL` (`14.85%`), `Resolution_Date`, `Last_Updated`, `Timespent`, `In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`, và `Description_Code`.
  3. **Nguy cơ rò rỉ do chia tập ngẫu nhiên (*Split Leakage*):** Nếu chia Train/Test ngẫu nhiên hoặc xếp theo `ID`, các công việc ước lượng ở tương lai sẽ lọt vào tập Train để dự đoán công việc ở quá khứ.

### ✅ Cách giải quyết đã áp dụng
1. **Khôi phục nhóm siêu dữ liệu cấu trúc về đúng mốc `Real_Estimation_Date`:**
   - Khôi phục `Clean_Type` và `Clean_Priority` bằng `From_String` của lần thay đổi đầu tiên sau `Real_Estimation_Date`.
   - Khôi phục `Clean_Components` bằng thuật toán hoàn tác ngược (Reverse-Replay) từ tập `Issue_Component` cuối cùng: duyệt ngược các bản ghi `Change_Log (Field = 'Component')` diễn ra sau `Real_Estimation_Date` để gỡ bỏ các Component được thêm muộn (`To_String`) và trả lại các Component bị xóa muộn (`From_String`).
2. **Loại bỏ 100% 12 cột rò rỉ tương lai khỏi `springxd_cleaned_dataset.csv`:**
   - Xóa hoàn toàn các cột `Status`, `Resolution`, `Resolution_Date`, `Last_Updated`, `Story_Point` (bản cuối), `Timespent`, `In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`, `Pull_Request_URL`, `Description_Code`, `Assignee_ID`, `Sprint_ID`.
3. **Thiết lập `Chronological_Split` (60% Train / 20% Val / 20% Test) theo `Real_Estimation_Date`:**
   - Sắp xếp toàn bộ 3,542 công việc theo thứ tự thời gian `Real_Estimation_Date` tăng dần rồi mới phân tách `train` (`2,125` mẫu), `val` (`708` mẫu), `test` (`709` mẫu), chặn đứng hoàn toàn *Split Leakage*.

---

## 📊 Bảng Tổng Hợp Đối Chiếu: Điểm Bất Thường $\leftrightarrow$ Giải Pháp Xử Lý

| STT | Điểm bất thường phát hiện trên Spring XD | Quy mô ảnh hưởng | Giải pháp xử lý trong Pipeline | Cột đầu ra trong `springxd_cleaned_dataset.csv` |
| :-: | :--- | :---: | :--- | :--- |
| **1** | Ký tự bọc chuỗi từ SQL Dump (`\"` và `\"\"\"`) ở bảng `Issue` | `3,542 / 3,542` dòng (`100%`) | Hàm `strip_sql_quotes()` cắt bỏ toàn bộ dấu nháy bọc ngoài ở cả `Issue` và `Change_Log` | `Clean_Title`, `Clean_Description`, `Clean_Text` |
| **2** | `Issue.Estimation_Date` bị lệch `-1.00h` và không cập nhật theo `Change_Log` | `2,442` dòng lệch `-1h` + `89` dòng chấm điểm muộn | Truy vết `Change_Log (Field='Story Points')` để xác định mốc ước lượng thực sự | `Real_Estimation_Date`, `Estimation_Source` |
| **3** | Điểm giả định lúc mở ticket (`10^10`, `9999999`, `1000`, `0`, `NULL`) & 6 mẫu ngoại lệ (`2567.0`, Epic `50-100`) | `89` dòng điểm nháp + `6` dòng ngoại lệ | Lọc điểm hợp lệ đầu tiên trong miền `[0.5, 40.0]` và gắn cờ kiểm soát thang đo | `Initial_Story_Point`, `Is_Valid_Scale_SP` |
| **4** | Cờ `Description_Changed = 0` báo sai; văn bản `Title` & `Description` bị sửa sau ước lượng | `969` dòng (`27.36%`) bị sửa văn bản (`594` Title, `576` Desc) | Lấy `From_String` của bản ghi sửa đổi đầu tiên sau `Real_Estimation_Date` trong `Change_Log` | `Clean_Title`, `Clean_Description`, `Clean_Text`, `Clean_Title_Word_Count`, `Clean_Desc_Word_Count` |
| **5** | `Type`, `Priority`, `Component` bị đổi sau ước lượng | `255` Type, `137` Priority, `252` Component | Hoàn tác toàn bộ thay đổi diễn ra sau `Real_Estimation_Date` | `Clean_Type`, `Clean_Priority`, `Clean_Components` |
| **6** | 12 thuộc tính chứa kết quả đóng task & nỗ lực thực tế phát sinh trong tương lai | Toàn bộ `3,542` dòng | Cắt bỏ hoàn toàn khỏi schema của bộ dữ liệu sạch | *(Đã loại bỏ 100% khỏi file CSV)* |
| **7** | Khác biệt 16 mẫu mới (`XD-3754`..`XD-3769`) so với tập 3,526 mẫu của GPT2SP & nguy cơ *Split Leakage* | `16` dòng mới + toàn bộ `3,542` dòng | Gắn cờ `Is_GPT2SP_3526_Subset` và sắp xếp theo `Real_Estimation_Date` để chia 60/20/20 | `Is_GPT2SP_3526_Subset`, `Chronological_Split` |

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc thông tin lưu trữ](01_data_scale_and_overview.md)**
2. 📋 **[Phần 2: Bảng dữ liệu đầy đủ & thống kê số lượng từng loại trong mỗi thuộc tính (`N = 3,542`)](02_attribute_breakdown_and_counts.md)**
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & giải pháp xử lý tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)** *(Tài liệu hiện tại)*
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)**
5. 📏 **[RULE.md: Bộ quy tắc chuẩn hóa dữ liệu & tài liệu cho các dự án tiếp theo](RULE.md)**
