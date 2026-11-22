# 🚀 Kaggle Modular Runner (GitHub ➔ Kaggle ➔ Hugging Face Hub)

Thư mục `kaggle/` được tổ chức theo kiến trúc **Thin Runner + Modular Python Scripts** phục vụ đề tài Nghiên cứu Khoa học:  
**"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"** *(WSESE / ICSE 2026)*.

Tài liệu này vừa hướng dẫn vận hành luồng chạy Kaggle, vừa **giải trình minh bạch nguồn gốc khoa học và kỹ thuật (Code Provenance & Traceability)** của từng dòng mã nguồn: đoạn nào kế thừa nguyên bản từ bài báo/repository của tác giả gốc, đoạn nào hiệu chỉnh kỹ thuật để tương thích phần cứng/thư viện, và đoạn nào là hạ tầng ResearchOps của Nhóm 3.

---

## 🔄 1. Kiến Trúc Luồng Thực Nghiệm

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

## 📂 2. Danh Sách File Trong `kaggle/`

| File | Vai trò |
| :--- | :--- |
| [config.py](config.py) | Cấu hình repo, bảng tham chiếu 16 dự án (IEEE TSE 2019 & 2023), helper tải CSV & tách `train`/`val`/`test` |
| [model.py](model.py) | Kiến trúc `GPT2SP(nn.Module)` thuần PyTorch (giữ nguyên MLP Head 2 tầng), `safe_torch_load` & dọn cache HF |
| [metrics.py](metrics.py) | Tính MAE, MdAE, Standardized Accuracy ($SA$), `safe_wilcoxon`, `vargha_delaney_a12`, `holm_bonferroni` |
| [hf_utils.py](hf_utils.py) | Đọc Kaggle Secrets (`HF_TOKEN`/`hf_token`), tự tạo HF repo, upload cuốn chiếu, auto-resume & ghi `run_metadata.json` |
| [run_gpt2sp_16projects.py](run_gpt2sp_16projects.py) | **Chiến lược 1:** Tái lập suy luận trên 16 dự án từ official HF checkpoints (`MickyMike/0-GPT2SP-*`) |
| [run_gpt2sp_retrain.py](run_gpt2sp_retrain.py) | **Chiến lược 2:** Huấn luyện lại GPT2SP từ đầu (`title_20`, `full_128`, `planning_clean`) & đẩy checkpoint lên HF |
| [run_deepse_audit.py](run_deepse_audit.py) | Thẩm định Baseline Inflation (Table II) và phép cộng `+1.0` trong `create_model.py` của Deep-SE trên 16 dự án |
| [kaggle_runner.ipynb](kaggle_runner.ipynb) | Thin Runner Notebook trên Kaggle (6 Markdown + 5 Code cells: cấu hình, auth HF Secrets, clone branch, run, xem tóm tắt) |
| [requirements.txt](requirements.txt) | Danh sách thư viện phụ thuộc tối thiểu (`numpy`, `pandas`, `scipy`, `matplotlib`, `torch`, `transformers>=4.36.0`, `huggingface_hub>=0.20.0`, `tqdm`) |
| [README.md](README.md) | Tài liệu vận hành & truy vết nguồn gốc mã nguồn |

---

## 📚 3. Cơ Sở Khoa Học & Nguồn Gốc Mã Nguồn (Code Provenance & Traceability)

### 3.1. Nguồn gốc bài báo & kho lưu trữ chính thức được đối soát

