# 📋 Requirements_3: Phân tích Tái lập Mô hình & Đánh giá (Model Reproduction & Evaluation)

> **Tài liệu đối chiếu Yêu cầu NCKH về Tái lập Mô hình (GPT2SP) & Đánh giá Thống kê giữa Hướng dẫn NCKH (`Huong 3 b2.pdf`, `Research_Nhom_3.pdf`) và Sản phẩm trên GitHub Repository.**

---

## 🎯 1. Bảng Đối chiếu Yêu cầu Tái lập & Mô hình hóa

| Yêu cầu NCKH (`Huong 3 b2.pdf` & `Research_Nhom_3.pdf`) | Nội dung Chi tiết Yêu cầu | Thực trạng trên GitHub Repository (`NCKH_Johnny_Snowflake`) | Đánh giá Trạng thái |
| :--- | :--- | :--- | :---: |
| **Reproduction Candidate Selection** | Chọn 1 mô hình từ bài báo công bố để tái lập: Mô hình **GPT2SP** (Fu & Tantithamthavorn, IEEE TSE 2023). | Đã chọn bài báo GPT2SP và đưa vào phân tích tài liệu tại [paper-information/paper_fu_2023_gpt2sp.md](file:///d:/NCKH_3/paper-information/paper_fu_2023_gpt2sp.md). | ✅ **Đã đáp ứng (Done)** |
| **Dữ liệu Thử nghiệm Tái lập** | Dự án **Spring XD** (3.526 issues; Chia 60/20/20 Chronological: 2.115 train / 705 val / 706 test). | Đã hoàn thành chia tập dữ liệu và chạy lại trên checkpoint `MickyMike/0-GPT2SP-springxd`. | ✅ **Đã đáp ứng (Done)** |
| **Báo cáo Kết quả Tái lập (Replication Report)** | Ghi nhận trung thực sai lệch kết quả giữa bài báo (MAE = 0.96) và chạy lại thực tế (MAE = 1.7330), phân tích nguyên nhân khác biệt. | Đã công bố bảng so sánh chi tiết và phân tích nguyên nhân lệch kết quả trong [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Mục 4). | ✅ **Đã đáp ứng (Done)** |
| **Thiết lập 2 Setting Thử nghiệm** | So sánh hiệu năng mô hình trên 2 setting: **Final Snapshot** vs **Planning-Time Snapshot** trên cùng issue/split. | Đã lập khung thử nghiệm trong Roadmap tại [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) (Mục 5). | ⚠️ **Đang phát triển (In Progress)** |
| **Bộ Mô hình Baseline & Advanced** | Chạy Baseline (Median effort, Mean effort, TF-IDF + Ridge) và Advanced Models (GPT2SP, SBERT + GBT). | Phân tích bài báo baseline Deep-SE, SBERT-GBT tại thư mục [paper-information/](file:///d:/NCKH_3/paper-information/). | ⚠️ **Đang phát triển (In Progress)** |
| **Đánh giá Thống kê (Statistical Evaluation)** | Báo cáo MAE, MdAE, SA, kiểm định ý nghĩa thống kê Wilcoxon Rank-Sum Test, Vargha-Delaney $\hat{A}_{12}$ effect size, Bootstrap 95% CI. | Quy chuẩn đánh giá thống kê đã được đưa vào [OVERVIEW.md](file:///d:/NCKH_3/OVERVIEW.md) và [ai-skills/RULE.md](file:///d:/NCKH_3/ai-skills/RULE.md). | ⚠️ **Đang phát triển (In Progress)** |

---

## 🧪 2. Bảng So sánh Kết quả Tái lập GPT2SP (Spring XD Project)

| Chỉ số / Metric | Báo cáo Paper (Fu et al., 2023) | Kết quả Chạy lại (Nhóm 3) | Đánh giá & Ghi nhận |
| :--- | :---: | :---: | :--- |
| **Số lượng Rows** | 3.526 | 3.526 | ✅ Khớp 100% |
| **Split (Train/Val/Test)** | 2.115 / 705 / 706 | 2.115 / 705 / 706 | ✅ Khớp 100% |
| **Median Baseline MAE** | `1,72` | `1,7153` | ✅ Khớp (sau làm tròn) |
| **GPT2SP Checkpoint MAE** | `0,96` | `1,7330` | ⚠️ **Partial Reproduction** (Chưa khớp) |
| **GPT2SP MdAE** | N/A | `1,2994` | 📝 Ghi nhận bổ sung |
| **Cải thiện so với Median** | ~44.2% | -1.03% | 🔍 Kém hơn Median baseline trên checkpoint công khai |

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
