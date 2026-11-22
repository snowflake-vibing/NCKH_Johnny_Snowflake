# 🚀 Kaggle Modular Runner (GitHub ➔ Kaggle ➔ Hugging Face Hub)

Thư mục `kaggle/` được tổ chức theo kiến trúc **Thin Runner + Modular Python Scripts** phục vụ đề tài:
**"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"** (WSESE / ICSE 2026).

---

## 🔄 Kiến Trúc Luồng Thực Nghiệm

```text
[Local Code (Branch)] ──git push──► [GitHub Public Repo]
                                           │
                                           ▼ (git clone -b <branch>)
[Kaggle GPU/CPU Runtime] ◄── [kaggle_runner.ipynb] (đọc HF_TOKEN / hf_token từ Secrets)
        │
        ├──► Lưu Results (.csv, .png, run_metadata.json) ──► [HF Dataset Repo]
        └──► Lưu Model Checkpoints (.bin, config.json)    ──► [HF Model Repo]
```

---

## 📂 Danh Sách File Trong `kaggle/`

| File | Vai trò |
| :--- | :--- |
| [config.py](file:///d:/NCKH_3/kaggle/config.py) | Cấu hình repo, bảng tham chiếu 16 dự án (IEEE TSE 2019 & 2023), hàm tải & tách tập Train/Val/Test |
| [model.py](file:///d:/NCKH_3/kaggle/model.py) | Kiến trúc `GPT2SP(nn.Module)` thuần PyTorch (giữ nguyên MLP Head 2 tầng) & dọn cache ổ đĩa |
| [metrics.py](file:///d:/NCKH_3/kaggle/metrics.py) | Tính MAE, MdAE, Standardized Accuracy ($SA$), Wilcoxon Signed-Rank Test, Vargha-Delaney $\hat{A}_{12}$, Holm-Bonferroni |
| [hf_utils.py](file:///d:/NCKH_3/kaggle/hf_utils.py) | Đọc Kaggle Secrets (`HF_TOKEN`/`hf_token`), tự động tạo HF repo, upload cuốn chiếu, auto-resume, xuất `run_metadata.json` |
| [run_gpt2sp_16projects.py](file:///d:/NCKH_3/kaggle/run_gpt2sp_16projects.py) | **Chiến lược 1:** Tái lập suy luận trên 16 dự án từ official Hugging Face checkpoints (`MickyMike/0-GPT2SP-*`) |
| [run_gpt2sp_retrain.py](file:///d:/NCKH_3/kaggle/run_gpt2sp_retrain.py) | **Chiến lược 2:** Huấn luyện lại GPT2SP từ đầu (`title_20`, `full_128`, `planning_clean`) kèm micro-batching & đẩy checkpoint lên HF |
| [run_deepse_audit.py](file:///d:/NCKH_3/kaggle/run_deepse_audit.py) | Thẩm định Baseline Inflation (Table II) và lỗi `+1.0` trong `create_model.py` của Deep-SE trên 16 dự án |
| [kaggle_runner.ipynb](file:///d:/NCKH_3/kaggle/kaggle_runner.ipynb) | Notebook Thin Runner tải lên Kaggle (5 cells: cấu hình, auth HF Secrets, clone branch, run, xem tóm tắt) |
| [requirements.txt](file:///d:/NCKH_3/kaggle/requirements.txt) | Danh sách thư viện phụ thuộc tối thiểu |

---

## ⚙️ Hướng Dẫn Thiết Lập & Chạy Trên Kaggle

### Bước 1: Tạo token Hugging Face quyền Write & gắn vào Kaggle Secrets
1. Trên Hugging Face: vào **Settings → Access Tokens → New token** với quyền **Write**.
2. Trên Kaggle Notebook: chọn **Add-ons → Secrets → Add a new secret**:
   * **Label:** `hf_token` *(hoặc `HF_TOKEN` — code tự nhận diện cả hai)*.
   * **Value:** dán token vừa tạo và nhớ **bật tích xanh** cho notebook sử dụng.
3. Ở cột phải Kaggle:
   * **Accelerator:** `GPU T4 x 2` (cho `gpt2sp_16projects` và `gpt2sp_retrain`) hoặc `CPU` (cho `deepse_audit`).
   * **Internet:** gạt sang **ON**.

### Bước 2: Chỉnh tham số ở Cell 1 của `kaggle_runner.ipynb` và bấm Run All
* `GIT_BRANCH`: đổi sang tên branch bạn vừa `git push` (ví dụ: `"exp/gpt2sp-16proj"`).
* `EXPERIMENT`: chọn `"gpt2sp_16projects"`, `"gpt2sp_retrain"`, hoặc `"deepse_audit"`.
* `EXTRA_ARGS` (tùy chọn):
  * Test nhanh 2 dự án: `"--projects springxd,bamboo"`
  * Huấn luyện lại trên dữ liệu sạch Planning-Time: `"--project springxd --setting planning_clean --epochs 20 --seeds 42,123"`
  * Huấn luyện Full Context (Title + Description): `"--project springxd --setting full_128 --epochs 20"`

---

## 💻 Chạy Thử Cục Bộ (Không Đẩy Lên HF)

```bash
python kaggle/run_gpt2sp_16projects.py --projects springxd --no-hf-push
python kaggle/run_gpt2sp_retrain.py --project springxd --setting planning_clean --epochs 3 --no-hf-push
python kaggle/run_deepse_audit.py --no-hf-push
```
