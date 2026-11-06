# 📘 CẨM NANG THỰC NGHIỆM TÁI LẬP GPT2SP TRÊN KAGGLE NOTEBOOKS
## HƯỚNG DẪN TỪNG BƯỚC (STEP-BY-STEP REPLICATION HARNESS: GITHUB & HUGGING FACE ➔ KAGGLE ➔ METRICS & CHECKPOINTS)

> **Tài liệu nghiên cứu:** Đề tài Nghiên cứu Khoa học 2026 — *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*.  
> **Nhóm thực hiện:** Lê Thành Hiệu (`24520496`), Phan Ngọc Đức Huy (`24520695`) — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM (UIT - VNU-HCM).  
> **Giảng viên hướng dẫn:** ThS. Tạ Việt Phương.  
> **Bài báo đối chứng:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Mục tiêu thực nghiệm:** Tái hiện trung thực quy trình thực nghiệm trên dự án **Spring XD** (3.526 Jira issues), kiểm chứng khoảng cách giữa Checkpoint công bố (`MickyMike/0-GPT2SP-springxd`) và Bảng 4 của bài báo gốc.

---

## 🧭 1. TỔNG QUAN LUỒNG THỰC NGHIỆM (REPLICATION WORKFLOW)

```text
[INPUT TỪ BÀI BÁO]
├── 1. Mã nguồn tác giả: https://github.com/awsm-research/gpt2sp
├── 2. Checkpoint tác giả: https://huggingface.co/MickyMike/0-GPT2SP-springxd
└── 3. Dataset Spring XD: 3.526 Jira issues (Chronological 60/20/20)
                       │
                       ▼
       [MÔI TRƯỜNG KAGGLE NOTEBOOK]
       (Kaggle GPU T4 x 2, PyTorch, Hugging Face Transformers)
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[PHA 1: SUY LUẬN CHECKPOINT]    [PHA 2: FINE-TUNE LẠI TỪ ĐẦU]
• Nạp checkpoint MickyMike       • Huấn luyện GPT-2 Base + MLP Head
• Inference tập Test 706 issues  • Lưu best_gpt2sp_springxd.pt
• Đo MAE, MdAE tức thì (~2 phút) • Kiểm chứng độ hội tụ loss (~30 phút)
       │                               │
       └───────────────┬───────────────┘
                       ▼
[OUTPUT & MINH CHỨNG HỌC THUẬT]
├── Bảng so sánh MAE / MdAE đối chứng với Median Effort Baseline
├── Kiểm định ý nghĩa thống kê Wilcoxon Signed-Rank Test (p-value)
└── Bằng chứng thực nghiệm phản hồi trong thư gửi tác giả bài báo
```

---

## ⚙️ 2. BƯỚC 1: KHỞI TẠO NOTEBOOK & CẤU HÌNH TRÊN KAGGLE

