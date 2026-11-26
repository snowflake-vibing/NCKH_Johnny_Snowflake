# 🚀 Kaggle Modular Runner for TAWOS Planning-Time Snapshot (`GitHub ➔ Kaggle ➔ HF Hub`)

Thư mục `kaggle_TAWOS/` đóng gói và mở rộng toàn bộ pipeline thực nghiệm **13 dự án TAWOS V1.1 × 3 Setting (`final`, `cross`, `planning`)** từ kho [`JohnnyPhan1712/SR-G3_planning-time-sp`](https://github.com/JohnnyPhan1712/SR-G3_planning-time-sp.git) để chạy độc lập trên **Kaggle CPU/GPU** và đẩy kết quả chuẩn **Phương án A** về **`Snowflake06/NCKH3-StoryPoint-Artifact`**.

> 💡 **Lưu ý điều hướng:**
> - Tái lập 16 dự án GPT2SP: [`../kaggle_GPT2SP/README.md`](../kaggle_GPT2SP/README.md)
> - Tái lập & thẩm định Deep-SE: [`../kaggle_DeepSE/README.md`](../kaggle_DeepSE/README.md)

---

## 🔄 1. Luồng Dữ Liệu & Thực Nghiệm

```text
[TAWOS.sql(.gz/.zip) / SQLite (.db) / Interim Parquet / Snapshot Parquet / MySQL]
        │
        ▼ (prepare_tawos_dataset.py — không cần cài MySQL khi đọc TAWOS.sql / SQLite)
[13 x <PROJECT>_snapshot.parquet + dataset_summary.csv]
        │
        ├──(1 commit)──► [HF: NCKH3-StoryPoint-Artifact / datasets/tawos_snapshots/]
        │
        ▼ (tự động kéo về Kaggle khi chạy thực nghiệm)
  ├── run_tawos_baseline.py  ──► Mean / Median / TF-IDF+Ridge + Wilcoxon/Â12/Holm
  └── run_tawos_gpt2sp.py    ──► GPT2SP 2-Model Optimization (Final + Planning -> 3 Settings)
```

---

## 📂 2. Danh Sách File & Truy Vết Mã Nguồn (`Provenance`)

| File trong `kaggle_TAWOS/` | Nguồn gốc từ `JohnnyPhan1712/SR-G3_planning-time-sp` | Chức năng chính & mở rộng trên Kaggle |
| :--- | :--- | :--- |
| [config.py](config.py) | `src/config.py`, `src/snapshot.py`, `src/baseline.py` | 13 `PROJECTS` ([`L18-L32`](config.py#L18-L32)), `SP_FIELDS` gồm cả `story points (obsolete)` ([`L54`](config.py#L54)), `SETTINGS` [`final`/`cross`/`planning`](config.py#L79-L83), `discover_snapshot_file` ([`L116-L161`](config.py#L116-L161)) |
| [prepare_tawos_dataset.py](prepare_tawos_dataset.py) | `src/snapshot.py` & `src/extract.py` | [`build_snapshot`](prepare_tawos_dataset.py#L139-L190) khớp 100% `test_snapshot()`; parser 2 lượt [`build_snapshots_from_sql`](prepare_tawos_dataset.py#L482-L615) (`TAWOS.sql`/`.gz`/`.zip`, không cần MySQL) + [`build_snapshots_from_sqlite`](prepare_tawos_dataset.py#L618-L669) (`tawos_eda.db`); [`compute_project_audit_row`](prepare_tawos_dataset.py#L800-L835) & upload HF 1 commit |
| [dataset.py](dataset.py) | `src/gpt2sp/dataset.py` | [`StoryPointDataset`](dataset.py#L20-L69), chia thời gian 60/20/20 [`load_tawos_snapshot`](dataset.py#L72-L134) (`SP <= 100`, sort `Planning_Date, ID`) |
| [model.py](model.py) | `src/gpt2sp/model.py` | [`GPT2SP`](model.py#L15-L87) (GPT-2 small + 3 tầng MLP không bias `768->3072->768->1` + Last Token Pooling + `nn.L1Loss`) |
| [metrics.py](metrics.py) | `src/gpt2sp/metrics.py` | [`compute_metrics`](metrics.py#L20-L58) sửa lỗi PR #2 + SA random guessing, [`sa_vs_median`](metrics.py#L61-L65), [`safe_wilcoxon`](metrics.py#L73-L82), [`vargha_delaney_a12`](metrics.py#L85-L100) |
| [compare.py](compare.py) | `src/compare.py` | [`a12`](compare.py#L29-L31), [`holm`](compare.py#L40-L49), [`compare`](compare.py#L96-L126) (Wilcoxon theo cặp + Holm theo `(pair, group)`), vẽ biểu đồ 300 DPI [`plot_tawos_3setting_comparison`](compare.py#L129-L201) |
| [hf_utils.py](hf_utils.py) | Nhóm 3 ResearchOps (`kaggle_GPT2SP/hf_utils.py`) | [`HFExperimentLogger`](hf_utils.py#L71-L328) gom 1 commit `create_commit`, auto-resume & [`ensure_tawos_snapshots`](hf_utils.py#L331-L398) |
| [run_tawos_baseline.py](run_tawos_baseline.py) | `src/baseline.py` | [`_constant_model`](run_tawos_baseline.py#L66-L70) (`mean`, `median`), [`_tfidf_ridge_model`](run_tawos_baseline.py#L73-L93), xuất 9 parquet + `summary.csv` + `wilcoxon.csv` |
| [run_tawos_gpt2sp.py](run_tawos_gpt2sp.py) | `src/gpt2sp/train_tawos.py` | [`run_tawos_project`](run_tawos_gpt2sp.py#L248-L335) tối ưu 2 mô hình (`Model Final` + `Model Planning`), [`_try_load_resumed_project`](run_tawos_gpt2sp.py#L338-L360) auto-resume từng dự án, đối chiếu Median bắt buộc & push 1 commit |
| [kaggle_runner.ipynb](kaggle_runner.ipynb) | Thin Runner Pattern | 5 Code cells hỗ trợ 4 chế độ (`prepare_tawos_dataset`, `tawos_baseline`, `tawos_gpt2sp`, `refresh_hf_artifact`) |
| [requirements.txt](requirements.txt) | `requirements.txt` | Danh sách thư viện phụ thuộc cho Kaggle / workstation |

---

## 🛠️ 3. Cách Chạy Script Chỉnh & Chuẩn Bị Dataset (`prepare_tawos_dataset.py`)

Điểm mạnh của [`prepare_tawos_dataset.py`](prepare_tawos_dataset.py#L901-L999) là **xây dựng lại toàn bộ 13 file `<PROJECT>_snapshot.parquet` không rò rỉ dữ liệu ngay trên Kaggle mà không cần cài MySQL Server** (hỗ trợ xử lý thứ tự bảng chữ cái `Change_Log` ➔ `Issue` ➔ `Project` của `mysqldump` bằng parser 2 lượt [`build_snapshots_from_sql`](prepare_tawos_dataset.py#L482-L615), hoặc đọc SQLite trực tiếp qua [`build_snapshots_from_sqlite`](prepare_tawos_dataset.py#L618-L669)).

### 5 chế độ đầu vào (`--source`):

1. **Từ file dump `TAWOS.sql` / `.sql.gz` / `.sql.zip` (Khuyên dùng — đầy đủ gốc 9,25 triệu dòng `Change_Log`):**
   ```bash
   python kaggle_TAWOS/prepare_tawos_dataset.py --source sql --sql-path /kaggle/input/tawos-sql/TAWOS.sql
   ```
   *(Hoặc để `--source auto` — mặc định trên Kaggle — script tự quét `/kaggle/input/**`, hoặc truyền `--download-url <URL>` nếu kéo từ URL công khai.)*

2. **Từ file SQLite (`tawos_eda.db` / `.sqlite`):**
   ```bash
   python kaggle_TAWOS/prepare_tawos_dataset.py --source sqlite --sqlite-path /kaggle/input/tawos-db/tawos_eda.db
   ```
   *(Lưu ý: `tawos_eda.db` trên máy cũ có `9.114.602` dòng `Change_Log`, ít hơn ~`138k` dòng so với `TAWOS.sql` gốc `9.253.419` dòng — ưu tiên `TAWOS.sql` nếu có thể.)*

3. **Từ bộ snapshot đã dựng sẵn trên máy Johnny (`<PROJECT>_snapshot.parquet` / `.csv`):**
   ```bash
   python kaggle_TAWOS/prepare_tawos_dataset.py --source snapshot --input-dir D:/NCKH_Johnny/data/processed
   ```
   Kiểm tra đủ 10 cột chuẩn (`SNAPSHOT_REQUIRED_COLS`), chuẩn hóa kiểu dữ liệu và khoảng trắng (không unquote kép sai dữ liệu), xuất bảng kiểm định `dataset_summary.csv` rồi đẩy lên `Snowflake06/NCKH3-StoryPoint-Artifact/datasets/tawos_snapshots/` chỉ trong **1 commit**.

4. **Từ bảng trung gian (`<PROJECT>_issue.parquet` + `<PROJECT>_changelog.parquet`):**
   ```bash
   python kaggle_TAWOS/prepare_tawos_dataset.py --source interim --input-dir D:/NCKH_Johnny/data/interim
   ```

5. **Trực tiếp từ MySQL cục bộ (`MYSQL_USER`, `MYSQL_PWD`, `MYSQL_DB`):**
   ```bash
   python kaggle_TAWOS/prepare_tawos_dataset.py --source mysql
   ```

> **Kiểm thử cục bộ không đẩy lên HF:** thêm `--no-hf-push` vào bất kỳ lệnh nào trên.

---

## ▶️ 4. Hướng Dẫn Chạy Trên Kaggle (`kaggle_runner.ipynb`)

1. Import file [kaggle_runner.ipynb](kaggle_runner.ipynb) lên Kaggle.
2. Bật **Internet: On** và **Add-ons → Secrets** (`hf_token` / `HF_TOKEN` quyền Write).
3. Chọn `EXPERIMENT` tại **Cell 1** rồi bấm **Run All**:

| Giá trị `EXPERIMENT` | Hardware khuyến nghị | Mục đích |
| :--- | :---: | :--- |
| `"prepare_tawos_dataset"` | **CPU** | Dựng/chuẩn hóa 13 snapshot parquets & đẩy lên `datasets/tawos_snapshots/` (`--sql-path` trong `EXTRA_ARGS`) |
| `"tawos_baseline"` | **CPU** | Chạy `Mean`, `Median`, `TF-IDF + Ridge` × 13 dự án × 3 setting + Wilcoxon/$\hat{A}_{12}$/Holm |
| `"tawos_gpt2sp"` | **GPU T4** | Huấn luyện GPT2SP (mặc định `--epochs 20 --lr 5e-4 --batch-size 32 --max-len 128`) kèm Auto-Resume & đối chiếu Median |
| `"refresh_hf_artifact"` | **CPU** | Chạy [`migrate_hf_artifact.py --in-place`](../scripts/migrate_hf_artifact.py) để tạo `README.md` (YAML HF Viewer), `comparisons/`, `datasets/` ngay trên repo HF hiện có mà không đụng tới kết quả GPT2SP/Deep-SE cũ |

---

## 📦 5. Cấu Trúc Kết Quả Trên `Snowflake06/NCKH3-StoryPoint-Artifact`

```text
NCKH3-StoryPoint-Artifact/
├── datasets/tawos_snapshots/
│   ├── <PROJECT>_snapshot.parquet   # 13 file snapshot tại SP_Estimation_Date
│   ├── dataset_summary.csv          # Audit rò rỉ dữ liệu & tỉ lệ changed/split
│   └── metadata.json
└── experiments/tawos/
    ├── baseline/13proj_3settings_seed42/
    │   ├── summary.csv
    │   ├── mae_by_group.csv
    │   ├── wilcoxon.csv
    │   ├── metadata.json
    │   ├── figures/tawos_3setting_comparison.png
    │   └── predictions/baseline_{mean,median,tfidf_ridge}_{final,cross,planning}.parquet
    └── gpt2sp/13proj_3settings_seed42/
        ├── summary.csv              # Đầy đủ GPT2SP vs Train+Val Median + SA_vs_Median + Wilcoxon
        ├── stat_tests_vs_median.csv # Kiểm định toàn cục từng setting vs Median
        ├── mae_by_group.csv         # MAE nhóm all / changed / unchanged
        ├── wilcoxon.csv             # Wilcoxon theo cặp setting (final-cross, cross-planning, final-planning)
        ├── metadata.json
        ├── figures/tawos_3setting_comparison.png
        └── predictions/
            ├── per_project/<PROJECT>_{final,cross,planning}.parquet
            └── gpt2sp_gpt2sp_{final,cross,planning}.parquet
```
