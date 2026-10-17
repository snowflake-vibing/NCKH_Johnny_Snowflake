# 📋 PHẦN 2. BẢNG DỮ LIỆU ĐẦY ĐỦ & THỐNG KÊ SỐ LƯỢNG TỪNG LOẠI TRONG MỖI THUỘC TÍNH (`N = 3,542` ISSUES CÓ STORY POINT)

> **Phạm vi thống kê:** Chỉ xét riêng trên quần thể **3,542 công việc có nhãn `Story_Point > 0` hợp lệ** của dự án **Spring XD (`Project_ID = 1`)** trong `C:/tawos/tawos_eda.db` (đã loại bỏ hoàn toàn các công việc không có điểm Story Point).

---

## 1. Bảng Kiểm Kê Đầy Đủ 30 Thuộc Tính Của Bảng `Issue` (`N = 3,542`)

Bảng dưới đây trình bày toàn bộ 30 thuộc tính trong bảng `Issue` đối với 3,542 công việc có Story Point của dự án Spring XD:

| STT | Tên thuộc tính (`Column`) | Kiểu dữ liệu | Số mẫu có dữ liệu (`Present`) | Số mẫu khuyết (`Missing / NULL`) | Tỷ lệ khuyết (%) | Số giá trị phân biệt (`Unique`) | Ý nghĩa và đặc điểm phân phối trên tập `N = 3,542` |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `ID` | `int64` | `3,542` | `0` | `0.00%` | `3,542` | Khóa chính định danh Issue trong CSDL (`65` $\rightarrow$ `3773`). |
| **2** | `Jira_ID` | `int64` | `3,542` | `0` | `0.00%` | `3,542` | ID nội bộ của Issue trên máy chủ Jira (`14772` $\rightarrow$ `87615`). |
| **3** | `Issue_Key` | `str` | `3,542` | `0` | `0.00%` | `3,542` | Mã công việc trên Jira (`XD-1` $\rightarrow$ `XD-3769`). |
| **4** | `URL` | `str` | `3,542` | `0` | `0.00%` | `3,542` | Đường dẫn REST API của từng Issue. |
| **5** | `Title` | `str` | `3,542` | `0` | `0.00%` | `3,477` | Tiêu đề tóm tắt công việc (độ dài trung bình `8.13` từ). |
| **6** | `Description` | `str` | `3,373` | `169` | `4.77%` | `3,341` | Nội dung mô tả đầy đủ (gồm cả văn bản và đoạn mã). |
| **7** | `Description_Text` | `str` | `3,370` | `172` | `4.86%` | `3,337` | Phần văn bản tự nhiên của mô tả (trung bình `52.97` từ). |
| **8** | `Description_Code` | `str` | `637` | `2,905` | `82.02%` | `634` | Đoạn mã nguồn hoặc stack trace trích xuất từ mô tả. |
| **9** | `Type` | `str` | `3,542` | `0` | `0.00%` | `5` | Loại công việc (`Story`, `Bug`, `Improvement`, `Technical task`, `Epic`). |
| **10** | `Priority` | `str` | `3,542` | `0` | `0.00%` | `5` | Độ ưu tiên (`Minor`, `Major`, `Critical`, `Blocker`, `Trivial`). |
| **11** | `Status` | `str` | `3,542` | `0` | `0.00%` | `4` | Trạng thái cuối (`Done`, `To Do`, `In Progress`, `In PR`). |
| **12** | `Resolution` | `str` | `2,940` | `602` | `17.00%` | `9` *(+ NULL)* | Kết quả giải quyết khi đóng (`Complete`, `Invalid`, `Duplicate`...). |
| **13** | `Creation_Date` | `datetime` | `3,542` | `0` | `0.00%` | `3,537` | Thời điểm tạo Issue (`2013-04-17 08:48:08` $\rightarrow$ `2018-11-16 15:57:31`). |
| **14** | `Estimation_Date` | `datetime` | `3,542` | `0` | `0.00%` | `3,537` | Mốc ước lượng lưu sẵn trong bảng `Issue` (`2013-04-17` $\rightarrow$ `2018-11-16`). |
| **15** | `Resolution_Date` | `datetime` | `2,940` | `602` | `17.00%` | `2,877` | Thời điểm đóng Issue (`2013-05-03 18:10:02` $\rightarrow$ `2017-03-21 16:55:23`). |
| **16** | `Last_Updated` | `datetime` | `3,542` | `0` | `0.00%` | `2,520` | Thời điểm cập nhật cuối cùng (`2013-06-01` $\rightarrow$ `2018-11-20`). |
| **17** | `Story_Point` | `float64` | `3,542` | `0` | `0.00%` | `25` | Điểm nỗ lực (`Min = 0.2`, `Median = 3.0`, `Mean = 3.98`, `Max = 2567.0`). |
| **18** | `Timespent` | `float64` | `2` | `3,540` | `99.94%` | `2` | Chỉ có 2 mẫu có giá trị (`1.0` và `20.0`), 99.94% bị bỏ trống. |
| **19** | `In_Progress_Minutes` | `float64` | `3,542` | `0` | `0.00%` | `1,462` | Số phút ở trạng thái đang làm (`1,813` mẫu bằng `0`; `1,729` mẫu `> 0`). |
| **20** | `Total_Effort_Minutes` | `float64` | `3,542` | `0` | `0.00%` | `1,640` | Tổng số phút nỗ lực (`1,603` mẫu bằng `0`; `1,939` mẫu `> 0`). |
| **21** | `Resolution_Time_Minutes` | `float64` | `3,542` | `0` | `0.00%` | `2,716` | Tổng thời gian giải quyết (`602` mẫu chưa đóng có giá trị `0`; `2,940` mẫu `> 0`). |
| **22** | `Title_Changed_After_Estimation` | `int64` | `3,542` | `0` | `0.00%` | `2` (`0`, `1`) | Cờ báo sửa tiêu đề sau ước lượng (`0`: 2,921 mẫu; `1`: 621 mẫu). |
| **23** | `Description_Changed_After_Estimation` | `int64` | `3,542` | `0` | `0.00%` | `1` (`chỉ có 0`) | Cờ báo sửa mô tả sau ước lượng (`0`: 3,542 mẫu — bị lỗi ghi nhận thiếu). |
| **24** | `Story_Point_Changed_After_Estimation` | `int64` | `3,542` | `0` | `0.00%` | `2` (`0`, `1`) | Cờ báo sửa Story Point sau ước lượng (`0`: 3,071 mẫu; `1`: 471 mẫu). |
| **25** | `Pull_Request_URL` | `str` | `617` | `2,925` | `82.58%` | `602` | Có `617` mẫu (`17.42%`) có link Pull Request; `2,925` mẫu để trống. |
| **26** | `Creator_ID` | `int64` | `3,542` | `0` | `0.00%` | `146` | Có `146` người dùng khác nhau từng khởi tạo Issue. |
| **27** | `Reporter_ID` | `int64` | `3,542` | `0` | `0.00%` | `146` | Có `146` người dùng khác nhau đứng tên báo cáo Issue. |
| **28** | `Assignee_ID` | `float64` | `2,550` | `992` | `28.01%` | `31` *(+ NULL)* | Có `2,550` mẫu (`71.99%`) có người nhận việc (thuộc 31 lập trình viên); `992` mẫu `NULL`. |
| **29** | `Project_ID` | `int64` | `3,542` | `0` | `0.00%` | `1` (`ID = 1`) | Hằng số `1` (định danh dự án Spring XD). |
| **30** | `Sprint_ID` | `float64` | `2,114` | `1,428` | `40.32%` | `66` *(+ NULL)* | Có `2,114` mẫu (`59.68%`) gắn vào 66 Sprint; `1,428` mẫu không gắn Sprint (`NULL`). |

