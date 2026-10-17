# 📌 PHẦN 1. GIỚI THIỆU QUY MÔ DỮ LIỆU & CẤU TRÚC THÔNG TIN LƯU TRỮ (SPRING XD — TAWOS v1.1)

> **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*  
> **Đối tượng phân tích:** Dự án **Spring XD (`Project_Key = 'XD'`, `Project_ID = 1`)** — Trích xuất từ `C:/tawos/tawos_eda.db` (TAWOS Dataset v1.1)  
> **Tệp dữ liệu sạch đầu ra:** [`springxd_cleaned_dataset.csv`](springxd_cleaned_dataset.csv) \| **Notebook xử lý:** [`EDA_SpringXD_Leakage_Free.ipynb`](EDA_SpringXD_Leakage_Free.ipynb)

---

## 1. Bối Cảnh & Ý Nghĩa Của Dữ Liệu Dự Án Spring XD

**Spring XD** (`Project_Key = 'XD'`, thuộc kho chứa Jira của **Spring Framework** tại `https://jira.spring.io/projects/XD/`) là nền tảng mã nguồn mở phục vụ thu thập, xử lý dữ liệu lớn theo luồng (Stream Processing) và theo lô (Batch Processing). Trong các nghiên cứu học máy dự báo nỗ lực Agile tiêu biểu như **Deep-SE (Choetkiertikul et al., 2019)** và **GPT2SP (Fu & Tantithamthavorn, 2023)**, Spring XD là dự án trọng tâm được sử dụng làm thước đo chuẩn (Benchmark).

Khác với các bộ dữ liệu CSV phẳng trước đây chỉ lưu trạng thái tĩnh cuối cùng khi công việc đã đóng lại (*Final Snapshot*), cơ sở dữ liệu quan hệ **TAWOS v1.1** (`C:/tawos/tawos_eda.db`) lưu trữ toàn bộ lịch sử cập nhật chi tiết đến từng giây của từng công việc kể từ lúc khởi tạo (`2013-04-12`) đến lần cập nhật cuối cùng (`2018-11-20`). Nhờ đó, ta có thể truy vết và khôi phục chính xác trạng thái của từng công việc tại đúng thời điểm đội phát triển thực hiện ước lượng điểm (*Planning-Time Snapshot*).

---

## 2. Xác Định Quần Thể Nghiên Cứu Có Nhãn Story Point Hợp Lệ (`N = 3,542`)

Trong bảng `Issue` của TAWOS v1.1, dự án Spring XD có tổng cộng `3,707` bản ghi công việc. Tuy nhiên, đối với bài toán học có giám sát dự báo điểm nỗ lực (Supervised Story Point Regression), các công việc không được chấm điểm (`Story_Point IS NULL` gồm `2` mẫu, hoặc `Story_Point = 0` gồm `163` mẫu) không mang nhãn mục tiêu thực tế và bắt buộc phải loại bỏ ngay từ đầu (tuyệt đối không điền khuyết bằng trung vị để tránh tạo nhãn giả).

Sau khi lọc cô lập quần thể có nhãn hợp lệ (`Story_Point > 0`), quy mô dữ liệu nghiên cứu chuẩn của dự án Spring XD được xác định như sau:

| Chỉ số quy mô quần thể nghiên cứu (`Story_Point > 0`) | Giá trị thống kê | Giải thích chi tiết |
| :--- | :---: | :--- |
| **Tổng số Issue hợp lệ của dự án Spring XD (`N`)** | **`3,542` issues** | Chiếm **95.55%** tổng số công việc của dự án Spring XD (từ mã `XD-1` đến `XD-3769`). |
| **Đối chiếu với tập chuẩn GPT2SP / Deep-SE (`3,526` issues)** | **`3,526` issues** *(+16 issues mới)* | Bộ dữ liệu của Choetkiertikul / GPT2SP thu thập đến ngày `31/03/2016` (dừng ở mã `XD-3753`, gồm đúng **3,526 issues**). Bản TAWOS v1.1 thu thập đến tháng `11/2018`, bổ sung thêm đúng **16 issues** (`XD-3754` $\rightarrow$ `XD-3769`). $3,526 + 16 = \mathbf{3,542\text{ issues}}$. |
| **Khoảng thời gian khởi tạo công việc (`Creation_Date`)** | `2013-04-17` $\rightarrow$ `2018-11-16` | Trải dài hơn 5.5 năm phát triển phần mềm theo quy trình Agile/Scrum. |
| **Tổng số bản ghi lịch sử chỉnh sửa (`Change_Log`)** | **`40,564` bản ghi** | Trung bình mỗi Issue có **11.45 lần cập nhật** trạng thái, văn bản hoặc siêu dữ liệu trong vòng đời. |

