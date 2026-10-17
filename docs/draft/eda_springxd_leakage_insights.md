# 📊 BÁO CÁO PHÂN TÍCH TOÀN DIỆN (EDA), XỬ LÝ BẤT THƯỜNG & THẨM ĐỊNH CLEAN DATA KHÔNG RÒ RỈ TRÊN DỰ ÁN SPRING XD (TAWOS v1.1)

> **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*  
> **Phạm vi dữ liệu:** Dự án **Spring XD (`Project_Key = 'XD'`, `Project_ID = 1`)** — Trích xuất từ `C:/tawos/tawos_eda.db` (TAWOS Dataset v1.1)  
> **Các tệp đầu ra trong `docs/draft/`:**  
> - **Notebook thực thi:** [`EDA_SpringXD_Leakage_Free.ipynb`](EDA_SpringXD_Leakage_Free.ipynb)  
> - **Bộ dữ liệu sạch (Clean Data):** [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv) *(3,542 dòng $\times$ 28 cột)*

---

## 📌 MỤC 1. GIỚI THIỆU QUY MÔ DỮ LIỆU & CẤU TRÚC THÔNG TIN LƯU TRỮ

### 1.1. Ý nghĩa và bối cảnh của dữ liệu Spring XD trong TAWOS v1.1
**Spring XD** (`Project_Key = 'XD'`, thuộc kho chứa Jira của **Spring Framework** tại `https://jira.spring.io/projects/XD/`) là một hệ thống mã nguồn mở quy mô lớn phục vụ xử lý dữ liệu lớn (Big Data ingestion, batch processing, stream analytics). Trong các nghiên cứu ước lượng nỗ lực Agile kinh điển như **Deep-SE (Choetkiertikul et al., 2019)** và **GPT2SP (Fu & Tantithamthavorn, 2023)**, Spring XD là dự án benchmark tiêu biểu nhất được sử dụng để đánh giá các mô hình học sâu.

Trong cơ sở dữ liệu quan hệ **TAWOS v1.1** (`C:/tawos/tawos_eda.db`), dữ liệu của dự án Spring XD không chỉ lưu trữ trạng thái cuối cùng của từng công việc (như các file CSV phẳng trước đây), mà còn lưu trữ **toàn bộ lịch sử biến đổi theo từng giây** của mọi thuộc tính kể từ lúc công việc được tạo ra (`2013-04-12`) đến lần cập nhật cuối cùng (`2018-11-20`).

### 1.2. Quy mô các bảng dữ liệu liên quan đến dự án Spring XD
Truy vấn trực tiếp từ `C:/tawos/tawos_eda.db` với `Project_ID = 1` ghi nhận tổng cộng **11 bảng quan hệ** lưu trữ các tầng thông tin khác nhau của dự án Spring XD:

| STT | Tên bảng trong CSDL | Số bản ghi của Spring XD | Giải thích ngắn gọn thông tin lưu trữ trong bảng |
| :-: | :--- | :---: | :--- |
| **1** | **`Project`** | `1` dự án | Hồ sơ dự án Spring XD (`ID = 1`, `Key = 'XD'`, mã trường Story Point trên Jira là `customfield_10142`). |
| **2** | **`Issue`** | `3,707` công việc | Bảng trung tâm lưu thông tin của từng ticket Jira (Tiêu đề, Mô tả, Loại, Độ ưu tiên, Trạng thái, Điểm Story Point, Thời gian tạo/ước lượng/đóng, Thời gian làm việc thực tế...). |
| **3** | **`Change_Log`** | `43,227` bản ghi<br>*(40,564 thuộc nhóm SP > 0)* | Nhật ký lịch sử lưu mọi thao tác chỉnh sửa trên từng Issue: trường nào bị sửa (`Field`), giá trị cũ (`From_String`), giá trị mới (`To_String`), người sửa (`Author_ID`) và thời điểm sửa (`Creation_Date`). |
| **4** | **`Component`** | `18` thành phần | Danh mục 18 phân hệ kỹ thuật của phần mềm Spring XD (như `Runtime`, `Stream Module`, `Batch`, `Hadoop`, `UI`, `CLI`...). |
| **5** | **`Issue_Component`** | `1,375` liên kết | Bảng trung gian (Many-to-Many) ánh xạ mỗi Issue thuộc về một hoặc nhiều `Component` kỹ thuật nào. |
| **6** | **`Sprint`** | `66` chu kỳ Sprint | Thông tin 66 Sprint của đội phát triển Spring XD (Tên Sprint, Trạng thái, Ngày bắt đầu, Ngày kết thúc, Ngày hoàn thành). |
| **7** | **`Version`** | `37` phiên bản | Danh sách các bản phát hành (Release Versions) của dự án (như `1.0.0.M1`, `1.1.0.RELEASE`, `1.3.2`...). |
| **8** | **`Fix_Version`** | `2,817` liên kết | Ánh xạ các phiên bản mà tại đó Issue được dự kiến hoặc đã được sửa lỗi/phát hành hoàn tất. |
| **9** | **`Affected_Version`** | `589` liên kết | Ánh xạ các phiên bản phần mềm bị ảnh hưởng bởi lỗi (Bug) được báo cáo trong Issue. |
| **10** | **`Issue_Link`** | `940` liên kết | Mối quan hệ phụ thuộc hai chiều giữa các Issue với nhau (như `Depends`, `Blocks`, `Duplicate`, `Relates`, `Supersedes`). |
| **11** | **`User`** | `189` thành viên | Danh sách mã định danh của các lập trình viên, người tạo ticket (`Creator`), người báo cáo (`Reporter`) và người được phân công (`Assignee`). |

