# 📌 PHẦN 1. GIỚI THIỆU QUY MÔ DỮ LIỆU & CẤU TRÚC 4 BẢNG LƯU TRỮ (DỰ ÁN SPRING XD — TAWOS v1.1)

> **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*  
> **Nguồn dữ liệu gốc:** Cơ sở dữ liệu `C:/tawos/tawos_eda.db` — Dự án **Spring XD (`Project_Key = 'XD'`, `Project_ID = 1`)**

---

## 1. Giới Thiệu Ngắn Gọn Dữ Liệu Lưu Trữ Thông Tin Gì?

Dữ liệu của dự án **Spring XD** được thu thập từ hệ thống quản lý công việc Jira chính thức của Spring Framework (`https://jira.spring.io/projects/XD/`) trong giai đoạn từ tháng **04/2013 đến tháng 11/2018**. Mỗi bản ghi công việc đại diện cho một yêu cầu phát triển tính năng (*Story*), một lỗi phần mềm (*Bug*), hoặc một tác vụ kỹ thuật (*Improvement / Technical task / Epic*) mà đội phát triển Agile/Scrum cần ước lượng độ phức tạp bằng điểm **Story Point**.

Để phục vụ bài toán ước lượng Story Point và kiểm soát rò rỉ dữ liệu theo thời gian, toàn bộ dữ liệu của dự án Spring XD được trích xuất từ **4 bảng dữ liệu gốc** trong `tawos_eda.db`:

1. **Bảng 1 — Bảng `Issue` (Bảng thông tin công việc ở trạng thái cuối — 30 cột):**
   - Mỗi dòng lưu thông tin của **1 công việc duy nhất** (gồm mã định danh, tiêu đề, mô tả, phân loại, độ ưu tiên, trạng thái đóng/mở, mốc thời gian tạo/ước lượng/đóng, và điểm Story Point).
   - **Đặc điểm cần lưu ý:** Bảng `Issue` chỉ lưu **bản chụp cuối cùng (*Final Snapshot*)** của công việc tại thời điểm thu thập dữ liệu (sau khi phần lớn công việc đã hoàn thành và đóng lại).

2. **Bảng 2 — Bảng `Change_Log` (Bảng nhật ký lịch sử chỉnh sửa — 10 cột):**
   - Lưu lại mọi sự kiện thay đổi diễn ra trên từng công việc của bảng `Issue` từ lúc mới tạo cho đến khi kết thúc.
   - Mỗi khi lập trình viên sửa tiêu đề, sửa mô tả, đổi trạng thái hoặc đổi điểm Story Point, Jira tự động ghi thêm **1 dòng lịch sử** vào bảng `Change_Log` (ghi rõ: mã công việc `Issue_ID`, tên thuộc tính bị sửa `Field`, giá trị cũ `From_String`, giá trị mới `To_String`, và thời điểm sửa `Creation_Date`).
   - Kết nối với bảng `Issue` theo quan hệ **1 - Nhiều** qua khóa **`Issue.ID = Change_Log.Issue_ID`**.

3. **Bảng 3 — Bảng `Issue_Component` (Bảng cầu nối công việc với phân hệ kỹ thuật — 2 cột):**
   - Vì **1 công việc có thể liên quan đến nhiều phân hệ kỹ thuật (`Component`) cùng lúc**, bảng trung gian này dùng để ánh xạ mã công việc (`Issue_ID`) sang mã phân hệ (`Component_ID`).

4. **Bảng 4 — Bảng `Component` (Bảng danh mục phân hệ kỹ thuật — 5 cột):**
   - Lưu danh sách tên và mô tả của **18 phân hệ kỹ thuật (module)** trong kiến trúc phần mềm Spring XD (như `Runtime`, `Stream Module`, `Batch`, `UI`, `Documentation`, `CLI`...).
   - Kết nối với `Issue_Component` qua khóa **`Issue_Component.Component_ID = Component.ID`**.

---

## 2. Quy Mô Dữ Liệu Nghiên Cứu Của Dự Án Spring XD (`N = 3,542`)

Trong bảng `Issue`, dự án Spring XD có tổng cộng `3,707` dòng công việc. Tuy nhiên, có `165` công việc không có điểm Story Point hợp lệ (`163` dòng có `Story_Point = 0` và `2` dòng có `Story_Point = NULL`). Vì bài toán của chúng ta là dự báo điểm Story Point nên các dòng không có điểm này bị loại bỏ ngay từ đầu.

Quy mô của **4 bảng dữ liệu gốc** tính trên tập công việc có Story Point hợp lệ (`Story_Point > 0`) như sau:

