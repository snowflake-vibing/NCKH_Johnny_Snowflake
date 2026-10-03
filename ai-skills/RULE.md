# 📜 Quy tắc Phát triển & Tương tác AI (Project Execution Rules)

> **File này quy định các quy tắc bắt buộc áp dụng cho toàn bộ thành viên dự án và trợ lý AI trong quá trình làm việc, chỉnh sửa mã nguồn, xử lý dữ liệu và cập nhật tài liệu.**

---

## 🚨 1. Quy tắc Bắt buộc Hàng đầu (Core Directives)

1. **Bắt buộc đọc `RULE.md` trước khi chỉnh sửa:**
   * Trước khi thực hiện bất kỳ thao tác chỉnh sửa, tái cấu trúc mã nguồn, cập nhật tài liệu hoặc xử lý dữ liệu nào trong dự án, trợ lý AI và developer phải đọc kỹ file [RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md) này để đảm bảo tuân thủ đúng định hướng.

2. **Cập nhật Cấu trúc Thư mục trong `README.md` khi tạo file/thư mục mới:**
   * Ngay sau khi tạo bất kỳ file hoặc thư mục mới nào trong dự án, **phải cập nhật lại sơ đồ Cấu trúc Thư mục Dự án** trong [README.md](file:///d:/NCKH_3/README.md) tương ứng.

---

## 🔬 2. Quy tắc Đề tài Nghiên cứu (Temporal & Data Leakage Rule)

3. **Kiểm soát Rò rỉ Thông tin Tương lai (Strict Temporal Control):**
   * Đây là lõi nghiên cứu của đề tài. Mọi script xử lý dữ liệu, trích xuất feature, và pipeline huấn luyện mô hình **tuyệt đối không được truy cập các thông tin/sự kiện phát sinh sau mốc `SP_Estimation_Date`**.
   * Không sử dụng các trường như `Resolution Date`, `Status = Closed`, các `Comments` phát sinh sau khi estimate, hay nội dung `Title/Description` đã bị sửa đổi sau thời điểm chấm điểm.

4. **Tính Tái lập Thử nghiệm (Reproducibility & Verification):**
   * Mọi thử nghiệm ML/DL (như GPT2SP, SBERT, Baselines) khi chạy phải ghi lại rõ ràng: **Random Seed, phiên bản thư viện, thông số hyperparameter, và log đầu ra**.
   * Không được tự ý thay đổi dữ liệu test set hoặc tiêu chuẩn đánh giá (MAE, MdAE, SA) mà không ghi nhận rõ ràng trong log.

---

## 📁 3. Quy tắc Quản lý Thư mục & Mã nguồn (Code & Directory Structure)

5. **Phân loại File Đúng Thư mục:**
   * `ai-skills/`: Chứa các file quy tắc (`RULE.md`), kịch bản hướng dẫn và cấu hình cho trợ lý AI.
   * `resources/`: Chứa dữ liệu gốc, dataset TAWOS, và tài nguyên mô hình.
   * `output_b2/`: Chứa kết quả trích xuất dữ liệu, artifacts báo cáo và biểu đồ EDA.
   * `skills/`: Chứa các kịch bản tự động hóa, pipeline xử lý chính.
   * `scratch/`: Chứa các script thử nghiệm tạm thời, code debug.
   * Không để file rác, file log tạm hay ảnh chụp màn hình nằm tự do ở thư mục gốc root ngoại trừ các file tài liệu chuẩn (`README.md`, `OVERVIEW.md`, `LICENSE`).

6. **Giữ Vệ sinh Repository & Git Cleanliness:**
   * Không commit các file tạm (`.tmp`, `.log`), các file bộ nhớ tạm hoặc dataset thô kích thước cực lớn gây nặng repository.
   * Viết commit message theo chuẩn **Conventional Commits** (ví dụ: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`).

---

## 📝 4. Quy tắc Đồng bộ Tài liệu (Documentation Sync Rule)

7. **Đồng bộ giữa `README.md` và `OVERVIEW.md`:**
   * [README.md](file:///d:/NCKH_3/README.md) đóng vai trò làm trang chủ / cổng định tuyến (entry point) của repository.
   * [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) đóng vai trò chứa thông tin chi tiết về sản phẩm, bối cảnh, kết quả EDA, tái lập và roadmap nghiên cứu.
   * Khi có sự thay đổi lớn về bối cảnh, kết quả thực nghiệm hoặc roadmap, phải cập nhật nội dung tương ứng vào `OVERVIEW.md`.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
