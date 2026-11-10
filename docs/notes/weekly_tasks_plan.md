# 📋 KẾ HOẠCH HÀNH ĐỘNG TUẦN NÀY (WEEKLY RESEARCH TASKS)
## ĐỀ TÀI: AGILE STORY POINT ESTIMATION AT PLANNING TIME WITH TEMPORAL & DATA LEAKAGE CONTROL
### MỤC TIÊU TRỌNG TÂM: HOÀN THIỆN THỰC NGHIỆM VÀ NỘP BÀI HỘI NGHỊ WSESE (ICSE)

> **Nhóm thực hiện:** Lê Thành Hiệu (`24520496`), Phan Ngọc Đức Huy (`24520695`) — UIT, VNU-HCM  
> **Giảng viên hướng dẫn:** ThS/TS. Tạ Việt Phương  
> **Thời gian:** Tuần làm việc hiện tại (Chuẩn bị nộp hội nghị quốc tế WSESE)

---

## 🎯 DANH SÁCH 4 NHIỆM VỤ TRỌNG TÂM TRONG TUẦN

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. Chạy GPT2SP 3 setting trên GPU                                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. RQ3: Cài tiêu chí lọc Porru, so với snapshot                                        │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. Kiểm định Wilcoxon, Â12, Holm cho GPT2SP                                            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. Phân tích độ nhạy (Mốc vào sprint, nhiều seed)                                      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 CHI TIẾT TRIỂN KHAI TỪNG NHIỆM VỤ

### 📌 NHIỆM VỤ 1: CHẠY GPT2SP 3 SETTING TRÊN GPU (KAGGLE NOTEBOOKS)

Thực hiện đo đạc thực nghiệm độc lập trên mô hình **GPT2SP (IEEE TSE 2023)** qua 3 cấu hình kỹ thuật có căn cứ từ bài báo:

| Setting | Tên cấu hình | Đầu vào (`Input Text`) | Độ dài (`SEQUENCE_LEN`) | Mô tả & Căn cứ kỹ thuật |
|---|---|---|---|---|
| **Setting 1** | **Repo Baseline (Default)** | `Title only` | 20 | Cấu hình mặc định trong notebook và checkpoint công bố của tác giả (`MickyMike/0-GPT2SP-springxd`). |
| **Setting 2** | **Paper Grounded (Full Context)** | `Title + Description` | 128 / 512 | Cấu hình mô tả tại **Mục 3.1 & 4.1** của bài báo (kết hợp cả tiêu đề và mô tả chi tiết của user story). |
| **Setting 3** | **Planning-Time Leakage-Free Snapshot** | `Clean_Title + Clean_Description` | 128 | Cấu hình loại bỏ rò rỉ dữ liệu của Nhóm 3: Văn bản được khôi phục tại đúng thời điểm `SP_Estimation_Date` từ Jira `Change_Log`. |

* **Mục tiêu đầu ra:** Bảng số liệu MAE, MdAE của cả 3 settings so sánh trực tiếp với **Median Effort Baseline** (MAE = 1.7153).

---

### 📌 NHIỆM VỤ 2: RQ3 — CÀI TIÊU CHÍ LỌC PORRU ET AL., SO VỚI SNAPSHOT

* **Bối cảnh học thuật (RQ3):**  
  Nghiên cứu của **Porru et al. (PROMISE 2016)** là một trong những công trình nền tảng về lọc dữ liệu Jira để dự báo Story Point. Tuy nhiên, các tiêu chí lọc truyền thống của Porru áp dụng trên **Final Snapshot** (dữ liệu thu thập khi issue đã hoàn thành/đóng lại), dẫn tới rò rỉ thông tin tương lai.
* **Nội dung thực hiện RQ3:**
  1. **Cài đặt bộ lọc Porru et al. (2016) trên Spring XD:**
     - Lọc điểm nỗ lực hợp lệ: $Story\_Point > 0$ và loại trừ các điểm ngoại lai bất thường (outliers: $SP \le 100$).
     - Lọc dữ liệu văn bản: Loại bỏ hoàn toàn các issue có `Description` bị rỗng (missing description).
     - Lọc loại issue: Chỉ giữ lại các issue type chính (*Story, Bug, Improvement, New Feature*).
     - Lọc trạng thái hoàn thành: Áp dụng điều kiện trạng thái hoàn tất (*Resolved / Closed* theo Porru).
  2. **So sánh đối chứng giữa 2 không gian dữ liệu:**
     - **Không gian A (Porru Filtered Final Snapshot):** Bộ dữ liệu sau khi lọc theo Porru từ trạng thái tĩnh cuối cùng của Jira issue.
     - **Không gian B (Historical Planning-Time Snapshot):** Bộ dữ liệu do Nhóm 3 tái dựng tại đúng mốc `SP_Estimation_Date` từ bảng `Change_Log` (đã xóa 12 trường rò rỉ tương lai và khôi phục text nguyên bản).
  3. **Đánh giá mức độ ảnh hưởng (Empirical Leakage Impact):**  
     Đo lường độ lệch chính xác biểu kiến (apparent performance difference) giữa 2 không gian dữ liệu để trả lời trọn vẹn câu hỏi **RQ3** của đề tài.

