# Dự báo Story Point tại Thời điểm Lập kế hoạch Agile với Kiểm soát Rò rỉ Thông tin Tương lai
> **Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control**

[![Study](https://img.shields.io/badge/Research-NCKH_2026-blue.svg)](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)
[![Dataset](https://img.shields.io/badge/Dataset-TAWOS_v1.1-orange.svg)](https://github.com/SOLAR-group/TAWOS)
[![Domain](https://img.shields.io/badge/Domain-Software_Engineering_&_Agile-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Thông tin Đề tài & Nhóm Nghiên cứu

* **Đơn vị thực hiện:** Khoa Hệ thống Thông tin — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNUHCM)
* **Báo cáo:** Báo cáo nghiên cứu lần 2 (2026)
* **Giảng viên hướng dẫn:** ThS/TS. Tạ Việt Phương
* **Thành viên nhóm (Nhóm 3):**
  1. **Phan Ngọc Đức Huy** — MSSV: `24520695`
  2. **Lê Thành Hiệu** — MSSV: `24520496`

---

## 📖 Tài liệu & Tổng quan Sản phẩm

Toàn bộ thông tin chi tiết về sản phẩm, bối cảnh nghiên cứu, định nghĩa bài toán, kết quả thống kê EDA, tái lập thử nghiệm (GPT2SP) và kế hoạch thực nghiệm (Roadmap) đã được chuyển sang tài liệu riêng:

👉 **Xem chi tiết tại:** [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md)

---

## 🤖 Quy tắc Phát triển & AI Workflow

Để đảm bảo tính nhất quán, kiểm soát rò rỉ thông tin dữ liệu (Temporal Leakage), giữ vệ sinh repository và quy trình làm việc chuẩn cho trợ lý AI:

👉 **Xem chi tiết các quy tắc tại:** [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md)

*Một số quy tắc cốt lõi:*
1. **Đọc `RULE.md` trước khi thao tác:** Mọi thao tác chỉnh sửa mã nguồn hay dữ liệu đều phải tuân thủ hướng dẫn trong `RULE.md`.
2. **Cập nhật `README.md` khi tạo file mới:** Mỗi khi tạo file hoặc thư mục mới, bắt buộc phải cập nhật sơ đồ Cấu trúc Thư mục Dự án bên dưới.
3. **Kiểm soát rò rỉ thông tin:** Tuyệt đối không dùng thông tin sau mốc `SP_Estimation_Date` khi huấn luyện mô hình.

---

## 📂 Cấu trúc Thư mục Dự án

```text
.
├── README.md                 # Cổng thông tin chính & Định tuyến repository
├── OVERVIEW.md               # Tài liệu chi tiết sản phẩm, EDA, kết quả & Roadmap
├── github_push.md            # Hướng dẫn chi tiết các bước push project lên GitHub
├── LICENSE                   # Giấy phép nguồn mở MIT
├── ai-skills/                # Quy tắc & hướng dẫn làm việc cho trợ lý AI
│   ├── RULE.md               # Các quy tắc phát triển, đồng bộ và kiểm soát dữ liệu
│   └── set_name.md           # Quy tắc đặt tên file phân tích bài báo khoa học
├── data/                     # Thư mục chứa kịch bản EDA (kết nối CSDL local C:/tawos)
│   ├── README.md             # Hướng dẫn quy trình thực thi EDA Notebook
│   └── EDA_TAWOS.ipynb       # Notebook phân tích trực quan hóa dữ liệu EDA
├── paper-information/        # Thư mục chứa các file phân tích bài báo khoa học (.md)
├── note_archive/             # Thư mục lưu trữ tài nguyên PDF/Word gốc
└── scratch/                  # Scripts thử nghiệm & kiểm tra dữ liệu
```

---

## 📚 Nguồn Tham khảo Chính

1. **Tawosi et al. (2022)** — *Agile Effort Estimation: Have We Solved the Problem Yet? Insights From a Replication Study*, IEEE TSE.
2. **Fu & Tantithamthavorn (2023)** — *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach*, IEEE TSE.
3. **Kapoor & Narayanan (2023)** — *Leakage and the Reproducibility Crisis in Machine-Learning-Based Science*, Patterns.

*(Chi tiết danh mục tài liệu tham khảo đầy đủ xem tại [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md))*

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
