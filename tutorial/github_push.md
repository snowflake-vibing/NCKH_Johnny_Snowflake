# 🚀 Hướng dẫn Quy trình Push Code & Dự án lên GitHub (GitHub Workflow Tutorial)

> **Tài liệu hướng dẫn chi tiết quy trình kiểm tra, staging, commit và push mã nguồn dự án `NCKH_Johnny_Snowflake` lên GitHub repository.**

---

## 📌 1. Quy tắc trước khi Push (Pre-push Requirements)

Trước khi thực hiện bất kỳ thao tác commit hay push nào, bạn **bắt buộc phải tuân thủ các quy tắc dự án** đã ghi trong [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md):

1. **Tuân thủ `set_name.md`:** Đảm bảo các file tài liệu hay phân tích mới tạo tuân thủ chuẩn đặt tên trong [ai-skills/set_name.md](file:///d:/NCKH_3/ai-skills/set_name.md).
2. **Cập nhật `README.md`:** Đã cập nhật sơ đồ Cấu trúc Thư mục trong [README.md](file:///d:/NCKH_3/README.md) nếu có tạo file hoặc thư mục mới.
3. **Vệ sinh Repository:** Không commit các file tạm (`.tmp`, `.log`), bộ nhớ đệm hay tập dữ liệu thô dung lượng lớn (`.db`, `.sql` tại `C:/tawos/`).

---

## 📋 2. Kiểm tra Trạng thái Dự án (Git Status)

Mở terminal tại thư mục gốc dự án (`d:\NCKH_3`) và chạy:

```bash
git status
```

Lệnh này hiển thị:
* Nhánh hiện tại (mặc định là `main`).
* Danh sách các file đã chỉnh sửa (`modified`).
* Các file mới tạo chưa được Git theo dõi (`untracked`).

---

## ➕ 3. Thêm File vào Git Staging (Git Add)

### Cách 1: Thêm toàn bộ thay đổi hợp lệ (Khuyên dùng sau khi kiểm tra status)
```bash
git add .
```

### Cách 2: Thêm từng file hoặc thư mục cụ thể
```bash
# Thêm file tài liệu & quy tắc
git add README.md OVERVIEW.md ai-skills/ tutorial/

# Thêm kịch bản và dữ liệu phân tích
git add data/ paper-information/ requirements/ note_archive/
```

---

## 💾 4. Tạo Commit chuẩn hóa (Git Commit)

Sử dụng chuẩn **Conventional Commits** để tạo commit kèm thông điệp rõ ràng:

```bash
git commit -m "docs: cap nhat huong dan github_push.md trong thư muc tutorial"
```

### 🏷️ Các Tiền tố Commit Chuẩn:
* `docs:` — Cập nhật tài liệu (README, OVERVIEW, Hướng dẫn tutorial).
* `feat:` — Thêm tính năng, mô hình, hoặc kịch bản phân tích mới.
* `fix:` — Sửa lỗi code, đường dẫn hoặc pipeline xử lý dữ liệu.
* `refactor:` — Tái cấu trúc thư mục/mã nguồn mà không đổi tính năng.

---

## 🔄 5. Đồng bộ Code mới từ Remote về Local (Git Pull)

Để tránh xung đột code khi có thành viên khác vừa push:

```bash
git pull origin main --rebase
```

*(Nếu xảy ra conflict, mở file bị xung đột để giải quyết, chạy `git add <file>` rồi tiếp tục `git rebase --continue`).*

---

## 📤 6. Push Code lên GitHub (Git Push)

Đẩy các commit local lên nhánh `main` trên GitHub:

```bash
git push origin main
```

---

## 🔑 7. Xử lý Lỗi Xác thực (Authentication & PAT Token)

Nếu gặp lỗi `403 Access Denied` hoặc `Authentication failed for 'https://github.com/...'`:

### Cách cập nhật Personal Access Token (PAT):
1. Truy cập GitHub: **Settings > Developer Settings > Personal Access Tokens (classic)**.
2. Tạo token mới (chọn scope `repo`).
3. Chạy lệnh cập nhật URL remote có chứa PAT mới:
   ```bash
   git remote set-url origin https://<YOUR_GITHUB_USERNAME>:<YOUR_NEW_PAT_TOKEN>@github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git
   ```
4. Thực hiện push lại:
   ```bash
   git push origin main
   ```

---

## 🛠️ 8. Tóm tắt Chuỗi Lệnh Nhanh (Quick Cheat Sheet)

```bash
# 1. Kiểm tra trạng thái
git status

# 2. Thêm file
git add .

# 3. Tạo commit
git commit -m "feat: cap nhat tinh nang moi"

# 4. Pull & Rebase đồng bộ
git pull origin main --rebase

# 5. Push lên GitHub
git push origin main
```

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