---

## 3. Cấu Trúc Các Bảng Quan Hệ & Thông Tin Lưu Trữ Trên Tập `N = 3,542` Issues

Dữ liệu của `3,542` công việc có Story Point trong dự án Spring XD được lưu trữ phân tán trên **11 bảng quan hệ** trong `C:/tawos/tawos_eda.db`:

| STT | Tên bảng trong CSDL | Số lượng bản ghi (trên tập `N = 3,542`) | Giải thích ngắn gọn dữ liệu lưu trữ thông tin gì |
| :-: | :--- | :---: | :--- |
| **1** | **`Project`** | `1` dự án | Lưu thông tin định danh dự án Spring XD (`ID = 1`, `Project_Key = 'XD'`, mã trường lưu Story Point trên Jira là `customfield_10142`). |
| **2** | **`Issue`** | `3,542` công việc | Bảng chính lưu 30 thuộc tính của mỗi công việc: định danh (`ID`, `Issue_Key`), văn bản (`Title`, `Description`, `Description_Text`, `Description_Code`), phân loại (`Type`, `Priority`, `Status`, `Resolution`), mốc thời gian (`Creation_Date`, `Estimation_Date`, `Resolution_Date`, `Last_Updated`), nhãn điểm (`Story_Point`) và nỗ lực thực tế (`In_Progress_Minutes`, `Total_Effort_Minutes`, `Resolution_Time_Minutes`). |
| **3** | **`Change_Log`** | `40,564` lịch sử thay đổi | Lưu vết từng thao tác chỉnh sửa trên 3,542 công việc: tên trường bị thay đổi (`Field`), giá trị trước khi sửa (`From_String`), giá trị sau khi sửa (`To_String`), thời điểm sửa (`Creation_Date`) và người thực hiện sửa (`Author_ID`). Đây là bảng cốt lõi để khôi phục dữ liệu chống rò rỉ. |
| **4** | **`Component`** | `18` phân hệ | Danh mục 18 thành phần kiến trúc của hệ thống Spring XD (như `Runtime`, `Stream Module`, `Documentation`, `Batch`, `Packaging`, `Hadoop`, `UI`, `CLI`...). |
| **5** | **`Issue_Component`** | `1,312` liên kết | Bảng nối (Many-to-Many) cho biết mỗi Issue trong 3,542 công việc liên quan đến những phân hệ `Component` nào. |
| **6** | **`Sprint`** | `66` chu kỳ Sprint | Lưu thông tin về 66 Sprint phát triển của dự án (tên Sprint, ngày bắt đầu, ngày kết thúc, trạng thái đóng/mở). |
| **7** | **`Version`** | `37` phiên bản | Danh sách 37 phiên bản phát hành (Release Versions) của phần mềm Spring XD (từ `1.0.0.M1` đến `1.3.2`). |
| **8** | **`Fix_Version`** | `2,775` liên kết | Ghi nhận phiên bản phần mềm mà tại đó công việc được hoàn thành và đóng gói phát hành. |
| **9** | **`Affected_Version`** | `573` liên kết | Ghi nhận phiên bản phần mềm bị ảnh hưởng bởi lỗi (Bug) được báo cáo trong công việc. |
| **10** | **`Issue_Link`** | `898` liên kết | Lưu mối quan hệ phụ thuộc giữa các Issue với nhau (như `Depends`, `Blocks`, `Duplicate`, `Relates`, `Supersedes`). |
| **11** | **`User`** | `146` người dùng hoạt động | Lưu mã định danh (`ID`) của các thành viên tham gia tạo ticket (`Creator_ID`), báo cáo (`Reporter_ID`) hoặc được phân công xử lý (`Assignee_ID`). |

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc thông tin lưu trữ](01_data_scale_and_overview.md)** *(Tài liệu hiện tại)*
2. 📋 **[Phần 2: Bảng dữ liệu đầy đủ & thống kê số lượng từng loại trong mỗi thuộc tính (`N = 3,542`)](02_attribute_breakdown_and_counts.md)**
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & giải pháp xử lý tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)**
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)**
