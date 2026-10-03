# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Báo cáo:** Dự báo Story Point tại Thời điểm Lập kế hoạch Agile với Kiểm soát Rò rỉ Thông tin Tương lai (Báo cáo NCKH Lần 2 — Nhóm 3)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nhóm 3** (*UIT - VNUHCM*) | 2026 | Hỗ trợ ước lượng nỗ lực trong Sprint Planning và loại bỏ triệt để sai lệch do rò rỉ thông tin tương lai (*Future-Information / Temporal Leakage*). | TAWOS Dataset v1.1 (SOLAR Group) với 458.232 issues từ 39 dự án và 12 repositories. | Initial Story Point tại mốc `SP_Estimation_Date` (khôi phục từ Change Log). | Thiết lập 2 setting thử nghiệm: **Final Snapshot** vs **Planning-Time Snapshot** kết hợp các mô hình Baseline (Median, Mean, TF-IDF) và Deep Models (GPT2SP, SBERT-GBT). | Median effort, Mean effort, Random guessing. | Chronological Split theo thứ tự thời gian khởi tạo issue (`SP_Estimation_Date`). | MAE, MdAE, SA, Bootstrap 95% CI, Wilcoxon Rank-Sum Test. | EDA chứng minh 11.969 issues (19%) bị thay đổi title/description sau estimation với trung vị độ trễ 2.3 ngày, khẳng định rò rỉ dữ liệu là nguy cơ thực tế quy mô lớn. | Tái lập GPT2SP trên Spring XD cho thấy sai lệch kết quả giữa báo cáo công bố và chạy lại thực tế (Partial Reproduction). | Mô hình hóa quy trình tái dựng lịch sử Jira issue tại đúng mốc `SP_Estimation_Date`. | Đây là báo cáo đề tài cốt lõi của Nhóm 3. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Dự báo Story Point tại Thời điểm Lập kế hoạch Agile với Kiểm soát Rò rỉ Thông tin Tương lai

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Tác giả:** Phan Ngọc Đức Huy (MSSV: 24520695), Lê Thành Hiệu (MSSV: 24520496).
* **GVHD:** ThS/TS. Tạ Việt Phương.
* **Đơn vị:** Khoa Hệ thống Thông tin — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM.
* **Thời gian:** Báo cáo nghiên cứu lần 2 (2026).

#### 2. Kết quả EDA & Đóng góp Nghiên cứu
1. **Độ phủ Story Point:** 63.011 issues (13.75%) thực sự được chấm Story Point.
2. **Bằng chứng Rò rỉ Thông tin:** 11.969 issues bị thay đổi văn bản sau khi estimate, với 51.485 lượt thay đổi và trung vị độ trễ 2.3 ngày.
3. **Bài toán Core (RQ):** Đánh giá sự suy giảm độ chính xác thực tế khi chuyển từ Final Snapshot sang Planning-Time Snapshot.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
