# ✅ PHẦN 4. THẨM ĐỊNH LẠI CLEAN DATA ĐỂ ĐẢM BẢO KHÔNG CÒN DATA LEAKAGE (`springxd_cleaned_dataset.csv`)

> **Mục tiêu thẩm định:** Kiểm tra định lượng độc lập trên bộ dữ liệu đầu ra [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv) (`3,542 dòng x 28 cột`) nhằm xác nhận rằng **100% thông tin tương lai (Temporal / Feature / Split / Format Leakage) đã bị loại bỏ hoàn toàn** và dữ liệu đã sẵn sàng cho bước huấn luyện mô hình.

---

## 1. Bảng Thẩm Định 8 Tiêu Chí Chống Rò Rỉ Dữ Liệu (Zero-Leakage Audit)

Bảng dưới đây đối chiếu trực tiếp trạng thái dữ liệu **trước khi làm sạch (`Raw Issue Table`)** và **sau khi làm sạch (`springxd_cleaned_dataset.csv`)** trên cả 8 tiêu chí kiểm soát rò rỉ:

| STT | Tiêu chí kiểm định chất lượng & chống rò rỉ | Trạng thái trên dữ liệu gốc (`Raw Issue Table`) | Trạng thái trên Clean Data (`springxd_cleaned_dataset.csv`) | Kết quả thẩm định |
| :-: | :--- | :---: | :---: | :---: |
| **1** | **Kiểm định Format Leakage:** Số bản ghi còn chứa ký tự bọc SQL (`\"` hoặc `\"\"\"`) ở đầu/cuối chuỗi văn bản | `3,542 / 3,542` dòng (`100.00%`) | **`0 / 3,542` dòng (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **2** | **Kiểm định Timestamp Integrity:** Số bản ghi có mốc ước lượng sớm hơn mốc khởi tạo (`Real_Estimation_Date < Creation_Date`) | `2,442 / 3,542` dòng (`68.94%` bị lệch `-1.00h`) | **`0 / 3,542` dòng (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **3** | **Kiểm định Target Leakage & Placeholder:** Số bản ghi trong tập chuẩn (`Is_Valid_Scale_SP = 1`) bị dính điểm nháp (`10^10`, `9999999`, `1000`, `0`, `NULL`) | `89` dòng bị lệch mốc/điểm nháp (Mean SP vọt lên `2,825,244.50`) | **`0` dòng** (Mean SP chuẩn = **`3.1497`**, Median = **`3.0000`**) | ✅ **ĐẠT TUYỆT ĐỐI** |
| **4** | **Kiểm định Text Leakage (`Clean_Title`):** Số bản ghi còn chứa nội dung tiêu đề phát sinh sau `Real_Estimation_Date` | `594 / 3,542` dòng (`16.77%` bị rò rỉ) | **`0 / 3,542` dòng (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **5** | **Kiểm định Text Leakage (`Clean_Description`):** Số bản ghi còn chứa nội dung mô tả phát sinh sau `Real_Estimation_Date` | `576 / 3,542` dòng (`16.26%` bị rò rỉ) | **`0 / 3,542` dòng (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **6** | **Kiểm định Metadata Leakage (`Clean_Type`, `Clean_Priority`, `Clean_Components`):** Số bản ghi còn chứa phân loại sửa đổi sau `Real_Estimation_Date` | `255` Type, `137` Priority, `252` Component bị rò rỉ | **`0 / 3,542` dòng (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **7** | **Kiểm định Feature Leakage:** Số cột chứa kết quả đóng task hoặc nỗ lực tương lai (`Status`, `Resolution`, `Timespent`, `In_Progress_Minutes`, `PR_URL`, `Assignee_ID`, `Sprint_ID`...) | `12 / 30` cột chứa thông tin tương lai | **`0 / 28` cột (`0.00%`)** | ✅ **ĐẠT TUYỆT ĐỐI** |
| **8** | **Kiểm định Missingness trên các cột đầu vào cốt lõi:** Số giá trị `NULL` ở `Clean_Title`, `Clean_Text`, `Clean_Type`, `Clean_Priority`, `Initial_Story_Point` | `172` dòng `NULL` ở `Description_Text` | **`0` giá trị `NULL`** (`Clean_Text` phủ kín `3,542 / 3,542` dòng) | ✅ **ĐẠT TUYỆT ĐỐI** |

---

## 2. Thẩm Định Ranh Giới Thời Gian Của `Chronological_Split` (Chống *Split Leakage*)

Để đảm bảo mô hình không bao giờ dùng dữ liệu ước lượng ở tương lai để huấn luyện dự báo cho quá khứ, toàn bộ 3,542 dòng trong `springxd_cleaned_dataset.csv` đã được sắp xếp tăng dần theo `Real_Estimation_Date` và chia theo tỷ lệ **60% Train / 20% Val / 20% Test**. Kết quả kiểm tra mốc thời gian đầu - cuối của từng tập như sau:

| Tập dữ liệu (`Chronological_Split`) | Số lượng mẫu (`N = 3,542`) | Số lượng mẫu chuẩn `[0.5, 40.0]` (`N = 3,536`) | Mốc `Real_Estimation_Date` sớm nhất (`Min`) | Mốc `Real_Estimation_Date` muộn nhất (`Max`) | Kiểm định không chồng lấn thời gian (Zero Temporal Overlap) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`train` (60%)** | `2,125` | `2,120` | `2013-04-17 08:48:08` | `2014-10-24 13:29:52` | Tập gốc quá khứ |
| **`val` (20%)** | `708` | `708` | `2014-10-24 13:30:21` | `2015-04-30 13:36:53` | ✅ `Min(val) > Max(train)` *(Cách nhau +29 giây, 0% chồng lấn)* |
| **`test` (20%)** | `709` | `708` | `2015-05-01 11:15:00` | `2018-11-16 15:57:31` | ✅ `Min(test) > Max(val)` *(Cách nhau +21 giờ 38 phút, 0% chồng lấn)* |

---

## 3. Thẩm Định Cấu Trúc 28 Cột Của File `springxd_cleaned_dataset.csv`

Toàn bộ 28 cột có mặt trong [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv) đều đã được xác thực về nguồn gốc thời gian tại mốc `Real_Estimation_Date`:

| Nhóm thuộc tính | Danh sách các cột trong `springxd_cleaned_dataset.csv` | Số cột | Xác nhận tính an toàn (Leakage-Free Status) |
| :--- | :--- | :---: | :--- |
| **1. Định danh & Dấu vết thời gian** | `ID`, `Issue_Key`, `Project_ID`, `Creation_Date`, `Real_Estimation_Date`, `Estimation_Source`, `Creator_ID`, `Reporter_ID` | `8` cột | ✅ 100% có sẵn tại hoặc trước thời điểm ước lượng. |
| **2. Đặc trưng văn bản sạch** | `Clean_Title`, `Clean_Description`, `Clean_Text`, `Clean_Title_Word_Count`, `Clean_Desc_Word_Count`, `Has_Clean_Description` | `6` cột | ✅ Khôi phục đúng tại `Real_Estimation_Date`, đã gỡ bỏ ký tự bọc SQL. |
| **3. Đặc trưng siêu dữ liệu sạch** | `Clean_Type`, `Clean_Priority`, `Clean_Components`, `Has_Clean_Component` | `4` cột | ✅ Khôi phục đúng trạng thái phân loại tại `Real_Estimation_Date`. |
| **4. Cờ kiểm toán biến đổi (Audit Flags)** | `Title_Modified_After_Est`, `Desc_Modified_After_Est`, `Type_Modified_After_Est`, `Priority_Modified_After_Est`, `Component_Modified_After_Est`, `SP_Modified_After_Est` | `6` cột | 📌 Chỉ dùng để phân tích độ nhạy (Sensitivity Analysis) giữa nhóm có sửa và không sửa sau ước lượng. |
| **5. Nhãn mục tiêu & Chia tập** | `Initial_Story_Point`, `Is_Valid_Scale_SP`, `Is_GPT2SP_3526_Subset`, `Chronological_Split` | `4` cột | ✅ Nhãn mục tiêu gốc tại `Real_Estimation_Date` và nhãn chia tập theo thời gian. |

---

## 4. Thẩm Định Trực Tiếp Trên 5 Case History Điển Hình Trước Và Sau Khi Làm Sạch

Bảng dưới đây đối chiếu 5 bản ghi thực tế trích xuất từ `springxd_cleaned_dataset.csv` để xác nhận thuật toán đã khôi phục chính xác dữ liệu tại thời điểm ước lượng:

| Mã Issue (`Issue_Key`) | Vấn đề rò rỉ / bất thường ở dữ liệu gốc | Trạng thái ở bảng `Issue` gốc (`Final / Raw Snapshot`) | Trạng thái đã làm sạch trong `springxd_cleaned_dataset.csv` (`Planning-Time Snapshot`) |
| :---: | :--- | :--- | :--- |
| **`XD-3470`** | Người tạo điền số giả định `10,000,000,000` lúc mở ticket (`2015-09-12`) | `Estimation_Date`: `2015-09-12 18:40:25` (lệch `-1h`)<br>`From_String`: `10000000000` | `Real_Estimation_Date`: **`2015-09-22 03:21:10`** (thời điểm đội Scrum chấm điểm thật)<br>`Initial_Story_Point`: **`1.0`** |
| **`XD-3476`** | Người tạo điền số giả định `9,999,999` lúc mở ticket (`2015-09-19`) | `Estimation_Date`: `2015-09-19 02:56:45` (lệch `-1h`)<br>`From_String`: `9999999` | `Real_Estimation_Date`: **`2015-09-22 03:20:08`**<br>`Initial_Story_Point`: **`1.0`** |
| **`XD-2829`** | Lúc tạo (`03:55:25`) chưa có điểm (`From_String = NULL`), sửa `Description` cả trước và sau lúc chấm điểm | `Estimation_Date`: gán sai về `03:55:25`<br>`Description`: chứa nội dung sửa sau khi ước lượng | `Real_Estimation_Date`: **`2015-03-18 06:03:36`** (lúc gán `To_String = 1`)<br>`Clean_Description`: Khôi phục đúng bản mô tả tại `06:03:36` (`47` từ thay vì `72` từ ở bản cuối) |
| **`XD-3672`** | Đổi cả `Title` lẫn `Story_Point` (`3` $\rightarrow$ `1` $\rightarrow$ `2`) trong quá trình làm Sprint | `Title`: `\"...\"` (đã sửa đổi)<br>`Final Story_Point`: **`2.0`** | `Clean_Title`: Khôi phục bản gốc lúc `2015-11-02 15:34:40` (đã xóa dấu `\"`)<br>`Initial_Story_Point`: **`3.0`** |
| **`XD-3765`** | Rút gọn `Title` vào ngày `2017-03-22` (sau khi đã đóng task `Done` ngày `2017-03-21`) | `Title`: `\"Fix stream failover\"` | `Clean_Title`: **`Fix stream failover on YARN`** (khôi phục đúng tiêu đề nguyên bản lúc ước lượng `2017-03-21 16:54:44`) |

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc thông tin lưu trữ](01_data_scale_and_overview.md)**
2. 📋 **[Phần 2: Bảng dữ liệu đầy đủ & thống kê số lượng từng loại trong mỗi thuộc tính (`N = 3,542`)](02_attribute_breakdown_and_counts.md)**
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & giải pháp xử lý tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)**
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)** *(Tài liệu hiện tại)*
