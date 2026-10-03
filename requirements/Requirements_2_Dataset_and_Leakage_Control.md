# 📋 Requirements_2: Phân tích Dữ liệu & Kiểm soát Leakage (Dataset & Leakage Control)

> **Tài liệu đối chiếu Yêu cầu NCKH về Dữ liệu TAWOS v1.1 & Kiểm soát Rò rỉ Thông tin Tương lai giữa Hướng dẫn NCKH (`Huong 3 b2.pdf`, `Research_Nhom_3.pdf`) và Sản phẩm trên GitHub Repository.**

---

## 🎯 1. Bảng Đối chiếu Chi tiết Dữ liệu TAWOS & Temporal Leakage

| Yêu cầu NCKH (`Huong 3 b2.pdf` & `Research_Nhom_3.pdf`) | Nội dung Chi tiết Yêu cầu | Thực trạng trên GitHub Repository (`NCKH_Johnny_Snowflake`) | Đánh giá Trạng thái |
| :--- | :--- | :--- | :---: |
| **Dataset Card v1** | Mô tả đầy đủ bộ dữ liệu TAWOS v1.1: 458.232 issues, 39 dự án, 12 Jira repositories, time span, license. | Thông tin bộ dữ liệu TAWOS v1.1 được trình bày chi tiết tại [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Mục 3) và [data/README.md](file:///d:/NCKH_3/data/README.md). | ✅ **Đã đáp ứng (Done)** |
| **Thống kê Đếm Story Point** | Xác định chính xác population có Story Point: 63.011 issues (13,75%) có SP, 395.221 issues (86,25%) không có SP. | Đã thực thi truy vấn đếm và trực quan hóa trong [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb) (Cell 3). | ✅ **Đã đáp ứng (Done)** |
| **Thống kê Khuyết văn bản** | Thống kê số lượng issue thiếu `Description` (29.128 issues ~ 6,36%). | Đã thực hiện phân tích missing values tại Cell 4 trong [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb). | ✅ **Đã đáp ứng (Done)** |
| **Minh chứng Rò rỉ Thông tin (Leakage Evidence)** | Thống kê số issue bị sửa Title/Description sau estimation: 11.969 issues (19%), 51.485 lượt thay đổi văn bản, trung vị độ trễ 2,3 ngày (55,3 giờ). | Đã hoàn thành phân tích Change Log chi tiết tại Cell 7 & 8 trong [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb) và đưa vào [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md). | ✅ **Đã đáp ứng (Done)** |
| **Case History Extraction** | Trích xuất các case history cụ thể từ Change Log để minh họa trực quan sự rò rỉ văn bản. | Đã trích xuất các ví dụ lịch sử sửa đổi văn bản tại Cell 9 trong [data/EDA_TAWOS.ipynb](file:///d:/NCKH_3/data/EDA_TAWOS.ipynb). | ✅ **Đã đáp ứng (Done)** |
| **Historical State Reconstruction** | Xây dựng pipeline dựng lại trạng thái lịch sử của từng issue tại mốc `SP_Estimation_Date` từ bảng `Change_Log`. | Đã định hình logic trong tài liệu [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Roadmap Bước 3) và quy tắc [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md). | ⚠️ **Đang phát triển (In Progress)** |

---

## 🔍 2. Kiểm soát Quy tắc Leakage (Temporal Leakage Audit)

### 🚨 5 Quy tắc Bắt buộc đã Cấu hình trong `ai-skills/RULE.md`:
1. **Rule 3.1:** Không dùng văn bản Title/Description đã bị cập nhật sau mốc `SP_Estimation_Date`.
2. **Rule 3.2:** Không sử dụng trường `Status = Closed` hoặc `Resolution Date`.
3. **Rule 3.3:** Không sử dụng các `Comments` phát sinh sau buổi họp estimation.
4. **Rule 3.4:** Không sử dụng thông tin `Assignee` tương lai nếu tại thời điểm estimation chưa xác định được người thực hiện.
5. **Rule 3.5:** Mọi bước `fit_transform` (Imputation, Scaling, Vocabulary Tokenization) chỉ được tính trên tập Train.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
