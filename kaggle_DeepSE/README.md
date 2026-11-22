# 🚀 Kaggle Modular Runner for Deep-SE (GitHub ➔ Kaggle ➔ Hugging Face Hub)

Thư mục `kaggle_DeepSE/` được thiết kế song song với [`../kaggle_GPT2SP/`](../kaggle_GPT2SP/) theo kiến trúc **Thin Runner + Modular Python Scripts** phục vụ đề tài Nghiên cứu Khoa học:  
**"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"** *(WSESE / ICSE 2026)*.

Tài liệu này vừa hướng dẫn vận hành luồng chạy Kaggle cho **Deep-SE**, vừa **giải trình minh bạch nguồn gốc khoa học và kỹ thuật (Code Provenance & Traceability)** của từng file mã nguồn: phần nào kế thừa trung thành từ kiến trúc gốc Keras/Theano của tác giả bài báo, phần nào được chuyển dịch sang PyTorch hiện đại để chạy ổn định trên Kaggle GPU/CPU, và phần nào là kiểm định rò rỉ dữ liệu & thống kê của Nhóm 3.

---

## 🔄 1. Kiến Trúc Luồng Thực Nghiệm

```text
[Local Code (Branch)] ──git push──► [GitHub Public Repo]
                                           │
                                           ▼ (git clone -b <branch>)
[Kaggle GPU/CPU Runtime] ◄── [kaggle_runner.ipynb] (đọc HF_TOKEN / hf_token từ Secrets)
        │
        ├──► Lưu Results (.csv, .png, run_metadata.json) ──► [HF Dataset Repo]
        └──► Lưu Model Checkpoints (.bin, .json)          ──► [HF Model Repo]
```

---

## 📂 2. Danh Sách File Trong `kaggle_DeepSE/`

| File | Vai trò |
| :--- | :--- |
| [config.py](config.py) | Cấu hình repo, bảng tham chiếu Table II (IEEE TSE 2019), helper tải `.csv`/`_3sets.txt`/`.pkl.gz`/`.dict.pkl.gz` & `prepare_sequence_tensors` |
| [model.py](model.py) | Kiến trúc `DeepSEModel(nn.Module)` thuần PyTorch (`Embedding` + Shared `LSTM` + `PoolingSeq` + Weight-tied `HighwayLayer`), nạp HDF5 NCE `lstm2v` & vòng lặp `train_deepse_session` |
| [metrics.py](metrics.py) | Tính MAE, MdAE, Standardized Accuracy ($SA$), `safe_wilcoxon`, `vargha_delaney_a12`, `holm_bonferroni` |
| [hf_utils.py](hf_utils.py) | Đọc Kaggle Secrets (`HF_TOKEN`/`hf_token`), tự tạo HF repo, upload cuốn chiếu, auto-resume & ghi `run_metadata.json` |
| [run_deepse_audit.py](run_deepse_audit.py) | Kiểm định Baseline Inflation (Table II) và lỗi `+1.0` trong `create_model.py` trên cả 16 dự án |
| [run_deepse_16projects.py](run_deepse_16projects.py) | **Chiến lược 1:** Tái lập mô hình LD-RNN Deep-SE trên 16 dự án từ `<project>.pkl.gz` & NCE `lstm2v` embeddings |
| [run_deepse_retrain.py](run_deepse_retrain.py) | **Chiến lược 2:** Huấn luyện có kiểm soát qua 3 setting (`official_pkl`, `final_raw`, `planning_clean`) & đẩy checkpoint lên HF |
| [kaggle_runner.ipynb](kaggle_runner.ipynb) | Thin Runner Notebook trên Kaggle cho Deep-SE (6 Markdown + 5 Code cells) |
| [requirements.txt](requirements.txt) | Thư viện phụ thuộc (`numpy`, `pandas`, `scipy`, `matplotlib`, `torch`, `h5py`, `huggingface_hub>=0.20.0`, `tqdm`) |
| [README.md](README.md) | Tài liệu vận hành & truy vết nguồn gốc mã nguồn Deep-SE |

> 👉 Kịch bản tái lập và huấn luyện lại **GPT2SP** nằm tại [`../kaggle_GPT2SP/README.md`](../kaggle_GPT2SP/README.md).

---

