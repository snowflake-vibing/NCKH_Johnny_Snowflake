# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Tài liệu:** Hướng 3 – Kế hoạch Nghiên cứu 2 tuần tiếp theo (Báo cáo Lần 2)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tạ Việt Phương** (*UIT - VNUHCM*) | 2026 | Xác định 4 nội dung cốt lõi cho đề tài "AI hỗ trợ ước lượng Story Point trong bối cảnh lập kế hoạch Agile thực tế": Prediction Task & Target, Estimation Time / Information cut-off, Feature Availability, và Evaluation. | Dữ liệu Jira / TAWOS Dataset. | Initial Story Point khôi phục từ Change Log. | Khai phá dữ liệu lịch sử Jira (TAWOS) kết hợp xây dựng pipeline tái tạo trạng thái issue tại mốc `SP_Estimation_Date`. | Baseline kinh điển: Median effort, Mean effort. | Chronological Split theo thời gian tạo issue. | MAE, MdAE, SA, Statistical significance. | Xác định 4 yêu cầu bắt buộc: (1) Khôi phục Initial SP làm Ground Truth, (2) Chốt mốc Information Cut-off không muộn hơn `SP_Estimation_Date`, (3) Loại bỏ triệt me các trường thông tin tương lai, (4) So sánh hiệu quả giữa Final Snapshot và Planning-Time Snapshot. | Cấm dùng các thông tin phát sinh sau estimation time (Status=Closed, Resolution Date, Comments phát sinh). | Khung định hướng 4 nội dung để triển khai báo cáo và thực nghiệm cho Nhóm 3. | Là kim chỉ nam trực tiếp cho đề tài NCKH của nhóm. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Hướng 3 – Kế hoạch Nghiên cứu Agile Story Point Estimation

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Giảng viên hướng dẫn:** ThS/TS. Tạ Việt Phương.
* **Chủ đề chung:** AI hỗ trợ ước lượng Story Point trong bối cảnh lập kế hoạch Agile thực tế.
* **Thời gian:** Tháng 9 - 10/2026.

#### 2. 4 Nội dung Bắt buộc:
1. **Prediction Task & Target:** Dự báo Story Point cho issue; xác định Initial SP làm ground truth.
2. **Estimation Time / Information cut-off:** Xác định mốc `SP_Estimation_Date`.
3. **Feature Availability:** Chỉ dùng các trường có sẵn trước hoặc tại mốc estimation date.
4. **Research Question (RQ):** Đánh giá tác động của Temporal Leakage giữa 2 bối cảnh thử nghiệm.

---
© 2026 **Khoa HTTT — Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
