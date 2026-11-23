# 🚀 Kaggle Modular Runner for GPT2SP (GitHub ➔ Kaggle ➔ Hugging Face Hub)

Thư mục `kaggle_GPT2SP/` được tổ chức theo kiến trúc **Thin Runner + Modular Python Scripts** phục vụ đề tài Nghiên cứu Khoa học:  
**"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"** *(WSESE / ICSE 2026)*.

Tài liệu này vừa hướng dẫn vận hành luồng chạy Kaggle cho **GPT2SP**, vừa **giải trình minh bạch nguồn gốc khoa học và kỹ thuật (Code Provenance & Traceability)** của từng dòng mã nguồn: đoạn nào kế thừa nguyên bản từ bài báo/repository của tác giả gốc, đoạn nào hiệu chỉnh kỹ thuật để tương thích phần cứng/thư viện, và đoạn nào là hạ tầng ResearchOps của Nhóm 3.

> 💡 **Lưu ý điều hướng:** Toàn bộ kịch bản tái lập và kiểm định **Deep-SE (Choetkiertikul et al., IEEE TSE 2019)** được tách riêng sang thư mục [`../kaggle_DeepSE/`](../kaggle_DeepSE/).

---

## 🔄 1. Kiến Trúc Luồng Thực Nghiệm

```text
[Local Code (Branch)] ──git push──► [GitHub Public Repo]
                                           │
                                           ▼ (git clone -b <branch>)
[Kaggle GPU/CPU Runtime] ◄── [kaggle_runner.ipynb] (đọc HF_TOKEN / hf_token từ Secrets)
        │
        ├──► Lưu Results (.csv, .png, metadata.json) ──► [HF Dataset Repo: NCKH3-StoryPoint-Artifact]
        └──► Lưu Model Checkpoints (.bin, config.json) ──► [HF Model Repo: NCKH3-StoryPoint-Checkpoints]
```

---

## 📂 2. Danh Sách File Trong `kaggle_GPT2SP/`

| File | Vai trò |
| :--- | :--- |
| [config.py](config.py) | Cấu hình repo (`NCKH3-StoryPoint-Artifact`), bảng tham chiếu 16 dự án (IEEE TSE 2019 & 2023), helper tải CSV & tách `train`/`val`/`test` |
| [model.py](model.py) | Kiến trúc `GPT2SP(nn.Module)` thuần PyTorch (giữ nguyên MLP Head 2 tầng), `safe_torch_load` & dọn cache HF |
| [metrics.py](metrics.py) | Tính MAE, MdAE, Standardized Accuracy ($SA$), `safe_wilcoxon`, `vargha_delaney_a12`, `holm_bonferroni` |
| [hf_utils.py](hf_utils.py) | Đọc Kaggle Secrets (`HF_TOKEN`/`hf_token`), tự tạo HF repo, `upload_results_batch` (`create_commit`), auto-resume & ghi `metadata.json` |
| [run_gpt2sp_16projects.py](run_gpt2sp_16projects.py) | **Chiến lược 1:** Tái lập suy luận trên 16 dự án từ official HF checkpoints (`MickyMike/0-GPT2SP-*`) |
| [run_gpt2sp_retrain.py](run_gpt2sp_retrain.py) | **Chiến lược 2:** Huấn luyện lại GPT2SP từ đầu (`title_20`, `full_128`, `planning_clean`) & đẩy checkpoint lên HF |
| [kaggle_runner.ipynb](kaggle_runner.ipynb) | Thin Runner Notebook trên Kaggle cho GPT2SP (6 Markdown + 5 Code cells: cấu hình, auth HF Secrets, clone branch, run, xem tóm tắt) |
| [requirements.txt](requirements.txt) | Danh sách thư viện phụ thuộc tối thiểu (`numpy`, `pandas`, `scipy`, `matplotlib`, `torch`, `transformers>=4.36.0`, `huggingface_hub>=0.20.0`, `tqdm`) |
| [README.md](README.md) | Tài liệu vận hành & truy vết nguồn gốc mã nguồn GPT2SP |

