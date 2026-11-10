# 🔬 KẾ HOẠCH NGHIÊN CỨU TỰ LỰC & THỰC NGHIỆM ĐỘC LẬP
## BIẾN ĐỘ LỆCH TÁI LẬP THÀNH ĐÓNG GÓP KHOA HỌC TRONG BÁO CÁO NCKH (EMPIRICAL AUDIT & ABLATION STUDY)

> **Tôn chỉ khoa học (AGENTS.md):**  
> Tuyệt đối không giả định hay bịa đặt kết quả. Nếu tác giả không phản hồi, độ lệch thực nghiệm giữa Checkpoint công bố (`MAE = 3.3090`) và Bảng 4 (`MAE = 0.96`) chính là một **phát hiện khoa học có giá trị cao về tính tái lập (Reproducibility & Replicability in Empirical Software Engineering)**.

---

## 🎯 1. ĐỊNH VỊ HỌC THUẬT: CÁCH TRÌNH BÀY TRONG BÁO CÁO NCKH & BÀI BÁO

Khi không có xác nhận từ tác giả, nghiên cứu của chúng ta không dừng lại mà được định vị ở cấp độ cao hơn:
1. **Reproducibility Audit (Kiểm toán tính tái lập):**
   - Đánh giá khách quan hiện trạng các mô hình Deep Learning trong ước lượng Story Point khi đem ra môi trường thực tế.
   - Chỉ ra rằng các mô hình phức tạp (GPT-2) nếu không có quy trình tinh chỉnh và kiểm soát chặt chẽ có thể **thua kém cả một bộ ước lượng đơn giản (Median Effort Baseline: MAE = 1.7153 vs GPT2SP: MAE = 3.3090, $p < 0.001$)**.
2. **Temporal Leakage Control (Kiểm soát rò rỉ dữ liệu theo thời gian):**
   - Phân tích vì sao việc sử dụng thông tin sau thời điểm lập kế hoạch (Sprint Planning) làm sai lệch kết quả thực nghiệm.
   - Xây dựng benchmark chuẩn hóa tại mốc thời gian ước lượng `SP_Estimation_Date`.

---

## 🧪 2. KẾ HOẠCH THỰC NGHIỆM ĐỘC LẬP (3 TRỤ CỘT THỰC NGHIỆM)

### 📌 Thí nghiệm 1: Phân tích bóc tách các giả định (Ablation Study trên Spring XD)
Mục tiêu: Tìm hiểu nguyên nhân gây ra sự chênh lệch giữa thực nghiệm và bài báo thông qua 4 cấu hình:

| ID | Cấu hình thử nghiệm | Input Text | Context Window (`SEQUENCE_LEN`) | Head Activation | Post-processing |
|---|---|---|---|---|---|
| **E1** | Checkpoint MickyMike (Mặc định) | `title` | 20 | Linear (theo code repo) | None |
| **E2** | Full Context | `title + description` | 128 / 512 | Linear | None |
| **E3** | Non-linear GELU MLP Head | `title` | 20 | `GELU()` (theo văn bản bài báo) | None |
| **E4** | Fibonacci Bin Mapping | `title` | 20 | Linear | Làm tròn về số Fibonacci gần nhất |

### 📌 Thí nghiệm 2: Kiểm chứng chéo trên các dự án khác (Cross-Project Verification)
Tác giả công bố checkpoint và dữ liệu cho nhiều dự án khác ngoài Spring XD trong repo `awsm-research/gpt2sp` (ví dụ: `MESOS`, `USERGRID`, `TIDB`, `APACHE`).
- **Mục tiêu:** Chạy kiểm thử checkpoint trên ít nhất 2–3 dự án khác để xác nhận:
  - Hiện tượng `GPT2SP MAE > Median Baseline` là đặc thù riêng của dự án Spring XD hay là hiện tượng phổ quát (systematic phenomenon) trên toàn bộ benchmark.

### 📌 Thí nghiệm 3: So sánh đối chuẩn với Mô hình Đề xuất của đề tài (Our Proposed Model)
- So sánh song song giữa:
  1. **Median Effort Baseline** (Baseline bắt buộc).
  2. **GPT2SP (Replicated)**.
  3. **Deep-SE (CNN/LSTM) / SBERT Baseline**.
  4. **Mô hình Đề xuất có Temporal Leakage Control**.
- Mọi so sánh đều thực hiện kiểm định ý nghĩa thống kê **Wilcoxon Signed-Rank Test** với mức ý nghĩa $\alpha = 0.05$.

---

## 📊 3. BẢNG MẪU BÁO CÁO KẾT QUẢ KHOA HỌC (ACADEMIC REPORT TABLE)

```markdown
| Phương pháp / Mô hình | Input Features | Context Len | MAE (Test) | MdAE (Test) | Wilcoxon vs Median (p-value) | Trạng thái Tái lập |
|---|---|---|---|---|---|---|
| **Median Effort Baseline** | Prior SP History | N/A | **1.7153** | **2.0000** | — | Tham chiếu chuẩn |
| **GPT2SP (Published - Table 4)** | Title + Description | Unspecified | 0.9600 | N/A | p < 0.05 | Số liệu công bố trong bài báo |
| **GPT2SP (Replication - E1)** | Title only | 20 | 3.3090 | 2.9523 | p = 1.48e-84 | Checkpoint MickyMike chính thức |
| **GPT2SP (Replication - E2)** | Title + Description | 128 | [Đang đo] | [Đang đo] | [Đang đo] | Ablation Study |
| **Mô hình Đề xuất (NCKH 2026)** | Planning-time Context | Dynamic | [Target < 1.70] | [Target < 2.0] | p < 0.05 | Đóng góp mới của đề tài |
```

---

## 📅 4. TIẾN ĐỘ THỰC HIỆN TỰ LỰC DỰ KIẾN

```text
[GIAI ĐOẠN 1: 10/11 - 19/11/2026]
 • Chờ phản hồi tự nhiên qua Email từ Dr. Michael Fu & Dr. Chakkrit.
 • Hoàn thiện notebook chạy thử nghiệm mở rộng trên Kaggle (Ablation & Cross-projects).

[GIAI ĐOẠN 2: 20/11 - 25/11/2026]
 • Gửi Gentle Reminder (Thư nhắc ngắn văn bản thuần 1 lần duy nhất).
 • Mở GitHub Issue trên awsm-research/gpt2sp và Hugging Face Discussion.

[GIAI ĐOẠN 3: 26/11/2026 TRỞ ĐI]
 • Khóa số liệu đối chứng GPT2SP (Ghi nhận đầy đủ hiện trạng thực nghiệm).
 • Tập trung toàn lực huấn luyện và đánh giá Mô hình Đề xuất của đề tài NCKH.
```
