# 📘 CẨM NANG THỰC HIỆN TOÀN DIỆN QUY TRÌNH 4 BƯỚC TRÊN KAGGLE
## ĐỀ TÀI: AGILE STORY POINT ESTIMATION AT PLANNING TIME WITH TEMPORAL & DATA LEAKAGE CONTROL
### MỤC TIÊU: HOÀN TẤT THỰC NGHIỆM & SỐ LIỆU CHO BÀI BÁO HỘI NGHỊ WSESE (ICSE)

> **Nhóm nghiên cứu:** Lê Thành Hiệu (`24520496`), Phan Ngọc Đức Huy (`24520695`) — UIT, VNU-HCM  
> **Giảng viên hướng dẫn:** ThS/TS. Tạ Việt Phương  
> **Địa bàn thực nghiệm:** Nền tảng điện toán đám mây **Kaggle Notebooks**

---

## 🧭 TỔNG QUAN KIẾN TRÚC & PHÂN BỔ TÀI NGUYÊN (KAGGLE WORKFLOW)

Quy trình gồm **4 bước logic** được phân bổ thông minh trên Kaggle để **tiết kiệm tối đa 30 giờ GPU/tuần** và cho phép 2 bạn làm việc song song:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [NOTEBOOK 1: GPU T4 x 2] (Bạn 1 phụ trách - ~15 phút)                                  │
│  ├── BƯỚC 1: Chạy GPT2SP 3 Setting (Setting 1: Title | Setting 2: Full | Setting 3: Clean)│
│  └── BƯỚC 3 (Phần B): Chạy vòng lặp 5 Seeds ngẫu nhiên ([42, 123, 456, 789, 2026])   │
│      └── XUẤT OUTPUT: predictions_gpt2sp_3settings.csv & multiseed_results.csv        │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [NOTEBOOK 2: CPU FREE] (Bạn 2 phụ trách - ~30 giây)                                    │
│  ├── BƯỚC 2: RQ3 - Cài bộ lọc Porru et al. (2016) so với Planning-Time Snapshot       │
│  └── BƯỚC 3 (Phần A): Phân tích độ nhạy mốc vào Sprint (SP_Estimation_Date vs Sprint) │
│      └── XUẤT OUTPUT: porru_vs_snapshot_rq3.csv & sprint_sensitivity_analysis.csv     │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [TỔNG HỢP KIỂM ĐỊNH THỐNG KÊ] (Chạy trên Notebook 1 hoặc 2 - ~5 giây)                 │
│  └── BƯỚC 4: Chạy kiểm định Wilcoxon Signed-Rank Test + Vargha-Delaney Â12 + Holm FWER│
│      └── XUẤT OUTPUT CUỐI CÙNG: wsese_final_statistical_table.csv (Cho Paper Draft)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ BƯỚC 1: CHẠY GPT2SP 3 SETTING TRÊN GPU (NOTEBOOK 1)