1. **GPT2SP (Fu & Tantithamthavorn, IEEE TSE 2023):**
   * **Bài báo:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach*, IEEE Transactions on Software Engineering, DOI: [`10.1109/TSE.2022.3158252`](https://doi.org/10.1109/TSE.2022.3158252).
   * **Vị trí công bố tài nguyên trong bài báo:** **Trang 2, Cột 2 (Section 1 — Open Science)** công bố kho mã nguồn [`awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp); **Trang 15, Cột 1 (Acknowledgments)** xác nhận công bố dataset, scripts, predictions và model checkpoints.
   * **Checkpoints chính thức trên Hugging Face Hub:** Tài khoản [`MickyMike`](https://huggingface.co/MickyMike) lưu trữ toàn bộ 217 model weights của tác giả, trong đó có 16 checkpoints Within-Project Seed 0 dạng `MickyMike/0-GPT2SP-<project>` (kèm các seed `1`, `2`, `6`, `7`).
2. **Deep-SE (Choetkiertikul et al., IEEE TSE 2019):**
   * **Bài báo:** *A Deep Learning Model for Estimating Story Points*, IEEE Transactions on Software Engineering, DOI: [`10.1109/TSE.2017.2787834`](https://doi.org/10.1109/TSE.2017.2787834).
   * **Kho lưu trữ gốc:** [`morakotch/datasets`](https://github.com/morakotch/datasets/tree/master/storypoint/IEEE%20TSE2018) (SEA@UOW), chứa 16 tập CSV, ma trận phân chia thời gian `_3sets.txt` (`divide_data_sortdate.py`) và mã nguồn huấn luyện `Deep-SE/classification/`.
3. **Chuẩn mực Phương pháp luận & Kiểm định Thống kê:**
   * **Shepperd & MacDonell (IEEE TSE 2012):** Khung đánh giá chuẩn Standardized Accuracy ($SA$) và Median/Mean/Random Baselines.
   * **Kitchenham et al. (IEEE TSE 2017):** Phép kiểm phi tham số Wilcoxon Signed-Rank Test, Effect Size và kiểm soát sai số đa kiểm định.
   * **Tawosi et al. (IEEE TSE 2022 / TAWOS v1.1):** Dữ liệu lịch sử Jira & tái lập kiểm soát rò rỉ dữ liệu.

---

### 3.2. Truy vết chi tiết từng module (`File-by-File Provenance`)

#### 1. `config.py` — Dữ liệu & Số liệu đối chứng 16 dự án
* **Nguồn dữ liệu CSV:**
  * `GPT2SP_DATA_BASE_URL` trỏ tới thư mục [`sp_dataset/marked_data/`](https://github.com/awsm-research/gpt2sp/tree/main/sp_dataset/marked_data) của `awsm-research/gpt2sp` (tải qua `load_gpt2sp_splits` dựa theo cột `split_mark` `train`/`val`/`test` tỷ lệ 60/20/20).
  * `DEEPSE_DATA_BASE_URL` trỏ tới [`storypoint/IEEE TSE2018/Deep-SE/data/`](https://github.com/morakotch/datasets/tree/master/storypoint/IEEE%20TSE2018/Deep-SE/data) của `morakotch/datasets` (tải file `<project>.csv` và ma trận `<project>_3sets.txt` sinh từ `divide_data_sortdate.py` qua `load_deepse_splits`).
* **Bảng tham chiếu `BENCHMARK_PROJECTS`:**
  * `reported_gpt2sp`, `reported_deepse_in_gpt2sp`, `rep_median`, `rep_mean`: Đối soát từ **Table 4** bài báo GPT2SP và file [`data_model_analysis/within_proj_data.csv`](https://github.com/awsm-research/gpt2sp/blob/main/data_model_analysis/within_proj_data.csv).
  * `reported_deepse`, `reported_deepse_sa`: Trích xuất từ **Table II (Trang 8)** bài báo Deep-SE (IEEE TSE 2019).

#### 2. `model.py` — Kiến trúc `GPT2SP` & Nạp Trọng Số Hugging Face
* **Lấy nguyên bản từ đâu:** File [`GPT2SP.py`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py) của `awsm-research/gpt2sp`, nơi tác giả định nghĩa lớp hồi quy trên nền `GPT2Model` với **MLP Head 2 tầng không bias**:
  * `self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)` ($768 \rightarrow 3072$)
  * `self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)` ($3072 \rightarrow 768$)
  * `self.score = nn.Linear(config.n_embd, 1, bias=False)` ($768 \rightarrow 1$)
  * Cơ chế **Last Token Pooling** lấy logit tại token thực cuối cùng trước padding (`pad_token_id = eos_token_id`).
* **Vì sao viết lại bằng `torch.nn.Module` thuần túy thay vì kế thừa `GPT2PreTrainedModel`:**
  1. Trên `transformers >= 4.40`, kế thừa `GPT2PreTrainedModel` dễ phát sinh `AttributeError: 'GPT2SP' object has no attribute 'all_tied_weights_keys'` trong `_finalize_model_loading`.
  2. Nếu dùng `GPT2ForSequenceClassification` mặc định của Hugging Face, hai tầng `dense1.weight` và `dense2.weight` trong checkpoint của tác giả sẽ bị bỏ qua (`UNEXPECTED`).
  3. Lớp `GPT2SP(nn.Module)` kèm hàm kiểm tra bắt buộc `required_head_keys = ("dense1.weight", "dense2.weight", "score.weight")` trong `load_official_gpt2sp_checkpoint`, `torch.clamp(..., min=0)` cho chuỗi toàn padding, `safe_torch_load` (`weights_only=True` có fallback), và `cleanup_downloaded_file` xóa cache nặng sau mỗi dự án để tránh tràn ổ đĩa 20GB của Kaggle.

#### 3. `run_gpt2sp_16projects.py` — Chiến lược 1: Kiểm chứng 16 Official Checkpoints
* **Tiền xử lý giữ nguyên theo code tác giả:** Lấy từ **Cell 4 & Cell 6** trong [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) của Fu et al.:
  * Hàm `prepare_dataframe` gốc chỉ nạp `data['title']` và `SEQUENCE_LEN = 20` (bỏ qua cột `description` dù phần văn bản bài báo mô tả dùng cả hai với độ dài tới 1024). Mặc định script chạy đúng `Title-only, max_length=20` để kiểm chứng công bằng chính weights tác giả phát hành (`MickyMike/0-GPT2SP-<project>`).
  * Cờ `--include-description --max-length 128` được bổ sung để kiểm chứng độc lập thiết lập Full Context (Title + Description) như bài báo tuyên bố.
* **Đánh giá trung thực:** Luôn tính `Real_Median_MAE` và `Real_Mean_MAE` **chỉ từ tập `train`** (`np.median(y_train)`, `np.mean(y_train)`), tuyệt đối không lấy thống kê từ `val`/`test`.

#### 4. `run_gpt2sp_retrain.py` — Chiến lược 2: Huấn luyện lại từ `gpt2` gốc
* **Siêu tham số gốc từ `model_training_notebook.ipynb` (Cell 4 & Cell 6):**
  * `EPOCHS = 20`, `LR = 5e-4`, hàm mất mát `nn.L1Loss()` (MAE Loss), optimizer `AdamW`, `get_linear_schedule_with_warmup`, gradient clipping `1.0`, và `BATCH_SIZE_RATIO = 0.3` (30% kích thước tập train).
  * Chọn checkpoint tốt nhất dựa trên `Validation MAE` qua từng epoch, sau đó đánh giá 1 lần trên `Test`.
* **Cải tiến kỹ thuật & Kiểm soát Leakage của Nhóm 3:**
  * **Micro-batching + Gradient Accumulation:** Batch động 30% (~635 mẫu với Spring XD) chạy được ở `seq_len=20` trên RTX 3090 (24GB) của tác giả nhưng sẽ gây tràn VRAM (OOM) ở `seq_len=128` trên Kaggle T4 (15GB). Script giữ nguyên effective batch size 30% nhưng chia micro-batch vật lý (32 hoặc 64) và cộng dồn gradient (`loss / accum_steps`).
  * **3 nhánh thực nghiệm (`--setting`):** `title_20` (theo code tác giả), `full_128` (theo văn bản bài báo), và `planning_clean` (đọc bộ dữ liệu sạch không rò rỉ tại `SP_Estimation_Date` từ [../docs/draft/springxd_cleaned_dataset.csv](../docs/draft/springxd_cleaned_dataset.csv) hoặc `data/clean/springxd_cleaned_dataset.csv`).

#### 5. `run_deepse_audit.py` — Kiểm định Baseline Inflation & Code Bias của Deep-SE
* **Lấy từ đâu:** Đối soát **Table II** bài báo Deep-SE (2019) và kiểm tra trực tiếp file [`Deep-SE/classification/create_model.py`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py) (dòng 114–118):
  ```python
  # Trích xuất nguyên văn từ Deep-SE create_model.py:
  y_pred_guess = numpy.ones(len(y_true)) + numpy.mean(self.train_label)
  mae_guess = metrics.mean_absolute_error(y_true, y_pred_guess)
  sa = (1 - (auc / mae_guess)) * 100
  ```
* Script tái tính đồng thời: `Real_Med_MAE`, `Real_Mean_MAE`, `Code_Plus1_Guess_MAE` (`1.0 + mean(y_train)`), mức độ thổi phồng baseline (`Med_Inflation`), và $SA$ trung thực so với $SA$ công bố trên cả 16 dự án.

#### 6. `metrics.py`, `hf_utils.py`, `kaggle_runner.ipynb` — Kiểm định & ResearchOps của Nhóm 3
* `metrics.py`: Cài đặt công thức Standardized Accuracy (`compute_sa`), `safe_wilcoxon` (xử lý an toàn khi 2 vector sai số trùng nhau hoàn toàn), Vargha-Delaney $\hat{A}_{12}$ dạng vectorized rank-based (`vargha_delaney_a12`: $>0.5$ nghĩa là mô hình tốt hơn baseline), và hiệu chỉnh đa kiểm định step-down `holm_bonferroni`.
* `hf_utils.py` & `kaggle_runner.ipynb`: Phần hạ tầng tự xây dựng để kết nối GitHub ➔ Kaggle ➔ Hugging Face Hub với Kaggle Secrets (`HF_TOKEN`/`hf_token`), auto-resume từng dự án, upload cuốn chiếu, và ghi vết phiên bản (`git_branch`, `git_commit`, phần cứng, phiên bản thư viện) vào `run_metadata.json` mà không bao giờ ghi lộ secret/token.

---

### 3.3. Tóm tắt đối chiếu: Giữ nguyên từ tác giả vs. Điều chỉnh của Nhóm 3

| Thành phần | Giữ nguyên 100% từ tác giả gốc | Điều chỉnh kỹ thuật / Mở rộng của Nhóm 3 |
| :--- | :--- | :--- |
| **Dataset & Split** | 16 CSV `marked_data` (`train`/`val`/`test`), `_3sets.txt` của Deep-SE | Thêm chế độ `planning_clean` tái dựng tại `SP_Estimation_Date` chống Temporal Leakage |
| **Kiến trúc GPT2SP** | `GPT2Model` + `dense1` (768→3072) + `dense2` (3072→768) + `score` (768→1), no bias, Last Token Pooling | Bọc bằng `nn.Module` thuần PyTorch tránh lỗi `all_tied_weights_keys`/drop head; `safe_torch_load`; dọn cache sau mỗi dự án |
| **Huấn luyện & Input** | `title`-only `max_len=20`, `L1Loss`, `AdamW`, `lr=5e-4`, linear warmup, dynamic batch 30% | Thêm micro-batch + gradient accumulation (tránh OOM T4 15GB) và cờ `--include-description` (`full_128`) |
| **Baseline & Kiểm định** | Đối chiếu kết quả báo cáo Table 4 (GPT2SP) & Table II (Deep-SE) | Bắt buộc tính Baseline chỉ từ `train`, thêm `safe_wilcoxon`, `vargha_delaney_a12`, `holm_bonferroni`, `SA` chuẩn |
| **Vận hành & Lưu trữ** | — | Thin Runner `kaggle_runner.ipynb`, đọc Secrets, auto-resume, push cuốn chiếu lên HF Dataset/Model repo & ghi `run_metadata.json` |

---

## ⚙️ 4. Hướng Dẫn Thiết Lập & Chạy Trên Kaggle

### Bước 1: Tạo token Hugging Face quyền Write & gắn vào Kaggle Secrets
1. Trên Hugging Face: vào **Settings → Access Tokens → New token** với quyền **Write**.
2. Trên Kaggle Notebook: chọn **Add-ons → Secrets → Add a new secret**:
   * **Label:** `hf_token` *(hoặc `HF_TOKEN` — code tự nhận diện cả hai)*.
   * **Value:** dán token vừa tạo và **bật tích xanh** cho notebook sử dụng.
3. Ở cột phải Kaggle:
   * **Accelerator:** `GPU T4 x 2` (cho `gpt2sp_16projects` và `gpt2sp_retrain`) hoặc `CPU` (cho `deepse_audit`).
   * **Internet:** gạt sang **ON**.

### Bước 2: Chỉnh tham số ở Cell 1 của `kaggle_runner.ipynb` và bấm Run All
* `GIT_BRANCH`: tên branch chứa code (ví dụ `"exp/kaggle-hf-pipeline"`).
* `EXPERIMENT`: chọn `"gpt2sp_16projects"`, `"gpt2sp_retrain"`, hoặc `"deepse_audit"`.
* `EXTRA_ARGS` (tùy chọn):
  * Test nhanh 2 dự án: `"--projects springxd,bamboo"`
  * Đánh giá GPT2SP với Full Context: `"--include-description --max-length 128"`
  * Huấn luyện lại trên dữ liệu sạch Planning-Time: `"--project springxd --setting planning_clean --epochs 20 --seeds 42,123"`
  * Huấn luyện Full Context (Title + Description): `"--project springxd --setting full_128 --epochs 20"`

---

## 💻 5. Chạy Thử Cục Bộ (Không Đẩy Lên HF)

```bash
python kaggle/run_gpt2sp_16projects.py --projects springxd --no-hf-push
python kaggle/run_gpt2sp_retrain.py --project springxd --setting planning_clean --epochs 3 --no-hf-push
python kaggle/run_deepse_audit.py --no-hf-push
```