### 1.3. Phân tầng quy mô công việc (`3,707` $\rightarrow$ `3,542` $\rightarrow$ `3,526` Issues)
- **Tổng số Issue của Spring XD trong TAWOS v1.1:** **`3,707` issues** (`XD-1` đến `XD-3769`).
- **Nhóm không có Story Point hợp lệ:** **`165` issues** (`4.45%`), bao gồm `163` issues có `Story_Point = 0` và `2` issues có `Story_Point = NULL`.
- **Quần thể có nhãn `Story_Point > 0` hợp lệ (Target Population):** **`3,542` issues** (`95.55%`), đi kèm **40,564 bản ghi `Change_Log`**.
- **Đối chiếu với con số `3,526` issues của bài báo GPT2SP (Fu, 2023) & Deep-SE (Choetkiertikul, 2019):** Tập dữ liệu CSV của Choetkiertikul được thu thập vào cuối tháng 03/2016 (dừng ở mã `XD-3753`, gồm đúng **3,526 issues**). Trong khi đó, TAWOS v1.1 thu thập dữ liệu đến tháng 11/2018 nên ghi nhận thêm đúng **16 issues mới hơn** (`XD-3754` đến `XD-3769`, tạo từ `2016-05-02` đến `2018-11-16`). Như vậy: $3,526 + 16 = \mathbf{3,542\text{ issues}}$.

---

## 📋 MỤC 2. BẢNG DỮ LIỆU ĐẦY ĐỦ & THỐNG KÊ SỐ LƯỢNG TỪNG LOẠI TRONG MỖI THUỘC TÍNH

### 2.1. Bảng kiểm kê đầy đủ 30 thuộc tính gốc của bảng `Issue`
Bảng dưới đây thống kê chi tiết toàn bộ 30 cột của bảng `Issue` trên cả toàn tập dự án (`N = 3,707`) và tập có chấm điểm Story Point (`N = 3,542`):

| STT | Tên thuộc tính (`Column`) | Kiểu dữ liệu | Số mẫu có dữ liệu (`N = 3,707`) | Số mẫu có dữ liệu (`N = 3,542`) | Số mẫu khuyết trên `3,542` (%) | Số giá trị phân biệt (`Unique`) | Mô tả chi tiết thuộc tính |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `ID` | `int64` | 3,707 | 3,542 | 0 (`0.00%`) | 3,542 | Khóa chính tự tăng trong CSDL TAWOS (`65` $\rightarrow$ `3773`). |
| **2** | `Jira_ID` | `int64` | 3,707 | 3,542 | 0 (`0.00%`) | 3,542 | ID nội bộ của ticket trên máy chủ Jira Spring. |
| **3** | `Issue_Key` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 3,542 | Mã định danh công việc hiển thị trên Jira (`XD-1` $\rightarrow$ `XD-3769`). |
| **4** | `URL` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 3,542 | Đường dẫn REST API gốc của ticket trên Jira. |
| **5** | `Title` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 3,477 | Tiêu đề tóm tắt công việc (`summary`). |
| **6** | `Description` | `object (str)` | 3,520 | 3,373 | 169 (`4.77%`) | 3,341 | Nội dung mô tả đầy đủ (bao gồm cả text và đoạn mã). |
| **7** | `Description_Text` | `object (str)` | 3,517 | 3,370 | 172 (`4.86%`) | 3,337 | Phần văn bản tự nhiên tách ra từ `Description`. |
| **8** | `Description_Code` | `object (str)` | 665 | 637 | 2,905 (`82.02%`) | 634 | Các đoạn mã nguồn/log tách ra từ `Description`. |
| **9** | `Type` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 5 | Phân loại công việc (`Story`, `Bug`, `Improvement`, `Technical task`, `Epic`). |
| **10** | `Priority` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 5 | Mức độ ưu tiên (`Minor`, `Major`, `Critical`, `Blocker`, `Trivial`). |
| **11** | `Status` | `object (str)` | 3,707 | 3,542 | 0 (`0.00%`) | 4 | Trạng thái hiện tại của ticket (`Done`, `To Do`, `In Progress`, `In PR`). |
| **12** | `Resolution` | `object (str)` | 3,046 | 2,940 | 602 (`17.00%`) | 9 (+ NULL) | Kết quả đóng công việc (`Complete`, `Invalid`, `Duplicate`, `Won't Fix`...). |
| **13** | `Creation_Date` | `datetime str` | 3,707 | 3,542 | 0 (`0.00%`) | 3,537 | Thời điểm khởi tạo công việc trên Jira. |
| **14** | `Estimation_Date` | `datetime str` | 3,705 | 3,542 | 0 (`0.00%`) | 3,537 | Thời điểm ước lượng ghi nhận sẵn trong bảng `Issue`. |
| **15** | `Resolution_Date` | `datetime str` | 3,046 | 2,940 | 602 (`17.00%`) | 2,877 | Thời điểm công việc được giải quyết hoàn tất. |
| **16** | `Last_Updated` | `datetime str` | 3,707 | 3,542 | 0 (`0.00%`) | 2,520 | Thời điểm chỉnh sửa cuối cùng của ticket. |
| **17** | `Story_Point` | `float64` | 3,705 | 3,542 | 0 (`0.00%`) | 25 | Điểm nỗ lực cuối cùng lưu trên bảng `Issue`. |
| **18** | `Timespent` | `float64` | 2 | 2 | 3,540 (`99.94%`) | 2 | Thời gian log work trực tiếp trên Jira (hầu hết để trống). |
| **19** | `In_Progress_Minutes` | `float64` | 3,707 | 3,542 | 0 (`0.00%`) | 1,462 | Tổng số phút ticket ở trạng thái `In Progress`. |
| **20** | `Total_Effort_Minutes` | `float64` | 3,707 | 3,542 | 0 (`0.00%`) | 1,640 | Tổng thời gian nỗ lực thực tế tính bằng phút. |
| **21** | `Resolution_Time_Minutes` | `float64` | 3,707 | 3,542 | 0 (`0.00%`) | 2,716 | Tổng số phút từ lúc mở đến lúc đóng ticket. |
| **22** | `Title_Changed_After_Estimation` | `int64 (0/1)` | 3,707 | 3,542 | 0 (`0.00%`) | 2 | Cờ báo tiêu đề thay đổi sau ước lượng trong bảng `Issue`. |
| **23** | `Description_Changed_After_Estimation` | `int64 (0/1)` | 3,707 | 3,542 | 0 (`0.00%`) | 1 (`chỉ có 0`) | Cờ báo mô tả thay đổi sau ước lượng (bị lỗi toàn bộ bằng `0`). |
| **24** | `Story_Point_Changed_After_Estimation` | `int64 (0/1)` | 3,707 | 3,542 | 0 (`0.00%`) | 2 | Cờ báo điểm Story Point thay đổi sau ước lượng. |
| **25** | `Pull_Request_URL` | `object (str)` | 621 | 617 | 2,925 (`82.58%`) | 602 | Đường dẫn Pull Request trên GitHub gắn với ticket. |
| **26** | `Creator_ID` | `int64` | 3,707 | 3,542 | 0 (`0.00%`) | 146 | ID người tạo ticket. |
| **27** | `Reporter_ID` | `int64` | 3,707 | 3,542 | 0 (`0.00%`) | 146 | ID người đứng tên báo cáo ticket. |
| **28** | `Assignee_ID` | `float64 (ID)` | 2,608 | 2,550 | 992 (`28.01%`) | 31 (+ NULL) | ID lập trình viên được phân công xử lý ticket. |
| **29** | `Project_ID` | `int64` | 3,707 | 3,542 | 0 (`0.00%`) | 1 (`ID = 1`) | Khóa ngoại trỏ về bảng `Project` (`Spring XD`). |
| **30** | `Sprint_ID` | `float64 (ID)` | 2,156 | 2,114 | 1,428 (`40.32%`) | 66 (+ NULL) | Khóa ngoại trỏ về bảng `Sprint`. |

