# 🏷️ Quy tắc Đặt tên File Phân tích Bài báo Khoa học (Paper Naming Convention Rule)

> **Tài liệu này quy định chuẩn đặt tên file và cấu trúc trình bày nội dung cho tất cả các file phân tích / ghi chú bài báo khoa học (Literature Notes) thuộc dự án NCKH.**

---

## 📌 1. Quy tắc Đặt tên File (File Naming Standard)

Tất cả các file phân tích bài báo trong thư mục `paper-information/` phải tuân thủ đúng cú pháp chuẩn sau:

### 🔹 Cú pháp Tổng quát (General Format)
```text
paper_<tác_giả_chính>_<năm>_<từ_khóa_chủ_đề>.md
```

### 📏 Các Nguyên tắc Bắt buộc:
1. **Viết thường toàn bộ (Lowercase):** Không sử dụng chữ in hoa.
2. **Dấu phân cách:** Sử dụng dấu gạch dưới `_` giữa các từ. Tuyệt đối **không dùng khoảng trắng (space)** hoặc ký tự đặc biệt (`&`, `@`, `#`, `?`, `/`, `\`).
3. **Tên tác giả:** Lấy họ (last name) của tác giả chính (first author). Nếu là tài liệu nhóm/nội bộ thì dùng mã định danh (`nhom3`, `uit`).
4. **Năm xuất bản:** Viết đủ 4 chữ số (ví dụ: `2022`, `2023`, `2024`, `2026`).
5. **Từ khóa chủ đề (Short Keyword):** 1-3 từ thể hiện tên mô hình hoặc đóng góp cốt lõi (ví dụ: `gpt2sp`, `deep_se`, `sbert_gbt`, `leakage`, `replication`).

---

## 📚 2. Bảng Danh mục Ánh xạ Chuẩn (Standard File Mapping)

| File PDF Gốc (`note_archive/`) | File Phân tích `.md` (`paper-information/`) | Tác giả & Năm | Chủ đề Cốt lõi |
| :--- | :--- | :--- | :--- |
| `2201.05401v2.pdf` | `paper_tawosi_2022_replication.md` | Tawosi et al. (2022) | Replication & Extension study của Deep-SE |
| `paper_gpt2sp.pdf` | `paper_fu_2023_gpt2sp.md` | Fu & Tantithamthavorn (2023) | GPT2SP Transformer-based effort estimation |
| `paper_deep-learning.pdf` | `paper_choetkiertikul_2019_deep_se.md` | Choetkiertikul et al. (2019) | Deep-SE baseline model |
| `paper_SBERT&GPT.pdf` | `paper_yalciner_2024_sbert_gbt.md` | Yalçıner et al. (2024) | SBERT + Gradient Boosted Trees |
| `paper_TBE&ERM.pdf` | `paper_wijaya_2024_tbe_erm.md` | Wijaya et al. (2024) | Transformer Embeddings + Ensemble Regression |
| `mmc2.pdf` / `literature_note_mmc2.md` | `paper_kapoor_2023_leakage.md` | Kapoor & Narayanan (2023) | Data Leakage & Reproducibility crisis (Patterns) |
| `Research_Nhom_3.pdf` | `paper_nhom3_2026_research_report.md` | Nhóm 3 (2026) | Báo cáo NCKH Lần 2 (Ước lượng SP kiểm soát Leakage) |
| `Hop lan 1.pdf` | `paper_uit_2026_intro_nckh.md` | ThS/TS. Tạ Việt Phương (2026) | Tài liệu định hướng & Nhập môn NCKH |
| `Huong 3 b2.pdf` | `paper_uit_2026_huong3_plan.md` | ThS/TS. Tạ Việt Phương (2026) | Tài liệu Kế hoạch Hướng 3 (Agile SP Estimation) |

---

## 📑 3. Cấu trúc Trình bày Nội dung Bắt buộc (Markdown Template)

Mỗi file phân tích bài báo `.md` phải bảo đảm chứa đầy đủ các mục chuẩn sau:

1. **Header & Tiêu đề bài báo**
2. **Bảng Thước đo Tiêu chuẩn (Table Matrix)**
3. **Thông tin Trích dẫn (Citation & Metadata)**
4. **Đặt Bài toán & Mục tiêu Nghiên cứu (Problem & Goal)**
5. **Dữ liệu & Phương pháp Thực nghiệm (Dataset & Methodology)**
6. **Kết quả & Đóng góp Chính (Results & Takeaways)**
7. **Giá trị Thực tiễn cho Đề tài NCKH của Nhóm (Team Application)**

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