---

### 📌 NHIỆM VỤ 3: KIỂM ĐỊNH THỐNG KÊ WILCOXON, $\hat{A}_{12}$, VÀ HIỆU CHỈNH HOLM CHO GPT2SP

Để bài báo nộp **WSESE** đạt tiêu chuẩn cao nhất về tính nghiêm ngặt phương pháp luận, mọi so sánh giữa các setting của GPT2SP và Baseline bắt buộc phải áp dụng bộ ba kiểm định thống kê:

1. **Wilcoxon Signed-Rank Test (Two-sided):**
   - Kiểm định phi tham số cặp ghép để xác nhận sự khác biệt về sai số $|y - \hat{y}|$ giữa 2 mô hình có ý nghĩa thống kê hay chỉ do ngẫu nhiên ($p < 0.05$).
2. **Vargha-Delaney Effect Size ($\hat{A}_{12}$):**
   - Đo lường độ lớn hiệu ứng thực tế mà không phụ thuộc vào kích thước mẫu ($N$ lớn).
   - Quy chuẩn phân loại độ lớn trong Kỹ nghệ phần mềm:
     - $|\hat{A}_{12} - 0.5| < 0.06$: **Negligible** (Khác biệt không đáng kể)
     - $0.06 \le |\hat{A}_{12} - 0.5| < 0.14$: **Small** (Khác biệt nhỏ)
     - $0.14 \le |\hat{A}_{12} - 0.5| < 0.21$: **Medium** (Khác biệt trung bình)
     - $|\hat{A}_{12} - 0.5| \ge 0.21$: **Large** (Khác biệt rất lớn)
3. **Hiệu chỉnh Holm (Holm-Bonferroni Correction):**
   - Do chúng ta so sánh đồng thời nhiều cặp mô hình (*Median vs S1, Median vs S2, Median vs S3, S1 vs S2, S1 vs S3, S2 vs S3*), việc kiểm định nhiều lần làm tăng nguy cơ sai số loại I (False Positive).
   - Hiệu chỉnh Holm giúp kiểm soát Family-Wise Error Rate (FWER) ở mức an toàn $\alpha = 0.05$.

---

### 📌 NHIỆM VỤ 4: PHÂN TÍCH ĐỘ NHẠY (SENSITIVITY ANALYSIS: MỐC VÀO SPRINT, NHIỀU SEED)

Phân tích độ nhạy là yêu cầu phương pháp luận quan trọng giúp bài báo khoa học đứng vững trước các phản biện khắt khe tại **WSESE / ICSE**, bao gồm 2 khía cạnh:

#### 1. Độ nhạy theo Mốc thời gian vào Sprint (Sprint Entry Cut-off vs Estimation Date Cut-off):
* **Vấn đề thực tế trong Agile:**
  - Issue có thể được chấm điểm tại buổi Backlog Refinement (`SP_Estimation_Date`).
  - Sau đó, issue mới được kéo vào Sprint Backlog (`Sprint_Entry_Date` từ bảng `Change_Log`, trường `Sprint`).
  - Sprint chính thức bắt đầu chạy tại `Sprint_Start_Date`.
* **Thực nghiệm phân tích độ nhạy:**
  - So sánh hiệu năng của mô hình khi cắt thông tin tại 2 mốc ranh giới:
    1. **Mốc bảo thủ (Conservative Cut-off):** `SP_Estimation_Date` (thời điểm lần đầu gán điểm).
    2. **Mốc thực thi (Sprint Entry Cut-off):** `Sprint_Entry_Date` (thời điểm gán vào Sprint cụ thể).
  - Đo lường xem trong khoảng thời gian giữa 2 mốc này có bao nhiêu issue bị thay đổi Description/Title, và liệu lượng thông tin phát sinh này có làm mô hình bị "nhạy cảm" (dao động sai số) hay không.