---

### 2.2. Thống kê chi tiết số lượng từng loại giá trị (Category Counts) trong mỗi thuộc tính

#### A. Thuộc tính `Type` (Loại công việc — 5 phân loại)
| Loại công việc (`Type`) | Toàn bộ Spring XD (`N = 3,707`) | Tập có `SP > 0` ở trạng thái cuối (`N = 3,542`) | Tập có `SP > 0` khôi phục tại lúc ước lượng (`Clean_Type`) | Nhận xét sự dịch chuyển |
| :--- | :---: | :---: | :---: | :--- |
| **`Story`** (User Story) | `2,593` (`69.95%`) | `2,535` (`71.57%`) | **`2,621` (`74.00%`)** | Có 86 ticket ban đầu lúc ước lượng là `Story` nhưng về sau bị đội đổi thành `Improvement` hoặc `Bug`. |
| **`Bug`** (Lỗi phần mềm) | `610` (`16.46%`) | `594` (`16.77%`) | **`576` (`16.26%`)** | Tăng từ 576 lên 594 sau quá trình kiểm thử/triển khai. |
| **`Improvement`** (Cải tiến) | `309` (`8.34%`) | `294` (`8.30%`) | **`218` (`6.15%`)** | Tăng từ 218 lên 294 do chuyển đổi từ `Story` sang sau khi ước lượng. |
| **`Technical task`** (Tác vụ kỹ thuật) | `86` (`2.32%`) | `73` (`2.06%`) | **`73` (`2.06%`)** | Giữ nguyên số lượng giữa lúc ước lượng và lúc đóng. |
| **`Epic`** (Chức năng lớn) | `109` (`2.94%`) | `46` (`1.30%`) | **`54` (`1.52%`)** | Hầu hết Epic không chấm SP (`63/109` có `SP = 0`); 8 Epic lúc đầu sau đó được hạ xuống thành `Story`. |
| **Tổng cộng** | **`3,707` (`100%`)** | **`3,542` (`100%`)** | **`3,542` (`100%`)** | Tổng cộng có **255 issues (`7.20%`)** bị đổi `Type` sau khi ước lượng. |

#### B. Thuộc tính `Priority` (Mức độ ưu tiên — 5 phân loại)
| Mức độ ưu tiên (`Priority`) | Toàn bộ Spring XD (`N = 3,707`) | Tập có `SP > 0` ở trạng thái cuối (`N = 3,542`) | Tập có `SP > 0` khôi phục tại lúc ước lượng (`Clean_Priority`) | Nhận xét sự dịch chuyển |
| :--- | :---: | :---: | :---: | :--- |
| **`Minor`** | `3,156` (`85.14%`) | `3,012` (`85.04%`) | **`3,116` (`87.97%`)** | Mặc định trên Jira của Spring XD là `Minor`; 104 ticket `Minor` về sau được nâng độ ưu tiên lên `Major`/`Critical`. |
| **`Major`** | `418` (`11.28%`) | `401` (`11.32%`) | **`317` (`8.95%`)** | Tăng thêm 84 ticket sau khi đi vào thực hiện Sprint. |
| **`Critical`** | `73` (`1.97%`) | `72` (`2.03%`) | **`60` (`1.69%`)** | Tăng thêm 12 ticket do phát hiện mức độ nghiêm trọng trong lúc sửa lỗi. |
| **`Blocker`** | `36` (`0.97%`) | `36` (`1.02%`) | **`36` (`1.02%`)** | Ổn định ở mức 36 ticket. |
| **`Trivial`** | `24` (`0.65%`) | `21` (`0.59%`) | **`13` (`0.37%`)** | Có 8 ticket được hạ xuống mức `Trivial` sau khi ước lượng. |
| **Tổng cộng** | **`3,707` (`100%`)** | **`3,542` (`100%`)** | **`3,542` (`100%`)** | Tổng cộng có **137 issues (`3.87%`)** bị đổi `Priority` sau khi ước lượng. |