| STT | Tên bảng trong `tawos_eda.db` | Số cột thuộc tính | Số dòng bản ghi (trên tập `Story_Point > 0`) | Giải thích ý nghĩa & mối liên hệ |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **`Issue`** | `30` cột | **`3,542` dòng** | Mỗi dòng là 1 công việc có `Story_Point > 0` (chiếm `95.55%` dự án Spring XD). *(Trong đó `3,526` công việc từ `XD-1` đến `XD-3753` trùng khớp với tập dữ liệu của bài báo GPT2SP; `16` công việc từ `XD-3754` đến `XD-3769` là dữ liệu mới thu thập thêm trong TAWOS v1.1)*. |
| **2** | **`Change_Log`** | `10` cột | **`40,542` dòng** | Toàn bộ lịch sử chỉnh sửa của `3,542` công việc trên (có `3,456 / 3,542` công việc có lịch sử chỉnh sửa; trung bình mỗi công việc có **11.45 lần chỉnh sửa**). |
| **3** | **`Issue_Component`** | `2` cột | **`1,312` dòng** | Ánh xạ `1,196` công việc (trong tổng số `3,542` công việc) vào các phân hệ kỹ thuật (1 công việc có thể gắn từ 1 đến 4 phân hệ). |
| **4** | **`Component`** | `5` cột | **`18` dòng** | Danh mục 18 phân hệ kỹ thuật chính thức của dự án Spring XD (`Project_ID = 1`). |

---

## 3. Ví Dụ Mẫu 5 Dòng Dữ Liệu Thực Tế Ở Cả 4 Bảng

Để hình dung trực quan dữ liệu lưu trữ những gì và 4 bảng kết nối với nhau ra sao, dưới đây là **5 dòng dữ liệu mẫu thực tế** trích xuất trực tiếp từ từng bảng trong `tawos_eda.db`:

### 3.1. Bảng 1 — Ví dụ 5 dòng dữ liệu trong bảng `Issue` (Trích các cột tiêu biểu trong 30 cột)
| `ID` | `Issue_Key` | `Title` (Tiêu đề lưu trong bảng `Issue`) | `Description_Text` (Mô tả văn bản — rút gọn) | `Type` | `Priority` | `Status` | `Resolution` | `Creation_Date` | `Estimation_Date` | `Story_Point` | `Creator_ID` | `Assignee_ID` |
| :-: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`65`** | `XD-3768` | `\"How do I make a job restartable in spring xd\"` | `\"\"\"The jobs that appear under Executions section of Jobs in spring xd admin ui, has restart button disabled...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-07-10 13:41:25` | `2017-07-10 12:41:25` | **`1.0`** | `68` | `NULL` |
| **`66`** | `XD-3767` | `\"admin config timezone command does not work\"` | `\"\"\"Working with Spring-XD version 1.3.2.RELEASE Starting the server with {{xd-singlenode}} command...\"\"\"` | `Bug` | `Trivial` | `To Do` | `NULL` | `2017-06-26 16:26:27` | `2017-06-26 15:26:27` | **`1.0`** | `69` | `NULL` |
| **`67`** | `XD-3766` | `\"Module Upload command not pushing jar to all containers\"` | `\"\"\"My project 7 node cluster and in that 2 node are Admin containers and remaining are non admin containers...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-05-19 22:28:43` | `2017-05-19 21:28:43` | **`10.0`** | `70` | `NULL` |
| **`68`** | `XD-3765` | `\"Fix stream failover \"` | `\"\"\"See https://github.com/spring-projects/spring-xd/issues/1924\"\"\"` | `Story` | `Minor` | `Done` | `Complete` | `2017-03-21 16:54:44` | `2017-03-21 16:54:44` | **`8.0`** | `72` | `71` |
| **`69`** | `XD-3764` | `\"SpringXD Job is still executing even after forceful Server shutdown\"` | `\"\"\"I'm trying to run a Job on SpringXD and the job has 7 steps, When I reach step 4 i'm shutting down...\"\"\"` | `Bug` | `Major` | `To Do` | `NULL` | `2017-03-06 20:01:41` | `2017-03-06 20:01:41` | **`5.0`** | `73` | `NULL` |

---

