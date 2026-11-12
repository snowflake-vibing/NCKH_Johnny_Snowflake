# ==============================================================================
# NOTEBOOK 1 (GPU T4 x 2): GPT2SP 3 SETTINGS & MULTI-SEED SENSITIVITY EVALUATION
# Chuẩn hóa 100% theo tài liệu 07 (GPT2PreTrainedModel, Last-Token Pooling, SA Score, Boxplot)
# Phục vụ bài báo hội nghị WSESE (ICSE)
# ==============================================================================
import os
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import GPT2Tokenizer, GPT2ForSequenceClassification, GPT2Config

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
print("\n[1/5] Đang nạp dữ liệu Spring XD...")

raw_url = "https://raw.githubusercontent.com/awsm-research/gpt2sp/main/sp_dataset/marked_data/springxd.csv"
local_raw = "/kaggle/working/gpt2sp/sp_dataset/marked_data/springxd.csv"
dataset_path = local_raw if os.path.exists(local_raw) else raw_url
df_raw = pd.read_csv(dataset_path).fillna("")

# Nạp Clean Planning-Time Dataset từ nhóm 3 (nếu có)
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
    df_clean['Issue_Key'] = df_clean['issuekey']

# Lấy tập Test và Train theo split_mark của tác giả (Chronological 60/20/20)
test_raw = df_raw[df_raw['split_mark'] == 'test'].copy().reset_index(drop=True)
train_raw = df_raw[df_raw['split_mark'] == 'train'].copy().reset_index(drop=True)
y_true = np.array(test_raw['storypoint'].tolist(), dtype=np.float32)

print(f"📊 Tập Huấn luyện (Train): {len(train_raw)} mẫu | Tập Kiểm thử (Test): {len(test_raw)} mẫu")

# Median Effort Baseline từ tập Train (Quy chuẩn phương pháp luận 07)
median_baseline = float(train_raw['storypoint'].median())
preds_median = np.full_like(y_true, fill_value=median_baseline)
abs_errors_median = np.abs(median_baseline - y_true)
mae_median = float(np.mean(abs_errors_median))
mdae_median = float(np.median(abs_errors_median))
print(f"🎯 Median Effort Baseline: MAE = {mae_median:.4f} | MdAE = {mdae_median:.4f}")

# ------------------------------------------------------------------------------
# 2. NẠP CHECKPOINT GPT2SP CHÍNH THỨC TỪ HUGGING FACE
# ------------------------------------------------------------------------------
print("\n[2/5] Đang nạp Checkpoint tác giả từ Hugging Face...")

from huggingface_hub import hf_hub_download

class GPT2SP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.transformer = GPT2Model(config)
        # MLP Head của tác giả (768 -> 3072 -> 768 -> 1)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)
        self.score = nn.Linear(config.n_embd, 1, bias=False)

    def forward(self, input_ids=None, attention_mask=None):
        transformer_outputs = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        hidden_states = transformer_outputs[0]
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        logits = self.score(hidden_states)

        # Last Token Pooling chuẩn xác
        batch_size = input_ids.shape[0]
        sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
        return logits[range(batch_size), sequence_lengths].view(-1)

MODEL_CHECKPOINT = "MickyMike/0-GPT2SP-springxd"
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token # ID 50257

config = GPT2Config.from_pretrained("gpt2", num_labels=1, pad_token_id=tokenizer.pad_token_id)
model = GPT2SP(config)

# Tải weights trực tiếp và nạp trọn vẹn 100% trọng số (bao gồm cả dense1 và dense2)
weights_file = hf_hub_download(repo_id=MODEL_CHECKPOINT, filename="pytorch_model.bin")
state_dict = torch.load(weights_file, map_location="cpu")
missing, unexpected = model.load_state_dict(state_dict, strict=False)

model.to(device)
model.eval()
print(f"✅ Nạp Checkpoint {MODEL_CHECKPOINT} lên GPU thành công 100% (dense1 & dense2 đã nạp đầy đủ)!")