#### C. Thuộc tính `Status` (Trạng thái công việc — 4 phân loại) & `Resolution` (Kết quả giải quyết — 10 phân loại)
| Thuộc tính `Status` | Số lượng trên `3,707` | Số lượng trên `3,542` (`SP > 0`) | Thuộc tính `Resolution` | Số lượng trên `3,707` | Số lượng trên `3,542` (`SP > 0`) |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **`Done`** (Đã đóng) | `3,046` (`82.17%`) | `2,940` (`83.00%`) | **`Complete`** (Hoàn thành) | `2,433` (`65.63%`) | `2,372` (`66.97%`) |
| **`To Do`** (Chưa làm) | `637` (`17.18%`) | `578` (`16.32%`) | **`NULL`** (Chưa đóng / Đang mở) | `661` (`17.83%`) | `602` (`17.00%`) |
| **`In Progress`** (Đang làm) | `20` (`0.54%`) | `20` (`0.56%`) | **`Invalid`** (Không hợp lệ) | `126` (`3.40%`) | `119` (`3.36%`) |
| **`In PR`** (Đang chờ duyệt PR) | `4` (`0.11%`) | `4` (`0.11%`) | **`Duplicate`** (Trùng lặp) | `133` (`3.59%`) | `118` (`3.33%`) |
| — | — | — | **`Won't Fix`** (Không sửa) | `129` (`3.48%`) | `114` (`3.22%`) |
| — | — | — | **`Deferred`** (Hoãn lại) | `111` (`2.99%`) | `110` (`3.11%`) |
| — | — | — | **`Works as Designed`** (Đúng thiết kế) | `46` (`1.24%`) | `42` (`1.19%`) |
| — | — | — | **`Fixed`** (Đã vá lỗi) | `39` (`1.05%`) | `36` (`1.02%`) |
| — | — | — | **`Cannot Reproduce`** (Không tái hiện được) | `20` (`0.54%`) | `20` (`0.56%`) |
| — | — | — | **`Incomplete`** (Chưa hoàn chỉnh) | `9` (`0.24%`) | `9` (`0.25%`) |
| **Tổng cộng** | **`3,707` (`100%`)** | **`3,542` (`100%`)** | **Tổng cộng** | **`3,707` (`100%`)** | **`3,542` (`100%`)** |