---

## 2. Thống Kê Số Lượng Chi Tiết Đối Với Từng Loại Trong Mỗi Thuộc Tính (`N = 3,542`)

### 2.1. Thuộc tính `Type` (Loại công việc — 5 loại giá trị)
| STT | Giá trị trong thuộc tính `Type` | Số lượng ở trạng thái cuối (`Issue.Type`) | Tỷ lệ (%) | Số lượng tại thời điểm ước lượng (`Clean_Type`) | Tỷ lệ (%) |
| :-: | :--- | :---: | :---: | :---: | :---: |
| **1** | **`Story`** (User Story) | `2,535` | `71.57%` | **`2,621`** | **`74.00%`** |
| **2** | **`Bug`** (Lỗi phần mềm) | `594` | `16.77%` | **`576`** | **`16.26%`** |
| **3** | **`Improvement`** (Cải tiến hệ thống) | `294` | `8.30%` | **`218`** | **`6.15%`** |
| **4** | **`Technical task`** (Tác vụ kỹ thuật) | `73` | `2.06%` | **`73`** | **`2.06%`** |
| **5** | **`Epic`** (Chức năng lớn) | `46` | `1.30%` | **`54`** | **`1.52%`** |
| — | **Tổng cộng** | **`3,542`** | **`100.00%`** | **`3,542`** | **`100.00%`** |