1. Truy cập [Kaggle](https://www.kaggle.com) $\rightarrow$ Đăng nhập tài khoản $\rightarrow$ Bấm nút **`Create`** (góc trên bên trái) $\rightarrow$ Chọn **`New Notebook`**.
2. Đổi tên Notebook thành: `GPT2SP-SpringXD-Replication-NCKH3`.
3. **Cấu hình phần cứng ở cột bên phải (Notebook options):**
   * **Accelerator:** Chọn **`GPU T4 x 2`** (hoặc `GPU P100`).
   * **Internet:** Gạt sang **`On`** *(bắt buộc bật để notebook tải code từ GitHub và weights từ Hugging Face Hub)*.
   * **Persistence:** Chọn **`Variables and files`** nếu muốn giữ dữ liệu phiên làm việc.

---

## 💻 3. BƯỚC 2: CÀI ĐẶT MÔI TRƯỜNG & CLONE REPO (CODE CELL 1)

Sao chép đoạn code dưới đây vào ô lệnh đầu tiên trên Kaggle:

```python
# ==============================================================================
# CELL 1: THIẾT LẬP MÔI TRƯỜNG & CLONE MÃ NGUỒN TÁC GIẢ
# ==============================================================================
!pip install -q transformers==4.30.2 evaluate datasets accelerate scipy

import os
import sys

# Clone replication package chính thức của tác giả Fu & Tantithamthavorn
if not os.path.exists('/kaggle/working/gpt2sp'):
    !git clone https://github.com/awsm-research/gpt2sp.git /kaggle/working/gpt2sp

# Nạp đường dẫn repo vào hệ thống
sys.path.append('/kaggle/working/gpt2sp')
os.chdir('/kaggle/working/gpt2sp')

print("✅ Đã thiết lập môi trường và nạp repo awsm-research/gpt2sp thành công!")
```

---

## 📂 4. BƯỚC 3: NẠP DỮ LIỆU & CHIA THEO TRỤC THỜI GIAN (CODE CELL 2)

> [!IMPORTANT]
> **Ràng buộc chống rò rỉ dữ liệu (No Temporal Leakage):** Tuyệt đối không dùng hàm `train_test_split(shuffle=True)` ngẫu nhiên. Dữ liệu Jira bắt buộc phải được chia theo thứ tự thời gian tạo (*Chronological Split*) theo tỷ lệ 60% Train, 20% Validation, 20% Test.

```python
# ==============================================================================
# CELL 2: NẠP DATASET SPRING XD VÀ PHÂN CHIA THEO SPLIT_MARK CỦA TÁC GIẢ
# ==============================================================================
import os
import pandas as pd
import numpy as np

# Đường dẫn file sau khi clone repo (kèm link raw GitHub dự phòng)
local_path = '/kaggle/working/gpt2sp/sp_dataset/marked_data/springxd.csv'
fallback_url = 'https://raw.githubusercontent.com/awsm-research/gpt2sp/main/sp_dataset/marked_data/springxd.csv'

dataset_path = local_path if os.path.exists(local_path) else fallback_url
df = pd.read_csv(dataset_path)

print(f"Tổng số User Stories / Issues của dự án Spring XD: {len(df)}")
print("3 mẫu đầu tiên:")
display(df[['issuekey', 'title', 'storypoint', 'split_mark']].head(3))

# Phân chia chuẩn xác theo cột 'split_mark' mà chính tác giả đã gắn nhãn trong dataset:
train_df = df[df['split_mark'] == 'train'].copy().reset_index(drop=True)
val_df = df[df['split_mark'] == 'val'].copy().reset_index(drop=True)
test_df = df[df['split_mark'] == 'test'].copy().reset_index(drop=True)

print(f"\n✅ Đã phân chia dữ liệu Chronological chuẩn mực theo tác giả:")
print(f" • Tập Huấn luyện (Train): {len(train_df)} issues ({len(train_df)/len(df)*100:.1f}%)")
print(f" • Tập Kiểm tra phát triển (Validation): {len(val_df)} issues ({len(val_df)/len(df)*100:.1f}%)")
print(f" • Tập Kiểm thử độc lập (Test): {len(test_df)} issues ({len(test_df)/len(df)*100:.1f}%)")
```

---

## ⚡ 5. BƯỚC 4: SUY LUẬN TRỰC TIẾP CHECKPOINT TÁC GIẢ (CODE CELL 3)

Bước này tải trực tiếp trọng số pre-trained `MickyMike/0-GPT2SP-springxd` từ Hugging Face Hub về và chạy dự đoán trên 706 issues của tập Test để kiểm chứng sai số thực tế.

```python
# ==============================================================================
# CELL 3: NẠP CHECKPOINT HUGGING FACE & CHẠY DỰ ĐOÁN TẬP TEST
# ==============================================================================
import torch
import torch.nn as nn
from transformers import GPT2Tokenizer, GPT2Model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Đang chạy trên phần cứng: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

# 1. Nạp Tokenizer của checkpoint
checkpoint_name = "MickyMike/0-GPT2SP-springxd"
tokenizer = GPT2Tokenizer.from_pretrained(checkpoint_name)
tokenizer.pad_token = tokenizer.eos_token

# 2. Định nghĩa cấu trúc GPT2SP đúng theo mã nguồn GPT2SP.py của bài báo
class GPT2SPModel(nn.Module):
    def __init__(self, model_checkpoint):
        super(GPT2SPModel, self).__init__()
        self.gpt2 = GPT2Model.from_pretrained(model_checkpoint)
        self.dense1 = nn.Linear(768, 3072, bias=False)
        self.dense2 = nn.Linear(3072, 768, bias=False)
        self.score = nn.Linear(768, 1, bias=False)

    def forward(self, input_ids, attention_mask):
        outputs = self.gpt2(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        batch_size = input_ids.shape[0]
        # Trích xuất vector ẩn tại token cuối cùng (Last-token pooling)
        sequence_lengths = (torch.ne(input_ids, tokenizer.pad_token_id).sum(dim=-1) - 1).to(device)
        pooled_logits = last_hidden_state[torch.arange(batch_size, device=device), sequence_lengths]
        
        # Đi qua 3 tầng MLP Regressor Head
        h = self.dense1(pooled_logits)
        h = self.dense2(h)
        logits = self.score(h)
        return logits.squeeze(-1)

# Khởi tạo mô hình và tải weights
model = GPT2SPModel(checkpoint_name).to(device)
model.eval()

# 3. Chạy suy luận (Inference) trên 706 mẫu Test (SEQUENCE_LEN = 20 theo notebook tác giả)
test_texts = test_df['title'].astype(str).tolist()
true_sp = test_df['storypoint'].values

predictions = []
batch_size = 32

print("Đang tiến hành suy luận trên tập Test...")
with torch.no_grad():
    for i in range(0, len(test_texts), batch_size):
        batch_texts = test_texts[i:i+batch_size]
        inputs = tokenizer(
            batch_texts, 
            padding='max_length', 
            truncation=True, 
            max_length=20, 
            return_tensors="pt"
        ).to(device)
        
        preds = model(inputs['input_ids'], inputs['attention_mask'])
        predictions.extend(preds.cpu().numpy().tolist())

gpt2sp_preds = np.array(predictions)
print(f"✅ Hoàn thành suy luận {len(gpt2sp_preds)} mẫu trong ~30 giây!")
```

---

## 📈 6. BƯỚC 5: TÍNH TOÁN BASELINE & KIỂM ĐỊNH THỐNG KÊ (CODE CELL 4)

Tính toán sai số đối chứng với **Median Effort Baseline** và kiểm định ý nghĩa thống kê bằng **Wilcoxon Signed-Rank Test**:

```python
# ==============================================================================
# CELL 4: TÍNH TOÁN MAE, MdAE & WILCOXON SIGNED-RANK TEST
# ==============================================================================
from scipy.stats import wilcoxon

# 1. Baseline Trung vị (Median Effort): Dự đoán mọi issue bằng trung vị tập Train
median_baseline_val = train_df['storypoint'].median()
baseline_preds = np.full_like(true_sp, fill_value=median_baseline_val)

# 2. Tính vector sai số tuyệt đối
errors_gpt2sp = np.abs(true_sp - gpt2sp_preds)
errors_baseline = np.abs(true_sp - baseline_preds)

# 3. Các chỉ số đo lường
mae_gpt2sp = np.mean(errors_gpt2sp)
mdae_gpt2sp = np.median(errors_gpt2sp)

mae_baseline = np.mean(errors_baseline)
mdae_baseline = np.median(errors_baseline)

# 4. Kiểm định giả thuyết thống kê Wilcoxon
w_stat, p_val = wilcoxon(errors_gpt2sp, errors_baseline)

# 5. Xuất bảng tổng hợp kết quả
results_df = pd.DataFrame({
    'Phương pháp / Mô hình': [
        'Median Effort Baseline (Chuẩn quy chiếu)', 
        'GPT2SP (Checkpoint MickyMike trên Kaggle)', 
        'GPT2SP (Công bố tại Bảng 4 IEEE TSE 2023)'
    ],
    'MAE': [f"{mae_baseline:.4f}", f"{mae_gpt2sp:.4f}", "0.9600"],
    'MdAE': [f"{mdae_baseline:.4f}", f"{mdae_gpt2sp:.4f}", "N/A"],
    'Wilcoxon p-value vs Baseline': ['—', f"{p_val:.4e}", "p < 0.05"]
})

print("="*80)
print("📊 BẢNG TỔNG HỢP KẾT QUẢ TÁI LẬP THỰC NGHIỆM TRÊN SPRING XD")
print("="*80)
display(results_df)

# Lưu kết quả ra file csv trong thư mục working của Kaggle
results_df.to_csv('/kaggle/working/replication_springxd_results.csv', index=False)
print("📁 Đã lưu file: /kaggle/working/replication_springxd_results.csv")
```

---

## 🔄 7. BƯỚC 6 (TÙY CHỌN): HUẤN LUYỆN LẠI TỪ ĐẦU & LƯU CHECKPOINT MỚI (CODE CELL 5)

Nếu muốn huấn luyện lại từ đầu (*Full Fine-Tuning*) bằng hàm mất mát $L_1$ Loss (MAE Loss) và lưu file checkpoint `.pt` tốt nhất vào thư mục Output của Kaggle:

```python
# ==============================================================================
# CELL 5: HUẤN LUYỆN LẠI (FINE-TUNE FROM SCRATCH) & LƯU CHECKPOINT
# ==============================================================================
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim

# 1. Hàm tạo DataLoader
def prepare_loader(data, batch_size=16, shuffle=True):
    encoded = tokenizer(
        data['title'].astype(str).tolist(),
        padding='max_length',
        truncation=True,
        max_length=20,
        return_tensors="pt"
    )
    labels = torch.tensor(data['storypoint'].values, dtype=torch.float32)
    dataset = TensorDataset(encoded['input_ids'], encoded['attention_mask'], labels)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

train_loader = prepare_loader(train_df, batch_size=16, shuffle=True)
val_loader = prepare_loader(val_df, batch_size=16, shuffle=False)

# 2. Khởi tạo mô hình từ gpt2 gốc và optimizer AdamW
scratch_model = GPT2SPModel("gpt2").to(device)
optimizer = optim.AdamW(scratch_model.parameters(), lr=1e-4)
criterion = nn.L1Loss()

epochs = 5
best_val_loss = float('inf')
checkpoint_dir = '/kaggle/working/checkpoints'
os.makedirs(checkpoint_dir, exist_ok=True)

print("🚀 Bắt đầu quá trình huấn luyện lại mô hình...")
for epoch in range(epochs):
    scratch_model.train()
    total_train_loss = 0.0
    
    for b_ids, b_mask, b_labels in train_loader:
        b_ids, b_mask, b_labels = b_ids.to(device), b_mask.to(device), b_labels.to(device)
        
        optimizer.zero_grad()
        preds = scratch_model(b_ids, b_mask)
        loss = criterion(preds, b_labels)
        loss.backward()
        optimizer.step()
        
        total_train_loss += loss.item() * len(b_labels)
        
    avg_train_loss = total_train_loss / len(train_df)
    
    # Đánh giá trên Validation Set
    scratch_model.eval()
    total_val_loss = 0.0
    with torch.no_grad():
        for b_ids, b_mask, b_labels in val_loader:
            b_ids, b_mask, b_labels = b_ids.to(device), b_mask.to(device), b_labels.to(device)
            preds = scratch_model(b_ids, b_mask)
            loss = criterion(preds, b_labels)
            total_val_loss += loss.item() * len(b_labels)
            
    avg_val_loss = total_val_loss / len(val_df)
    print(f"Epoch {epoch+1:02d}/{epochs:02d} | Train MAE: {avg_train_loss:.4f} | Val MAE: {avg_val_loss:.4f}")
    
    # Lưu checkpoint tốt nhất khi Val MAE cải thiện
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        best_checkpoint_path = os.path.join(checkpoint_dir, 'best_gpt2sp_springxd.pt')
        torch.save(scratch_model.state_dict(), best_checkpoint_path)
        print(f" ⭐ Đã lưu checkpoint mới tốt nhất tại: {best_checkpoint_path}")

print("\n🎉 Hoàn thành quá trình huấn luyện lại!")
```

---

## 📥 8. BƯỚC 7: CÁCH TẢI CHECKPOINT VÀ FILE KẾT QUẢ VỀ MÁY TÍNH

Sau khi chạy xong notebook trên Kaggle:
1. Nhìn sang cột bên phải giao diện Kaggle, mở rộng mục **Output** (`/kaggle/working`).
2. Bạn sẽ thấy các file được sinh ra:
   * `replication_springxd_results.csv` (Bảng số liệu MAE, p-value đối chứng).
   * `checkpoints/best_gpt2sp_springxd.pt` (File trọng số mô hình đã huấn luyện).
3. Bấm vào biểu tượng **`3 dấu chấm (...)`** ở bên phải tên từng file $\rightarrow$ Chọn **`Download`** để tải về máy tính làm minh chứng thực nghiệm cho báo cáo NCKH!