#### D. Thuộc tính `Story_Point` (Đầy đủ 27 mức điểm từ `NULL`, `0.0` đến `2567.0`)
| Giá trị điểm (`Story Point`) | Toàn bộ bảng `Issue` (`N = 3,707`) | `Final Story_Point` (`N = 3,542`) | `Initial_Story_Point` đã khôi phục (`N = 3,542`) | Phân loại theo thang điểm của dự án Spring XD |
| :---: | :---: | :---: | :---: | :--- |
| **`NULL`** | `2` (`0.05%`) | `0` | `0` | ❌ Không có nhãn (Loại bỏ khỏi tập mô hình hóa) |
| **`0.0`** | `163` (`4.40%`) | `0` | `0` | ❌ Không ước lượng / Điểm `0` (Loại bỏ khỏi tập mô hình hóa) |
| **`0.2`** | `1` (`0.03%`) | `1` (`0.03%`) | `0` *(Khôi phục về `0.5`)* | ⚠️ `XD-1970` ban đầu ước lượng `0.5`, sau đó hạ xuống `0.2` |
| **`0.5`** | `0` (`0.00%`) | `0` (`0.00%`) | **`1` (`0.03%`)** | ✅ Điểm Fibonacci nửa đơn vị hợp lệ (`XD-1970`) |
| **`1.0`** | `826` (`22.28%`) | `826` (`23.32%`) | **`805` (`22.73%`)** | ✅ Mức điểm phổ biến số 1 (Thang chuẩn Fibonacci) |
| **`2.0`** | `639` (`17.24%`) | `639` (`18.04%`) | **`651` (`18.38%`)** | ✅ Mức điểm phổ biến số 3 (Thang chuẩn Fibonacci) |
| **`3.0`** | `755` (`20.37%`) | `755` (`21.32%`) | **`754` (`21.29%`)** | ✅ Mức điểm phổ biến số 2 (Thang chuẩn Fibonacci) |
| **`4.0`** | `211` (`5.69%`) | `211` (`5.96%`) | **`221` (`6.24%`)** | ✅ Mức điểm trung gian hợp lệ |
| **`5.0`** | `572` (`15.43%`) | `572` (`16.15%`) | **`570` (`16.09%`)** | ✅ Mức điểm phổ biến số 4 (Thang chuẩn Fibonacci) |
| **`6.0`** | `27` (`0.73%`) | `27` (`0.76%`) | **`29` (`0.82%`)** | ✅ Mức điểm trung gian hợp lệ |
| **`7.0`** | `3` (`0.08%`) | `3` (`0.08%`) | **`3` (`0.08%`)** | ✅ Mức điểm trung gian hợp lệ |
| **`8.0`** | `394` (`10.63%`) | `394` (`11.12%`) | **`394` (`11.12%`)** | ✅ Mức điểm phổ biến số 5 (Thang chuẩn Fibonacci) |
| **`9.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`1` (`0.03%`)** | ✅ Mức điểm hợp lệ |
| **`10.0`** | `45` (`1.21%`) | `45` (`1.27%`) | **`49` (`1.38%`)** | ✅ Mức điểm hợp lệ |
| **`12.0`** | `5` (`0.13%`) | `5` (`0.14%`) | **`5` (`0.14%`)** | ✅ Mức điểm hợp lệ |
| **`13.0`** | `5` (`0.13%`) | `5` (`0.14%`) | **`3` (`0.08%`)** | ✅ Mức điểm chuẩn Fibonacci |
| **`14.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`0`** | ✅ Ban đầu chấm ở mức chuẩn, sau điều chỉnh thành `14.0` |
| **`15.0`** | `2` (`0.05%`) | `2` (`0.06%`) | **`3` (`0.08%`)** | ✅ Mức điểm hợp lệ |
| **`16.0`** | `18` (`0.49%`) | `18` (`0.51%`) | **`15` (`0.42%`)** | ✅ Mức điểm hợp lệ |
| **`20.0`** | `17` (`0.46%`) | `17` (`0.48%`) | **`18` (`0.51%`)** | ✅ Mức điểm chuẩn Planning Poker |
| **`21.0`** | `7` (`0.19%`) | `7` (`0.20%`) | **`7` (`0.20%`)** | ✅ Mức điểm chuẩn Fibonacci |
| **`24.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`0`** | ✅ Ban đầu chấm `16.0`, sau điều chỉnh thành `24.0` |
| **`30.0`** | `0` (`0.00%`) | `0` (`0.00%`) | **`1` (`0.03%`)** | ✅ Ban đầu chấm `30.0`, sau điều chỉnh giảm xuống |
| **`32.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`1` (`0.03%`)** | ✅ Mức điểm hợp lệ |
| **`40.0`** | `5` (`0.13%`) | `5` (`0.14%`) | **`5` (`0.14%`)** | ✅ Ngưỡng trần chuẩn của thẻ bài Planning Poker (`40.0`) |
| **`50.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`1` (`0.03%`)** | ⚠️ Ngoại lệ: `XD-836` (`Type = Epic`, đóng `Duplicate`, gắn cờ `Is_Valid_Scale_SP = 0`) |
| **`80.0`** | `2` (`0.05%`) | `2` (`0.06%`) | **`2` (`0.06%`)** | ⚠️ Ngoại lệ: `XD-92` & `XD-1141` (`Type = Epic`, gắn cờ `Is_Valid_Scale_SP = 0`) |
| **`100.0`** | `2` (`0.05%`) | `2` (`0.06%`) | **`2` (`0.06%`)** | ⚠️ Ngoại lệ: `XD-996` (`Epic`) & `XD-3562` (`To Do`, gắn cờ `Is_Valid_Scale_SP = 0`) |
| **`2567.0`** | `1` (`0.03%`) | `1` (`0.03%`) | **`1` (`0.03%`)** | 🚨 Điểm rác: `XD-2602` (`Works as Designed`, gắn cờ `Is_Valid_Scale_SP = 0`) |
| **Tổng cộng** | **`3,707` (`100%`)** | **`3,542` (`100%`)** | **`3,542` (`100%`)** | **`3,536 / 3,542` mẫu (`99.83%`) nằm gọn trong miền chuẩn `[0.5, 40.0]`** |

#### E. Thuộc tính `Component` (Đầy đủ 18 thành phần hệ thống của Spring XD)
| STT | Tên `Component` | Số Issue trên `3,707` | Số Issue trên `3,542` (`SP > 0`) | STT | Tên `Component` | Số Issue trên `3,707` | Số Issue trên `3,542` (`SP > 0`) |
| :-: | :--- | :---: | :---: | :-: | :--- | :---: | :---: |
| **1** | `Runtime` | `277` | `264` | **10** | `Configuration` | `58` | `57` |
| **2** | `Stream Module` | `140` | `133` | **11** | `Acceptance Testing` | `54` | `54` |
| **3** | `Documentation` | `120` | `113` | **12** | `REST` | `40` | `39` |
| **4** | `Batch` | `107` | `103` | **13** | `Ingest` | `40` | `35` |
| **5** | `Packaging` | `106` | `106` | **14** | `Testing` | `33` | `33` |
| **6** | `Hadoop` | `105` | `92` | **15** | `YARN Runtime` | `28` | `27` |
| **7** | `UI` | `95` | `94` | **16** | `Performance Testing` | `18` | `18` |
| **8** | `CLI` | `77` | `69` | **17** | `DSL` | `14` | `12` |
| **9** | `Analytics` | `60` | `60` | **18** | `Export` | `3` | `3` |

---

## 🚨 MỤC 3. PHÁT HIỆN CÁC ĐIỂM BẤT THƯỜNG (ANOMALIES) CẦN GIẢI QUYẾT

Qua quá trình kiểm toán chéo giữa bảng `Issue` và `40,564` bản ghi `Change_Log` của dự án Spring XD, nhóm phát hiện **5 điểm bất thường nghiêm trọng** trong dữ liệu thô:

### 3.1. Bất thường 1: Ký tự nháy kép dư thừa từ SQL Dump (`\"...\"` và `\"\"\"...\"\"\"`) gây rò rỉ định dạng
- **Mô tả bất thường:** Trong bảng `Issue` của `tawos_eda.db`, toàn bộ 100% giá trị cột `Title` bị bọc bởi cặp ký tự `\"...\"` (ví dụ: `\"How do I make a job restartable in spring xd\"`), cột `Description` bị bọc bởi `\"...\"`, và cột `Description_Text` bị bọc bởi 3 cặp `\"\"\"...\"\"\"`. Ngược lại, trong bảng `Change_Log`, các cột `From_String` và `To_String` lưu văn bản thuần không có dấu nháy bọc ngoài.
- **Nguy cơ nếu không xử lý:** Khi khôi phục văn bản lúc ước lượng, những issue lấy từ `Change_Log` sẽ không có `\"`, còn những issue giữ nguyên từ bảng `Issue` lại có `\"` ở đầu câu. Mô hình học máy sẽ học vẹt ký tự `\"` này như một tín hiệu rò rỉ nhân tạo (*Synthetic Format Leakage*).

### 3.2. Bất thường 2: Cột cờ `Description_Changed_After_Estimation` trong bảng `Issue` bị lỗi bằng `0` toàn bộ
- **Mô tả bất thường:** Trong bảng `Issue`, cột `Description_Changed_After_Estimation` có giá trị `0` trên cả `3,707 / 3,707` dòng (`100%`).
- **Đối chiếu thực tế từ `Change_Log`:** Truy vấn bảng `Change_Log` với `Field = 'description'` chứng minh có tới **581 công việc** (`576` công việc sau khi trừ các lần sửa trùng nội dung) bị thay đổi mô tả sau khi đã ước lượng Story Point với **886 lượt chỉnh sửa**. Điều này khẳng định không thể tin tưởng cột cờ có sẵn mà phải tự viết thuật toán truy vết từ `Change_Log`.