> 👉 Kịch bản kiểm định & tái lập Deep-SE nằm tại [`../kaggle_DeepSE/README.md`](../kaggle_DeepSE/README.md).

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

### 3.2. Truy vết chi tiết từng module (`File-by-File & Line-Level Provenance`)

#### 1. `config.py` — Dữ liệu & Số liệu đối chứng 16 dự án ([config.py](config.py))
* **Nguồn dữ liệu CSV:**
  * [`config.py#L10-L12`](config.py#L10-L12) (`GPT2SP_DATA_BASE_URL`) & [`config.py#L227-L250`](config.py#L227-L250) (`load_gpt2sp_splits`): Trỏ tới thư mục [`sp_dataset/marked_data/`](https://github.com/awsm-research/gpt2sp/tree/main/sp_dataset/marked_data) của `awsm-research/gpt2sp` (tương ứng `DATA_PATH = './sp_dataset/marked_data/'` ở **Cell 4 L16** của [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb)), tách `train`/`val`/`test` theo cột `split_mark` (60/20/20).
  * [`config.py#L253-L263`](config.py#L253-L263) (`format_issue_texts`): Điều khiển chọn `title`-only (mặc định theo code gốc) hoặc ghép `title + description` khi bật cờ full context.
* **Bảng tham chiếu `BENCHMARK_PROJECTS` ([`config.py#L20-L181`](config.py#L20-L181)):**
  * `reported_gpt2sp`, `reported_deepse_in_gpt2sp`, `rep_median`, `rep_mean`: Đối soát từ **Table 4** bài báo GPT2SP và file [`data_model_analysis/within_proj_data.csv`](https://github.com/awsm-research/gpt2sp/blob/main/data_model_analysis/within_proj_data.csv).
  * `reported_deepse`, `reported_deepse_sa`: Trích xuất từ **Table II (Trang 8)** bài báo Deep-SE (IEEE TSE 2019).
* **Tiện ích CLI & tải file:** [`resolve_output_dir`](config.py#L184-L194) (`L184-L194`), [`parse_projects_arg`](config.py#L197-L206) (`L197-L206`), [`download_file_with_retry`](config.py#L209-L224) (`L209-L224`), cấu hình HF repos mặc định [`L14-L15`](config.py#L14-L15) (`NCKH3-StoryPoint-Artifact` & `NCKH3-StoryPoint-Checkpoints`).

#### 2. `model.py` — Kiến trúc `GPT2SP` & Nạp Trọng Số Hugging Face ([model.py](model.py))
* **Lấy nguyên bản từ đâu:** File [`GPT2SP.py#L7-L110`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L7-L110) (`class GPT2ForSequenceClassification`) của `awsm-research/gpt2sp`:
  * Backbone [`GPT2SP.py#L13`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L13) (`self.transformer = GPT2Model(config)`) ➔ tái tạo tại [`model.py#L21`](model.py#L21).
  * **MLP Head 2 tầng không bias** ([`GPT2SP.py#L14-L16`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L14-L16) & [`GPT2SP.py#L61-L67`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L61-L67)) ➔ tái tạo tại [`model.py#L22-L24`](model.py#L22-L24) & [`model.py#L35-L38`](model.py#L35-L38):
    * `self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)` ($768 \rightarrow 3072$)
    * `self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)` ($3072 \rightarrow 768$)
    * `self.score = nn.Linear(config.n_embd, 1, bias=False)` ($768 \rightarrow 1$)
  * Cơ chế **Last Token Pooling** lấy logit tại token thực cuối cùng trước padding (`pad_token_id = eos_token_id`, [`GPT2SP.py#L77-L89`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L77-L89)) ➔ tái tạo tại [`model.py#L40-L53`](model.py#L40-L53).
* **Vì sao viết lại bằng `torch.nn.Module` thuần túy thay vì kế thừa `GPT2PreTrainedModel`:**
  1. Trên `transformers >= 4.40`, kế thừa `GPT2PreTrainedModel` dễ phát sinh `AttributeError: 'GPT2SP' object has no attribute 'all_tied_weights_keys'` trong `_finalize_model_loading`.
  2. Nếu dùng `GPT2ForSequenceClassification` mặc định của Hugging Face, hai tầng `dense1.weight` và `dense2.weight` trong checkpoint của tác giả sẽ bị bỏ qua (`UNEXPECTED`).
  3. Lớp [`GPT2SP(nn.Module)`](model.py#L11-L53) kèm: [`build_tokenizer_and_config`](model.py#L56-L65), [`safe_torch_load`](model.py#L68-L73), kiểm tra bắt buộc `required_head_keys = ("dense1.weight", "dense2.weight", "score.weight")` trong [`load_official_gpt2sp_checkpoint`](model.py#L76-L105) (`L90-L101`), [`torch.clamp(..., min=0)`](model.py#L43) cho chuỗi toàn padding, [`init_gpt2sp_for_training`](model.py#L108-L117), và [`cleanup_downloaded_file`](model.py#L120-L133) xóa cache nặng sau mỗi dự án để tránh tràn ổ đĩa 20GB của Kaggle.

#### 3. `run_gpt2sp_16projects.py` — Chiến lược 1: Kiểm chứng 16 Official Checkpoints ([run_gpt2sp_16projects.py](run_gpt2sp_16projects.py))
* **Tiền xử lý & nguồn gốc sai lệch Table 4 (`~1.80x` MAE bug — PR #2):**
  * Trong [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb), **Cell 4 (`L5`)** đặt `SEQUENCE_LEN = 20` và **Cell 6 (`L111-L116`)** `prepare_dataframe()` chỉ lấy `data['title']` (bỏ qua cột `description`). Do đó mặc định [`parse_args`](run_gpt2sp_16projects.py#L40-L85) & [`infer_texts`](run_gpt2sp_16projects.py#L88-L112) chạy `Title-only, max_length=20` trên các official weights [`MickyMike/{seed}-GPT2SP-{p}`](run_gpt2sp_16projects.py#L153-L160) để tái lập công bằng.
  * Cờ `--include-description --max-length 128` bổ sung thiết lập Full Context (Title + Description) như bài báo tuyên bố.
  * **Truy vết PR #2 ([`awsm-research/gpt2sp#2`](https://github.com/awsm-research/gpt2sp/pull/2), commit [`1117294`](https://github.com/awsm-research/gpt2sp/commit/1117294), merge ngày 21/08/2022 bởi Michael Fu từ Vali Tawosi):** Trong **Cell 6 (`L248-L257`)** của `model_training_notebook.ipynb`, code gốc khi in bài báo tính `MAE = total_distance / total_data_point` với `total_data_point = len(predictions) * len(predictions[0])`. Với `BATCH_SIZE_RATIO = 0.3` (`Cell 4 L4`) và chia 60/20/20 (`Cell 6 L130-L135`), tập test $0.20N$ bị chia làm 2 batch có kích thước đầu $0.18N$, làm `total_data_point = 0.36N` (gấp $1.80\times$ tập test thật!), đẩy `MAE` Table 4 giảm nhân tạo ~`1.80x`. PR #2 sửa bằng `MAE = np.mean(np.array(distance_records))`. Nhóm tính `compute_mae_mdae` trung thực tại [`run_single_project`](run_gpt2sp_16projects.py#L115-L237).
* **Đánh giá & kiểm định thống kê trung thực:** Tính `Real_Median_MAE` và `Real_Mean_MAE` **chỉ từ tập `train`** ([`L150-L151`](run_gpt2sp_16projects.py#L150-L151)), tính $SA$, Wilcoxon, $\hat{A}_{12}$ từng dự án ([`L206-L208`](run_gpt2sp_16projects.py#L206-L208)), điều chỉnh [`holm_bonferroni`](run_gpt2sp_16projects.py#L365) (`main` [`L313-L448`](run_gpt2sp_16projects.py#L313-L448)), kiểm định toàn cục 16 dự án ([`L373-L407`](run_gpt2sp_16projects.py#L373-L407)), vẽ biểu đồ 300 DPI ([`save_audit_plot`](run_gpt2sp_16projects.py#L240-L310)), và gom toàn bộ file kết thúc vào 1 commit via [`upload_results_batch`](run_gpt2sp_16projects.py#L428).

#### 4. `run_gpt2sp_retrain.py` — Chiến lược 2: Huấn luyện lại từ `gpt2` gốc ([run_gpt2sp_retrain.py](run_gpt2sp_retrain.py))
* **Siêu tham số gốc từ [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb):**
  * `EPOCHS = 20` (**Cell 4 L3**), `BATCH_SIZE_RATIO = 0.3` (**Cell 4 L4**), `SEQUENCE_LEN = 20` (**Cell 4 L5**), `LEARNING_RATE = 5e-4` (**Cell 4 L6**); `DYNAMIC_BATCH = True` / `int(len(train_text) * 0.3)` (**Cell 6 L3, L24-L25**); `AdamW` & `get_linear_schedule_with_warmup` (**Cell 6 L145-L149**); `nn.L1Loss()` (**Cell 6 L164**); `clip_grad_norm_(..., 1.0)` (**Cell 6 L184**).
  * Đối ứng tại [`parse_args`](run_gpt2sp_retrain.py#L33-L67), [`set_seed`](run_gpt2sp_retrain.py#L70-L75), [`make_loader`](run_gpt2sp_retrain.py#L146-L157), [`evaluate_loader`](run_gpt2sp_retrain.py#L160-L171), [`train_one_seed`](run_gpt2sp_retrain.py#L188-L339) (`L215` `nn.L1Loss()`, `L216` `AdamW`, `L246` `clip_grad_norm_`, `L308` batch upload), [`save_loss_curve`](run_gpt2sp_retrain.py#L174-L185), và [`main`](run_gpt2sp_retrain.py#L342-L395) (`L389`).
* **Cải tiến kỹ thuật & Kiểm soát Leakage của Nhóm 3:**
  * **Micro-batching + Gradient Accumulation ([`L202-L205`](run_gpt2sp_retrain.py#L202-L205)):** Giữ nguyên effective batch size 30% tập train nhưng chia micro-batch vật lý (32 hoặc 64) và cộng dồn gradient (`loss / accum_steps`) để tránh OOM trên Kaggle T4 (15GB) khi chạy `seq_len=128`.
  * **3 nhánh thực nghiệm ([`prepare_setting_data`](run_gpt2sp_retrain.py#L93-L143)):** `title_20` & `full_128` ([`L129-L143`](run_gpt2sp_retrain.py#L129-L143)), và `planning_clean` ([`L98-L127`](run_gpt2sp_retrain.py#L98-L127)) tự động định vị bộ dữ liệu sạch tại `SP_Estimation_Date` qua [`resolve_clean_csv`](run_gpt2sp_retrain.py#L78-L90) từ [../docs/draft/springxd_cleaned_dataset.csv](../docs/draft/springxd_cleaned_dataset.csv) hoặc `data/clean/springxd_cleaned_dataset.csv`.

#### 5. `metrics.py`, `hf_utils.py`, `kaggle_runner.ipynb` — Kiểm định & ResearchOps của Nhóm 3
* [`metrics.py`](metrics.py): [`compute_mae_mdae`](metrics.py#L8-L13), [`compute_sa`](metrics.py#L16-L20), [`safe_wilcoxon`](metrics.py#L23-L33), [`vargha_delaney_a12`](metrics.py#L36-L57) ($>0.5$ nghĩa là mô hình vượt baseline), và [`holm_bonferroni`](metrics.py#L60-L73).
* [`hf_utils.py`](hf_utils.py): [`resolve_hf_token`](hf_utils.py#L12-L38), [`get_git_info`](hf_utils.py#L41-L55), và [`HFExperimentLogger`](hf_utils.py#L58-L306) ([`remote_file_exists`](hf_utils.py#L143-L164), [`download_result_if_exists`](hf_utils.py#L166-L182), [`upload_result`](hf_utils.py#L196-L211), [`upload_results_batch`](hf_utils.py#L213-L237), [`upload_checkpoint_dir`](hf_utils.py#L239-L256), [`write_and_upload_metadata`](hf_utils.py#L258-L306)).
* [`kaggle_runner.ipynb`](kaggle_runner.ipynb): 5 Code cells (`L23-L48` Config, `L58-L95` HF Secrets Auth, `L105-L129` Git Clone/Pull, `L139-L183` Run Script stream log realtime — gồm `"migrate_hf_artifact"`, `L193-L219` Summary & HF Link).

---

### 3.3. Bảng Ánh Xạ Từng Dòng Mã Nguồn (`Line-by-Line Traceability Matrix`)

| Thành phần | Nguồn gốc tác giả (File & Dòng) | Mã nguồn Nhóm 3 (File & Dòng) | Ghi chú đối soát |
| :--- | :--- | :--- | :--- |
| **Data URL & 60/20/20 split** | [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) (Cell 4 `L16`; Cell 6 `L130-L135`) & [`within_proj_data.csv`](https://github.com/awsm-research/gpt2sp/blob/main/data_model_analysis/within_proj_data.csv) | [`config.py#L10-L12`](config.py#L10-L12), [`config.py#L20-L181`](config.py#L20-L181), [`config.py#L227-L250`](config.py#L227-L250) | Giữ nguyên CSV `marked_data`, bổ sung đối chứng Table II Deep-SE |
| **Kiến trúc `GPT2SP` + MLP Head** | [`GPT2SP.py#L7-L110`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L7-L110) (`L13`, `L14-L16`, `L61-L67`) | [`model.py#L11-L53`](model.py#L11-L53) (`L21`, `L22-L24`, `L35-L38`) | Bọc `nn.Module` thuần tránh lỗi `all_tied_weights_keys` / drop `dense1,dense2` |
| **Last Token Pooling** | [`GPT2SP.py#L77-L89`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py#L77-L89) | [`model.py#L40-L53`](model.py#L40-L53) (`torch.clamp` `L43`) | Bảo vệ khỏi chỉ số `-1` khi chuỗi toàn token padding |
| **Xác thực Checkpoint HF** | HF Repo [`MickyMike/0-GPT2SP-*`](https://huggingface.co/MickyMike) | [`model.py#L76-L105`](model.py#L76-L105) (`L90-L101`), [`run_gpt2sp_16projects.py#L153-L160`](run_gpt2sp_16projects.py#L153-L160) | Bắt buộc khớp đủ 3 key head (`dense1`, `dense2`, `score`) & dọn cache [`L120-L133`](model.py#L120-L133) |
| **Tiền xử lý Title-only (`len=20`)** | [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) (Cell 4 `L5`; Cell 6 `L111-L116`) | [`config.py#L253-L263`](config.py#L253-L263), [`run_gpt2sp_16projects.py#L88-L112`](run_gpt2sp_16projects.py#L88-L112) | Thêm `--include-description --max-length 128` để test thiết lập Full Context |
| **Công thức tính MAE (PR #2)** | [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) (Cell 6 `L248-L257`) & [PR #2 (`1117294`)](https://github.com/awsm-research/gpt2sp/commit/1117294) | [`metrics.py#L8-L13`](metrics.py#L8-L13), [`run_gpt2sp_16projects.py#L202-L212`](run_gpt2sp_16projects.py#L202-L212) | Giải thích sai số `1.80x` giữa Table 4 bài báo và official checkpoints |
| **Vòng lặp Huấn luyện & Siêu tham số** | [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) (Cell 4 `L3-L6`; Cell 6 `L3,L24-L25,L145-L184`) | [`run_gpt2sp_retrain.py#L188-L339`](run_gpt2sp_retrain.py#L188-L339) (`L202-L216`, `L246`) | Thêm micro-batch + gradient accumulation tránh OOM trên T4 |
| **Chống Temporal Leakage** | — *(bài báo dùng Final Snapshot)* | [`run_gpt2sp_retrain.py#L78-L127`](run_gpt2sp_retrain.py#L78-L127) | Dữ liệu `planning_clean` tại `SP_Estimation_Date` |
| **Kiểm định Thống kê & HF Ops** | — *(bài báo không tính $SA$ / Holm / $\hat{A}_{12}$)* | [`metrics.py#L16-L73`](metrics.py#L16-L73), [`hf_utils.py#L12-L306`](hf_utils.py#L12-L306), [`kaggle_runner.ipynb`](kaggle_runner.ipynb) | Train-only Median, Wilcoxon, $\hat{A}_{12}$, Holm-Bonferroni, `upload_results_batch` |

---

### 3.4. Tóm tắt đối chiếu: Giữ nguyên từ tác giả vs. Điều chỉnh của Nhóm 3

| Thành phần | Giữ nguyên 100% từ tác giả gốc | Điều chỉnh kỹ thuật / Mở rộng của Nhóm 3 |
| :--- | :--- | :--- |
| **Dataset & Split** | 16 CSV `marked_data` (`train`/`val`/`test`) từ [`config.py#L227-L250`](config.py#L227-L250) | Thêm chế độ `planning_clean` tái dựng tại `SP_Estimation_Date` chống Temporal Leakage |
| **Kiến trúc GPT2SP** | `GPT2Model` + `dense1` (768→3072) + `dense2` (3072→768) + `score` (768→1), no bias, Last Token Pooling | Bọc bằng `nn.Module` thuần PyTorch tránh lỗi `all_tied_weights_keys`/drop head; `safe_torch_load`; dọn cache sau mỗi dự án |
| **Huấn luyện & Input** | `title`-only `max_len=20`, `L1Loss`, `AdamW`, `lr=5e-4`, linear warmup, dynamic batch 30% | Thêm micro-batch + gradient accumulation (tránh OOM T4 15GB) và cờ `--include-description` (`full_128`) |
| **Baseline & Kiểm định** | Đối chiếu kết quả báo cáo Table 4 (GPT2SP) & Table II (Deep-SE) | Bắt buộc tính Baseline chỉ từ `train`, truy vết lỗi MAE `1.80x` ([PR #2](https://github.com/awsm-research/gpt2sp/pull/2)), thêm `safe_wilcoxon`, `vargha_delaney_a12`, `holm_bonferroni`, `SA` chuẩn |
| **Vận hành & Lưu trữ** | — | Thin Runner `kaggle_runner.ipynb`, chuẩn Phương án A (`NCKH3-StoryPoint-Artifact` / `NCKH3-StoryPoint-Checkpoints`), gom commit qua `create_commit` |

---

## ⚙️ 4. Hướng Dẫn Thiết Lập & Chạy Trên Kaggle

### Bước 1: Tạo token Hugging Face quyền Write & gắn vào Kaggle Secrets
1. Trên Hugging Face: vào **Settings → Access Tokens → New token** với quyền **Write**.
2. Trên Kaggle Notebook: chọn **Add-ons → Secrets → Add a new secret**:
   * **Label:** `hf_token` *(hoặc `HF_TOKEN` — code tự nhận diện cả hai)*.
   * **Value:** dán token vừa tạo và **bật tích xanh** cho notebook sử dụng.
3. Ở cột phải Kaggle:
   * **Accelerator:** `GPU T4 x 2` (cho `gpt2sp_16projects` và `gpt2sp_retrain`) hoặc `CPU` (cho `migrate_hf_artifact`).
   * **Internet:** gạt sang **ON**.

### Bước 2: Chỉnh tham số ở Cell 1 của `kaggle_runner.ipynb` và bấm Run All
* `GIT_BRANCH`: tên branch chứa code (mặc định `"main"`).
* `EXPERIMENT`: chọn `"gpt2sp_16projects"`, `"gpt2sp_retrain"`, hoặc `"migrate_hf_artifact"`.
* `HF_RESULTS_REPO`: `"NCKH3-StoryPoint-Artifact"` *(HF Dataset Repo trung tâm theo Phương án A)*.
* `HF_CHECKPOINTS_REPO`: `"NCKH3-StoryPoint-Checkpoints"` *(HF Model Repo trung tâm lưu model weights khi chạy `gpt2sp_retrain`)*.
* `EXTRA_ARGS` (tùy chọn):
  * Gom kết quả đã chạy từ `NCKH_GPT2SP` + `NCKH_DeepSE` sang `NCKH3-StoryPoint-Artifact` (~15s CPU): đặt `EXPERIMENT = "migrate_hf_artifact"`, `EXTRA_ARGS = ""`
  * Test nhanh 2 dự án: `"--projects springxd,bamboo"`
  * Đánh giá GPT2SP với Full Context: `"--include-description --max-length 128"`
  * Huấn luyện lại trên dữ liệu sạch Planning-Time: `"--project springxd --setting planning_clean --epochs 20 --seeds 42,123"`
  * Huấn luyện Full Context (Title + Description): `"--project springxd --setting full_128 --epochs 20"`

---

## 💻 5. Chạy Thử Cục Bộ (Không Đẩy Lên HF)

```bash
python scripts/migrate_hf_artifact.py --no-hf-push
python kaggle_GPT2SP/run_gpt2sp_16projects.py --projects springxd --no-hf-push
python kaggle_GPT2SP/run_gpt2sp_retrain.py --project springxd --setting planning_clean --epochs 3 --no-hf-push
```

---

## 📦 6. Giải Thích Các File Output Theo Phương Án A (`Snowflake06/NCKH3-StoryPoint-Artifact`)

Toàn bộ artifact chuẩn hóa của đề tài được quy về **1 HF Dataset Repo duy nhất** (kèm Model Repo `Snowflake06/NCKH3-StoryPoint-Checkpoints` cho trọng số `.bin`):  
🔗 **Unified HF Artifact:** [`https://huggingface.co/datasets/Snowflake06/NCKH3-StoryPoint-Artifact`](https://huggingface.co/datasets/Snowflake06/NCKH3-StoryPoint-Artifact)  
*(Dữ liệu gốc từ lần chạy trước hiện vẫn được bảo toàn nguyên vẹn tại [`Snowflake06/NCKH_GPT2SP`](https://huggingface.co/datasets/Snowflake06/NCKH_GPT2SP) và có thể đồng bộ 1-click qua `EXPERIMENT = "migrate_hf_artifact"` mà không cần train/suy luận lại 16 dự án).*

### 6.1. Cấu trúc chuẩn hóa cho Chiến lược 1 (`experiments/gpt2sp/replication/<run>/`)

```text
Snowflake06/NCKH3-StoryPoint-Artifact/
├── README.md                                  # Dataset Card + YAML configs (bật HF Dataset Viewer)
├── datasets/
│   └── springxd_planning_clean.csv            # Bộ dữ liệu sạch không rò rỉ tại SP_Estimation_Date
├── comparisons/
│   ├── cross_model_16proj.csv                 # Bảng đối chiếu 16 dự án: Median vs Deep-SE vs GPT2SP
│   └── figures/
│       └── cross_model_benchmark.png          # Biểu đồ 300 DPI so sánh MAE & SA chéo mô hình
└── experiments/gpt2sp/replication/seed0_title_len20/
    ├── summary.csv                            # Bảng tổng hợp 16 dự án (16 dòng x 18 cột)
    ├── stat_tests.csv                         # Kiểm định Wilcoxon & A12 toàn cục (2 dòng x 6 cột)
    ├── metadata.json                          # Nhật ký tái lập phiên bản, phần cứng & tham số CLI
    ├── figures/
    │   └── benchmark_audit.png                # Biểu đồ 2 panel 300 DPI đối chiếu MAE & SA
    └── predictions/                           # Dự báo chi tiết từng Jira issue của 16 dự án
        ├── appceleratorstudio.csv
        ├── ... (tổng 16 file <project>.csv)
        └── usergrid.csv
```

### 6.2. Ý nghĩa từng file & kết quả đối chiếu đã kiểm chứng (`seed0_title_len20`)

#### 1. `summary.csv` (16 dòng $\times$ 18 cột)
| Nhóm cột | Tên cột | Ý nghĩa chi tiết |
| :--- | :--- | :--- |
| **Định danh & Quy mô** | `Project`, `Abbr`, `Name`, `N_Test` | Khóa dự án, mã viết tắt (`AS`, `XD`...), tên đầy đủ và số Jira issue tập `test` |
| **Kết quả GPT2SP** | `GPT2SP_Reported_MAE`, `GPT2SP_Actual_MAE`, `GPT2SP_Actual_MdAE`, `Reproduction_Gap` | MAE công bố ở Table 4, MAE/MdAE chạy thật từ official HF checkpoint, và độ lệch `Actual - Reported` |
| **Baselines thật (`train`)** | `Real_Median_MAE`, `Real_Median_MdAE`, `Real_Mean_MAE` | Baseline chuẩn hóa tính thuần từ `train` (`median(y_train)`, `mean(y_train)`) |
| **So sánh & Đối chứng** | `SA_vs_Median (%)`, `DeepSE_Reported_MAE` | Standardized Accuracy so với `Real_Median_MAE` (`> 0%` thắng Median) và MAE Deep-SE từ `within_proj_data.csv` |
| **Kiểm định thống kê** | `Wilcoxon_W_vs_Med`, `Wilcoxon_p_vs_Med`, `Wilcoxon_p_Holm`, `A12_vs_Med`, `Verdict` | Wilcoxon ghép cặp theo issue, $p$-value sau hiệu chỉnh **Holm-Bonferroni**, $\hat{A}_{12}$ và nhãn `BEATS_MEDIAN` / `LOSES_TO_MEDIAN` |

> **Kết quả thực nghiệm đã xác nhận (`Tesla T4`, `PyTorch 2.11.0+cu130`, `Transformers 5.20.2`):** **9/16 dự án** gắn nhãn `LOSES_TO_MEDIAN`, `Mean Reproduction_Gap = +1.1335 SP`, và `Mean SA vs Median = +0.07%`.

#### 2. `stat_tests.csv` (2 dòng $\times$ 6 cột)
* **`Actual_Checkpoint_MAE vs Paper_Reported_MAE`** (`N_Projects=16`, `Mean_Diff=+1.1335`, `W=0.0`, `p=0.000031`, `A12=NaN`): Xác nhận sai lệch `~1.80x` do lỗi chia mẫu số `total_data_point` ([PR #2](https://github.com/awsm-research/gpt2sp/pull/2)).
* **`Actual_Checkpoint_MAE vs Real_Median_MAE`** (`N_Projects=16`, `Mean_Diff=-0.0277`, `W=67.0`, `p=0.979950`, `A12=0.5078`): Khẳng định trên toàn cục 16 dự án, official checkpoints tương đương thống kê với Median tập train ($p = 0.98$, $\hat{A}_{12} \approx 0.50$).

#### 3. `predictions/<project>.csv` (16 file $\times$ 8 cột)
Gồm `issuekey`, `Ground_Truth_SP`, `Pred_GPT2SP`, `Pred_Median_Baseline`, `Pred_Mean_Baseline`, `Error_GPT2SP`, `Error_Median`, `Error_Mean` (vd `springxd.csv` có 706 dòng).

#### 4. `figures/benchmark_audit.png` & `metadata.json`
* `benchmark_audit.png`: Biểu đồ 2 panel 300 DPI sinh bởi [`save_audit_plot`](run_gpt2sp_16projects.py#L240-L310).
* `metadata.json`: Lưu `timestamp_utc`, `git_branch`, `git_commit`, `device`/`gpu_name`, phiên bản thư viện, CLI `args` (đã lọc bỏ secret) và `extra_info`.

---

### 6.3. Cấu trúc output khi chạy Chiến lược 2 (`run_gpt2sp_retrain.py`)

* **Dataset Repo (`experiments/gpt2sp/retrain/<project>_<setting>/`):**
  * `summary.csv` & `metadata.json` (upload gộp cuối chạy)
  * `seed_<seed>/history.csv`, `seed_<seed>/predictions.csv` & `figures/loss_curve_seed_<seed>.png` (upload gộp theo từng seed)
* **Model Repo (`Snowflake06/NCKH3-StoryPoint-Checkpoints/experiments/gpt2sp/retrain/<project>_<setting>/seed_<seed>/`):**
  * `pytorch_model.bin` & `config.json` (checkpoint có `val_mae` tốt nhất).
