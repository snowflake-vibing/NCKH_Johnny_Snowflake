# 📘 SỔ TAY HƯỚNG DẪN TÁI LẬP THỰC NGHIỆM GPT2SP TRÊN KAGGLE NOTEBOOKS TỪ A ĐẾN Z
## QUY TRÌNH TỪNG BƯỚC: THIẾT LẬP, BẬT GPU, NẠP DỮ LIỆU, CHẠY KIỂM CHỨNG VÀ XUẤT BẰNG CHỨNG LƯU TRÊN CLOUD

> **Mục tiêu:** Hướng dẫn chi tiết từng thao tác bấm chuột và từng ô lệnh (Cell) để bạn có thể tự mình thiết lập và thực thi toàn bộ quy trình tái lập mô hình GPT2SP trên nền tảng **Kaggle Notebooks**, tận dụng GPU đám mây miễn phí và lưu trữ dữ liệu vĩnh viễn trên Cloud.

---

## 🧭 1. VÌ SAO CHỌN KAGGLE NOTEBOOKS CHO ĐỀ TÀI NÀY?

1. **GPU miễn phí mạnh mẽ:** Cung cấp **30 giờ GPU/tuần** (NVIDIA Tesla T4 x2 hoặc P100) có sẵn 16GB VRAM.
2. **Khả năng chạy ngầm (Background Execution):** Bạn chỉ cần bấm *Save & Run All (Commit)* rồi tắt máy tính đi ngủ, hệ thống đám mây của Kaggle sẽ tự chạy ngầm và lưu toàn bộ kết quả vào Cloud.
3. **Minh chứng khoa học minh bạch (Open Science):** Khi nghiệm thu đề tài NCKH hoặc nộp bài báo quốc tế (WSESE), bạn chỉ cần gửi kèm đường link Kaggle Notebook công khai. Reviewer chỉ cần bấm vào là thấy toàn bộ mã nguồn, biểu đồ và số liệu thực nghiệm nguyên bản.

---

## 🛠️ 2. CHUẨN BỊ TÀI KHOẢN VÀ CẤU HÌNH KAGGLE BAN ĐẦU