### 3.3. Bất thường 3: Cột `Issue.Estimation_Date` bị gán cứng theo `Creation_Date` và lệch múi giờ `-1.00 giờ`
- **Mô tả bất thường:** Kiểm tra hiệu số `Issue.Estimation_Date - Issue.Creation_Date` trên 3,542 công việc của Spring XD cho thấy:
  - **2,442 công việc (`68.94%`)** có `Estimation_Date` **sớm hơn `Creation_Date` đúng `-1.00 giờ`** (vô lý về mặt thời gian vật lý do lỗi lệch múi giờ DST/BST khi công cụ của TAWOS sinh dữ liệu).
  - **1,100 công việc (`31.06%`)** có `Estimation_Date == Creation_Date`.
  - **0 công việc (`0.00%`)** có `Estimation_Date > Creation_Date`, ngay cả khi công việc đó lúc mới tạo chưa hề có điểm (`From_String = NULL` hoặc `0`) và chỉ được gán điểm nhiều ngày sau đó trong `Change_Log`!

### 3.4. Bất thường 4: Điểm giả định / Placeholder (`10000000000`, `9999999`, `1000`, `444`, `100`, `0`) và nhãn nhiễu (`2567.0`)
- **Mô tả bất thường:**
  1. Có **89 công việc** khi mới tạo trên Jira chưa có điểm thực sự: trong đó `23` mẫu để `NULL`, `47` mẫu điền `0`, và `19` mẫu bị người tạo ticket điền các con số giả định khổng lồ hoặc ngoài thang đo để đánh dấu "chưa ước lượng" (như `XD-3470` điền `10000000000`, `XD-3476` điền `9999999`, `XD-3474` & `XD-3475` điền `999999`, `XD-2731` điền `1000`, `XD-3710` điền `610`, `XD-2974` điền `444`, `XD-3713` điền `233`, `XD-3712` điền `111`, `XD-1584` điền `100`, `XD-2675` điền `-1`, `XD-2580` điền `0.01`), sau đó đội Scrum mới vào thay thế bằng điểm thật (`1, 2, 3, 5, 8`) trong `Change_Log`. Nếu lấy mù quáng `From_String > 0` của lần đổi đầu tiên làm `Initial_Story_Point`, giá trị trung bình của nhãn sẽ vọt lên **2.82 triệu điểm**!
  2. Có **6 công việc (`0.17%`)** giữ nguyên điểm dị biệt ngoài thang đo chuẩn `[0.5, 40.0]` cho đến cuối: gồm 1 ticket lỗi `XD-2602` (`Story_Point = 2567.0`, đóng với lý do `Works as Designed`), 1 ticket `XD-3562` (`Story_Point = 100.0`, trạng thái `To Do` chưa từng được làm), và 4 Epic lớn (`XD-92`, `XD-836`, `XD-996`, `XD-1141` có điểm `50, 80, 100`).

### 3.5. Bất thường 5: Rò rỉ thông tin tương lai (*Temporal Leakage*) diện rộng sau thời điểm ước lượng
Sau mốc `Real_Estimation_Date`, hàng loạt thuộc tính bị cập nhật thông tin phát sinh trong quá trình lập trình và đóng công việc:
- **Các thuộc tính kết quả/tiến độ bị thay đổi sau ước lượng:** `status` (`83.37%` issues), `resolution` (`82.38%`), `Fix Version` (`75.24%`), `Rank` (`69.93%`), `Workflow` (`66.94%`), `Sprint` (`63.55%`), `assignee` (`50.51%`), `Pull Request URL` (`14.85%`), `Time Spent` (`7.14%`).
- **Các thuộc tính đầu vào hợp lệ nhưng bị sửa đổi sau ước lượng:** `Title` (`594` issues — `16.77%`), `Description` (`576` issues — `16.26%`), `Type` (`255` issues — `7.20%`), `Component` (`252` issues — `7.11%`), `Priority` (`137` issues — `3.87%`), và nhãn `Story_Point` (`411` issues — `11.60%`).

---

## 🛠️ MỤC 4. CÁC HƯỚNG ĐÃ XỬ LÝ ĐỂ TẠO RA CLEAN DATA (`springxd_cleaned_dataset.csv`)

Để giải quyết triệt để cả 5 nhóm bất thường nêu trên, quy trình làm sạch trong [`EDA_SpringXD_Leakage_Free.ipynb`](EDA_SpringXD_Leakage_Free.ipynb) đã thực thi **5 bước xử lý chuẩn hóa**:

1. **Hướng xử lý 1 — Cô lập quần thể có nhãn và chuẩn hóa định dạng văn bản (`strip_sql_quotes`):**
   - Lọc bỏ `165` công việc không có điểm hợp lệ (`Story_Point = 0` hoặc `NULL`), giữ lại `3,542` công việc có `Story_Point > 0`.
   - Áp dụng hàm `strip_sql_quotes()` cắt bỏ hoàn toàn các ký tự nháy kép bọc ngoài (`\"` và `\"\"\"`) trên `Title`, `Description` và `Description_Text`, đưa định dạng văn bản của bảng `Issue` về đồng nhất 100% với bảng `Change_Log`.

