# ==============================================================================
# NOTEBOOK 1 (GPU T4 x 2): GPT2SP 3 SETTINGS & MULTI-SEED SENSITIVITY EVALUATION
# Phục vụ bài báo hội nghị WSESE (ICSE)
# ==============================================================================
import os
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from transformers import GPT2Tokenizer, GPT2Model

try:
    display
except NameError:
    display = print

output_dir = "/kaggle/working" if os.path.exists("/kaggle/working") else "kaggle/output"
os.makedirs(output_dir, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🔥 Hardware Accelerator: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

# ------------------------------------------------------------------------------
# 1. NẠP DỮ LIỆU SPRING XD (RAW & CLEAN PLANNING-TIME SNAPSHOT)
# ------------------------------------------------------------------------------
print("\n[1/4] Đang nạp dữ liệu Spring XD...")

# Dataset gốc của tác giả (có cột split_mark: train, val, test)
raw_url = "https://raw.githubusercontent.com/awsm-research/gpt2sp/main/sp_dataset/marked_data/springxd.csv"
local_raw = "/kaggle/working/gpt2sp/sp_dataset/marked_data/springxd.csv"
dataset_path = local_raw if os.path.exists(local_raw) else raw_url
df_raw = pd.read_csv(dataset_path)

# Dataset sạch do Nhóm 3 khôi phục từ Change_Log (Planning-Time Snapshot)
clean_candidates = [
    "docs/draft/springxd_cleaned_dataset.csv",
    "/kaggle/working/NCKH_Johnny_Snowflake/docs/draft/springxd_cleaned_dataset.csv",
    "/kaggle/input/springxd-clean/springxd_cleaned_dataset.csv",
    "/kaggle/working/springxd_cleaned_dataset.csv"
]
df_clean = None
for cp in clean_candidates:
    if os.path.exists(cp):
        df_clean = pd.read_csv(cp)
        print(f"✅ Đã nạp thành công Clean Planning-Time Dataset từ {cp} ({len(df_clean)} issues)")
        break

if df_clean is None:
    print("⚠️ Không tìm thấy file clean cục bộ, tạo bối cảnh Clean Snapshot từ tập gốc...")
    df_clean = df_raw.copy()
    df_clean['Clean_Title'] = df_clean['title']
    df_clean['Clean_Description'] = df_clean['description'].fillna('')

# Lấy tập Test của Spring XD (706 issues)
test_raw = df_raw[df_raw['split_mark'] == 'test'].copy().reset_index(drop=True)
train_raw = df_raw[df_raw['split_mark'] == 'train'].copy().reset_index(drop=True)
true_sp = test_raw['storypoint'].values

print(f"📊 Tập Train: {len(train_raw)} issues | Tập Test: {len(test_raw)} issues")

# ------------------------------------------------------------------------------
# 2. KHỞI TẠO MÔ HÌNH VÀ CHECKPOINT TÁC GIẢ
# ------------------------------------------------------------------------------
print("\n[2/4] Đang nạp Checkpoint tác giả từ Hugging Face...")
checkpoint_name = "MickyMike/0-GPT2SP-springxd"
tokenizer = GPT2Tokenizer.from_pretrained(checkpoint_name)
tokenizer.pad_token = tokenizer.eos_token

class GPT2SPModel(nn.Module):
    def __init__(self, ckpt):
        super().__init__()
        self.gpt2 = GPT2Model.from_pretrained(ckpt)
        self.dense1 = nn.Linear(768, 3072, bias=False)
        self.dense2 = nn.Linear(3072, 768, bias=False)
        self.score = nn.Linear(768, 1, bias=False)

    def forward(self, input_ids, attention_mask):
        outputs = self.gpt2(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        batch_size = input_ids.shape[0]
        seq_lengths = (torch.ne(input_ids, tokenizer.pad_token_id).sum(dim=-1) - 1).to(device)
        pooled = last_hidden_state[torch.arange(batch_size, device=device), seq_lengths]
        return self.score(self.dense2(self.dense1(pooled))).squeeze(-1)

model = GPT2SPModel(checkpoint_name).to(device)
model.eval()

def run_inference(texts, max_len=20, batch_size=32):
    preds = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            inp = tokenizer(batch, padding='max_length', truncation=True, max_length=max_len, return_tensors="pt").to(device)
            p = model(inp['input_ids'], inp['attention_mask'])
            preds.extend(p.cpu().numpy().tolist())
    return np.array(preds)

# ------------------------------------------------------------------------------
# 3. CHẠY 3 SETTINGS THỰC NGHIỆM CỦA GPT2SP
# ------------------------------------------------------------------------------
print("\n[3/4] Đang chạy suy luận cho 3 Settings thực nghiệm...")

# Setting 1: Title only, len = 20 (Repo Baseline Default)
texts_s1 = test_raw['title'].astype(str).tolist()
preds_s1 = run_inference(texts_s1, max_len=20)
print(f" • Hoàn tất Setting 1 (Title only, len=20): MAE = {np.mean(np.abs(true_sp - preds_s1)):.4f}")

# Setting 2: Title + Description, len = 128 (Paper Grounded Section 3.1 & 4.1)
desc_filled = test_raw['description'].fillna('').astype(str)
texts_s2 = (test_raw['title'].astype(str) + " " + desc_filled).tolist()
preds_s2 = run_inference(texts_s2, max_len=128)
print(f" • Hoàn tất Setting 2 (Full Context, len=128): MAE = {np.mean(np.abs(true_sp - preds_s2)):.4f}")

# Setting 3: Clean Planning-Time Snapshot (Nhóm 3 Leakage-Free)
# Khớp theo issuekey giữa test_raw và df_clean
merged_test = pd.merge(test_raw[['issuekey', 'storypoint']], df_clean[['Issue_Key', 'Clean_Title', 'Clean_Description']], 
                       left_on='issuekey', right_on='Issue_Key', how='left')
merged_test['Clean_Title'] = merged_test['Clean_Title'].fillna(test_raw['title'])
merged_test['Clean_Description'] = merged_test['Clean_Description'].fillna('')
texts_s3 = (merged_test['Clean_Title'].astype(str) + " " + merged_test['Clean_Description'].astype(str)).tolist()
preds_s3 = run_inference(texts_s3, max_len=128)
print(f" • Hoàn tất Setting 3 (Planning-Time Snapshot, len=128): MAE = {np.mean(np.abs(true_sp - preds_s3)):.4f}")

# Median Effort Baseline
median_val = float(train_raw['storypoint'].median())
preds_median = np.full_like(true_sp, fill_value=median_val)
print(f" • Tham chiếu Median Baseline: MAE = {np.mean(np.abs(true_sp - preds_median)):.4f}")

# Xuất file kết quả chi tiết từng mẫu
pred_df = pd.DataFrame({
    'issuekey': test_raw['issuekey'],
    'true_storypoint': true_sp,
    'pred_median_baseline': preds_median,
    'pred_gpt2sp_setting1': preds_s1,
    'pred_gpt2sp_setting2': preds_s2,
    'pred_gpt2sp_setting3': preds_s3,
    'err_median_baseline': np.abs(true_sp - preds_median),
    'err_gpt2sp_setting1': np.abs(true_sp - preds_s1),
    'err_gpt2sp_setting2': np.abs(true_sp - preds_s2),
    'err_gpt2sp_setting3': np.abs(true_sp - preds_s3)
})
pred_out = os.path.join(output_dir, 'predictions_gpt2sp_3settings.csv')
pred_df.to_csv(pred_out, index=False, encoding='utf-8-sig')
print(f"💾 Đã lưu: {pred_out}")

# ------------------------------------------------------------------------------
# 4. PHÂN TÍCH ĐỘ NHẠY ĐA HẠT GIỐNG NGẪU NHIÊN (MULTI-SEED ROBUSTNESS)
# ------------------------------------------------------------------------------
print("\n[4/4] Đang thực hiện Phân tích độ nhạy qua 5 Seeds ngẫu nhiên...")
seeds = [42, 123, 456, 789, 2026]
seed_records = []

for s in seeds:
    torch.manual_seed(s)
    np.random.seed(s)
    # Lấy mẫu ngẫu nhiên có hoàn lại 80% test set (Bootstrap evaluation) để đo tính ổn định
    indices = np.random.choice(len(true_sp), size=int(len(true_sp)*0.8), replace=True)
    sub_true = true_sp[indices]
    sub_p1 = preds_s1[indices]
    sub_p2 = preds_s2[indices]
    sub_p3 = preds_s3[indices]
    
    seed_records.append({
        'seed': s,
        'Setting_1_MAE': np.mean(np.abs(sub_true - sub_p1)),
        'Setting_2_MAE': np.mean(np.abs(sub_true - sub_p2)),
        'Setting_3_MAE': np.mean(np.abs(sub_true - sub_p3)),
        'Median_Baseline_MAE': np.mean(np.abs(sub_true - median_val))
    })

seed_df = pd.DataFrame(seed_records)
print("\nBảng kết quả kiểm tra độ nhạy qua 5 seeds:")
display(seed_df)

seed_summary = pd.DataFrame({
    'Configuration': ['Median Effort Baseline', 'GPT2SP Setting 1 (Title)', 'GPT2SP Setting 2 (Full Context)', 'GPT2SP Setting 3 (Planning-Time)'],
    'MAE Mean': [seed_df['Median_Baseline_MAE'].mean(), seed_df['Setting_1_MAE'].mean(), seed_df['Setting_2_MAE'].mean(), seed_df['Setting_3_MAE'].mean()],
    'MAE Std': [seed_df['Median_Baseline_MAE'].std(), seed_df['Setting_1_MAE'].std(), seed_df['Setting_2_MAE'].std(), seed_df['Setting_3_MAE'].std()]
})
seed_summary['Formatted (Mean +- Std)'] = seed_summary.apply(lambda r: f"{r['MAE Mean']:.4f} +- {r['MAE Std']:.4f}", axis=1)
display(seed_summary[['Configuration', 'Formatted (Mean +- Std)']])

seed_out = os.path.join(output_dir, 'multiseed_results.csv')
seed_summary.to_csv(seed_out, index=False, encoding='utf-8-sig')
print(f"💾 Đã lưu: {seed_out}")
print("\n🎉 HOÀN THÀNH NOTEBOOK 1 THÀNH CÔNG RỰC RỠ!")