---

### 2.2. Thuộc tính `Priority` (Mức độ ưu tiên — 5 loại giá trị)
| STT | Giá trị trong thuộc tính `Priority` | Số lượng ở trạng thái cuối (`Issue.Priority`) | Tỷ lệ (%) | Số lượng tại thời điểm ước lượng (`Clean_Priority`) | Tỷ lệ (%) |
| :-: | :--- | :---: | :---: | :---: | :---: |
| **1** | **`Minor`** (Ưu tiên thấp/mặc định) | `3,012` | `85.04%` | **`3,116`** | **`87.97%`** |
| **2** | **`Major`** (Ưu tiên quan trọng) | `401` | `11.32%` | **`317`** | **`8.95%`** |
| **3** | **`Critical`** (Ưu tiên nghiêm trọng) | `72` | `2.03%` | **`60`** | **`1.69%`** |
| **4** | **`Blocker`** (Ưu tiên khẩn cấp/chặn) | `36` | `1.02%` | **`36`** | **`1.02%`** |
| **5** | **`Trivial`** (Ưu tiên rất nhỏ) | `21` | `0.59%` | **`13`** | **`0.37%`** |
| — | **Tổng cộng** | **`3,542`** | **`100.00%`** | **`3,542`** | **`100.00%`** |

---

### 2.3. Thuộc tính `Status` (Trạng thái công việc — 4 loại giá trị)
| STT | Giá trị trong thuộc tính `Status` | Số lượng (`N = 3,542`) | Tỷ lệ (%) | Ý nghĩa trạng thái |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **`Done`** | `2,940` | `83.00%` | Công việc đã xử lý xong và đóng lại. |
| **2** | **`To Do`** | `578` | `16.32%` | Công việc đã được ước lượng điểm nhưng vẫn nằm trong Backlog chưa thực thi. |
| **3** | **`In Progress`** | `20` | `0.56%` | Công việc đang trong quá trình thực hiện. |
| **4** | **`In PR`** | `4` | `0.11%` | Công việc đã viết mã xong và đang chờ duyệt Pull Request. |
| — | **Tổng cộng** | **`3,542`** | **`100.00%`** | — |

---