### 3.2. Bảng 2 — Ví dụ 5 dòng dữ liệu trong bảng `Change_Log` (Nối với `Issue` qua `Issue_ID = Issue.ID`)
| `ID` | `Issue_ID` *(Nối với `Issue.ID`)* | `Field` *(Tên thuộc tính bị sửa)* | `From_Value` | `To_Value` | `From_String` *(Giá trị cũ trước khi sửa)* | `To_String` *(Giá trị mới sau khi sửa)* | `Change_Type` | `Creation_Date` *(Thời điểm sửa)* | `Author_ID` |
| :-: | :---: | :--- | :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| **`6`** | **`68`** (`XD-3765`) | `Fix Version` | `NULL` | `15482` | `NULL` | `1.3.2` | `OTHER` | `2017-03-21 16:54:56` | `72` |
| **`7`** | **`68`** (`XD-3765`) | `resolution` | `NULL` | `10000` | `NULL` | `Complete` | `STATUS` | `2017-03-21 16:55:23` | `72` |
| **`8`** | **`68`** (`XD-3765`) | `status` | `10000` | `10001` | `To Do` | `Done` | `STATUS` | `2017-03-21 16:55:23` | `72` |
| **`9`** | **`68`** (`XD-3765`) | `summary` | `NULL` | `NULL` | **`Fix stream failover on YARN`** | **`Fix stream failover `** | `DESCRIPTION` | `2017-03-22 18:27:01` | `72` |
| **`43`** | **`79`** (`XD-3754`) | `summary` | `NULL` | `NULL` | **`Composed Module Validated Too Early`** | **`Composed Module Child Module Validated Too Early`** | `DESCRIPTION` | `2016-05-02 23:14:39` | `82` |

> 💡 **Nhận xét từ dòng `ID = 9` của bảng `Change_Log`:** Công việc `XD-3765` (`Issue_ID = 68`) lúc mới tạo ngày `2017-03-21` có tiêu đề gốc là **`"Fix stream failover on YARN"`**, nhưng đến ngày `2017-03-22` (sau khi đã đóng task `Done`) người dùng sửa lại thành **`"Fix stream failover "`**. Nhờ bảng `Change_Log` ta mới khôi phục lại được đúng tiêu đề lúc ước lượng.

---

### 3.3. Bảng 3 — Ví dụ 5 dòng dữ liệu trong bảng cầu nối `Issue_Component` (Nối `Issue.ID` với `Component.ID`)
| STT dòng | `Issue_ID` *(Khóa ngoại nối về `Issue.ID`)* | `Component_ID` *(Khóa ngoại nối về `Component.ID`)* | Giải thích ý nghĩa liên kết thực tế |
| :-: | :---: | :---: | :--- |
| **1** | **`67`** *(tức `XD-3766`)* | **`74`** | Công việc `XD-3766` thuộc phân hệ có mã `74` (`Stream Module`). |
| **2** | **`69`** *(tức `XD-3764`)* | **`75`** | Công việc `XD-3764` thuộc phân hệ có mã `75` (`Batch`). |
| **3** | **`71`** *(tức `XD-3762`)* | **`76`** | Công việc `XD-3762` thuộc phân hệ thứ nhất có mã `76` (`Documentation`). |
| **4** | **`71`** *(tức `XD-3762`)* | **`77`** | Cùng công việc `XD-3762` thuộc thêm phân hệ thứ hai có mã `77` (`Packaging`). |
| **5** | **`71`** *(tức `XD-3762`)* | **`78`** | Cùng công việc `XD-3762` thuộc thêm phân hệ thứ ba có mã `78` (`Runtime`). |

> 💡 **Nhận xét từ 3 dòng cuối của bảng `Issue_Component`:** Chỉ riêng 1 công việc `Issue_ID = 71` (`XD-3762`) đã xuất hiện **3 dòng** trong bảng `Issue_Component` vì công việc này tác động lên cả 3 phân hệ kỹ thuật (`76`, `77`, `78`) cùng lúc.

---

### 3.4. Bảng 4 — Ví dụ 5 dòng dữ liệu trong bảng danh mục `Component` (Tra cứu tên phân hệ từ `Component.ID`)
| `ID` *(Khóa chính)* | `Jira_ID` *(Mã trên Jira Server)* | `Name` *(Tên phân hệ kỹ thuật)* | `Description` *(Mô tả chức năng của phân hệ trong Spring XD)* | `Project_ID` |
| :-: | :---: | :--- | :--- | :---: |
| **`74`** | `12731` | **`Stream Module`** | `Development of source, processing, sink module functionality` | `1` *(Spring XD)* |
| **`75`** | `12697` | **`Batch`** | `Execution of workflow activities on and off Hadoop` | `1` *(Spring XD)* |
| **`76`** | `12710` | **`Documentation`** | `Documentation on the wiki` | `1` *(Spring XD)* |
| **`77`** | `12693` | **`Packaging`** | `Creating out of the box server style distribution artifacts` | `1` *(Spring XD)* |
| **`78`** | `12695` | **`Runtime`** | `DIRT Runtime` | `1` *(Spring XD)* |

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc 4 bảng lưu trữ](01_data_scale_and_overview.md)** *(Tài liệu hiện tại)*
2. 📋 **[Phần 2: Sơ đồ ERD & Bảng mô tả đầy đủ các thuộc tính kèm các loại giá trị (`N = 3,542`)](02_attribute_breakdown_and_counts.md)**
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & cách giải quyết tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)**
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)**
5. 📏 **[RULE.md: Bộ quy tắc chuẩn hóa khi xử lý và viết báo cáo cho các dự án khác](RULE.md)**
