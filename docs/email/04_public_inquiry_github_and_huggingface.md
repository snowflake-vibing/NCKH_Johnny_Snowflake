# 🌐 MẪU CÂU HỎI KÊNH CÔNG KHAI (GITHUB ISSUE & HUGGING FACE DISCUSSION)

> **Mục tiêu:** Tạo kênh trao đổi kỹ thuật công khai, minh bạch, mang lại giá trị cho cộng đồng nghiên cứu mã nguồn mở mà không phụ thuộc vào hòm thư cá nhân.  
> **Thời điểm thực hiện:** Song song hoặc sau khi gửi thư nhắc (khoảng ngày 20/11/2026 trở đi).

---

## 🐙 PHẦN 1: GITHUB ISSUE TRÊN REPOSITORY `awsm-research/gpt2sp`

* **Đường dẫn tạo Issue:** [`https://github.com/awsm-research/gpt2sp/issues/new`](https://github.com/awsm-research/gpt2sp/issues/new)
* **Tiêu đề Issue (Title):**
  ```text
  [Question] Clarification on Evaluation Setup and Discrepancy on Spring XD Benchmark (Table 4)
  ```
* **Nội dung Issue (Body - Markdown):**

```markdown
### Description & Context

Hi @awsm-research team, @yeh-fu,

First of all, thank you very much for open-sourcing the code and checkpoints for your seminal work **"GPT2SP: A Transformer-Based Agile Story Point Estimation Approach" (IEEE TSE 2023)**.

As part of an independent academic replication study at UIT - VNU-HCM on Agile Story Point Estimation, we reproduced your evaluation pipeline on the **Spring XD** benchmark using:
1. Official code: `GPT2SP.py` and `model_training_notebook.ipynb` from this repository.
2. Official model weights: `MickyMike/0-GPT2SP-springxd` on Hugging Face Hub.
3. Dataset: `sp_dataset/marked_data/springxd.csv` (using the author-labeled chronological 60/20/20 `split_mark` with 706 test issues).

### Observation & Empirical Discrepancy

When running inference on the test split following the notebook parameters (`SEQUENCE_LEN = 20`, `title` as input, pad token `50257`):
- **Our Replicated GPT2SP MAE:** `3.3090` (MdAE = `2.9523`)
- **Training Set Median Effort Baseline MAE:** `1.7153` (MdAE = `2.0000`)
- **Wilcoxon Signed-Rank Test (GPT2SP vs Baseline):** `p = 1.48e-84` (Baseline achieves lower error)
- **Reported MAE in Table 4 of the Paper:** `0.96`

### Specific Questions

To help us and future researchers faithfully align with your published benchmarks, could you kindly clarify:

1. **Input Fields:** Does Table 4 evaluate models trained on `title` only (as written in `prepare_dataframe()`: `d = {'text': (data['title']).tolist(), ...}`), or was `title + description` concatenated during the final evaluation?
2. **Context Length:** Was `SEQUENCE_LEN = 20` applied during Table 4 evaluation, or was a longer context window (e.g., 128 / 512) employed?
3. **Post-Processing / Rounding:** Was there any post-processing applied to the continuous regression predictions (e.g., clipping, normalization back-transform, or Fibonacci bin mapping)?
4. **Evaluation Script:** Is there a dedicated evaluation script or test harness notebook that you could share to reproduce the exact `0.96` MAE?

We have documented our end-to-end Kaggle replication harness, logs, and checkpoints transparently in our repository:
👉 https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake

Thank you very much for your time and contribution to open research in software engineering!
```

---

## 🤗 PHẦN 2: HUGGING FACE COMMUNITY DISCUSSION TRÊN `MickyMike/0-GPT2SP-springxd`

* **Đường dẫn tạo Discussion:** [`https://huggingface.co/MickyMike/0-GPT2SP-springxd/discussions/new`](https://huggingface.co/MickyMike/0-GPT2SP-springxd/discussions/new)
* **Tiêu đề Discussion (Title):**
  ```text
  Test set evaluation discrepancy on Spring XD: MAE 3.31 vs paper Table 4 (0.96)
  ```
* **Nội dung Discussion (Markdown):**

```markdown
Hi @MickyMike,

Thank you for publishing your pre-trained GPT2SP checkpoints on Hugging Face!

When running inference with this checkpoint (`MickyMike/0-GPT2SP-springxd`) over the 706 chronological test issues of Spring XD (`sp_dataset/marked_data/springxd.csv`), our evaluation yields an MAE of **3.3090** (with a training set Median Baseline yielding **1.7153**), whereas Table 4 in the IEEE TSE 2023 paper reports an MAE of **0.96**.

We would love to know:
- Does this checkpoint expect input formatted as `title` only or `title + description`?
- What was the exact sequence length and tokenizer configuration used during evaluation?

Our complete open-source replication environment and code are available at: https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake

Any insights would be greatly appreciated!
```
