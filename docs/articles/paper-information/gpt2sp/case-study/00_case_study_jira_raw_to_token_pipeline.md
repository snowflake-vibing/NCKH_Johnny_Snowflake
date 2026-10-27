# 🔬 CASE STUDY 00: TỪ JIRA TICKET THÔ ĐẾN CHUỖI TOKENS ĐẦU VÀO GPT2SP
## GIẢI MÃ TOÀN BỘ QUY TRÌNH TIỀN XỬ LÝ, NỐI CHUỖI VĂN BẢN VÀ CẮT CỤT TRÊN JIRA ISSUE XD-3751

> **Chuyên mục:** Nghiên cứu tình huống thực tế (Practical Case Study).  
> **Dự án thực nghiệm:** Spring XD (Jira Repository).  
> **Issue mục tiêu:** **XD-3751** — *"Trigger job should not fail when job name does not exist"*.  
> **Câu hỏi trọng tâm:** Trong thực tế, một ticket Jira có rất nhiều trường (Key, Summary, Description, Type, Priority, Reporter, Status, Comments...). Nhóm tác giả Fu et al. đã lấy những trường nào, ghép chúng lại ra sao, và dùng thuật toán BPE biến chúng thành chuỗi số nguyên (`input_ids`) nạp vào GPT-2 như thế nào?

---

## 🧭 1. DỮ LIỆU THÔ CỦA JIRA TICKET XD-3751 TRONG CSDL

Dưới đây là bản ghi nguyên bản của issue **XD-3751** trích xuất từ kho lưu trữ Jira Spring XD:

* **Issue Key:** `XD-3751`
* **Issue Type:** `Bug`
* **Priority:** `Major`
* **Summary (Title):** `"Trigger job should not fail when job name does not exist"`
* **Description:**  
  `"Currently, when a trigger task is executed against a job that does not exist in the repository, the trigger job throws a fatal NullPointerException and halts the entire batch pipeline. It should gracefully catch the exception, log an ERROR message, and exit with status COMPLETED."`
* **Story Point thực tế ghi nhận:** `3.0`

---

## 🔄 2. QUY TRÌNH TIỀN XỬ LÝ VĂN BẢN (TEXT PREPROCESSING PIPELINE)

Trước khi đưa vào mô hình, tác giả thực hiện quy trình tiền xử lý 4 bước:

* **Bước 1: Làm sạch ký tự lạ và chuẩn hóa khoảng trắng**  
  Loại bỏ các mã điều khiển (`\r\n`, tabs thừa, URLs không cần thiết), chuyển đổi các ký tự Unicode về dạng ASCII tiêu chuẩn.
* **Bước 2: Nối trường (Field Concatenation)**  
  Tác giả ghép nối trường tiêu đề (`Summary`) và trường mô tả (`Description`) lại thành một chuỗi duy nhất với dấu cách ở giữa:
  ```text
  Full_Text = Summary + " " + Description
  ```
* **Bước 3: Thêm Token báo hiệu kết thúc văn bản**  
  Trong GPT-2, ký tự đặc biệt đại diện cho điểm kết thúc của một khối văn bản độc lập là `<|endoftext|>`:
  ```text
  Input_Prompt = Full_Text + "<|endoftext|>"
  ```
* **Bước 4: Cắt cụt (Truncation) & Đệm (Padding)**  
  * *Theo mô tả trong bài báo IEEE TSE 2023:* Chiều dài tối đa được thiết lập là `max_length = 512` tokens. Nếu văn bản vượt quá 512, mô hình cắt bỏ phần đuôi. Nếu ngắn hơn 512, mô hình đệm thêm token `<|pad|>`.
  * *Đối chiếu thực tế trong mã nguồn công khai:* Tác giả chỉ dùng riêng trường `Title` và đặt `max_length = 20` tokens (đây chính là một trong những nguyên nhân khiến kết quả tái lập của Nhóm 3 bị tụt giảm!).

---