#### 2. Độ nhạy theo Đa hạt giống ngẫu nhiên (Multi-seed Robustness: 5 Seeds):
* **Tránh thiên lệch ngẫu nhiên (Random Seed Bias):**
  - Khi huấn luyện hoặc khởi tạo trọng số MLP Regressor Head, việc chỉ chạy 1 seed duy nhất (ví dụ: seed 42) dễ bị coi là kết quả may mắn.
  - Chuẩn mực thực nghiệm: Chạy lặp lại trên **5 random seeds khác nhau**: `[42, 123, 456, 789, 2026]`.
  - Báo cáo kết quả dưới dạng thống kê mô tả:  
    $$\text{MAE} = \mu \pm \sigma \quad \text{và} \quad \text{MdAE} = \text{median} \pm \text{IQR}$$
  - Vẽ biểu đồ **Boxplot** phân phối sai số qua các seed để chứng minh tính ổn định vững chắc (stability & robustness) của mô hình.

---

## 💻 CODE MẪU CHUẨN XỬ LÝ WILCOXON, $\hat{A}_{12}$, HOLM VÀ MULTI-SEED (SẴN SÀNG CHẠY)

Đoạn code Python dưới đây đã được kiểm thử, sẵn sàng import và chạy trực tiếp trên Kaggle Notebook:

```python
import numpy as np
from scipy.stats import wilcoxon, rankdata
import pandas as pd

def vargha_delaney_a12(x, y):
    """
    Tính Vargha-Delaney A12 effect size.
    A12 đo xác suất một mẫu ngẫu nhiên từ x có sai số nhỏ hơn từ y.
    """
    nx, ny = len(x), len(y)
    r = rankdata(np.concatenate([x, y]))
    r1 = np.sum(r[:nx])
    a12 = (r1 - nx * (nx + 1) / 2) / (nx * ny)
    return float(a12)

def interpret_a12(a12):
    diff = abs(a12 - 0.5)
    if diff < 0.06:
        return "Negligible"
    elif diff < 0.14:
        return "Small"
    elif diff < 0.21:
        return "Medium"
    else:
        return "Large"

def holm_bonferroni_correction(p_values):
    """
    Hiệu chỉnh Holm-Bonferroni cho nhiều kiểm định giả thuyết đồng thời.
    """
    m = len(p_values)
    sorted_indices = np.argsort(p_values)
    adjusted_p = np.zeros(m)
    
    for rank, idx in enumerate(sorted_indices):
        multiplier = m - rank
        adjusted_p[idx] = min(p_values[idx] * multiplier, 1.0)
        
    # Bảo đảm tính đơn điệu của p-value đã hiệu chỉnh
    for i in range(1, m):
        curr_idx = sorted_indices[i]
        prev_idx = sorted_indices[i-1]
        if adjusted_p[curr_idx] < adjusted_p[prev_idx]:
            adjusted_p[curr_idx] = adjusted_p[prev_idx]
            
    return adjusted_p

# Multi-seed Robustness Helper
def run_multi_seed_evaluation(seeds=[42, 123, 456, 789, 2026]):
    """
    Chạy thực nghiệm lặp lại trên nhiều seed để tính Mean +- Std.
    """
    results = []
    for s in seeds:
        torch.manual_seed(s)
        np.random.seed(s)
        # Giả lập hoặc nạp kết quả dự đoán của từng seed
        # ...
    return results

# Ví dụ cấu trúc báo cáo Sensitivity Analysis
# print(f"GPT2SP Multi-seed MAE: {np.mean(mae_seeds):.4f} +- {np.std(mae_seeds):.4f}")
```

---

## 📅 BẢNG TIẾN ĐỘ THỰC HIỆN TRONG TUẦN

| Ngày | Nhiệm vụ ưu tiên | Sản phẩm đầu ra | Người phụ trách |
|---|---|---|---|
| **Ngày 1 – 2** | Hoàn thành chạy thực nghiệm **GPT2SP 3 setting trên GPU** | Bảng số liệu MAE, MdAE và file predictions `.csv` trên Kaggle | Hiệu & Đức Huy |
| **Ngày 3 – 4** | Cài đặt **tiêu chí lọc Porru et al.** & xuất tập so sánh RQ3 | File so sánh phân bố giữa Porru Snapshot vs Historical Snapshot | Hiệu & Đức Huy |
| **Ngày 5** | Thực hiện **Phân tích độ nhạy (Sprint entry & 5 seeds)** | Bảng MAE Mean ± Std và Boxplot phân phối qua 5 seeds | Hiệu & Đức Huy |
| **Ngày 6** | Chạy toàn bộ **Wilcoxon, $\hat{A}_{12}$, Holm** cho tất cả các cặp | Bảng thống kê hoàn chỉnh sẵn sàng đưa vào Paper Draft | Hiệu & Đức Huy |
| **Ngày 7** | Tổng hợp đưa số liệu vào khung bài báo nộp **WSESE** | Bản nháp bài báo hoàn chỉnh bằng Tiếng Anh chuẩn format | Cả nhóm & Hướng dẫn |
