# 📌 PHẦN 1. GIỚI THIỆU QUY MÔ DỮ LIỆU & CẤU TRÚC LƯU TRỮ (DỰ ÁN SPRING XD — TAWOS v1.1)

> **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*  
> **Nguồn dữ liệu gốc:** Cơ sở dữ liệu `C:/tawos/tawos_eda.db` — Dự án **Spring XD (`Project_Key = 'XD'`, `Project_ID = 1`)**

---

## 1. Giới Thiệu Ngắn Gọn Dữ Liệu Lưu Trữ Thông Tin Gì?

Dữ liệu của dự án **Spring XD** được thu thập từ hệ thống quản lý công việc Jira chính thức của Spring Framework (`https://jira.spring.io/projects/XD/`) trong giai đoạn từ tháng **04/2013 đến tháng 11/2018**. Mỗi bản ghi công việc đại diện cho một yêu cầu phát triển tính năng (*Story*), một lỗi phần mềm (*Bug*), hoặc một tác vụ kỹ thuật (*Improvement / Technical task*) mà đội phát triển Agile/Scrum cần ước lượng độ phức tạp bằng điểm **Story Point**.

Để phục vụ bài toán ước lượng Story Point và kiểm soát rò rỉ dữ liệu theo thời gian, toàn bộ dữ liệu của dự án Spring XD được trích xuất từ **2 bảng cốt lõi** trong `tawos_eda.db`:

1. **Bảng 1 — Bảng `Issue` (Bảng thông tin công việc ở trạng thái cuối):**
   - Mỗi dòng lưu thông tin của **1 công việc duy nhất** (gồm **30 cột thuộc tính**: mã định danh, tiêu đề, mô tả, phân loại, độ ưu tiên, trạng thái đóng/mở, mốc thời gian tạo/ước lượng/đóng, và điểm Story Point).
   - **Đặc điểm cần lưu ý:** Bảng `Issue` chỉ lưu **bản chụp cuối cùng (*Final Snapshot*)** của công việc tại thời điểm thu thập dữ liệu (sau khi phần lớn công việc đã làm xong và đóng lại).

2. **Bảng 2 — Bảng `Change_Log` (Bảng lịch sử chỉnh sửa theo thời gian):**
   - Lưu lại mọi sự kiện thay đổi diễn ra trên từng công việc của bảng `Issue` từ lúc mới tạo cho đến khi kết thúc.
   - Mỗi khi một lập trình viên sửa tiêu đề, sửa mô tả, đổi trạng thái hoặc đổi điểm Story Point của một công việc, Jira tự động ghi thêm **1 dòng lịch sử** vào bảng `Change_Log` (ghi rõ: mã công việc `Issue_ID`, tên trường bị sửa `Field`, giá trị cũ trước khi sửa `From_String`, giá trị mới sau khi sửa `To_String`, và thời điểm sửa `Creation_Date`).
   - Bảng `Change_Log` kết nối trực tiếp với bảng `Issue` thông qua khóa **`Issue.ID = Change_Log.Issue_ID`**.

*(Ngoài 2 bảng chính trên, CSDL có bảng danh mục phụ `Component` và `Issue_Component` dùng để tra cứu tên 18 thành phần hệ thống như `Runtime`, `Batch`, `UI` gắn với từng công việc).*

---

## 2. Quy Mô Dữ Liệu Nghiên Cứu Của Dự Án Spring XD (`N = 3,542`)

Trong bảng `Issue`, dự án Spring XD có tổng cộng `3,707` dòng công việc. Tuy nhiên, có `165` công việc không có điểm Story Point hợp lệ (`163` dòng có `Story_Point = 0` và `2` dòng có `Story_Point = NULL`). Vì bài toán của chúng ta là dự báo điểm Story Point nên các dòng không có điểm này bị loại bỏ hoàn toàn.

Quy mô tập dữ liệu có Story Point hợp lệ (`Story_Point > 0`) của dự án Spring XD như sau:

| Thành phần dữ liệu (trên tập có `Story_Point > 0`) | Số lượng bản ghi | Giải thích ý nghĩa |
| :--- | :---: | :--- |
| **Số lượng công việc hợp lệ trong bảng `Issue`** | **`3,542` dòng** | Mỗi dòng là 1 công việc có nhãn `Story_Point > 0` (chiếm `95.55%` dự án Spring XD), gồm **30 cột thuộc tính**. *(Trong đó `3,526` công việc từ `XD-1` đến `XD-3753` trùng khớp với tập dữ liệu của bài báo GPT2SP; `16` công việc từ `XD-3754` đến `XD-3769` là dữ liệu mới thu thập thêm trong TAWOS v1.1)*. |
| **Số lượng bản ghi lịch sử trong bảng `Change_Log`** | **`40,564` dòng** | Toàn bộ lịch sử chỉnh sửa của `3,542` công việc trên (trung bình mỗi công việc có **11.45 lần chỉnh sửa** trong vòng đời). |
| **Số lượng liên kết thành phần trong `Issue_Component`** | **`1,312` dòng** | Ánh xạ các công việc trong tập `3,542` vào 18 phân hệ kỹ thuật (`Component`) của Spring XD. |

---

## 3. Ví Dụ Mẫu 5 Dòng Dữ Liệu Thực Tế Trong Bảng `Issue` Và Bảng `Change_Log`