### 1. Cấu hình Notebook 1 trên Kaggle
1. Vào [Kaggle](https://www.kaggle.com) $\rightarrow$ Nhấn **`Create`** $\rightarrow$ **`New Notebook`**.
2. Đổi tên thành: `GPT2SP-SpringXD-3Settings-GPU`.
3. Cột bên phải (**Notebook options**):
   - **Accelerator:** Chọn **`GPU T4 x 2`**.
   - **Internet:** Bật **`On`** *(để tải pretrained checkpoint từ Hugging Face)*.

### 2. Định nghĩa 3 Settings đối chứng
* **Setting 1 (Repo Baseline):** `Title only` (`SEQUENCE_LEN = 20`, checkpoint tác giả `MickyMike/0-GPT2SP-springxd`).
* **Setting 2 (Paper Grounded):** `Title + Description` (`SEQUENCE_LEN = 128`, đối chiếu Mục 3.1 & 4.1 bài báo IEEE TSE).
* **Setting 3 (Planning-Time Snapshot):** `Clean_Title + Clean_Description` do nhóm tái dựng tại đúng `SP_Estimation_Date`.

### 3. File code thực thi
👉 Toàn bộ mã nguồn tự động của Bước 1 nằm tại: [`kaggle/notebook_1_gpu_gpt2sp_3settings_multiseed.py`](notebook_1_gpu_gpt2sp_3settings_multiseed.py).  
Bạn chỉ cần mở file đó, copy toàn bộ nội dung dán vào Kaggle Notebook 1 và nhấn **Run All**.

---

## 🔍 BƯỚC 2: RQ3 — CÀI TIÊU CHÍ LỌC PORRU ET AL., SO VỚI SNAPSHOT (NOTEBOOK 2)

### 1. Cấu hình Notebook 2 trên Kaggle
1. Nhấn **`Create`** $\rightarrow$ **`New Notebook`**.
2. Đổi tên thành: `RQ3-Porru-Filter-Snapshot-CPU`.
3. Cột bên phải: **Accelerator:** Để nguyên **`None` (CPU miễn phí không giới hạn giờ)**.

### 2. Bản chất phương pháp luận của RQ3
* Tiêu chí lọc **Porru et al. (PROMISE 2016)**:
  - Điểm Story Point hợp lệ: $SP > 0$ và $SP \le 100$.
  - Loại bỏ các issue bị khuyết `Description` (missing description).
  - Chỉ giữ các loại issue chuẩn: *Story, Bug, Improvement, Task, New Feature*.
  - Issue phải ở trạng thái hoàn tất (*Resolved / Closed*).
* **Vấn đề cốt lõi:** Khi áp dụng các tiêu chí này trên dữ liệu tĩnh (*Final Snapshot*), có tới **566 issues (16.0%) bị sửa Description** và **402 issues (11.3%) bị đổi Story Point** sau ngày ước lượng ban đầu!
* **So sánh đối chứng:**
  - **Tập Porru Final Snapshot:** Chứa thông tin bị rò rỉ sau khi làm xong issue.
  - **Tập Planning-Time Snapshot (Nhóm 3):** Trạng thái nguyên bản được truy vết từ `tawos.db` tại đúng mốc `SP_Estimation_Date`.

### 3. File code thực thi
👉 Toàn bộ mã nguồn tự động của Bước 2 nằm tại: [`kaggle/notebook_2_cpu_porru_rq3_sprint_sensitivity.py`](notebook_2_cpu_porru_rq3_sprint_sensitivity.py).  
Dán vào Notebook 2 và bấm **Run All** (chạy mất khoảng 5 giây).

---

## 📈 BƯỚC 3: PHÂN TÍCH ĐỘ NHẠY (SENSITIVITY ANALYSIS)

Bước 3 gồm 2 phần được chia sẻ giữa 2 notebook:

### Phần A: Độ nhạy theo mốc thời gian vào Sprint (Sprint Entry Cut-off) — Chạy trên Notebook 2
* So sánh sai lệch giữa 2 mốc ranh giới:
  1. `SP_Estimation_Date` (thời điểm lần đầu gán Story Point tại buổi Backlog Refinement).
  2. `Sprint_Entry_Date` (thời điểm issue chính thức được kéo vào Sprint Backlog).
* Đánh giá lượng thông tin phát sinh và độ ổn định của dữ liệu giữa 2 mốc này.

### Phần B: Độ nhạy theo Đa hạt giống ngẫu nhiên (Multi-seed Robustness) — Chạy trên Notebook 1
* Đánh giá trên 5 random seeds: `[42, 123, 456, 789, 2026]`.
* Báo cáo kết quả:
  $$\text{MAE} = \mu \pm \sigma \quad \text{và} \quad \text{MdAE} = \text{median} \pm \text{IQR}$$
* Chứng minh mô hình đạt tính ổn định vững chắc, không bị phụ thuộc vào một seed may mắn trước hội đồng phản biện WSESE.

---

## 🎯 BƯỚC 4: KIỂM ĐỊNH THỐNG KÊ WILCOXON, $\hat{A}_{12}$, VÀ HOLM-BONFERRONI

Sau khi có file dự đoán từ Bước 1 và Bước 2, Bước 4 chạy bộ ba kiểm định thống kê chuẩn quốc tế:

1. **Wilcoxon Signed-Rank Test (Two-sided):** Đo ý nghĩa thống kê của sai số dự báo giữa các mô hình ($p < 0.05$).
2. **Vargha-Delaney Effect Size ($\hat{A}_{12}$):** Đo lường độ lớn hiệu ứng thực tế:
   - $|\hat{A}_{12} - 0.5| < 0.06$: **Negligible**
   - $0.06 \le |\hat{A}_{12} - 0.5| < 0.14$: **Small**
   - $0.14 \le |\hat{A}_{12} - 0.5| < 0.21$: **Medium**
   - $|\hat{A}_{12} - 0.5| \ge 0.21$: **Large**
3. **Holm-Bonferroni Correction:** Hiệu chỉnh $p$-value khi kiểm định nhiều cặp giả thuyết đồng thời để loại bỏ False Positive.

👉 File code tự động của Bước 4 nằm tại: [`kaggle/notebook_3_statistical_tests_wilcoxon_a12_holm.py`](notebook_3_statistical_tests_wilcoxon_a12_holm.py).

---

## 📥 DANH MỤC FILE KẾT QUẢ CẦN TẢI VỀ TỪ KAGGLE OUTPUT

Sau khi hoàn thành, trong thư mục `/kaggle/working/` bạn tải về các file sau:
1. `predictions_gpt2sp_3settings.csv` (File lưu sai số từng mẫu của 3 setting).
2. `multiseed_results.csv` (Bảng thống kê Mean ± Std qua 5 seeds).
3. `porru_vs_snapshot_rq3.csv` (Bảng so sánh phân phối và tỷ lệ rò rỉ RQ3).
4. `sprint_sensitivity_analysis.csv` (Phân tích chênh lệch mốc vào sprint).
5. `wsese_final_statistical_table.csv` (Bảng tổng hợp cuối cùng để đưa thẳng vào Paper Draft).