### 2.4. Thuộc tính `Resolution` (Kết quả đóng công việc — 10 loại giá trị)
| STT | Giá trị trong thuộc tính `Resolution` | Số lượng (`N = 3,542`) | Tỷ lệ (%) | Ý nghĩa kết quả giải quyết |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **`Complete`** | `2,372` | `66.97%` | Hoàn thành toàn bộ yêu cầu của công việc. |
| **2** | **`NULL` (Chưa có Resolution)** | `602` | `17.00%` | Các công việc đang ở trạng thái `To Do` (`578`), `In Progress` (`20`), `In PR` (`4`). |
| **3** | **`Invalid`** | `119` | `3.36%` | Công việc/lỗi báo cáo không hợp lệ. |
| **4** | **`Duplicate`** | `118` | `3.33%` | Công việc bị trùng lặp với một ticket khác. |
| **5** | **`Won't Fix`** | `114` | `3.22%` | Đội dự án quyết định không thực hiện/không sửa. |
| **6** | **`Deferred`** | `110` | `3.11%` | Tạm hoãn sang giai đoạn hoặc dự án khác. |
| **7** | **`Works as Designed`** | `42` | `1.19%` | Hệ thống hoạt động đúng thiết kế, không phải lỗi. |
| **8** | **`Fixed`** | `36` | `1.02%` | Đã vá lỗi thành công. |
| **9** | **`Cannot Reproduce`** | `20` | `0.56%` | Không thể tái hiện được lỗi như mô tả. |
| **10** | **`Incomplete`** | `9` | `0.25%` | Thông tin mô tả không đủ để giải quyết. |
| — | **Tổng cộng** | **`3,542`** | **`100.00%`** | — |

---

### 2.5. Thuộc tính `Story_Point` (Nhãn điểm nỗ lực — Toàn bộ các mức điểm trên `N = 3,542`)
| STT | Mức điểm (`Story Point`) | Số lượng ở cột gốc (`Issue.Story_Point`) | Tỷ lệ gốc (%) | Số lượng sau khi khôi phục (`Initial_Story_Point`) | Tỷ lệ khôi phục (%) | Phân loại trên thang đo Spring XD |
| :-: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **`0.2`** | `1` | `0.03%` | `0` | `0.00%` | `XD-1970` ban đầu chấm `0.5`, sau đó sửa thành `0.2`. |
| **2** | **`0.5`** | `0` | `0.00%` | **`1`** | **`0.03%`** | ✅ Khôi phục từ `XD-1970` (điểm nửa đơn vị chuẩn). |
| **3** | **`1.0`** | `826` | `23.32%` | **`805`** | **`22.73%`** | ✅ Mức điểm Fibonacci phổ biến thứ 1. |
| **4** | **`2.0`** | `639` | `18.04%` | **`651`** | **`18.38%`** | ✅ Mức điểm Fibonacci phổ biến thứ 3. |
| **5** | **`3.0`** | `755` | `21.32%` | **`754`** | **`21.29%`** | ✅ Mức điểm Fibonacci phổ biến thứ 2. |
| **6** | **`4.0`** | `211` | `5.96%` | **`221`** | **`6.24%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **7** | **`5.0`** | `572` | `16.15%` | **`570`** | **`16.09%`** | ✅ Mức điểm Fibonacci phổ biến thứ 4. |
| **8** | **`6.0`** | `27` | `0.76%` | **`29`** | **`0.82%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **9** | **`7.0`** | `3` | `0.08%` | **`3`** | **`0.08%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **10** | **`8.0`** | `394` | `11.12%` | **`394`** | **`11.12%`** | ✅ Mức điểm Fibonacci phổ biến thứ 5. |
| **11** | **`9.0`** | `1` | `0.03%` | **`1`** | **`0.03%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **12** | **`10.0`** | `45` | `1.27%` | **`49`** | **`1.38%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **13** | **`12.0`** | `5` | `0.14%` | **`5`** | **`0.14%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **14** | **`13.0`** | `5` | `0.14%` | **`3`** | **`0.08%`** | ✅ Mức điểm chuẩn Fibonacci. |
| **15** | **`14.0`** | `1` | `0.03%` | **`0`** | `0.00%` | Sửa đổi sau khi ước lượng. |
| **16** | **`15.0`** | `2` | `0.06%` | **`3`** | **`0.08%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **17** | **`16.0`** | `18` | `0.51%` | **`15`** | **`0.42%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **18** | **`20.0`** | `17` | `0.48%` | **`18`** | **`0.51%`** | ✅ Mức điểm chuẩn Planning Poker. |
| **19** | **`21.0`** | `7` | `0.20%` | **`7`** | **`0.20%`** | ✅ Mức điểm chuẩn Fibonacci. |
| **20** | **`24.0`** | `1` | `0.03%` | **`0`** | `0.00%` | Sửa đổi sau khi ước lượng. |
| **21** | **`30.0`** | `0` | `0.00%` | **`1`** | **`0.03%`** | ✅ Điểm ước lượng ban đầu hợp lệ. |
| **22** | **`32.0`** | `1` | `0.03%` | **`1`** | **`0.03%`** | ✅ Mức điểm hợp lệ trong miền `[0.5, 40.0]`. |
| **23** | **`40.0`** | `5` | `0.14%` | **`5`** | **`0.14%`** | ✅ Mức trần chuẩn của Planning Poker (`40.0`). |
| **24** | **`50.0`** | `1` | `0.03%` | **`1`** | **`0.03%`** | ⚠️ Ngoại lệ: `XD-836` (`Epic`, `Is_Valid_Scale_SP = 0`). |
| **25** | **`80.0`** | `2` | `0.06%` | **`2`** | **`0.06%`** | ⚠️ Ngoại lệ: `XD-92`, `XD-1141` (`Epic`, `Is_Valid_Scale_SP = 0`). |
| **26** | **`100.0`** | `2` | `0.06%` | **`2`** | **`0.06%`** | ⚠️ Ngoại lệ: `XD-996` (`Epic`), `XD-3562` (`To Do`, `Is_Valid_Scale_SP = 0`). |
| **27** | **`2567.0`** | `1` | `0.03%` | **`1`** | **`0.03%`** | 🚨 Điểm nhiễu: `XD-2602` (`Works as Designed`, `Is_Valid_Scale_SP = 0`). |
| — | **Tổng cộng** | **`3,542`** | **`100.00%`** | **`3,542`** | **`100.00%`** | **`3,536` mẫu (`99.83%`) thuộc miền chuẩn `[0.5, 40.0]`**. |

