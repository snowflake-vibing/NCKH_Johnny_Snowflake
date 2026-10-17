# 📊 BÁO CÁO PHÂN TÍCH CHUYÊN SÂU (EDA) & KIỂM TOÁN ĐẶC TRƯNG KHÔNG RÒ RỈ TRÊN DỰ ÁN SPRING XD (TAWOS v1.1)

> **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*  
> **Đối tượng phân tích:** Dự án **Spring XD (`Project_Key = 'XD'`, `Project_ID = 1`)** — Cơ sở dữ liệu `C:/tawos/tawos_eda.db` (TAWOS Dataset v1.1)  
> **Đầu ra dữ liệu sạch (Cleaned Dataset):**  
> - [`docs/draft/springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv)  
> - `D:/NCKH_3/data/clean/springxd_cleaned_dataset.csv`  
> - `C:/tawos/springxd_cleaned_dataset.csv`  
> **Notebook thực thi:** [`docs/draft/EDA_SpringXD_Leakage_Free.ipynb`](EDA_SpringXD_Leakage_Free.ipynb)

---

## 🎯 1. Tổng Quan & Đối Chiếu Quy Mô Dữ Liệu (3,707 $\rightarrow$ 3,542 $\rightarrow$ 3,526 Issues)

Khi truy xuất trực tiếp dự án **Spring XD (`Project_ID = 1`)** từ CSDL `C:/tawos/tawos_eda.db`, nhóm phát hiện mối liên hệ chính xác tuyệt đối giữa bản TAWOS v1.1 và bộ dữ liệu chuẩn của **Choetkiertikul et al. (2019)** / **GPT2SP (Fu & Tantithamthavorn, 2023)**:

| Cấp độ tập dữ liệu (Population Tier) | Số lượng Issue | Phạm vi mã công việc (`Issue_Key`) | Giải thích & Ý nghĩa Khoa học |
| :--- | :---: | :---: | :--- |
| **1. Toàn bộ dự án Spring XD trong TAWOS v1.1** | **3,707** | `XD-1` $\rightarrow$ `XD-3769` | Gồm toàn bộ công việc được tạo từ `2013-04-12` đến `2018-11-16`, kèm theo **43,227 bản ghi `Change_Log`** và **4,122 liên kết `Issue_Component`**. |
| **2. Issue không có điểm hợp lệ (`SP = 0` hoặc `NULL`)** | **165** | `163` mẫu `SP = 0`<br>`2` mẫu `SP = NULL` | Các công việc chưa được chấm điểm hoặc dùng giá trị `0` làm mặc định. **Bắt buộc loại bỏ**, tuyệt đối không điền khuyết (impute) bằng Median. |
| **3. Quần thể có `Story_Point > 0` trên TAWOS v1.1** | **3,542** | `XD-1` $\rightarrow$ `XD-3769` | Chiếm **95.55%** toàn dự án Spring XD. Đây là tập dữ liệu đầy đủ trong `springxd_cleaned_dataset.csv`. |
| **4. Tập chuẩn đối đầu 1-1 với bài báo GPT2SP / Deep-SE** | **3,526** | `XD-1` $\rightarrow$ `XD-3753` | Choetkiertikul thu thập dữ liệu đến hết **31/03/2016** (`XD-3753`, đúng **3,526 issues**). TAWOS v1.1 thu thập bổ sung thêm đúng **16 issues** (`XD-3754` $\rightarrow$ `XD-3769`) phát sinh từ tháng 05/2016 đến tháng 11/2018 ($3,526 + 16 = 3,542$). Trong `cleaned_dataset`, cột cờ `Is_GPT2SP_3526_Subset = 1` lọc ra chính xác 3,526 mẫu này. |

---

## 🔍 2. Bốn Lỗi Tiềm Ẩn (Data Pitfalls) Phát Hiện Khi Kiểm Toán Sâu CSDL TAWOS v1.1

Nếu chỉ lấy trực tiếp các cột có sẵn trong bảng `Issue` của `tawos_eda.db` mà không kiểm toán chéo với bảng `Change_Log`, mô hình học máy sẽ mắc phải **4 sai lệch nghiêm trọng** sau đây (tất cả đã được xử lý triệt để trong [EDA_SpringXD_Leakage_Free.ipynb](EDA_SpringXD_Leakage_Free.ipynb)):

### 🚨 Phát hiện 1: Rò rỉ định dạng nhân tạo (Synthetic Quote-Wrapper Leakage) giữa bảng `Issue` và `Change_Log`
- **Hiện tượng:** Trong bảng `Issue` của `tawos_eda.db`, do quá trình xuất/nhập SQL dump, toàn bộ chuỗi ở cột `Title` đều bị bọc bởi cặp ký tự `\"...\"` (ví dụ: `\"How do I make a job restartable in spring xd\"`), cột `Description` bị bọc bởi `\"...\"`, và cột `Description_Text` bị bọc bởi `\"\"\"...\"\"\"`. Ngược lại, các chuỗi `From_String` và `To_String` trong bảng `Change_Log` **không hề có** các ký tự bọc này.
- **Hậu quả nếu không xử lý:** Khi khôi phục văn bản, những issue bị sửa sau ước lượng (lấy từ `Change_Log`) sẽ không có dấu `\"`, còn những issue không bị sửa (lấy từ `Issue`) lại bắt đầu bằng `\"` hoặc `\"\"\"`. Mô hình Transformer (như GPT-2, RoBERTa) sẽ ngay lập tức nhận diện dấu `\"` ở đầu câu như một "mẹo rò rỉ" (shortcut feature) để phân biệt issue nào từng bị sửa trong quá trình làm việc!
- **Giải pháp đã áp dụng:** Hàm `strip_sql_quotes()` làm sạch hoàn toàn các dấu bọc `\"` và `\"\"\"` ở cả hai bảng trước khi so sánh và ghép nối.

### 🚨 Phát hiện 2: Cột cờ `Description_Changed_After_Estimation` trong bảng `Issue` bị lỗi bằng `0`
- **Hiện tượng:** Trong bảng `Issue`, cột `Description_Changed_After_Estimation` hiển thị giá trị `0` cho toàn bộ 3,542 công việc của Spring XD (cũng như toàn bộ 63,011 công việc của TAWOS).
- **Sự thật khi truy vết `Change_Log`:** Khi truy vấn trực tiếp bảng `Change_Log` với `Field = 'description'` sau thời điểm ước lượng, dự án Spring XD thực chất có tới **581 công việc (`16.40%`)** có bản ghi cập nhật mô tả sau khi đã chấm điểm (trong đó **576 công việc** có nội dung mô tả thay đổi thực sự so với lúc ước lượng). Nếu cộng gộp cả `Title` (`summary`) và `Description`, có tới **969 công việc (`27.36%` toàn dự án Spring XD)** bị biến đổi văn bản sau thời điểm ước lượng!

### 🚨 Phát hiện 3: Lỗi gán cứng `Estimation_Date` và độ lệch múi giờ `-1.00 giờ` trong bảng `Issue`
- **Hiện tượng:** Khi kiểm tra cột `Issue.Estimation_Date` của 3,542 công việc trong Spring XD:
  - Có **2,442 công việc (`68.94%`)** có `Estimation_Date` sớm hơn `Creation_Date` đúng **`-1.00 giờ`** (do lỗi quy đổi múi giờ DST/BST khi tác giả TAWOS sinh cột `Estimation_Date` từ `Creation_Date`).
  - Có **1,100 công việc (`31.06%`)** có `Estimation_Date == Creation_Date`.
  - **Không có bất kỳ dòng nào (`0 dòng`)** trong `Issue.Estimation_Date` của Spring XD có `Estimation_Date > Creation_Date`, kể cả những công việc lúc mới tạo chưa hề có điểm (`From_String = NULL` hoặc `From_String = 0`) và chỉ được chấm điểm sau đó vài ngày trong `Change_Log`!
- **Giải pháp đã áp dụng:** Xây dựng thuật toán truy vết trực tiếp trên chuỗi sự kiện `Field = 'Story Points'` của bảng `Change_Log` để xác định mốc **`Real_Estimation_Date`** (thời điểm thực tế lần đầu tiên công việc nhận một điểm Story Point hợp lệ).

### 🚨 Phát hiện 4: Hiện tượng "Điểm Giả Định / Placeholder" (`9999999`, `10000000000`, `1000`, `444`, `100`, `0`) khi tạo Issue
- **Hiện tượng:** Khi kiểm tra giá trị `From_String` trong lần thay đổi `Story Points` đầu tiên trên `Change_Log`, nhóm phát hiện **87 công việc** được người báo cáo (Reporter) nhập các con số giả định/nháp lúc mới tạo ticket (trước khi họp Sprint Planning):
  - `23` công việc lúc tạo để trống (`From_String = NULL`).
  - `47` công việc lúc tạo điền `0` (`From_String = '0'`).
  - `17` công việc lúc tạo điền số khổng lồ hoặc ngoài thang đo để đánh dấu "chưa ước lượng": ví dụ `XD-3470` (`From_String = 10000000000` $\rightarrow$ `To_String = 1`), `XD-3476` (`9999999` $\rightarrow$ `1`), `XD-3474` & `XD-3475` (`999999` $\rightarrow$ `1`), `XD-2731` (`1000` $\rightarrow$ `5`), `XD-2974` (`444` $\rightarrow$ `2`), `XD-3710` (`610` $\rightarrow$ `8`), `XD-3713` (`233` $\rightarrow$ `5`), `XD-3712` (`111` $\rightarrow$ `1`), `XD-1584` (`100` $\rightarrow$ `1`), `XD-2675` (`-1` $\rightarrow$ `3`), `XD-2580` (`0.01` $\rightarrow$ `1`).
- **Hậu quả nếu lấy mù quáng `From_String`:** Nếu lấy trực tiếp `From_String > 0` làm `Initial_Story_Point`, các con số `10,000,000,000` và `9,999,999` sẽ làm trung bình nhãn mục tiêu vọt lên tới **2.82 triệu điểm**!
- **Giải pháp đã áp dụng:** Xác định miền thang điểm chuẩn của Spring XD là **`[0.5, 40.0]`**:
  1. Nếu `From_String` của lần đổi `Story Points` đầu tiên nằm trong `[0.5, 40.0]` (**430 issues**): Công việc đã được ước lượng hợp lệ ngay lúc tạo (`Real_Estimation_Date = Creation_Date`, `Initial_Story_Point = From_String`), và lần đổi trong `Change_Log` là sự điều chỉnh lại điểm trong Sprint.
  2. Nếu `From_String` là `NULL`, `0`, hoặc nằm ngoài `[0.5, 40.0]` (**80 issues**): Công việc chưa được ước lượng lúc tạo; thời điểm ước lượng thực sự (`Real_Estimation_Date`) chính là `Creation_Date` của bản ghi `Change_Log` đầu tiên gán giá trị `To_String` hợp lệ trong `[0.5, 40.0]`, và `Initial_Story_Point = To_String`.
  3. Còn lại **7 công việc** (`0.20%`) có điểm không bao giờ nằm trong `[0.5, 40.0]` (gồm 4 Epic lớn có điểm `50, 80, 100`; 1 Story `XD-3562` đang ở trạng thái `To Do` với điểm nháp `100`; 1 issue `XD-2602` đóng với trạng thái `Works as Designed` mang điểm lỗi `2567`; và 1 issue `XD-1970` có điểm `0.2`) được gắn cờ `Is_Valid_Scale_SP = 0` để dễ dàng lọc khi huấn luyện mô hình.

---

## 📈 3. Kết Quả Kiểm Toán Rò Rỉ Dữ Liệu Trên Dự Án Spring XD (`N = 3,542`)

Bảng dưới đây tổng hợp mức độ biến động của các thuộc tính **sau mốc `Real_Estimation_Date`** trên 3,542 công việc của Spring XD:

| Thứ hạng | Trường dữ liệu trong `Change_Log` | Số lượt thay đổi sau ước lượng | Số Issue bị thay đổi | Tỷ lệ rò rỉ trên Spring XD (%) | Đánh giá & Quyết định Kiểm soát Rò rỉ |
| :-: | :--- | :---: | :---: | :---: | :--- |
| **1** | `status` (Trạng thái công việc) | 6,099 | **2,953** | **83.37%** | ❌ **Loại bỏ 100%** (Phản ánh tiến độ làm việc & đóng task `Done`) |
| **2** | `resolution` (Kết quả giải quyết) | 3,162 | **2,918** | **82.38%** | ❌ **Loại bỏ 100%** (Chỉ xuất hiện khi task đã kết thúc: `Complete`, `Fixed`...) |
| **3** | `Fix Version` (Phiên bản phát hành) | 4,369 | **2,665** | **75.24%** | ❌ **Loại bỏ 100%** (Được gán/dời liên tục khi đóng gói bản build) |
| **4** | `Rank` (Thứ tự ưu tiên backlog) | 7,611 | **2,477** | **69.93%** | ❌ **Loại bỏ 100%** (Thay đổi liên tục trong suốt vòng đời dự án) |
| **5** | `Workflow` (Quy trình Jira) | 2,390 | **2,371** | **66.94%** | ❌ **Loại bỏ 100%** (Biến động quản trị hệ thống sau ước lượng) |
| **6** | `Sprint` (Chu kỳ Sprint) | 4,973 | **2,251** | **63.55%** | ❌ **Loại bỏ 100%** (Phản ánh Sprint cuối cùng sau khi task bị tràn/dời Sprint) |
| **7** | `assignee` (Người được giao việc) | 2,035 | **1,789** | **50.51%** | ❌ **Loại bỏ ở mô hình cơ sở** (Hơn một nửa số task mới được gán người làm sau khi ước lượng) |
| **8** | `Link` (Liên kết giữa các Issue) | 1,084 | **674** | **19.03%** | ❌ **Loại bỏ** (Phần lớn liên kết phát sinh trong lúc lập trình/tách task) |
| **9** | `summary` (`Title` - Tiêu đề) | 802 | **594** | **16.77%** | 🔄 **Bắt buộc khôi phục `Clean_Title`** tại `Real_Estimation_Date` |
| **10** | `description` (`Description` - Mô tả) | 886 | **576** | **16.26%** | 🔄 **Bắt buộc khôi phục `Clean_Description`** tại `Real_Estimation_Date` |
| **11** | `Epic Link` (Liên kết Epic) | 665 | **565** | **15.95%** | ⚠️ Hạn chế hoặc chỉ dùng trạng thái trước `Real_Estimation_Date` |
| **12** | `Pull Request URL` (Liên kết PR GitHub) | 541 | **526** | **14.85%** | ❌ **Loại bỏ 100%** (Link PR chứa thẳng code giải pháp sau khi làm xong) |
| **13** | `Story Points` (Điểm nỗ lực) | 482 | **411** | **11.60%** | 🎯 **Khôi phục `Initial_Story_Point`** làm nhãn Ground Truth chuẩn |
| **14** | `Component` (Thành phần hệ thống) | 350 | **256** | **7.23%** | 🔄 **Khôi phục `Clean_Components`** bằng cách hoàn tác các thay đổi sau ước lượng |
| **15** | `issuetype` (`Type` - Loại Issue) | 275 | **255** | **7.20%** | 🔄 **Khôi phục `Clean_Type`** tại `Real_Estimation_Date` (Ổn định 92.80%) |
| **16** | `Time Spent` (Thời gian làm thực tế) | 257 | **253** | **7.14%** | ❌ **Loại bỏ 100%** (Cùng với `In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`) |
| **17** | `priority` (`Priority` - Độ ưu tiên) | 145 | **137** | **3.87%** | 🔄 **Khôi phục `Clean_Priority`** tại `Real_Estimation_Date` (Ổn định 96.13%) |

---

## 🧬 4. Cấu Trúc Chi Tiết Bộ Dữ Liệu Sạch (`springxd_cleaned_dataset.csv`)

Bộ dữ liệu đầu ra đã được xuất thành công với **3,542 dòng $\times$ 28 cột** (hoàn toàn không chứa bất kỳ cột rò rỉ tương lai nào) tại `D:/NCKH_3/data/clean/springxd_cleaned_dataset.csv` và `C:/tawos/springxd_cleaned_dataset.csv`:

```mermaid
flowchart LR
    subgraph Raw["CSDL TAWOS v1.1 (C:/tawos/tawos_eda.db)"]
        I["Bảng Issue\n(3,707 dòng x 30 cột)"]
        CL["Bảng Change_Log\n(43,227 dòng)"]
        CP["Bảng Component & Issue_Component\n(4,122 liên kết)"]
    end

    subgraph Engine["Pipeline Kiểm Soát Rò Rỉ (Notebook)"]
        S1["1. Lọc Story_Point > 0 (3,542 dòng)\n& Xóa ký tự bọc SQL (\\\" và \\\"\\\"\\\")"]
        S2["2. Khôi phục Real_Estimation_Date\n& Initial_Story_Point hợp lệ [0.5, 40]"]
        S3["3. Tái dựng Clean_Title, Clean_Description,\nClean_Type, Clean_Priority, Clean_Components"]
        S4["4. Cắt bỏ 12 cột rò rỉ tương lai\n& Chia Chronological Split 60/20/20"]
    end

    subgraph Out["Cleaned Dataset (28 cột sạch)"]
        CSV["springxd_cleaned_dataset.csv\n(3,542 dòng; 3,535 dòng chuẩn [0.5, 40])"]
    end

    I --> S1
    CL --> S2
    CP --> S3
    S1 --> S2 --> S3 --> S4 --> CSV
```

### Danh mục 28 cột trong `springxd_cleaned_dataset.csv`:

| Nhóm cột | Tên cột trong `cleaned_dataset` | Kiểu dữ liệu | Mô tả & Vai trò trong Mô hình Học máy |
| :--- | :--- | :---: | :--- |
| **1. Định danh & Thời gian gốc** | `ID`, `Issue_Key`, `Project_ID` | `int / str` | Mã định danh duy nhất của Issue (`XD-1` .. `XD-3769`). |
| | `Creation_Date` | `datetime str` | Thời điểm tạo Issue trên Jira. |
| | `Real_Estimation_Date` | `datetime str` | **Mốc cắt thông tin chuẩn (`Information Cut-off`)**: Thời điểm thực tế Issue nhận điểm Story Point hợp lệ đầu tiên. Dùng để sắp xếp thứ tự thời gian. |
| | `Estimation_Source` | `str` | Nguồn xác định điểm ban đầu (`Set_At_Creation_Unchanged`: 3,025; `Set_At_Creation_Later_Revised`: 430; `Estimated_Later_In_ChangeLog`: 80; `Unresolved_Outlier_SP`: 7). |
| | `Creator_ID`, `Reporter_ID` | `int` | Mã định danh người tạo và người báo cáo Issue (có sẵn từ lúc mở ticket). |
| **2. Đặc trưng Văn bản Sạch (Input cho LLM / NLP)** | `Clean_Title` | `str` | Tiêu đề công việc tại đúng thời điểm `Real_Estimation_Date` (đã loại bỏ mọi chỉnh sửa sau ước lượng và ký tự bọc SQL). |
| | `Clean_Description` | `str` | Mô tả chi tiết tại đúng thời điểm `Real_Estimation_Date`. |
| | `Clean_Text` | `str` | Ghép nối chuẩn `Clean_Title + " " + Clean_Description` (nếu Description rỗng chỉ lấy `Clean_Title`), sẵn sàng đưa vào Tokenizer của **GPT2SP / SBERT / RoBERTa / TF-IDF**. |
| **3. Đặc trưng Cấu trúc Sạch (Input cho Tabular / Hybrid ML)** | `Clean_Type` | `str` | Loại công việc tại thời điểm ước lượng (`Story`, `Bug`, `Improvement`, `Technical task`, `Epic`). |
| | `Clean_Priority` | `str` | Độ ưu tiên tại thời điểm ước lượng (`Major`, `Minor`, `Critical`, `Trivial`, `Blocker`). |
| | `Clean_Components` | `str` | Danh sách các thành phần hệ thống (`Container`, `Batch`, `Shell`, `Stream`...) gắn với Issue tại thời điểm ước lượng. |
| | `Clean_Title_Word_Count` | `int` | Số lượng từ trong `Clean_Title` (trung bình `8.13` từ). |
| | `Clean_Desc_Word_Count` | `int` | Số lượng từ trong `Clean_Description` (trung bình `52.97` từ). |
| | `Has_Clean_Description` | `0 / 1` | Cờ nhị phân cho biết Issue có mô tả tại thời điểm ước lượng hay không (`94.75%` có mô tả). |
| | `Has_Clean_Component` | `0 / 1` | Cờ nhị phân cho biết Issue đã được gắn Component tại thời điểm ước lượng hay không (`88.96%` có Component). |
| **4. Cờ Kiểm toán Thay đổi (Phục vụ Phân tích Độ nhạy)** | `Title_Modified_After_Est` | `0 / 1` | `1` nếu tiêu đề bị sửa sau `Real_Estimation_Date` (`594` issues — `16.77%`). |
| | `Desc_Modified_After_Est` | `0 / 1` | `1` nếu mô tả bị sửa sau `Real_Estimation_Date` (`576` issues — `16.26%`). |
| | `Type_Modified_After_Est` | `0 / 1` | `1` nếu loại công việc bị đổi sau `Real_Estimation_Date` (`255` issues — `7.20%`). |
| | `Priority_Modified_After_Est` | `0 / 1` | `1` nếu độ ưu tiên bị đổi sau `Real_Estimation_Date` (`137` issues — `3.87%`). |
| | `Component_Modified_After_Est` | `0 / 1` | `1` nếu danh sách Component bị đổi sau `Real_Estimation_Date` (`252` issues — `7.11%`). |
| | `SP_Modified_After_Est` | `0 / 1` | `1` nếu điểm Story Point cuối cùng khác với điểm ước lượng ban đầu (`411` issues — `11.60%`). |
| **5. Nhãn Mục tiêu & Cờ Chia tập (Target & Evaluation Split)** | **`Initial_Story_Point`** | `float` | **Nhãn mục tiêu chuẩn (Ground Truth):** Điểm Story Point ước lượng ban đầu tại `Real_Estimation_Date` (Mean = `3.1536`, Median = `3.0000` trên tập hợp lệ). |
| | `Is_Valid_Scale_SP` | `0 / 1` | `1` cho **3,535 issues (`99.80%`)** có điểm nằm trong thang đo hợp lệ `[0.5, 40.0]`; `0` cho 7 mẫu dị biệt (`2567.0`, `100.0`, `80.0`, `50.0`, `0.2`). |
| | `Is_GPT2SP_3526_Subset` | `0 / 1` | `1` cho đúng **3,526 issues** (`XD-1` .. `XD-3753`) trùng khớp với tập dữ liệu của bài báo GPT2SP; `0` cho 16 issues mới hơn (`XD-3754` .. `XD-3769`). |
| | `Chronological_Split` | `str` | Nhãn chia tập theo đúng thứ tự thời gian `Real_Estimation_Date` tỷ lệ **60% / 20% / 20%** (`train`: 2,125 mẫu; `val`: 708 mẫu; `test`: 709 mẫu), ngăn chặn hoàn toàn hiện tượng *Split Leakage*. |

---

## 💡 5. Hướng Dẫn Sử Dụng Nhanh `springxd_cleaned_dataset.csv` Cho Bước Mô Hình Hóa Tiếp Theo

Khi nạp `springxd_cleaned_dataset.csv` để huấn luyện các mô hình Baseline (Median, Mean, TF-IDF + Ridge/SVR) hoặc Deep Learning (GPT2SP, SBERT + GBT):

```python
import pandas as pd

df = pd.read_csv("D:/NCKH_3/data/clean/springxd_cleaned_dataset.csv")

# Lọc quần thể có thang điểm hợp lệ [0.5, 40.0] (3,535 issues)
df_model = df[df["Is_Valid_Scale_SP"] == 1].copy()

# Chia tập Train / Val / Test theo thời gian (Chronological Split)
train_df = df_model[df_model["Chronological_Split"] == "train"]
val_df   = df_model[df_model["Chronological_Split"] == "val"]
test_df  = df_model[df_model["Chronological_Split"] == "test"]

# Đặc trưng đầu vào không rò rỉ (X) và nhãn mục tiêu (y)
X_train_text = train_df["Clean_Text"]
y_train      = train_df["Initial_Story_Point"]
```