### Bước 2.1: Đăng ký & Xác thực tài khoản
1. Truy cập [kaggle.com](https://www.kaggle.com) và đăng nhập tài khoản Google.
2. **Kích hoạt GPU (Bắt buộc một lần duy nhất):**
   - Bấm vào ảnh đại diện góc trên bên phải $\rightarrow$ Chọn **Settings**.
   - Cuộn xuống mục **Phone verification** $\rightarrow$ Nhập số điện thoại để nhận mã SMS kích hoạt.
   - *(Lưu ý: Nếu không xác thực số điện thoại, Kaggle sẽ không mở khóa quyền dùng GPU miễn phí).*

### Bước 2.2: Khởi tạo Notebook mới
1. Tại thanh menu bên trái, bấm nút **`+ Create`** $\rightarrow$ Chọn **`New Notebook`**.
2. Đổi tên Notebook (ở góc trên bên trái màn hình) thành:  
   `GPT2SP_SpringXD_Reproduction_Verification`

---

## ⚙️ 3. THIẾT LẬP THÔNG SỐ NOTEBOOK (CỰC KỲ QUAN TRỌNG)

Nhìn sang bảng điều khiển **Notebook options / Settings** ở cột bên phải màn hình:

```text
┌────────────────────────────────────────────────────────┐
│ NOTEBOOK OPTIONS (Cột bên phải màn hình Kaggle)        │
├────────────────────────────────────────────────────────┤
│ 1. Accelerator:  [ GPU T4 x2 ]    <── BẮT BUỘC CHỌN    │
│ 2. Language:     [ Python ]                            │
│ 3. Environment:  [ Always use latest environment ]     │
│ 4. Internet:     [ Internet on ]  <── BẮT BUỘC BẬT     │
│ 5. Persistence:  [ Variables and files ] (Tùy chọn)   │
└────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> * **Accelerator:** Bắt buộc đổi từ `None` sang **`GPU T4 x2`** (hoặc `GPU P100`) để mô hình chạy trên card đồ họa.
> * **Internet on:** Bắt buộc **BẬT công tắc Internet** sang màu xanh. Nếu tắt, Kaggle sẽ bị chặn mạng và không thể tải thư viện hoặc checkpoint từ Hugging Face Hub!

---

## 💻 4. CHI TIẾT TỪNG Ô MÃ NGUỒN (CELL-BY-CELL) ĐỂ DÁN VÀO NOTEBOOK

Bạn chỉ cần tạo lần lượt các Cell trong Kaggle Notebook và dán các đoạn code tương ứng dưới đây:

### 🔹 Cell 1: Kiểm tra GPU & Cài đặt thư viện phụ thuộc
*Mục đích: Xác nhận GPU đã sẵn sàng và cài đặt các thư viện cần thiết.*

```python
# CELL 1: KIỂM TRA PHẦN CỨNG & CÀI ĐẶT THƯ VIỆN
import torch

print(f"Phiên bản PyTorch: {torch.__version__}")
if torch.cuda.is_available():
    print(f"✅ Đã kích hoạt GPU: {torch.cuda.get_device_name(0)}")
    print(f"💾 Dung lượng VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️ CẢNH BÁO: Đang chạy trên CPU! Hãy vào Settings bên phải -> Accelerator -> Chọn GPU T4 x2.")

# Cài đặt thư viện Transformers và Scipy
!pip install -q transformers scipy scikit-learn matplotlib seaborn
```

---

### 🔹 Cell 2: Tự động nạp tập dữ liệu Spring XD & Chronological Split
*Mục đích: Tự động tải file `springxd.csv` trực tiếp từ GitHub của bài báo (không cần upload thủ công), chia tập 60/20/20 theo thời gian và tính Median Baseline.*

```python
# CELL 2: NẠP DỮ LIỆU & PHÂN CHIA THEO THỜI GIAN (60/20/20)
import os
import math
import pandas as pd
import urllib.request

DATA_URL = "https://raw.githubusercontent.com/morakotch/datasets/master/storypoint/IEEE%20TSE2018/dataset/springxd.csv"
DATASET_FILE = "springxd.csv"

# Tự động tải dataset nếu chưa có
if not os.path.exists(DATASET_FILE):
    print("📥 Đang tải tập dữ liệu Spring XD từ GitHub...")
    urllib.request.urlretrieve(DATA_URL, DATASET_FILE)
    print(f"✅ Tải thành công! Kích thước file: {os.path.getsize(DATASET_FILE) / 1024:.1f} KB")

df = pd.read_csv(DATASET_FILE).fillna("")
print(f"📊 Tổng số issues trong dataset: {len(df)}")

# Phân chia theo thứ tự thời gian (Section 4.1 trong bài báo)
def chronological_split(data, train_ratio=0.6, val_ratio=0.2):
    n_total = len(data)
    n_train = math.ceil(n_total * train_ratio)
    n_val = math.ceil(n_total * val_ratio)
    
    train_data = data.iloc[:n_train].copy()
    val_data = data.iloc[n_train : n_train + n_val].copy()
    test_data = data.iloc[n_train + n_val :].copy()
    return train_data, val_data, test_data

train_df, val_df, test_df = chronological_split(df, train_ratio=0.6, val_ratio=0.2)
print(f"   * Tập Huấn luyện (Train) : {len(train_df)} mẫu (60%)")
print(f"   * Tập Xác thực (Val)     : {len(val_df)} mẫu (20%)")
print(f"   * Tập Kiểm thử (Test)    : {len(test_df)} mẫu (20%)")

# Tính Median Baseline từ tập Train (Quy chuẩn phương pháp luận)
median_baseline = float(train_df["storypoint"].median())
print(f"\n🎯 Median Effort Baseline (tính từ Train): {median_baseline:.4f} Story Points")
```

---

### 🔹 Cell 3: Định nghĩa kiến trúc mô hình GPT2SP
*Mục đích: Dựng lại class `GPT2SP` đúng nguyên mẫu với 12 khối GPT-2 Backbone, MLP Regressor Head ($768 \rightarrow 3072 \rightarrow 768 \rightarrow 1$) và Last Token Pooling.*

```python
# CELL 3: ĐỊNH NGHĨA KIẾN TRÚC MÔ HÌNH GPT2SP
import torch.nn as nn
from transformers import GPT2Model, GPT2PreTrainedModel, GPT2Config, GPT2Tokenizer

class GPT2SP(GPT2PreTrainedModel):
    _keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        
        # MLP Regressor Head
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)  # 768 -> 3072
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)  # 3072 -> 768
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)      # 768 -> 1

        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None):
        transformer_outputs = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        hidden_states = transformer_outputs[0]

        # Lan truyền qua MLP Head
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        logits = self.score(hidden_states)

        # Last Token Pooling
        batch_size = input_ids.shape[0]
        sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
        pooled_logits = logits[range(batch_size), sequence_lengths]

        return pooled_logits

print("✅ Đã định nghĩa kiến trúc GPT2SP thành công!")
```

---

### 🔹 Cell 4: Nạp Checkpoint chính thức của tác giả từ Hugging Face
*Mục đích: Tải các trọng số fine-tuned chính thức mà nhóm tác giả đã công bố lên Hugging Face Hub (`MickyMike/0-GPT2SP-springxd`).*

```python
# CELL 4: TẢI BỘ TÁCH TỪ & CHECKPOINT CHÍNH THỨC CỦA TÁC GIẢ
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_CHECKPOINT = "MickyMike/0-GPT2SP-springxd"