---

### 2.6. Thuộc tính `Component` (18 phân hệ kỹ thuật trên tập `N = 3,542`)
Trong `3,542` công việc có Story Point, có `1,093` công việc được gắn ít nhất 1 Component (tổng cộng `1,312` liên kết `Issue_Component`) và `2,449` công việc không gắn Component:

| STT | Tên `Component` | Số lượng Issue (`N = 3,542`) | Tỷ lệ trên `3,542` (%) | STT | Tên `Component` | Số lượng Issue (`N = 3,542`) | Tỷ lệ trên `3,542` (%) |
| :-: | :--- | :---: | :---: | :-: | :--- | :---: | :---: |
| **1** | **`Runtime`** | `264` | `7.45%` | **10** | **`Configuration`** | `57` | `1.61%` |
| **2** | **`Stream Module`** | `133` | `3.75%` | **11** | **`Acceptance Testing`** | `54` | `1.52%` |
| **3** | **`Documentation`** | `113` | `3.19%` | **12** | **`REST`** | `39` | `1.10%` |
| **4** | **`Packaging`** | `106` | `2.99%` | **13** | **`Ingest`** | `35` | `0.99%` |
| **5** | **`Batch`** | `103` | `2.91%` | **14** | **`Testing`** | `33` | `0.93%` |
| **6** | **`UI`** | `94` | `2.65%` | **15** | **`YARN Runtime`** | `27` | `0.76%` |
| **7** | **`Hadoop`** | `92` | `2.60%` | **16** | **`Performance Testing`** | `18` | `0.51%` |
| **8** | **`CLI`** | `69` | `1.95%` | **17** | **`DSL`** | `12` | `0.34%` |
| **9** | **`Analytics`** | `60` | `1.69%` | **18** | **`Export`** | `3` | `0.08%` |

