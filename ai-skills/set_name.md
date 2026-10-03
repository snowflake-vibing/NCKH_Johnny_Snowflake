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

## 📋 4. Quy tắc Đặt tên File Phân tích Yêu cầu (`requirements/`)

Tất cả các file phân tích yêu cầu và đối chiếu sản phẩm nằm trong thư mục `requirements/` **bắt buộc phải đặt tên theo định dạng:**

```text
Requirements_[X].md
```

* Trong đó `[X]` đại diện cho tên hoặc mã số chủ đề phân tích yêu cầu (ví dụ: `Requirements_1_Task_Definition.md`, `Requirements_2_Dataset_and_Leakage_Control.md`, `Requirements_3_Model_Replication_and_Evaluation.md`, `Requirements_4_Github_Gap_Analysis_and_Roadmap.md`).
* **Mô tả đối chiếu:** Mỗi file `Requirements_[X].md` phải đối chiếu trực tiếp giữa **Yêu cầu NCKH** (từ `Huong 3 b2.pdf` và `Research_Nhom_3.pdf`) với **Thực trạng Sản phẩm/Mã nguồn trên GitHub repository**.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