print(f"📥 Đang tải weights từ Hugging Face: {MODEL_CHECKPOINT}...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token # ID 50257

config = GPT2Config.from_pretrained("gpt2", num_labels=1, pad_token_id=tokenizer.pad_token_id)
model = GPT2SP.from_pretrained(MODEL_CHECKPOINT, config=config)
model.to(device)
model.eval()

print("✅ Nạp Checkpoint lên GPU thành công!")
```

---

### 🔹 Cell 5: Thực thi suy luận (Inference) trên toàn bộ 706 Issues của tập Test
*Mục đích: Chạy dự báo hàng loạt với thanh tiến trình trực quan (`tqdm`), tuân thủ cấu hình `max_length = 20` tokens của tác giả.*

```python
# CELL 5: CHẠY SUY LUẬN TRÊN TẬP TEST
import numpy as np
from tqdm.auto import tqdm

test_titles = test_df["title"].tolist()
y_true = np.array(test_df["storypoint"].tolist(), dtype=np.float32)

BATCH_SIZE = 64
all_preds = []

print(f"🚀 Bắt đầu suy luận trên {len(test_titles)} mẫu kiểm thử...")
with torch.no_grad():
    for i in tqdm(range(0, len(test_titles), BATCH_SIZE), desc="Suy luận Test Set"):
        batch_texts = test_titles[i : i + BATCH_SIZE]
        encoding = tokenizer(
            batch_texts,
            max_length=20, # Giới hạn 20 tokens theo đúng mã nguồn bài báo
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        input_ids = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)
        
        preds = model(input_ids=input_ids, attention_mask=attention_mask)
        all_preds.extend(preds.view(-1).cpu().numpy().tolist())

y_pred = np.array(all_preds, dtype=np.float32)
print("✅ Đã hoàn thành suy luận cho 706 issues!")
```

---

### 🔹 Cell 6: Tính toán các thông số đầu ra làm bằng chứng thực nghiệm
*Mục đích: Tính toán MAE, MdAE, Standardized Accuracy (SA) và kiểm định Wilcoxon Signed-Rank Test để xác thực bài báo.*

```python
# CELL 6: TÍNH TOÁN CÁC THÔNG SỐ ĐẦU RA LÀM BẰNG CHỨNG THỰC NGHIỆM
from scipy import stats

abs_errors_model = np.abs(y_pred - y_true)
abs_errors_median = np.abs(median_baseline - y_true)

# 1. MAE
mae_model = float(np.mean(abs_errors_model))
mae_median = float(np.mean(abs_errors_median))

# 2. MdAE
mdae_model = float(np.median(abs_errors_model))
mdae_median = float(np.median(abs_errors_median))

# 3. Standardized Accuracy (SA)
sa_score = (1.0 - (mae_model / mae_median)) * 100.0

# 4. Wilcoxon Signed-Rank Test
wilcoxon_stat, wilcoxon_p = stats.wilcoxon(abs_errors_model, abs_errors_median)

print("=" * 85)
print("📊 KẾT QUẢ THẨM ĐỊNH THỰC NGHIỆM ĐỘC LẬP TRÊN DỰ ÁN SPRING XD")
print("=" * 85)
print(f"{'Chỉ số đo lường':<35}{'GPT2SP (Checkpoint)':<25}{'Median Baseline':<20}")
print("-" * 85)
print(f"{'MAE (Mean Absolute Error)':<35}{mae_model:<25.4f}{mae_median:<20.4f}")
print(f"{'MdAE (Median Absolute Error)':<35}{mdae_model:<25.4f}{mdae_median:<20.4f}")
print(f"{'Standardized Accuracy (SA)':<35}{sa_score:<25.2f}%{'0.00% (Baseline)':<20}")
print(f"{'Wilcoxon p-value':<35}{wilcoxon_p:<25.4e}{'N/A':<20}")
print("=" * 85)

print("\n🔍 ĐỐI SOÁT VỚI BÀI BÁO GỐC (IEEE TSE 2023):")
print(f"   * MAE bài báo công bố : ~ 0.96")
print(f"   * MAE thực tế tái lập : {mae_model:.4f}")
print(f"   * Median Baseline     : {mae_median:.4f}")
if mae_model >= mae_median:
    print("🔴 KẾT LUẬN: Checkpoint chính thức của tác giả THUA Median Baseline!")
    print("   Bằng chứng thực nghiệm cho thấy kết quả công bố không thể tái lập.")
```

---

### 🔹 Cell 7: Trực quan hóa sai số và lưu ảnh biểu đồ
*Mục đích: Vẽ biểu đồ Boxplot so sánh sai số giữa hai phương pháp để làm hình minh họa trong bài báo khoa học.*

```python
# CELL 7: VẼ BIỂU ĐỒ TRỰC QUAN HÓA PHÂN PHỐI SAI SỐ
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 5))