---

### 2.7. Các thuộc tính Cờ nhị phân (Binary Flags) & Các trường văn bản/liên kết khác (`N = 3,542`)
| Tên thuộc tính | Loại giá trị `1` (Có / Đúng) | Loại giá trị `0` (Không / Khuyết) | Nhận xét chi tiết |
| :--- | :---: | :---: | :--- |
| **`Has_Clean_Description`** *(Có mô tả lúc ước lượng)* | `3,356` (`94.75%`) | `186` (`5.25%`) | Có 14 công việc lúc ước lượng chưa có mô tả, về sau mới được viết thêm mô tả (`3,370 - 3,356 = 14`). |
| **`Has_Clean_Component`** *(Có Component lúc ước lượng)* | `991` (`27.98%`) | `2,551` (`72.02%`) | Có 102 công việc lúc ước lượng chưa gắn Component, về sau mới được gắn thêm trong quá trình làm. |
| **`Title_Changed_After_Estimation`** *(Cờ gốc bảng Issue)* | `621` (`17.53%`) | `2,921` (`82.47%`) | Sau khi khôi phục `Real_Estimation_Date`, số mẫu thực sự đổi nội dung `Title` là **`594` mẫu (`16.77%`)**. |
| **`Description_Changed_After_Estimation`** *(Cờ gốc bảng Issue)* | `0` (`0.00%` — *Lỗi*) | `3,542` (`100.00%`) | Cờ gốc bị lỗi ghi `0`; kiểm toán thực tế từ `Change_Log` có **`576` mẫu (`16.26%`)** đổi nội dung `Description`. |
| **`Story_Point_Changed_After_Estimation`** *(Cờ gốc bảng Issue)* | `471` (`13.30%`) | `3,071` (`86.70%`) | Sau khi loại trừ 89 mẫu gán điểm lần đầu trong `Change_Log`, có **`411` mẫu (`11.60%`)** bị sửa điểm sau ước lượng. |
| **`Pull_Request_URL`** *(Liên kết PR GitHub)* | `617` (`17.42%`) | `2,925` (`82.58%`) | Thuộc tính sinh ra khi lập trình viên gửi code giải pháp (rò rỉ tương lai). |
| **`Description_Code`** *(Đoạn mã trong mô tả cuối)* | `637` (`17.98%`) | `2,905` (`82.02%`) | Trích xuất từ `Description` cuối cùng. |
| **`Assignee_ID`** *(Lập trình viên nhận việc)* | `2,550` (`71.99%`) | `992` (`28.01%`) | Phân bổ trên 31 lập trình viên; `50.51%` bị gán hoặc đổi sau khi ước lượng. |
| **`Sprint_ID`** *(Chu kỳ Sprint)* | `2,114` (`59.68%`) | `1,428` (`40.32%`) | Phân bổ trên 66 Sprint; `63.55%` bị thay đổi sau khi ước lượng. |

---

## 🔗 Điều Hướng Tài Liệu Trong Chuỗi Báo Cáo (`docs/draft/`)

1. 📌 **[Phần 1: Giới thiệu quy mô dữ liệu & cấu trúc thông tin lưu trữ](01_data_scale_and_overview.md)**
2. 📋 **[Phần 2: Bảng dữ liệu đầy đủ & thống kê số lượng từng loại trong mỗi thuộc tính (`N = 3,542`)](02_attribute_breakdown_and_counts.md)** *(Tài liệu hiện tại)*
3. 🛠️ **[Phần 3: Phát hiện các điểm bất thường & giải pháp xử lý tương ứng để tạo Clean Data](03_anomalies_and_cleaning_solutions.md)**
4. ✅ **[Phần 4: Thẩm định lại Clean Data để đảm bảo không còn Data Leakage](04_clean_data_verification_audit.md)**