## 🔤 3. KẾT QUẢ PHÂN TÁCH TỪ CON BPE (BYTE-PAIR ENCODING)

Chuỗi văn bản sau khi được đưa qua bộ tách từ `GPT2Tokenizer` sử dụng từ điển $50.257$ từ:

```text
Chuỗi thô: "Trigger job should not fail when job name does not exist..."
          │
          ▼ (BPE Tokenizer)
Chuỗi Tokens con: ['Tr', 'igger', ' job', ' should', ' not', ' fail', ' when', ' job', ' name', ' does', ' not', ' exist', ... '<|endoftext|>']
          │
          ▼ (Ánh xạ vào vocab.json)
Danh sách Input IDs: [15984, 18320, 1917, 816, 407, 3064, 618, 1917, 1438, 857, 407, 2378, ... 50256]
```

### Bảng theo dõi phân tách từng từ trên issue XD-3751:

| Từ gốc trong Jira | Token BPE sinh ra | ID trong từ điển ($50.257$) | Giải thích cơ chế |
| :--- | :--- | :---: | :--- |
| `"Trigger"` | `'Tr'`, `'igger'` | `15984`, `18320` | Từ này được chia làm 2 subwords con. |
| `" job"` | `' job'` | `1917` | Có dấu cách đi trước từ "job". |
| `" should"` | `' should'` | `816` | Từ thông dụng có sẵn trong từ điển. |
| `"NullPointerException"` | `'Null'`, `'Pointer'`, `'Exception'` | `26574`, `34091`, `9912` | Từ chuyên ngành lập trình được chia thành 3 gốc từ Java quen thuộc. |
| Kết thúc văn bản | `'<|endoftext|>'` | `50256` | Token kết thúc câu của GPT-2. |

Tổng cộng chuỗi văn bản của XD-3751 sau khi token hóa có đúng **$48$ tokens**.

---

## 📦 4. TẠO TENSOR ĐẦU VÀO PYTORCH (INPUT TENSORS)

Trong PyTorch, mô hình yêu cầu 2 tensor đầu vào có kích thước `[1, seq_len]`:

```python
import torch
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# Thiết lập pad_token trùng với eos_token vì GPT-2 không có sẵn pad_token
tokenizer.pad_token = tokenizer.eos_token

raw_title = "Trigger job should not fail when job name does not exist"
raw_desc = "Currently, when a trigger task is executed against a job that does not exist in the repository, the trigger job throws a fatal NullPointerException and halts the entire batch pipeline. It should gracefully catch the exception, log an ERROR message, and exit with status COMPLETED."

prompt = raw_title + " " + raw_desc

# Tokenize và sinh tensor
inputs = tokenizer(
    prompt, 
    return_tensors='pt', 
    max_length=64, 
    truncation=True, 
    padding='max_length'
)

input_ids = inputs['input_ids']           # Shape: [1, 64]
attention_mask = inputs['attention_mask'] # Shape: [1, 64]
```

### Ý nghĩa của 2 Tensor này:
* `input_ids`: Chứa 48 số nguyên ID của các token thật, theo sau là 16 số nguyên ID `50256` (đại diện cho `<|pad|>`).
* `attention_mask`: Chứa 48 con số `1` (báo hiệu nơ-ron tính toán trên các token thật) và 16 con số `0` (báo hiệu bỏ qua các token đệm).

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG HỆ THỐNG

* 🔬 [Case Study 01: Dòng chảy qua 12 khối Transformer Decoders](01_case_study_12_transformer_decoders.md)
* 🔬 [Case Study 03: Dòng chảy Last Token Pooling trên Issue XD-3751](03_case_study_last_token_pooling_xd3751.md)
* 🧠 [Phân tích 05: Bản chất Merge Operations & BPE từ điển](../critical-thinking/05_merge_operations_and_subword_vocabularies.md)
* 📋 [Báo cáo Tổng quan Điều hành dành cho Partner](../explanation/00_executive_report_and_partner_briefing.md)