Để hình dung trực quan dữ liệu lưu trữ những gì và 2 bảng nối với nhau ra sao, dưới đây là **5 dòng dữ liệu mẫu đầu tiên** trích xuất trực tiếp từ bảng `Issue` (`ID` từ `65` đến `69`):

### 3.1. Ví dụ 5 dòng dữ liệu trong bảng `Issue` (Trích các cột tiêu biểu trong 30 cột)
| `ID` | `Issue_Key` | `Title` (Tiêu đề lưu trong bảng `Issue`) | `Description_Text` (Mô tả văn bản — rút gọn) | `Type` | `Priority` | `Status` | `Resolution` | `Creation_Date` | `Estimation_Date` | `Story_Point` | `Creator_ID` | `Assignee_ID` |
| :-: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`65`** | `XD-3768` | `\"How do I make a job restartable in spring xd\"` | `\"\"\"The jobs that appear under Executions section of Jobs in spring xd admin ui, has restart button disabled...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-07-10 13:41:25` | `2017-07-10 12:41:25` | **`1.0`** | `68` | `NULL` |
| **`66`** | `XD-3767` | `\"admin config timezone command does not work\"` | `\"\"\"Working with Spring-XD version 1.3.2.RELEASE Starting the server with {{xd-singlenode}} command...\"\"\"` | `Bug` | `Trivial` | `To Do` | `NULL` | `2017-06-26 16:26:27` | `2017-06-26 15:26:27` | **`1.0`** | `69` | `NULL` |
| **`67`** | `XD-3766` | `\"Module Upload command not pushing jar to all containers\"` | `\"\"\"My project 7 node cluster and in that 2 node are Admin containers and remaining are non admin containers...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-05-19 22:28:43` | `2017-05-19 21:28:43` | **`10.0`** | `70` | `NULL` |
| **`68`** | `XD-3765` | `\"Fix stream failover \"` | `\"\"\"See https://github.com/spring-projects/spring-xd/issues/1924\"\"\"` | `Story` | `Minor` | `Done` | `Complete` | `2017-03-21 16:54:44` | `2017-03-21 16:54:44` | **`8.0`** | `72` | `71` |
| **`69`** | `XD-3764` | `\"SpringXD Job is still executing even after forceful Server shutdown\"` | `\"\"\"I'm trying to run a Job on SpringXD and the job has 7 steps, When I reach step 4 i'm shutting down...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-03-06 20:01:41` | `2017-03-06 20:01:41` | **`5.0`** | `73` | `NULL` |

### 3.2. Ví dụ 5 dòng lịch sử tương ứng trong bảng `Change_Log`
Hãy nhìn vào công việc có **`ID = 68` (`XD-3765`)** ở bảng `Issue` phía trên: khi tra cứu `Issue_ID = 68` trong bảng `Change_Log`, ta thấy toàn bộ quá trình công việc này bị thay đổi theo thời gian như sau:

| `ID` (Mã Log) | `Issue_ID` *(Nối với `Issue.ID`)* | `Field` *(Tên trường bị sửa)* | `From_String` *(Giá trị cũ trước khi sửa)* | `To_String` *(Giá trị mới sau khi sửa)* | `Change_Type` | `Creation_Date` *(Thời điểm sửa)* | `Author_ID` |
| :-: | :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| `6` | **`68`** (`XD-3765`) | `Fix Version` | `NULL` | `1.3.2` | `FIX_VERSION` | `2017-03-21 16:54:56` | `72` |
| `7` | **`68`** (`XD-3765`) | `resolution` | `NULL` | `Complete` | `RESOLUTION` | `2017-03-21 16:55:23` | `72` |
| `8` | **`68`** (`XD-3765`) | `status` | `To Do` | `Done` | `STATUS` | `2017-03-21 16:55:23` | `72` |
| `9` | **`68`** (`XD-3765`) | `summary` | **`Fix stream failover on YARN`** | **`Fix stream failover `** | `SUMMARY` | `2017-03-22 18:27:01` | `72` |
| `43` | **`79`** (`XD-3754`) | `summary` | **`Composed Module Validated Too Early`** | **`Composed Module Child Module Validated Too Early`** | `SUMMARY` | `2016-05-02 23:14:39` | `82` |

> 💡 **Nhận xét trực quan từ dòng `ID = 9` của bảng `Change_Log`:**  
> Công việc `XD-3765` được tạo và ước lượng lúc `2017-03-21 16:54:44` với tiêu đề ban đầu là **`"Fix stream failover on YARN"`**. Đến ngày hôm sau (`2017-03-22 18:27:01`), người dùng mới sửa lại tiêu đề thành **`"Fix stream failover "`**. Vì bảng `Issue` chỉ lưu trạng thái cuối cùng nên cột `Title` của bảng `Issue` ghi nhận `"Fix stream failover "`, còn nhờ bảng `Change_Log` ta mới biết được tiêu đề gốc lúc ước lượng là `"Fix stream failover on YARN"`.

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc thông tin lưu trữ](01_data_scale_and_overview.md)** *(Tài liệu hiện tại)*
2. 📋 **[Phần 2: Thống kê 30 cột dữ liệu gốc & số lượng từng phân loại (`N = 3,542`)](02_attribute_breakdown_and_counts.md)**
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & cách giải quyết tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)**
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)**
5. 📏 **[RULE.md: Bộ quy tắc chuẩn hóa khi xử lý và viết báo cáo cho các dự án khác](RULE.md)**
