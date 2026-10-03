# 📋 Requirements_1: Phân tích Định nghĩa Bài toán (Task Definition Analysis)

> **Tài liệu đối chiếu Yêu cầu NCKH về Định nghĩa Bài toán (Task Definition v1) giữa Hướng dẫn NCKH (`Huong 3 b2.pdf`, `Research_Nhom_3.pdf`) và Sản phẩm trên GitHub Repository.**

---

## 🎯 1. Bảng Đối chiếu Chi tiết (Requirements vs GitHub Artifacts)

| Thành phần Yêu cầu | Định nghĩa Chi tiết từ NCKH (`Huong 3 b2.pdf` & `Research_Nhom_3.pdf`) | Thực trạng trên GitHub Repository (`NCKH_Johnny_Snowflake`) | Đánh giá Trạng thái |
| :--- | :--- | :--- | :---: |
| **Problem Definition** | Hỗ trợ ước lượng nỗ lực (Story Point) trong các buổi họp *Sprint Planning* và loại bỏ triệt để sai lệch do rò rỉ thông tin phát sinh sau planning (*Temporal Leakage*). | Đã được mô tả chi tiết trong [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Mục 1 & 2) và [README.md](file:///d:/NCKH_3/README.md). | ✅ **Đã đáp ứng (Done)** |
| **Target User** | Đội ngũ Agile/Scrum (Developers, Product Owner, Scrum Master) sử dụng kết quả dự báo làm căn cứ tham khảo thảo luận. | Được xác định rõ trong bảng Task Definition v1 tại [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md). | ✅ **Đã đáp ứng (Done)** |
| **Unit of Analysis** | Một Jira Issue / User Story đơn lẻ đủ điều kiện được chấm Story Point trong hệ thống quản lý task. | Được mô tả và xử lý ở mức single issue trong kịch bản EDA tại [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb). | ✅ **Đã đáp ứng (Done)** |
| **Prediction Task** | Bài toán **Supervised Regression** dự báo một giá trị Story Point tương đối dạng số thực. | Định nghĩa bài toán hồi quy supervised được nêu rõ trong tài liệu [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md). | ✅ **Đã đáp ứng (Done)** |
| **Estimation Time** | Mốc thời gian `SP_Estimation_Date` (thời điểm giá trị Story Point lần đầu tiên được ghi nhận trong Jira Changelog). | Đã trích xuất và xác minh trường `SP_Estimation_Date` trong kịch bản [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb). | ✅ **Đã đáp ứng (Done)** |
| **Ground Truth / Target** | Giá trị **Initial Story Point** tại mốc `SP_Estimation_Date`. Khôi phục giá trị ban đầu từ `Change_Log` nếu bị chỉnh sửa về sau. | Đã định nghĩa quy tắc khôi phục Initial SP từ Change Log trong [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) và [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md). | ✅ **Đã đáp ứng (Done)** |
| **Input Available** | Chỉ sử dụng thông tin có sẵn tại mốc `SP_Estimation_Date`: Title, Description, Issue Type, Priority, Components. *(Cấm dùng: Status=Closed, Resolution Date, Comments phát sinh)*. | Đã quy định rõ trong quy tắc kiểm soát Temporal Leakage tại [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md). | ✅ **Đã đáp ứng (Done)** |
| **Research Question (RQ)** | *"Việc dựng lại trạng thái Jira issue đúng tại `SP_Estimation_Date` làm thay đổi độ chính xác của mô hình dự báo như thế nào so với Final Snapshot?"* | Được chốt làm câu hỏi nghiên cứu cốt lõi tại [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Mục 2). | ✅ **Đã đáp ứng (Done)** |

---

## 🔍 2. Phân tích Chi tiết & Đánh giá Bỏ sót (Gap Analysis)

### 📌 Các điểm đã hoàn thành tốt:
1. **Rõ ràng về mốc thời gian (Information Cut-off):** Đã làm rõ sự khác biệt giữa thời điểm issue được tạo (`created`) và thời điểm issue được chấm Story Point (`SP_Estimation_Date`).
2. **Khái niệm Ground Truth:** Định nghĩa chính xác Initial Story Point thay vì dùng Final Story Point (tránh bẫy rò rỉ khi điểm SP bị chỉnh sửa lại sau khi làm xong).

### ⚠️ Các điểm cần hoàn thiện ở bước tiếp theo:
1. **Data Pipeline Code:** Cần đẩy script tự động hóa trích xuất `Initial SP` từ CSDL `tawos_eda.db` vào mã nguồn sản phẩm (hiện mới thực hiện ở dạng kịch bản EDA).

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