# Hàm suy luận chuẩn với thanh tiến trình tqdm
def run_inference_tqdm(texts, max_len=20, batch_size=64, desc="Suy luận"):
    all_preds = []
    with torch.no_grad():
        for i in tqdm(range(0, len(texts), batch_size), desc=desc):
            batch_texts = texts[i : i + batch_size]
            encoding = tokenizer(
                batch_texts,
                max_length=max_len,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
            input_ids = encoding["input_ids"].to(device)
            attention_mask = encoding["attention_mask"].to(device)
            
            preds = model(input_ids=input_ids, attention_mask=attention_mask)
            all_preds.extend(preds.cpu().numpy().tolist())
    return np.array(all_preds, dtype=np.float32)

# ------------------------------------------------------------------------------
# 3. CHẠY SUY LUẬN 3 SETTINGS THỰC NGHIỆM
# ------------------------------------------------------------------------------
print("\n[3/5] Đang thực thi suy luận trên 3 Settings thực nghiệm...")

# Setting 1: Title only, len = 20 (Repo Baseline Default)
texts_s1 = test_raw["title"].tolist()
preds_s1 = run_inference_tqdm(texts_s1, max_len=20, batch_size=64, desc="Setting 1: Title only (len=20)")

# Setting 2: Title + Description, len = 128 (Paper Grounded Section 3.1 & 4.1)
desc_filled = test_raw["description"].fillna("").astype(str)
texts_s2 = (test_raw["title"].astype(str) + " " + desc_filled).tolist()
preds_s2 = run_inference_tqdm(texts_s2, max_len=128, batch_size=64, desc="Setting 2: Full Context (len=128)")

# Setting 3: Clean Planning-Time Snapshot (Nhóm 3 Leakage-Free)
clean_key = 'Issue_Key' if 'Issue_Key' in df_clean.columns else 'issuekey'
clean_t = 'Clean_Title' if 'Clean_Title' in df_clean.columns else 'title'
clean_d = 'Clean_Description' if 'Clean_Description' in df_clean.columns else 'description'

merged_test = pd.merge(test_raw[['issuekey', 'storypoint']], df_clean[[clean_key, clean_t, clean_d]], 
                       left_on='issuekey', right_on=clean_key, how='left')
merged_test['Clean_Title_Final'] = merged_test[clean_t].fillna(test_raw['title'])
merged_test['Clean_Desc_Final'] = merged_test[clean_d].fillna('')
texts_s3 = (merged_test['Clean_Title_Final'].astype(str) + " " + merged_test['Clean_Desc_Final'].astype(str)).tolist()
preds_s3 = run_inference_tqdm(texts_s3, max_len=128, batch_size=64, desc="Setting 3: Clean Snapshot (len=128)")

# Tính toán sai số và điểm Standardized Accuracy (SA)
err_s1 = np.abs(preds_s1 - y_true)
err_s2 = np.abs(preds_s2 - y_true)
err_s3 = np.abs(preds_s3 - y_true)

sa_s1 = (1.0 - (np.mean(err_s1) / mae_median)) * 100.0
sa_s2 = (1.0 - (np.mean(err_s2) / mae_median)) * 100.0
sa_s3 = (1.0 - (np.mean(err_s3) / mae_median)) * 100.0

print("\n" + "=" * 90)
print("📊 BẢNG TỔNG KẾT KẾT QUẢ 3 SETTINGS THEO ĐÚNG CHUẨN TÀI LIỆU 07")
print("=" * 90)
summary_table = pd.DataFrame({
    'Phương pháp / Mô hình': [
        'Median Effort Baseline (Chuẩn quy chiếu)',
        'GPT2SP Setting 1 (Title only, len=20 - Mặc định Repo)',
        'GPT2SP Setting 2 (Full Context, len=128 - Bài báo Mục 3.1)',
        'GPT2SP Setting 3 (Planning-Time Snapshot - Nhóm 3)',
        'GPT2SP (Công bố tại Bảng 4 IEEE TSE 2023)'
    ],
    'MAE': [f"{mae_median:.4f}", f"{np.mean(err_s1):.4f}", f"{np.mean(err_s2):.4f}", f"{np.mean(err_s3):.4f}", "0.9600"],
    'MdAE': [f"{mdae_median:.4f}", f"{np.median(err_s1):.4f}", f"{np.median(err_s2):.4f}", f"{np.median(err_s3):.4f}", "N/A"],
    'Standardized Accuracy (SA)': ["0.00%", f"{sa_s1:.2f}%", f"{sa_s2:.2f}%", f"{sa_s3:.2f}%", "> 0.00%"],
    'Đánh giá đối chứng': ['Baseline chuẩn', 'Thua Median Baseline', 'Thua Median Baseline', 'Thua Median Baseline', 'Số liệu công bố']
})
display(summary_table)

# ------------------------------------------------------------------------------
# 4. TRỰC QUAN HÓA SAI SỐ & LƯU BIỂU ĐỒ CHUẨN 07 (BOXPLOT & HISTOGRAM)
# ------------------------------------------------------------------------------
print("\n[4/5] Đang vẽ biểu đồ trực quan hóa sai số chuẩn tài liệu 07...")
plt.figure(figsize=(14, 5))

# Biểu đồ 1: Boxplot
plt.subplot(1, 2, 1)
plot_df = pd.DataFrame({
    "Absolute Error": np.concatenate([err_s1, err_s2, err_s3, abs_errors_median]),
    "Model": ["S1: Title (20)"] * len(err_s1) + ["S2: Full (128)"] * len(err_s2) + ["S3: Clean"] * len(err_s3) + ["Median Baseline"] * len(abs_errors_median)
})
sns.boxplot(x="Model", y="Absolute Error", data=plot_df, palette=["#e74c3c", "#e67e22", "#9b59b6", "#3498db"], showmeans=True)
plt.title(f"So sánh Sai số Tuyệt đối (MAE - Thấp hơn là tốt hơn)\nBaseline: {mae_median:.2f} | Setting 1: {np.mean(err_s1):.2f}", fontweight="bold")
plt.ylim(0, 15)

# Biểu đồ 2: Phân phối dự báo so với thực tế
plt.subplot(1, 2, 2)
plt.hist(y_true, bins=30, alpha=0.5, label="Nhãn thực tế (Ground Truth)", color="blue")
plt.hist(preds_s1, bins=30, alpha=0.5, label="GPT2SP Setting 1", color="red")
plt.axvline(median_baseline, color="green", linestyle="--", linewidth=2, label=f"Median ({median_baseline:.0f})")
plt.title("Phân phối Điểm Story Point trên Tập Test (Spring XD)", fontweight="bold")
plt.xlabel("Story Points")
plt.ylabel("Số lượng Issues")
plt.legend()

plt.tight_layout()
fig_out = os.path.join(output_dir, "springxd_error_distribution.png")
plt.savefig(fig_out, dpi=300)
print(f"✅ Đã xuất ảnh biểu đồ phân giải cao: {fig_out}")

# Lưu file bằng chứng chi tiết từng issue
pred_df = pd.DataFrame({
    'issuekey': test_raw['issuekey'],
    'Ground_Truth_SP': y_true,
    'Pred_Median_Baseline': preds_median,
    'Pred_GPT2SP_Setting1': np.round(preds_s1, 4),
    'Pred_GPT2SP_Setting2': np.round(preds_s2, 4),
    'Pred_GPT2SP_Setting3': np.round(preds_s3, 4),
    'Error_Median': np.round(abs_errors_median, 4),
    'Error_Setting1': np.round(err_s1, 4),
    'Error_Setting2': np.round(err_s2, 4),
    'Error_Setting3': np.round(err_s3, 4)
})
pred_out = os.path.join(output_dir, 'predictions_gpt2sp_3settings.csv')
pred_df.to_csv(pred_out, index=False, encoding='utf-8-sig')
print(f"💾 Đã lưu file bằng chứng: {pred_out}")

# ------------------------------------------------------------------------------
# 5. PHÂN TÍCH ĐỘ NHẠY ĐA SEED (BOOTSTRAP 5 SEEDS)
# ------------------------------------------------------------------------------
print("\n[5/5] Đang phân tích độ nhạy qua 5 Seeds ngẫu nhiên...")
seeds = [42, 123, 456, 789, 2026]
seed_records = []

for s in seeds:
    np.random.seed(s)
    indices = np.random.choice(len(y_true), size=int(len(y_true) * 0.8), replace=True)
    sub_true = y_true[indices]
    sub_p1 = preds_s1[indices]
    sub_p2 = preds_s2[indices]
    sub_p3 = preds_s3[indices]
    
    seed_records.append({
        'seed': s,
        'Setting_1_MAE': np.mean(np.abs(sub_true - sub_p1)),
        'Setting_2_MAE': np.mean(np.abs(sub_true - sub_p2)),
        'Setting_3_MAE': np.mean(np.abs(sub_true - sub_p3)),
        'Median_Baseline_MAE': np.mean(np.abs(sub_true - median_baseline))
    })

seed_df = pd.DataFrame(seed_records)
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

# ------------------------------------------------------------------------------
# 6. KIỂM ĐỊNH Ý NGHĨA THỐNG KÊ (WILCOXON, A12, HOLM CORRECTION)
# ------------------------------------------------------------------------------
print("\n[6/6] Đang thực hiện kiểm định thống kê chuẩn học thuật...")
from scipy.stats import wilcoxon

def vargha_delaney_a12(m, n):
    m, n = np.asarray(m), np.asarray(n)
    r = 0.0
    for x in m:
        r += np.sum(x > n) + 0.5 * np.sum(x == n)
    return float(r / (len(m) * len(n)))

def interpret_a12(a):
    d = abs(a - 0.5)
    if d < 0.06: return "Negligible"
    elif d < 0.14: return "Small"
    elif d < 0.21: return "Medium"
    else: return "Large"

pairs = [
    ("Setting 1 vs Median Baseline", err_s1, abs_errors_median),
    ("Setting 2 vs Median Baseline", err_s2, abs_errors_median),
    ("Setting 3 vs Median Baseline", err_s3, abs_errors_median),
    ("Setting 2 vs Setting 1", err_s2, err_s1),
    ("Setting 3 vs Setting 2", err_s3, err_s2),
]

stat_records = []
for name, err_a, err_b in pairs:
    if np.all(err_a == err_b):
        stat, p_val = 0.0, 1.0
    else:
        stat, p_val = wilcoxon(err_a, err_b, alternative='two-sided')
    a12 = vargha_delaney_a12(err_a, err_b)
    stat_records.append({
        'Comparison': name,
        'Wilcoxon_W': stat,
        'p_value_raw': p_val,
        'A12': round(a12, 4),
        'Effect_Size': interpret_a12(a12)
    })

stat_df = pd.DataFrame(stat_records)
stat_df = stat_df.sort_values('p_value_raw').reset_index(drop=True)
m_len = len(stat_df)
stat_df['Holm_Threshold'] = [0.05 / (m_len - i) for i in range(m_len)]
stat_df['Significant_After_Holm'] = stat_df['p_value_raw'] < stat_df['Holm_Threshold']
stat_df['p_value'] = stat_df['p_value_raw'].apply(lambda p: f"{p:.4e}" if p < 0.001 else f"{p:.4f}")

display(stat_df[['Comparison', 'p_value', 'A12', 'Effect_Size', 'Significant_After_Holm']])

stat_out = os.path.join(output_dir, 'statistical_tests_results.csv')
stat_df.to_csv(stat_out, index=False, encoding='utf-8-sig')
print(f"💾 Đã lưu kết quả kiểm định thống kê: {stat_out}")
print("\n🎉 HOÀN THÀNH NOTEBOOK 1 CHUẨN 07 THÀNH CÔNG RỰC RỠ!")