2. **Hướng xử lý 2 — Thuật toán khôi phục `Real_Estimation_Date` và `Initial_Story_Point` theo miền hợp lệ `[0.5, 40.0]`:**
   - **Trường hợp 1 (`Set_At_Creation_Unchanged` — `3,051` issues, `86.14%`):** Công việc được gán điểm hợp lệ ngay lúc tạo và không thay đổi về sau $\rightarrow$ `Real_Estimation_Date = Creation_Date` (đã loại bỏ hoàn toàn lỗi lệch `-1.00 giờ`), `Initial_Story_Point = Story_Point`.
   - **Trường hợp 2 (`Set_At_Creation_Later_Revised` — `402` issues, `11.35%`):** Công việc có bản ghi thay đổi `Story Points` trong `Change_Log` mà giá trị ban đầu `From_String` đã là một điểm hợp lệ trong `[0.5, 40.0]` $\rightarrow$ Công việc đã được ước lượng ngay lúc tạo với `Real_Estimation_Date = Creation_Date` và nhãn gốc được khôi phục về `Initial_Story_Point = float(From_String)`.
   - **Trường hợp 3 (`Estimated_Later_In_ChangeLog` — `89` issues, `2.51%`):** Công việc lúc mới tạo có `From_String` là `NULL`, `0`, hoặc số giả định ngoài thang đo (`10000000000`, `9999999`, `1000`, `444`, `100`, `-1`, `0.01`...) $\rightarrow$ Công việc chưa được ước lượng lúc tạo; thuật toán quét chuỗi `Change_Log` để tìm bản ghi đầu tiên gán `To_String` hợp lệ trong `[0.5, 40.0]`, đặt `Real_Estimation_Date = max(Creation_Date, Change_Log.Creation_Date)` và `Initial_Story_Point = float(To_String)`.

3. **Hướng xử lý 3 — Tái dựng trạng thái lịch sử (`Historical State Reconstruction`) tại đúng `Real_Estimation_Date`:**
   - Với `Clean_Title`, `Clean_Description`, `Clean_Type`, `Clean_Priority`: Đối với mỗi công việc, lọc các bản ghi `Change_Log` có `Creation_Date > Real_Estimation_Date`. Nếu có sự thay đổi sau mốc ước lượng, khôi phục giá trị tại thời điểm ước lượng bằng `From_String` của bản ghi thay đổi đầu tiên diễn ra ngay sau `Real_Estimation_Date`; nếu không có thay đổi sau ước lượng, giữ nguyên giá trị đã làm sạch từ bảng `Issue`.
   - Với `Clean_Components`: Xuất phát từ tập Component cuối cùng trong bảng `Issue_Component`, duyệt ngược (reverse-replay) toàn bộ các bản ghi `Change_Log` (`Field = 'Component'`) có `Creation_Date > Real_Estimation_Date` theo thứ tự thời gian giảm dần (xóa `To_String` được thêm vào sau ước lượng, khôi phục `From_String` bị gỡ bỏ sau ước lượng) để tái dựng chính xác tập `Clean_Components` tại thời điểm ước lượng.

4. **Hướng xử lý 4 — Loại bỏ triệt để 12 thuộc tính rò rỉ tương lai:**
   - Cắt bỏ hoàn toàn khỏi tập dữ liệu sạch các cột: `Status`, `Resolution`, `Resolution_Date`, `Last_Updated`, `Story_Point` (điểm cuối), `Timespent`, `In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`, `Pull_Request_URL`, `Description_Code`, `Assignee_ID`, và `Sprint_ID`.

5. **Hướng xử lý 5 — Gắn cờ kiểm soát ngoại lệ và chia tập theo thời gian (`Chronological_Split`):**
   - Tạo cột `Is_Valid_Scale_SP` (`1` cho `3,536` mẫu nằm trong thang điểm chuẩn `[0.5, 40.0]`; `0` cho `6` mẫu ngoại lệ `50, 80, 100, 2567`).
   - Tạo cột `Is_GPT2SP_3526_Subset` (`1` cho đúng `3,526` mẫu `XD-1` $\rightarrow$ `XD-3753` của bài báo GPT2SP; `0` cho `16` mẫu mới hơn).
   - Sắp xếp toàn bộ dữ liệu tăng dần theo `Real_Estimation_Date` và chia tập `Chronological_Split` theo tỷ lệ chuẩn **60% Train (`2,125` mẫu) / 20% Val (`708` mẫu) / 20% Test (`709` mẫu)**.

---

## ✅ MỤC 5. THẨM ĐỊNH LẠI CLEAN DATA (ZERO-LEAKAGE VERIFICATION AUDIT)

Để chứng minh bộ dữ liệu đầu ra [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv) hoàn toàn sạch và **không còn bất kỳ rò rỉ dữ liệu nào**, nhóm thực hiện 4 bài kiểm tra thẩm định độc lập dưới đây:

### 5.1. Kiểm định 1: Bảng đối chiếu chỉ số trước và sau khi làm sạch (`Raw Final Snapshot` vs `Clean Data`)
| Tiêu chí thẩm định trên Spring XD | Trước khi xử lý (`Raw Final Snapshot`) | Sau khi xử lý (`springxd_cleaned_dataset.csv`) | Kết luận thẩm định |
| :--- | :---: | :---: | :--- |
| **1. Tỷ lệ dòng còn chứa ký tự bọc SQL (`\"` hoặc `\"\"\"`)** | `100.00%` (`3,542 / 3,542` dòng) | **`0.00%` (`0 / 3,542` dòng)** | ✅ Đã triệt tiêu 100% *Synthetic Format Leakage* |
| **2. Số dòng có `Estimation_Date < Creation_Date` (Lỗi `-1h`)** | `68.94%` (`2,442 / 3,542` dòng) | **`0.00%` (`0 / 3,542` dòng)** | ✅ 100% `Real_Estimation_Date >= Creation_Date` |
| **3. Số dòng bị dính điểm giả định (`10^10`, `9999999`, `1000`, `444`...) khi lấy `From_String`** | `19` dòng (làm Mean SP vọt lên `2,825,244.50`) | **`0` dòng** (Mean SP chuẩn = **`3.1497`**) | ✅ Đã khôi phục đúng điểm thật khi đội Scrum ước lượng |
| **4. Số dòng chứa văn bản `Title` phát sinh sau ước lượng** | `594` dòng (`16.77%` bị rò rỉ) | **`0` dòng (`0.00%` bị rò rỉ)** | ✅ Đã khôi phục toàn bộ 594 `Clean_Title` về lúc ước lượng |
| **5. Số dòng chứa văn bản `Description` phát sinh sau ước lượng** | `576` dòng (`16.26%` bị rò rỉ) | **`0` dòng (`0.00%` bị rò rỉ)** | ✅ Đã khôi phục toàn bộ 576 `Clean_Description` về lúc ước lượng |
| **6. Số dòng chứa `Type` / `Priority` / `Component` bị sửa sau ước lượng** | `255` / `137` / `252` dòng bị rò rỉ | **`0` dòng (`0.00%` bị rò rỉ)** | ✅ Đã hoàn tác 100% về trạng thái tại `Real_Estimation_Date` |
| **7. Số cột chứa thông tin kết quả tương lai (`Status`, `Resolution`, `Timespent`, `PR_URL`...)** | `12` cột rò rỉ tương lai | **`0` cột (`Đã cắt bỏ 100%`)** | ✅ Hoàn toàn không còn *Feature Leakage* |
| **8. Số giá trị `NULL` ở các cột đặc trưng bắt buộc (`Clean_Title`, `Clean_Text`, `Clean_Type`, `Clean_Priority`, `Initial_Story_Point`)** | Có `NULL` ở `Description` (`172` dòng) | **`0` giá trị `NULL`** (`Clean_Text` đầy đủ `3,542 / 3,542` dòng) | ✅ Sẵn sàng nạp trực tiếp vào mọi mô hình ML/DL |

