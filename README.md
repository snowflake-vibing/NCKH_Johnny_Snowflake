# 📘 Dự báo Story Point tại Thời điểm Lập kế hoạch Agile với Kiểm soát Rò rỉ Dữ liệu

> **Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control**

[![Study](https://img.shields.io/badge/Research-NCKH_2026-blue.svg)](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)
[![Dataset](https://img.shields.io/badge/Dataset-TAWOS_v1.1-orange.svg)](https://github.com/SOLAR-group/TAWOS)
[![Domain](https://img.shields.io/badge/Domain-Software_Engineering_&_Agile-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Thông tin Đề tài & Nhóm Nghiên cứu

- **Đơn vị thực hiện:** Khoa Hệ thống Thông tin — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNUHCM)
- **Giảng viên hướng dẫn:** ThS/TS. Tạ Việt Phương
- **Thành viên nhóm (Nhóm 3):**
  1. **Phan Ngọc Đức Huy** — MSSV: `24520695`
  2. **Lê Thành Hiệu** — MSSV: `24520496`

---

## 🎯 1. Bối cảnh & Vấn đề Nghiên cứu (Introduction & Problem Statement)

Trong quy trình **Agile / Scrum**, việc ước lượng nỗ lực (Story Point) giúp đội phát triển đánh giá độ phức tạp tương đối của công việc trong buổi họp _Sprint Planning_. Tuy nhiên, hầu hết các nghiên cứu học máy (Machine Learning/Deep Learning) hiện nay như _Deep-SE_, _GPT2SP_, _SBERT + GBT_ đều sử dụng dữ liệu tĩnh dạng **Final Snapshot** — tức dữ liệu được thu thập sau khi issue đã hoàn thành và đóng lại.

### 🔴 Nguy cơ Rò rỉ Thông tin Tương lai (Future-Information / Temporal Leakage):

- Sau buổi họp planning, title và description của Jira issue thường xuyên được lập trình viên bổ sung nguyên nhân lỗi, giải pháp kỹ thuật, stack trace hoặc tên module chi tiết.
- Nếu huấn luyện mô hình trên dữ liệu sau khi hoàn thành, mô hình sẽ nhìn thấy thông tin mà nhóm phát triển **chưa thể có tại thời điểm ước lượng**.
- Điều này dẫn đến độ chính xác biểu kiến tăng ảo (overoptimistic results) nhưng hoàn toàn mất tính khả thi khi triển khai hỗ trợ thực tế trong Sprint Planning.

---

## 🔍 2. Định nghĩa Bài toán (Task Formulation)

| Thành phần                  | Định nghĩa của Nhóm Nghiên cứu                                                                                                                                                                    |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Problem**                 | Hỗ trợ ước lượng nỗ lực trong Sprint Planning và loại bỏ triệt để sai lệch do thông tin phát sinh sau planning (_Temporal Leakage_).                                                              |
| **Target User**             | Scrum Team (Developers, Product Owner, Scrum Master) dùng kết quả làm căn cứ tham khảo thảo luận.                                                                                                 |
| **Unit of Analysis**        | Một Jira Issue / User Story đủ điều kiện được chấm Story Point.                                                                                                                                   |
| **Prediction Task**         | Bài toán **Supervised Regression** dự báo một giá trị Story Point (dạng số thực/điểm tương đối).                                                                                                  |
| **Estimation Time**         | Mốc `SP_Estimation_Date` (thời điểm Story Point lần đầu được điền).                                                                                                                               |
| **Ground Truth**            | Initial Story Point tại mốc estimation. Khôi phục giá trị ban đầu từ `CHANGELOG` nếu bị sửa đổi sau đó.                                                                                           |
| **Input Available**         | Title, Description, Issue Type, Priority, Components tại thời điểm **không muộn hơn** `SP_Estimation_Date`. _(Cấm dùng: Status=Closed, Resolution Date, Comments phát sinh, Assignee tương lai)_. |
| **Nghiên cứu Cốt lõi (RQ)** | _Việc dựng lại trạng thái Jira issue đúng tại `SP_Estimation_Date` làm thay đổi độ chính xác được báo cáo của mô hình dự báo như thế nào so với Final Snapshot?_                                  |

---

## 📊 3. Dữ liệu & Kết quả Phân tích EDA (TAWOS Dataset v1.1)

Nguồn dữ liệu thực nghiệm là **TAWOS Dataset v1.1** (SOLAR Research Group - UCL) gồm **458.232 issues** thuộc **39 dự án** và **12 Jira Repositories**.

### 💡 Key EDA Insights & Bằng chứng Rò rỉ Dữ liệu:

1. **Độ phủ Story Point:**
   - **63.011 issues** (chiếm `13,75%`) thực sự được chấm Story Point.
   - **395.221 issues** (`86,25%`) không được chấm điểm (các task quản lý lỗi hàng ngày) $\rightarrow$ Cần lọc bỏ population không phù hợp.
2. **Độ khuyết văn bản:**
   - `29.128 issues` (`6,36%`) bị thiếu trường Description.
3. **Minh chứng Rò rỉ Thông tin Tương lai trong Dữ liệu thực tế:**
   - **11.969 issues** (tương đương `~19%` số issue có Story Point) bị thay đổi nội dung văn bản (title/description) sau thời điểm estimation.
   - Tổng cộng **51.485 lượt thay đổi văn bản** diễn ra sau khi estimate.
   - **Trung vị độ trễ:** `2,30 ngày` (`55,30 giờ`). Trong đó:
     - `25%` lượt thay đổi xảy ra nhanh trong vòng `0,38 giờ`.
     - **14.883 lượt thay đổi** diễn ra trong **chưa đầy 1 giờ** sau khi họp estimate.
     - `75%` lượt thay đổi kéo dài tới `34,88 ngày`.

> ⚠️ **Kết luận EDA:** Future-Information Leakage là nguy cơ thực tế có quy mô rất lớn trong dữ liệu Jira, không phải giả định lý thuyết.

---

## 🧪 4. Kết quả Tái lập Nghiên cứu Cơ sở (Artifact Reproduction — GPT2SP)

Nhóm đã thực hiện tái lập một phần kết quả của bài báo công bố trên **IEEE TSE 2023**:

> _Fu & Tantithamthavorn (2023), "GPT2SP: A Transformer-Based Agile Story Point Estimation Approach"_

- **Tập dữ liệu thử nghiệm:** Project **Spring XD** (3.526 issues; Chia 60/20/20 chronological: `2.115 train` / `705 val` / `706 test`).
- **Môi trường:** Google Colab Tesla T4, PyTorch 2.11.0, Transformers 4.39.3, Checkpoint `MickyMike/0-GPT2SP-springxd`.

### Bảng So sánh Kết quả Tái lập:

| Chỉ số / Metric             |   Kết quả Paper   | Chạy lại (Replication) | Đánh giá Trạng thái                        |
| :-------------------------- | :---------------: | :--------------------: | :----------------------------------------- |
| **Dataset rows**            |       3.526       |         3.526          | ✅ Khớp hoàn toàn                          |
| **Train/Val/Test Split**    | 2.115 / 705 / 706 |   2.115 / 705 / 706    | ✅ Khớp hoàn toàn                          |
| **Median Baseline MAE**     |      `1,72`       |        `1,7153`        | ✅ Khớp (sau làm tròn)                     |
| **GPT2SP Checkpoint MAE**   |      `0,96`       |        `1,7330`        | ⚠️ Chưa khớp (Partial Reproduction)        |
| **GPT2SP MdAE**             |        N/A        |        `1,2994`        | 📝 Ghi nhận bổ sung                        |
| **Cải thiện so với Median** |      ~44.2%       |         -1.03%         | 🔍 Kém hơn Median baseline trên checkpoint |

#### 📌 Phân tích nguyên nhân sai lệch:

1. **Khác biệt Input:** Bài báo mô tả kết hợp `Title + Description`, nhưng Notebook/Artifact công khai của tác giả chỉ dùng riêng `Title` (`max_length=20`).
2. **Khác biệt Môi trường:** Thay đổi về phiên bản thư viện Transformer/PyTorch ảnh hưởng đến pooling, padding và serialization checkpoint.
3. **Nguyên tắc khoa học:** Nhóm ghi nhận trung thực sai lệch này dưới dạng **Partial Reproduction**, làm tiền đề cho các thí nghiệm tự huấn luyện lại từ đầu.

---

## 🗺️ 5. Lộ trình Thực nghiệm (Methodology & Roadmap)

```mermaid
flowchart LR
    A["1. Chuẩn hóa Timestamp (UTC)"] --> B["2. Xác minh CHANGELOG Mapping"]
    B --> C["3. Dựng Historical Snapshot (State Reconstruction)"]
    C --> D["4. Chốt Clean Population & Initial SP"]
    D --> E["5. Thiết lập 2 Settings: Final vs Planning-Time"]
    E --> F["6. Run Baselines (Median, Mean, TF-IDF)"]
    F --> G["7. Evaluated & Deep Models (GPT2SP, SBERT-GBT)"]
```

| Bước  | Công việc                | Kết quả Cần có                                                                  |
| :---: | :----------------------- | :------------------------------------------------------------------------------ |
| **1** | Chuẩn hóa Timestamp      | Chuyển UTC, sửa lỗi parse năm bất thường, lọc `estimation < created`.           |
| **2** | Xác minh Change_Log      | Chuẩn hóa field name cho summary/title/description và Story Point.              |
| **3** | Dựng Historical Snapshot | Reconstruct từng field tại `SP_Estimation_Date`, kiểm thử bằng case history.    |
| **4** | Chốt Population          | Lọc issue có Initial SP hợp lệ và đầy đủ input tại thời điểm estimation.        |
| **5** | Tạo 2 Setting Thử nghiệm | So sánh **Final Snapshot** vs **Planning-Time Snapshot** trên cùng issue/split. |
| **6** | Chạy Baseline            | Median, Mean, Random và TF-IDF baseline trước khi chạy mô hình sâu.             |
| **7** | Đánh giá Thống kê        | MAE / MdAE / SA theo từng project, tính Bootstrap CI và paired test.            |
| **8** | Mô hình Mở rộng          | Huấn luyện lại GPT2SP và SBERT-GBT trên pipeline kiểm soát leakage.             |

---

## 📂 6. Cấu trúc Thư mục Dự án (Project Structure)

```text
.
├── .agents/                  # Kỹ năng và công cụ mở rộng dành cho AI Agent
├── data/                     # Dữ liệu nghiên cứu theo các tầng xử lý
│   ├── raw/                  # Dữ liệu thô (CSDL TAWOS gốc, bản trích xuất Jira thô)
│   └── clean/                # Dữ liệu sau tiền xử lý & kiểm soát rò rỉ (Reconstructed Snapshot)
├── docs/                     # Toàn bộ tài liệu nghiên cứu khoa học của đề tài
│   ├── articles/             # Quản lý bài báo khoa học & số hóa tri thức
│   │   ├── paper-information/# Phân tích chi tiết từng bài báo (kết hợp ma trận 21 trường)
│   │   │   ├── template.md
│   │   │   ├── paper_choetkiertikul_2019_deep_se.md
│   │   │   ├── paper_fu_2023_gpt2sp.md
│   │   │   ├── paper_khan_2025_comparative_learning.md
│   │   │   ├── paper_tawosi_2022_replication.md
│   │   │   ├── paper_wijaya_2024_tbe_erm.md
│   │   │   └── paper_yalciner_2024_sbert_gbt.md
│   │   ├── *.pdf             # Bản sao file PDF gốc của các bài báo khoa học
│   │   └── README.md         # Quy trình quản lý & bảng tra cứu bài báo
│   ├── draft/                # Thư mục lưu trữ các bản thảo nghiên cứu (Work-in-progress drafts)
│   ├── glossary/             # Thư mục bảng thuật ngữ nội bộ (được bỏ qua khi push git)
│   ├── reproduction-candidate/ # Ứng viên tái lập & hệ thống chấm điểm định lượng
│   │   ├── candidate_fu_2023_gpt2sp.md
│   │   ├── candidate_khan_2025_comparative_learning.md
│   │   ├── candidate_tawosi_2022_replication.md
│   │   └── reproduction-score.md # Đánh giá 3 ứng viên theo thang điểm 100
│   ├── notes/                # Biên bản họp nhóm & ghi chú định hướng
│   └── reports/              # Báo cáo đề tài NCKH chính thức
├── notebooks/                # Jupyter Notebooks phục vụ phân tích & thực nghiệm
├── .gitignore                # Cấu hình loại trừ file rác, dữ liệu lớn, model weights & glossary
├── AGENTS.md                 # Quy tắc và hướng dẫn làm việc cho AI Agent
└── README.md                 # Cổng thông tin chính & tổng quan đề tài
```

### 📋 Mô tả Vai trò các Thư mục Chính:

- **`data/`**: Phân chia rõ ràng giữa dữ liệu nguyên bản (`raw/`) và dữ liệu đã kiểm soát rò rỉ thời gian (`clean/`) nhằm đảm bảo tính tái lập (reproducibility).
- **`docs/`**: Kho lưu trữ tri thức toàn diện của đề tài, bao gồm các bài báo gốc, ghi chú học thuật chuyên sâu, các ứng viên tái lập, bản thảo hội nghị và báo cáo tiến độ.
- **`notebooks/`**: Nơi lưu trữ các kịch bản tương tác phục vụ EDA, kiểm định giả thuyết thống kê và trực quan hóa phân phối dữ liệu.
- **`.agents/` & `AGENTS.md`**: Bộ quy tắc và các kỹ năng chuyên biệt giúp trợ lý AI làm việc chính xác, an toàn và tuân thủ chặt chẽ các giả định nghiên cứu khoa học.

---

## 🚀 7. Cài đặt & Bắt đầu (Quick Start & Usage)

### Yêu cầu Tiên quyết

- **Python:** `>= 3.9`
- **Jupyter Notebook / JupyterLab**
- **CSDL TAWOS:** Cơ sở dữ liệu SQLite hoặc MySQL từ [TAWOS Dataset](https://github.com/SOLAR-group/TAWOS) (cấu hình đường dẫn kết nối cục bộ trong notebook).

### Chạy Thử nghiệm EDA

1. Clone repository về máy:
   ```bash
   git clone https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake.git
   cd NCKH_Johnny_Snowflake
   ```
2. Cài đặt các gói phụ thuộc cơ bản:
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```
3. Khởi chạy Notebook EDA:
   ```bash
   jupyter notebook notebooks/EDA_TAWOS.ipynb
   ```

---

## 🤖 8. Quy tắc Phát triển & AI Workflow

Để đảm bảo tính nhất quán, bảo toàn nguyên tắc kiểm soát dữ liệu (_Temporal Leakage Control_) và giữ chuẩn mực làm việc giữa lập trình viên và trợ lý AI:

👉 **Xem chi tiết các quy tắc tại:** [AGENTS.md](AGENTS.md)

- **Nguyên tắc cốt lõi:**
  1. **Tuân thủ quy tắc làm việc:** Mọi chỉnh sửa mã nguồn, truy vấn CSDL hay xử lý dữ liệu đều tuân thủ nguyên tắc nghiên cứu khoa học.
  2. **Cập nhật cây thư mục:** Khi thêm file/thư mục mới, luôn cập nhật lại mục _Cấu trúc Thư mục_ trong `README.md`.
  3. **Bảo toàn mốc thời gian:** Tuyệt đối không dùng các trường dữ liệu sinh ra sau mốc `SP_Estimation_Date`.

---

## 📚 9. Nguồn Tham khảo Chính (References)

1. **Tawosi et al. (2022)** — _Agile Effort Estimation: Have We Solved the Problem Yet? Insights From a Replication Study_, IEEE Transactions on Software Engineering (TSE). DOI: `10.1109/TSE.2022.3204902`.
2. **Fu & Tantithamthavorn (2023)** — _GPT2SP: A Transformer-Based Agile Story Point Estimation Approach_, IEEE Transactions on Software Engineering (TSE). DOI: `10.1109/TSE.2022.3158252`.
3. **Kapoor & Narayanan (2023)** — _Leakage and the Reproducibility Crisis in Machine-Learning-Based Science_, Patterns. DOI: `10.1016/j.patter.2023.100804`.
4. **Pasuksmit et al. (2024)** — _A Systematic Literature Review on Reasons and Approaches for Accurate Effort Estimations in Agile_, arXiv:2405.01569.
5. **Choetkiertikul et al. (2019)** — _A Deep Learning Model for Estimating Story Points_, IEEE TSE.
6. **Yalciner et al. (2024)** — _Combining SBERT and Gradient Boosted Trees for Agile Effort Estimation_, IEEE Access.
7. **SOLAR Group TAWOS Dataset v1.1** — [GitHub Repository](https://github.com/SOLAR-group/TAWOS).

---

© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
