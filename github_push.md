# 🚀 Hướng dẫn Push Code lên GitHub (GitHub Push Guide)

> **Tài liệu hướng dẫn các bước chi tiết để kiểm tra, commit và push mã nguồn dự án `NCKH_Johnny_Snowflake` lên GitHub.**

---

## 📋 1. Kiểm tra Trạng thái Dự án (Git Status)

Mở terminal tại thư mục gốc dự án (`d:\NCKH_3`) và chạy lệnh:

```bash
git status
```

Lệnh này giúp bạn xem danh sách các file đã thay đổi (modified), file mới chưa được theo dõi (untracked), và nhánh hiện tại (branch).

---

## ➕ 2. Thêm các File vào Git Staging (Git Add)

### Cách 1: Thêm toàn bộ các file thay đổi & file mới
```bash
git add .
```

### Cách 2: Thêm từng file/thư mục cụ thể (Khuyên dùng)
```bash
# Thêm file tài liệu & quy tắc mới
git add README.md OVERVIEW.md ai-skills/ github_push.md

# Thêm mã nguồn hoặc kịch bản
git add skills/ resources/ output_b2/
```

> ⚠️ **Lưu ý:** Không `git add` các file tạm, file log rác (`.tmp`, `.log`), hoặc các file ảnh nháp không cần thiết.

---

## 💾 3. Tạo Commit (Git Commit)

Tạo commit kèm thông điệp mô tả rõ ràng các thay đổi (tuân thủ chuẩn Conventional Commits):

```bash
git commit -m "docs: cập nhật OVERVIEW.md, quy tắc ai-skills/RULE.md và hướng dẫn github_push.md"
```

**Các tiền tố commit phổ biến:**
* `docs:` — Cập nhật tài liệu (README, OVERVIEW, GUIDES).
* `feat:` — Thêm tính năng/mô hình/script mới.
* `fix:` — Sửa lỗi code hoặc pipeline xử lý dữ liệu.
* `refactor:` — Cấu trúc lại code mà không thay đổi tính năng.

---

## 🔄 4. Cập nhật Code mới từ Remote về Local (Git Pull)

Trước khi push, luôn đảm bảo local của bạn đồng bộ với nhánh remote:

```bash
git pull origin main --rebase
```

*(Nếu có xung đột/conflict, giải quyết xung đột trước khi tiếp tục).*

---

## 📤 5. Push Code lên GitHub (Git Push)

Đẩy các commit lên nhánh `main` trên GitHub:

```bash
git push origin main
```

---

## 🔑 6. Giải quyết Lỗi Xác thực (Authentication Error)

Nếu GitHub yêu cầu đăng nhập hoặc báo lỗi `403 Access Denied` / `Authentication failed`:

### Trường hợp 1: Sử dụng Personal Access Token (PAT)
1. Truy cập GitHub: **Settings > Developer Settings > Personal Access Tokens > Tokens (classic)**.
2. Tạo token mới với quyền `repo` (Toàn quyền trên repository).
3. Sử dụng lệnh thiết lập URL remote có chứa PAT:
   ```bash
   git remote set-url origin https://<YOUR_GITHUB_USERNAME>:<YOUR_PAT_TOKEN>@github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git
   ```
4. Sau đó thực hiện lại: `git push origin main`.

### Trường hợp 2: Sử dụng SSH Key
1. Kiểm tra hoặc đổi URL remote sang SSH:
   ```bash
   git remote set-url origin git@github.com:snowflake-vibing/NCKH_Johnny_Snowflake.git
   ```
2. Thực hiện push: `git push origin main`.

---

## 🛠️ 7. Tóm tắt Chuỗi Lệnh Nhanh (Quick Cheat Sheet)

```bash
# Bước 1: Thêm thay đổi
git add .

# Bước 2: Commit
git commit -m "docs: cap nhat tai lieu va quy tac du an"

# Bước 3: Push
git push origin main
```

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