## 📚 3. Cơ Sở Khoa Học & Nguồn Gốc Mã Nguồn (Code Provenance & Traceability)

### 3.1. Nguồn gốc bài báo & kho lưu trữ chính thức
1. **Deep-SE (Choetkiertikul et al., IEEE TSE 2019):**
   * **Bài báo:** *A Deep Learning Model for Estimating Story Points*, IEEE Transactions on Software Engineering, Vol. 45, No. 7, DOI: [`10.1109/TSE.2017.2787834`](https://doi.org/10.1109/TSE.2017.2787834).
   * **Kho lưu trữ gốc:** [`morakotch/datasets/storypoint/IEEE TSE2018/Deep-SE`](https://github.com/morakotch/datasets/tree/master/storypoint/IEEE%20TSE2018/Deep-SE) (SEA@UOW), chứa:
     * `data/`: 16 tập `.csv`, ma trận chia thời gian `_3sets.txt`, dữ liệu đã số hóa `.pkl.gz` và từ điển 9 kho Jira `.dict.pkl.gz`.
     * `NCE/bestModels/`: 36 file trọng số language model LSTM tiền huấn luyện `lstm2v_<repo>_dim{10,50,100,200}.hdf5`.
     * `classification/`: mã nguồn Keras 1.0.6 / Theano gồm `exp_script.py`, `prepare_data.py`, `create_model.py` và `training.py`.
2. **Chuẩn mực Phương pháp luận & Kiểm định Thống kê:**
   * **Shepperd & MacDonell (IEEE TSE 2012):** Standardized Accuracy ($SA$) và Median/Mean Effort Baselines.
   * **Kitchenham et al. (IEEE TSE 2017):** Kiểm định phi tham số Wilcoxon Signed-Rank Test, Vargha-Delaney $\hat{A}_{12}$ và hiệu chỉnh đa kiểm định Holm-Bonferroni.

---

### 3.2. Truy vết chi tiết từng module (`File-by-File & Line-Level Provenance`)

#### 1. `config.py` — Dữ liệu, Từ điển & Tiền xử lý chuỗi ([config.py](config.py))
* **Nguồn URL & HF Repos mặc định:** [`config.py#L15-L23`](config.py#L15-L23) trỏ tới `morakotch/datasets/storypoint/IEEE TSE2018/Deep-SE/` (`data/` và `NCE/bestModels/`).
* **Bảng tham chiếu `BENCHMARK_PROJECTS` ([`config.py#L28-L173`](config.py#L28-L173)):** Số liệu `reported_deepse`, `reported_deepse_sa`, `rep_median`, `rep_mean` và ánh xạ 16 dự án ➔ 9 repo Jira trích xuất từ **Table II (Trang 8)** bài báo Deep-SE và `datasetDict` trong [`exp_script.py#L15-L33`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/exp_script.py#L15-L33).
* **Nạp dữ liệu nhị phân & từ điển gốc:**
  * [`load_deepse_splits`](config.py#L218-L232): Tải `<project>.csv` + `<project>_3sets.txt` để giữ đúng chia cắt thời gian 60/20/20 gốc.
  * [`load_deepse_pkl_splits`](config.py#L235-L259) & [`load_deepse_dict`](config.py#L262-L272): Giải nén `.pkl.gz` / `.dict.pkl.gz` với `encoding="latin1"`, kế thừa hàm `load()` tại [`prepare_data.py#L41-L48`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L41-L48).
  * [`build_vocab_from_texts`](config.py#L275-L285) & [`texts_to_word_ids`](config.py#L288-L294): Chuyển dịch trực tiếp `build_dict()` ([`NCE/preprocess.py#L12-L38`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/NCE/preprocess.py#L12-L38)) và `grab_data()` ([`NCE/preprocess.py#L40-L46`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/NCE/preprocess.py#L40-L46)).
  * [`prepare_sequence_tensors`](config.py#L297-L326): Chuyển dịch trực tiếp `prepare_data()` / `create_mask()` tại [`prepare_data.py#L50-L78`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L50-L78) (lọc token ID $< \text{vocab\_size}=500$, cộng `+1` để dành index `0` làm PAD, cắt/đệm tới `max_len=100`).
* **Tiện ích CLI & tải file:** [`resolve_output_dir`](config.py#L176-L185), [`parse_projects_arg`](config.py#L188-L197), [`download_file_with_retry`](config.py#L200-L215).

#### 2. `model.py` — Chuyển dịch Keras 1.0.6 / Theano ➔ PyTorch 2.x Thuần Túy ([model.py](model.py))
Mã nguồn gốc của tác giả viết bằng **Python 2 + Keras 1.0.6 + Theano (2016)** vốn không còn cài đặt được trên Kaggle hiện đại (CUDA 12/13, PyTorch 2.x, Python 3.13). Nhóm 3 chuyển dịch trung thành 100% toán học kiến trúc từ [`classification/create_model.py`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py):
* **Shared LSTM Backbone ([`create_model.py#L259-L354`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L259-L354)):** Định nghĩa trong [`DeepSEModel`](model.py#L58-L143) với embedding tại [`L83-L100`](model.py#L83-L100), một tầng [`self.lstm`](model.py#L104) dùng chung cho cả nhánh `Title` và `Description`, và hàm khởi tạo [`_init_lstm_keras_style`](model.py#L114-L120) (`xavier_uniform_` input, `orthogonal_` recurrent, `forget_bias = 1.0`), kèm `Dropout(0.2)`.
* **`PoolingSeq` & Average Merge:** Class [`PoolingSeq`](model.py#L36-L55) tái lập từ [`create_model.py#L190-L217`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L190-L217) (`mean`, masked `max`, `last`), sau đó trung bình cộng hai nhánh `0.5 * (pooled_title + pooled_descr)` tại [`model.py#L138`](model.py#L138) (tương ứng `merge(..., mode='ave')` ở [`create_model.py#L299`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L299) & [`L344`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L344)).
* **Weight-tied Highway Network:** Trong [`create_model.py#L220-L228`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L220-L228) (`create_highway`), tác giả **khởi tạo 1 đối tượng `Highway` duy nhất rồi lặp qua `hdl=10` lần** với `activation='relu'`, `init='glorot_normal'` và `transform_bias=-1`. Class [`HighwayLayer`](model.py#L18-L33) (`transform_bias=-1.0` tại `L21`, `L28`) + instance dùng chung [`self.highway`](model.py#L110) lặp `for _ in range(self.hidden_layers)` tại [`model.py#L140-L141`](model.py#L140-L141) tái hiện nguyên vẹn cơ chế chia sẻ trọng số này.
* **Nạp trọng số tiền huấn luyện NCE:** [`load_pretrained_lm_embedding`](model.py#L146-L179) đọc trực tiếp `NCE/bestModels/lstm2v_<repo>_dim<dim>.hdf5` bằng `h5py` và nạp vào `nn.Embedding` với hàng `0` là vector không cho PAD (thay cho [`prepare_data.py#L80-L107`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L80-L107) `load_weight()` & `to_features()`).
* **Chiến lược tối ưu & Early Stopping:** [`train_deepse_session`](model.py#L249-L401) áp dụng hàm mất mát `MSE` ([`training.py#L49`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/training.py#L49)), tối ưu `RMSprop(lr=0.01)` ([`training.py#L84`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/training.py#L84); [`model.py#L295`](model.py#L295)), và cơ chế giảm nửa LR / dừng sớm từ `SaveResult` ([`create_model.py#L53,L170-L177`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L170-L177); [`model.py#L354-L385`](model.py#L354-L385)) cùng `NanStopping` ([`create_model.py#L180-L187`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L180-L187)). Ngoài ra có [`set_seed`](model.py#L182-L188), [`safe_torch_load`](model.py#L191-L196), [`cleanup_downloaded_file`](model.py#L199-L207), [`make_deepse_loader`](model.py#L210-L225), và [`evaluate_deepse_loader`](model.py#L228-L246).

#### 3. `run_deepse_audit.py` — Kiểm định Baseline Inflation & Phép cộng `+1.0` ([run_deepse_audit.py](run_deepse_audit.py))
Đối soát trực tiếp **Table II** của bài báo Deep-SE với dữ liệu thật và hàm `_compute_result` trong [`create_model.py#L89-L91`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L89-L91):
```python
# Trích xuất nguyên văn từ Deep-SE classification/create_model.py (L89-L91):
y_pred_guess = numpy.ones(len(y_true)) + numpy.mean(self.train_label)
mae_guess = metrics.mean_absolute_error(y_true, y_pred_guess)
sa = (1 - (auc / mae_guess)) * 100
```
* [`parse_args`](run_deepse_audit.py#L27-L37), [`save_deepse_plot`](run_deepse_audit.py#L40-L107), và [`main`](run_deepse_audit.py#L110-L225) tái tính đồng thời `biased_guess_mae` ([`L144`](run_deepse_audit.py#L144)), mức thổi phồng baseline [`med_inflation`](run_deepse_audit.py#L147), Standardized Accuracy trung thực [`sa_honest_med`](run_deepse_audit.py#L150), và kiểm định Wilcoxon/$\hat{A}_{12}$ toàn cục ([`L190-L192`](run_deepse_audit.py#L190-L192)).

#### 4. `run_deepse_16projects.py` & `run_deepse_retrain.py` — Hai Chiến lược Thực nghiệm
* **[`run_deepse_16projects.py`](run_deepse_16projects.py) (Chiến lược 1):** [`parse_args`](run_deepse_16projects.py#L41-L118) kế thừa mặc định tác giả (`dim=50`, `vocab=500`, `max_length=100`, `hidden_layers=10`, `pool="mean"`, `pretrain="fixed_lm"`, `loss="mse"`, `lr=0.01`, `batch_size=100`, `seed=1234` từ [`exp_script.py#L9,L35-L48`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/exp_script.py#L9) & [`prepare_data.py#L17-L26`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L17-L26)). [`run_single_project`](run_deepse_16projects.py#L121-L301) nạp embedding NCE ([`L163-L167`](run_deepse_16projects.py#L163-L167)), gọi [`train_deepse_session`](run_deepse_16projects.py#L187-L208), lưu `Code_Plus1_Guess` ([`L216`](run_deepse_16projects.py#L216)), và hỗ trợ auto-resume HF. [`save_deepse_benchmark_plot`](run_deepse_16projects.py#L304-L374) & [`main`](run_deepse_16projects.py#L377-L511) áp dụng `holm_bonferroni` ([`L431`](run_deepse_16projects.py#L431)) và 3 phép kiểm định Wilcoxon toàn cục ([`L441-L476`](run_deepse_16projects.py#L441-L476)).
* **[`run_deepse_retrain.py`](run_deepse_retrain.py) (Chiến lược 2):** [`parse_args`](run_deepse_retrain.py#L35-L82), [`resolve_clean_csv`](run_deepse_retrain.py#L85-L97), và [`prepare_setting_data`](run_deepse_retrain.py#L100-L207) so sánh có kiểm soát giữa:
  * `official_pkl` ([`L115-L121`](run_deepse_retrain.py#L115-L121)): Dữ liệu `.pkl.gz` số hóa sẵn của tác giả.
  * `final_raw` ([`L155-L170`](run_deepse_retrain.py#L155-L170)): Văn bản Final Snapshot từ `.csv` + `_3sets.txt` ánh xạ qua [`load_deepse_dict`](run_deepse_retrain.py#L173).
  * `planning_clean` ([`L133-L154`](run_deepse_retrain.py#L133-L154)): Dữ liệu sạch tại `SP_Estimation_Date` từ [../docs/draft/springxd_cleaned_dataset.csv](../docs/draft/springxd_cleaned_dataset.csv) (hoặc `data/clean/`), hỗ trợ chọn từ điển train-only tại [`L175`](run_deepse_retrain.py#L175). Kết quả mỗi seed chạy qua [`run_one_seed`](run_deepse_retrain.py#L247-L369), vẽ loss curve qua [`save_loss_curve`](run_deepse_retrain.py#L210-L244), và tổng hợp ở [`main`](run_deepse_retrain.py#L372-L425).

#### 5. `metrics.py`, `hf_utils.py`, `kaggle_runner.ipynb` — Kiểm định & ResearchOps của Nhóm 3
* [`metrics.py`](metrics.py): [`compute_mae_mdae`](metrics.py#L8-L13), [`compute_sa`](metrics.py#L16-L20), [`safe_wilcoxon`](metrics.py#L23-L33), [`vargha_delaney_a12`](metrics.py#L36-L57), và [`holm_bonferroni`](metrics.py#L60-L73).
* [`hf_utils.py`](hf_utils.py): [`resolve_hf_token`](hf_utils.py#L12-L38), [`get_git_info`](hf_utils.py#L41-L55), và [`HFExperimentLogger`](hf_utils.py#L58-L278) ([`remote_file_exists`](hf_utils.py#L143-L164), [`download_result_if_exists`](hf_utils.py#L166-L182), [`upload_result`](hf_utils.py#L196-L211), [`upload_checkpoint_dir`](hf_utils.py#L213-L230), [`write_and_upload_metadata`](hf_utils.py#L232-L278)).
* [`kaggle_runner.ipynb`](kaggle_runner.ipynb): 5 Code cells (`L23-L48` Config, `L58-L95` HF Secrets Auth, `L105-L129` Git Clone/Pull, `L139-L184` Run Script stream log realtime, `L194-L220` Summary & HF Link).

---

### 3.3. Bảng Ánh Xạ Từng Dòng Mã Nguồn (`Line-by-Line Traceability Matrix`)

| Thành phần | Nguồn gốc tác giả (File & Dòng) | Mã nguồn Nhóm 3 (File & Dòng) | Ghi chú đối soát |
| :--- | :--- | :--- | :--- |
| **Ánh xạ 16 dự án ➔ 9 Repo & Table II** | [`exp_script.py#L15-L33`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/exp_script.py#L15-L33) & Table II | [`config.py#L28-L173`](config.py#L28-L173) | Đối chứng `reported_deepse`, `SA`, `rep_median`, `rep_mean` |
| **Token hóa & Tạo Mask chuỗi** | [`NCE/preprocess.py#L12-L46`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/NCE/preprocess.py#L12-L46), [`prepare_data.py#L50-L78`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L50-L78) | [`config.py#L275-L326`](config.py#L275-L326) | Bảo toàn ngưỡng `vocab_size=500`, `max_len=100`, `+1` shift cho PAD |
| **Embedding & NCE Pretrain HDF5** | [`prepare_data.py#L80-L107`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py#L80-L107) & `NCE/bestModels/*.hdf5` | [`model.py#L83-L100`](model.py#L83-L100), [`model.py#L146-L179`](model.py#L146-L179) | Đọc trực tiếp weights `lstm2v_<repo>_dim<dim>.hdf5` qua `h5py` |
| **Shared LSTM + `PoolingSeq` + `ave`** | [`create_model.py#L190-L217`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L190-L217), [`L259-L354`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L259-L354) | [`model.py#L36-L143`](model.py#L36-L143) (`L104-L138`) | Khởi tạo LSTM kiểu Keras (`orthogonal_` + `forget_bias=1.0`) |
| **Weight-tied Highway (`hdl=10`)** | [`create_model.py#L220-L228`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L220-L228) | [`model.py#L18-L33`](model.py#L18-L33), [`model.py#L110`](model.py#L110), [`model.py#L140-L141`](model.py#L140-L141) | Dùng đúng 1 layer `Highway` lặp 10 bước như bản Keras gốc |
| **Huấn luyện `MSE` / `RMSprop` / EarlyStop** | [`training.py#L49,L84,L96-L103`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/training.py#L49), [`create_model.py#L170-L187`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L170-L187) | [`model.py#L249-L401`](model.py#L249-L401) (`L295`, `L354-L385`) | Giữ nguyên quy tắc giảm nửa `lr` mỗi lần đạt `patience` (`5..30`) |
| **Lỗi `+1.0` trong tính `SA` & Audit** | [`create_model.py#L89-L91`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py#L89-L91) | [`run_deepse_audit.py#L143-L152`](run_deepse_audit.py#L143-L152), [`run_deepse_16projects.py#L216`](run_deepse_16projects.py#L216) | Lật tẩy mức thổi phồng Baseline Median & $SA$ công bố |
| **Chống Temporal Leakage & Stats** | — *(bài báo dùng Final Snapshot)* | [`run_deepse_retrain.py#L133-L154`](run_deepse_retrain.py#L133-L154), [`metrics.py#L8-L73`](metrics.py#L8-L73) | Dữ liệu `planning_clean` + Wilcoxon, $\hat{A}_{12}$, Holm-Bonferroni |

---

### 3.4. Tóm tắt đối chiếu: Giữ nguyên từ tác giả vs. Điều chỉnh của Nhóm 3

| Thành phần | Giữ nguyên từ tác giả Deep-SE (2019) | Điều chỉnh kỹ thuật / Kiểm soát của Nhóm 3 |
| :--- | :--- | :--- |
| **Dataset & Split** | 16 `.pkl.gz`, `.csv` + `_3sets.txt`, 9 `.dict.pkl.gz`, NCE `lstm2v` `.hdf5` | Thêm chế độ `planning_clean` khôi phục đúng trạng thái tại `SP_Estimation_Date` |
| **Kiến trúc Mô hình** | Shared `LSTM`, `PoolingSeq(mean/max/last)`, `ave` merge, Weight-tied `Highway` $\times 10$, Dropout `0.2`/`0.5` | Chuyển dịch từ Keras 1.0.6/Theano (2016) sang PyTorch `nn.Module` tương thích CUDA/Python 3.13 |
| **Huấn luyện** | `vocab=500`, `max_len=100`, `MSE`, `RMSprop(lr=0.01)`, giảm nửa LR theo `patience=5..30` | Hỗ trợ chọn `--pretrain {fixed_lm,finetune_lm,scratch}`, `--loss {mse,mae}`, `--pool` |
| **Baseline & Kiểm định** | Đối chiếu bảng Table II (LD-RNN MAE, Rep Median, Rep Mean, SA) | Tính Baseline thật từ `train`, bóc lỗi `+1.0`, bổ sung Wilcoxon, $\hat{A}_{12}$, Holm-Bonferroni |
| **Vận hành & Lưu trữ** | — | Thin Runner `kaggle_runner.ipynb`, đọc Secrets, auto-resume & đẩy lên HF Dataset/Model repo |

---

## ⚙️ 4. Hướng Dẫn Thiết Lập & Chạy Trên Kaggle

### Bước 1: Gắn Hugging Face Write Token vào Kaggle Secrets
1. Trên Kaggle Notebook: chọn **Add-ons → Secrets → Add a new secret**.
2. **Label:** `hf_token` *(hoặc `HF_TOKEN`)*.
3. **Value:** dán token quyền **Write** từ Hugging Face và bật công tắc sử dụng cho notebook.
4. Ở cột phải Kaggle: chọn **Accelerator** (`CPU` cho `deepse_audit`; `GPU T4 x 2` hoặc `CPU` cho `deepse_16projects` / `deepse_retrain`) và bật **Internet = ON**.

### Bước 2: Chỉnh tham số ở Cell 1 của `kaggle_runner.ipynb` và bấm Run All
* `GIT_BRANCH`: `"main"` (hoặc branch thử nghiệm).
* `EXPERIMENT`: `"deepse_audit"`, `"deepse_16projects"`, hoặc `"deepse_retrain"`.
* `EXTRA_ARGS` gợi ý:
  * Chạy audit 16 dự án: `EXPERIMENT = "deepse_audit"`, `EXTRA_ARGS = ""`
  * Chạy 16 dự án với NCE `fixed_lm` mặc định: `EXPERIMENT = "deepse_16projects"`, `EXTRA_ARGS = "--dim 50"`
  * Test nhanh 2 dự án + lưu checkpoints: `EXPERIMENT = "deepse_16projects"`, `EXTRA_ARGS = "--projects springxd,bamboo --upload-checkpoints"`
  * Huấn luyện lại trên dữ liệu sạch Planning-Time: `EXPERIMENT = "deepse_retrain"`, `EXTRA_ARGS = "--project springxd --setting planning_clean --pretrain scratch --epochs 150 --seeds 1234,42"`

---

## 💻 5. Chạy Thử Cục Bộ (Không Đẩy Lên HF)

```bash
python kaggle_DeepSE/run_deepse_audit.py --projects springxd --no-hf-push
python kaggle_DeepSE/run_deepse_16projects.py --projects springxd --pretrain scratch --epochs 5 --no-hf-push
python kaggle_DeepSE/run_deepse_retrain.py --project springxd --setting planning_clean --pretrain scratch --epochs 5 --no-hf-push
```
