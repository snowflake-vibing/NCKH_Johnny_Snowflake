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

### 3.2. Truy vết chi tiết từng module (`File-by-File Provenance`)

#### 1. `config.py` — Dữ liệu, Từ điển & Tiền xử lý chuỗi
* **Bảng tham chiếu `BENCHMARK_PROJECTS`:** Số liệu `reported_deepse`, `reported_deepse_sa`, `rep_median`, `rep_mean` và ánh xạ 16 dự án ➔ 9 repo Jira (`datasetDict`) trích xuất trực tiếp từ **Table II (Trang 8)** bài báo Deep-SE và [`classification/exp_script.py`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/exp_script.py).
* **Nạp dữ liệu nhị phân & từ điển gốc:**
  * `load_deepse_splits`: Tải `<project>.csv` + `<project>_3sets.txt` để giữ đúng chia cắt thời gian 60/20/20 gốc.
  * `load_deepse_pkl_splits` & `load_deepse_dict`: Giải nén `.pkl.gz` / `.dict.pkl.gz` với `encoding="latin1"` để đọc chính xác file pickle Python 2 của tác giả trên Python 3.13 / NumPy 2.x.
  * `texts_to_word_ids` & `prepare_sequence_tensors`: Chuyển dịch trực tiếp logic `grab_data()` trong `NCE/preprocess.py` và `create_mask()` trong [`classification/prepare_data.py`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/prepare_data.py) (lọc từ có ID $< \text{vocab\_size}$, cộng `+1` để dành index `0` làm PAD, cắt/đệm tới `max_len=100`).

#### 2. `model.py` — Chuyển dịch Keras 1.0.6 / Theano ➔ PyTorch 2.x Thuần Túy
Mã nguồn gốc của tác giả viết bằng **Python 2 + Keras 1.0.6 + Theano (2016)** vốn không còn cài đặt được trên Kaggle hiện đại (CUDA 12/13, PyTorch 2.x, Python 3.13). Nhóm 3 chuyển dịch trung thành 100% toán học kiến trúc từ [`classification/create_model.py`](https://github.com/morakotch/datasets/blob/master/storypoint/IEEE%20TSE2018/Deep-SE/classification/create_model.py):
* **Shared LSTM Backbone (`create_model` / `create_fixed`):** Một tầng `nn.LSTM(emb_dim, emb_dim)` dùng chung cho cả nhánh `Title` và `Description`, khởi tạo `xavier_uniform_` (input), `orthogonal_` (recurrent) và `forget_bias = 1.0` giống Keras `forget_bias_init='one'`, kèm dropout đầu vào `0.2`.
* **`PoolingSeq` & Average Merge:** Tái lập lớp custom Keras `PoolingSeq` với 3 chế độ `mean` (mặc định), `max` (mask vị trí padding bằng `-1e9`) và `last` (token thực cuối cùng), sau đó trung bình cộng hai vector `0.5 * (pooled_title + pooled_descr)`.
* **Weight-tied Highway Network (`create_highway`, dòng 220–228 trong `create_model.py`):** Chi tiết cực kỳ quan trọng trong code gốc là tác giả **khởi tạo 1 đối tượng `Highway` duy nhất rồi lặp qua `hdl=10` lần** (chia sẻ trọng số qua 10 bước), với `activation='relu'`, `init='glorot_normal'` và `transform_bias=-1`. `HighwayLayer` giữ nguyên hoàn toàn cơ chế trọng số chia sẻ này cùng `Dropout(0.5)` ở hai đầu và `Linear(emb_dim, 1)` cuối.
* **Nạp trọng số tiền huấn luyện NCE (`load_pretrained_lm_embedding`):** Đọc trực tiếp file `lstm2v_<repo>_dim<dim>.hdf5` trong `NCE/bestModels/` bằng `h5py`, trích ma trận embedding và gắn vào `nn.Embedding` với hàng `0` là vector không cho PAD (tương đương `prepare_data.to_features()`).
* **Chiến lược tối ưu & Early Stopping (`train_deepse_session`):** Áp dụng hàm mất mát `MSE` (mặc định gốc), tối ưu `RMSprop(lr=0.01)` và cơ chế giảm nửa learning rate từ callback `SaveResult` (`patience` khởi đầu `5`, mỗi lần không cải thiện `val_mae` đạt `wait == patience` thì `lr /= 2`, tăng `patience += 5`, dừng khi `patience > 30` hoặc xuất hiện `NaN`).

#### 3. `run_deepse_audit.py` — Kiểm định Baseline Inflation & Phép cộng `+1.0`
Đối soát trực tiếp **Table II** của bài báo Deep-SE với dữ liệu thật và hàm `_compute_result` trong `create_model.py` (dòng 114–118):
```python
# Trích xuất nguyên văn từ Deep-SE classification/create_model.py:
y_pred_guess = numpy.ones(len(y_true)) + numpy.mean(self.train_label)
mae_guess = metrics.mean_absolute_error(y_true, y_pred_guess)
sa = (1 - (auc / mae_guess)) * 100
```
Script đo định lượng mức độ thổi phồng của Reported Median MAE và chứng minh tỷ lệ `SA` bị đẩy cao giả tạo do `+ 1.0`.

#### 4. `run_deepse_16projects.py` & `run_deepse_retrain.py` — Hai Chiến lược Thực nghiệm
* **`run_deepse_16projects.py` (Chiến lược 1):** Tái lập huấn luyện Deep-SE trên cả 16 dự án từ `<project>.pkl.gz` và embeddings NCE `lstm2v` (mặc định `fixed_lm`, `dim=50`, `vocab=500`, `max_length=100`, `hidden_layers=10`), xuất dự báo chi tiết từng issue, bảng tổng hợp 16 dự án, kiểm định toàn cục (Wilcoxon + $\hat{A}_{12}$ + Holm-Bonferroni) và biểu đồ 300 DPI.
* **`run_deepse_retrain.py` (Chiến lược 2):** So sánh có kiểm soát trên cùng một dự án giữa 3 setting:
  * `official_pkl`: Dữ liệu `.pkl.gz` số hóa sẵn của tác giả.
  * `final_raw`: Văn bản Final Snapshot từ `.csv` + `_3sets.txt` ánh xạ qua từ điển `<repo>.dict.pkl.gz`.
  * `planning_clean`: Dữ liệu sạch tại thời điểm `SP_Estimation_Date` không chứa rò rỉ tương lai từ [`../docs/draft/springxd_cleaned_dataset.csv`](../docs/draft/springxd_cleaned_dataset.csv) (hoặc `data/clean/`).

#### 5. `metrics.py`, `hf_utils.py`, `kaggle_runner.ipynb` — Kiểm định & ResearchOps của Nhóm 3
* Tính toán Baseline **chỉ từ tập `train`**, kiểm định Wilcoxon Signed-Rank Test, $\hat{A}_{12}$, Holm-Bonferroni.
* Hạ tầng GitHub ➔ Kaggle ➔ Hugging Face Hub với auto-resume và ghi `run_metadata.json` không lộ token.

---

### 3.3. Tóm tắt đối chiếu: Giữ nguyên từ tác giả vs. Điều chỉnh của Nhóm 3

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