### 5.2. Kiểm định 2: Thẩm định tính bất khả xâm phạm về thời gian của `Chronological_Split` (Chống *Split Leakage*)
Kiểm tra mốc thời gian ước lượng thực tế (`Real_Estimation_Date`) trên 3 tập `train`, `val`, `test` trong `springxd_cleaned_dataset.csv`:

| Tập dữ liệu (`Chronological_Split`) | Số lượng mẫu (`N = 3,542`) | Tỷ lệ (%) | Mốc `Real_Estimation_Date` sớm nhất (`Min`) | Mốc `Real_Estimation_Date` muộn nhất (`Max`) | Kiểm tra chồng lấn thời gian (Temporal Overlap) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`train` (Tập huấn luyện)** | `2,125` | `59.99%` | `2013-04-17 08:48:08` | `2014-10-24 13:29:52` | — |
| **`val` (Tập kiểm định)** | `708` | `19.99%` | `2014-10-24 13:30:21` | `2015-04-30 13:36:53` | ✅ `Min(val) > Max(train)` *(Cách nhau +29 giây, 0% chồng lấn)* |
| **`test` (Tập kiểm thử)** | `709` | `20.02%` | `2015-05-01 11:15:00` | `2018-11-16 15:57:31` | ✅ `Min(test) > Max(val)` *(Cách nhau +21 giờ 38 phút, 0% chồng lấn)* |

> **Kết luận Kiểm định 2:** Ranh giới thời gian giữa `train` $\rightarrow$ `val` $\rightarrow$ `test` tách biệt tuyệt đối (`Max(Train) < Min(Val) < Max(Val) < Min(Test)`), đảm bảo **0% Split Leakage** (mô hình không bao giờ được nhìn thấy công việc ước lượng ở tương lai khi dự báo công việc ở quá khứ).

### 5.3. Kiểm định 3: Minh chứng trên các Case History thực tế đã được làm sạch trong `springxd_cleaned_dataset.csv`
Bảng dưới đây trích xuất 5 trường hợp thực tế từ `springxd_cleaned_dataset.csv` để chứng minh cơ chế khôi phục đã loại bỏ hoàn toàn rò rỉ dữ liệu và điểm giả định:

| Mã Issue (`Issue_Key`) | Loại bất thường trong dữ liệu gốc | Dữ liệu bị rò rỉ / bị nhiễu ở bản gốc (`Raw Issue Table`) | Dữ liệu sạch đã khôi phục trong `springxd_cleaned_dataset.csv` |
| :---: | :--- | :--- | :--- |
| **`XD-3470`** | Điền điểm giả định `10,000,000,000` lúc tạo ticket (`2015-09-12`) | `Estimation_Date`: `2015-09-12 18:40:25` (lệch -1h)<br>`From_String`: `10000000000` | `Real_Estimation_Date`: **`2015-09-22 03:21:10`** (thời điểm đội Scrum chấm điểm thật)<br>`Initial_Story_Point`: **`1.0`** |
| **`XD-3476`** | Điền điểm giả định `9,999,999` lúc tạo ticket (`2015-09-19`) | `Estimation_Date`: `2015-09-19 02:56:45` (lệch -1h)<br>`From_String`: `9999999` | `Real_Estimation_Date`: **`2015-09-22 03:20:08`**<br>`Initial_Story_Point`: **`1.0`** |
| **`XD-2829`** | Lúc tạo (`03:55:25`) chưa có SP (`From_String = NULL`), sửa `Description` trước và sau khi chấm điểm | `Estimation_Date` gán sai về `03:55:25`; `Description` cuối chứa nội dung đã sửa sau planning | `Real_Estimation_Date`: **`2015-03-18 06:03:36`** (lúc gán `To_String = 1`)<br>`Initial_Story_Point`: **`1.0`** |
| **`XD-3672`** | Đổi cả `Title` lẫn `Story_Point` (`3` $\rightarrow$ `1` $\rightarrow$ `2`) trong quá trình làm Sprint | `Title`: `\"...\"` đã sửa đổi;<br>`Final Story_Point`: **`2.0`** | `Clean_Title`: Khôi phục bản gốc lúc `2015-11-02 15:34:40`;<br>`Initial_Story_Point`: **`3.0`** |
| **`XD-3765`** | Rút gọn `Title` sau khi đã đóng task (`Done` / `Complete`) | `Final_Title`: `\"Fix stream failover\"` (đã bị sửa ngày `2017-03-22`, sau ngày đóng `2017-03-21`) | `Clean_Title`: **`Fix stream failover on YARN`** (khôi phục đúng tiêu đề lúc ước lượng `2017-03-21 16:54:44`) |