# Biểu đồ 1: Boxplot
plt.subplot(1, 2, 1)
plot_df = pd.DataFrame({
    "Absolute Error": np.concatenate([abs_errors_model, abs_errors_median]),
    "Model": ["GPT2SP (Checkpoint)"] * len(abs_errors_model) + ["Median Baseline"] * len(abs_errors_median)
})
sns.boxplot(x="Model", y="Absolute Error", data=plot_df, palette=["#e74c3c", "#3498db"], showmeans=True)
plt.title(f"So sánh Sai số MAE (Thấp hơn là tốt hơn)\nGPT2SP: {mae_model:.2f} | Median: {mae_median:.2f}", fontweight="bold")
plt.ylim(0, 15)

# Biểu đồ 2: Phân phối dự báo so với thực tế
plt.subplot(1, 2, 2)
plt.hist(y_true, bins=30, alpha=0.5, label="Nhãn thực tế (Ground Truth)", color="blue")
plt.hist(y_pred, bins=30, alpha=0.5, label="GPT2SP Dự báo", color="red")
plt.axvline(median_baseline, color="green", linestyle="--", linewidth=2, label=f"Median ({median_baseline:.0f})")
plt.title("Phân phối Điểm Story Point trên Tập Test", fontweight="bold")
plt.xlabel("Story Points")
plt.ylabel("Số lượng Issues")
plt.legend()

plt.tight_layout()
plt.savefig("/kaggle/working/springxd_error_distribution.png", dpi=300)
plt.show()
print("✅ Đã xuất ảnh biểu đồ chất lượng cao vào: /kaggle/working/springxd_error_distribution.png")
```

---

### 🔹 Cell 8: Xuất file CSV bằng chứng chi tiết cho từng Issue
*Mục đích: Xuất file CSV lưu trên Cloud chứa toàn bộ dự báo của 706 issues để tải về máy hoặc nộp làm Artifact kèm bài báo.*

```python
# CELL 8: XUẤT FILE CSV LƯU TRỮ BẰNG CHỨNG TRÊN CLOUD
evidence_df = pd.DataFrame({
    "Test_Index": range(len(test_df)),
    "Issue_Title": test_titles,
    "Ground_Truth_SP": y_true,
    "Predicted_SP_GPT2SP": np.round(y_pred, 4),
    "Absolute_Error_GPT2SP": np.round(abs_errors_model, 4),
    "Absolute_Error_Median": np.round(abs_errors_median, 4)
})

output_path = "/kaggle/working/springxd_reproduction_evidence.csv"
evidence_df.to_csv(output_path, index=False)

print(f"🎉 ĐÃ LƯU TRỮ VĨNH VIỄN BẰNG CHỨNG KHOA HỌC TRÊN CLOUD!")
print(f"📁 Đường dẫn file: {output_path} ({len(evidence_df)} dòng)")
display(evidence_df.head(5))
```

---

## ☁️ 5. QUY TRÌNH CHẠY NỀN & TẢI KẾT QUẢ TỪ KAGGLE VỀ MÁY

Sau khi dán xong 8 Cells trên vào Kaggle Notebook, bạn thực hiện quy trình sau để lưu trữ vĩnh viễn trên Cloud:

```text
[Bấm Save Version (Góc phải trên)]
               │
               ▼
[Chọn: Save & Run All (Commit)] ──> Bấm "Save"
               │
               ▼
[Có thể tắt máy tính / Ngắt mạng thoải mái]
(Server Google chạy ngầm 5-10 phút)
               │
               ▼
[Quay lại trang Kaggle Notebook] ──> Vào tab "Output"
               │
               ▼
[Tải 2 file bằng chứng về máy tính:]
├── springxd_reproduction_evidence.csv (Bảng dữ liệu chi tiết 706 issues)
└── springxd_error_distribution.png     (Ảnh biểu đồ độ phân giải cao 300 DPI)
```

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 🔬 [06_end_to_end_reproduction_guide_github_to_metrics.md](06_end_to_end_reproduction_guide_github_to_metrics.md): Lý thuyết phương pháp luận tái lập từ GitHub.
* ⚠️ [03_code_vs_paper_discrepancies.md](03_code_vs_paper_discrepancies.md): Mổ xẻ 4 điểm sai lệch giữa code thực tế và bài báo.
* 📜 [00_full_source_code.md](00_full_source_code.md): Toàn bộ mã nguồn gốc GPT2SP.
* 📑 [Danh mục toàn bộ tài liệu mã nguồn: README.md](README.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
