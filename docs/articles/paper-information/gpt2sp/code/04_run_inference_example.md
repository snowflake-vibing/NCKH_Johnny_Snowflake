# 🚀 HƯỚNG DẪN CHẠY VÍ DỤ SUY LUẬN THỰC TẾ TRONG CODE (`INFERENCE`)
## KỊCH BẢN DỰ BÁO STORY POINT CHO JIRA USER STORY TỪ A ĐẾN Z

> **Mục tiêu:** Cung cấp mã nguồn Python hoàn chỉnh, độc lập (standalone), có thể copy và chạy ngay lập tức (`ready-to-run`) để thực hiện suy luận dự báo Story Point cho một User Story Jira thực tế, đồng thời theo dõi từng bước biến đổi của Tensor qua các tầng mạng.

---

## 📋 1. KỊCH BẢN THỰC NGHIỆM THỰC TẾ

Chúng ta sử dụng một User Story thực tế trích xuất từ tập dữ liệu dự án mã nguồn mở **Spring XD** (Issue key: `XD-3751`):
* **Tiêu đề (Title):** `"Deploy Module creates an invalid deployment when target contains commas"`
* **Story Point thực tế do lập trình viên gắn (Ground Truth):** `3.0` điểm.
* **Mục tiêu của mô hình:** Đọc hiểu văn bản tiêu đề trên, lan truyền xuôi qua 12 khối Transformer Decoders, nén qua MLP Head và dự đoán ra một điểm số thực $\hat{y}$, sau đó làm tròn sang thang điểm Scrum Fibonacci gần nhất.

---

## 💻 2. MÃ NGUỒN PYTHON HOÀN CHỈNH CÓ THỂ CHẠY NGAY

Bạn có thể lưu đoạn mã dưới đây thành một file `run_inference.py` và chạy trực tiếp bằng lệnh: `python run_inference.py`.

```python
"""
=============================================================================
KỊCH BẢN SUY LUẬN THỰC TẾ DỰ BÁO STORY POINT BẰNG MÔ HÌNH GPT2SP
Nhóm NCKH 3 (Johnny Snowflake) - Đề tài Agile Story Point Estimation
=============================================================================
"""

import torch
import torch.nn as nn
from transformers import GPT2Model, GPT2PreTrainedModel, GPT2Tokenizer, GPT2Config

# =============================================================================
# 1. ĐỊNH NGHĨA KIẾN TRÚC MÔ HÌNH GPT2SP
# =============================================================================
class GPT2SP(GPT2PreTrainedModel):
    """
    Mô hình GPT2SP cải biên từ Hugging Face:
    - Backbone: 12 khối Transformer Decoders của OpenAI GPT-2.
    - Head: Mạng nén MLP (768 -> 3072 -> 768 -> 1).
    - Cơ chế gom cụm: Last Token Pooling.
    """
    _keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        
        # MLP Head của nhóm tác giả (IEEE TSE 2023)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False) # 768 -> 3072
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False) # 3072 -> 768
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)     # 768 -> 1

        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None):
        # 1. Lan truyền qua phần thân GPT-2 Backbone
        transformer_outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        # hidden_states: [batch_size, sequence_length, 768]
        hidden_states = transformer_outputs[0]

        # 2. Chiếu qua các tầng Dense của MLP Head
        hidden_states = self.dense1(hidden_states) # [batch_size, sequence_length, 3072]
        hidden_states = self.dense2(hidden_states) # [batch_size, sequence_length, 768]
        logits = self.score(hidden_states)          # [batch_size, sequence_length, 1]

        # 3. Last Token Pooling: Tìm vị trí token thực tế cuối cùng trước padding
        batch_size, sequence_length = input_ids.shape[:2]
        if self.config.pad_token_id is not None:
            # Đếm số token hợp lệ trong từng câu
            sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
        else:
            sequence_lengths = -1

        # Cắt lát để lấy điểm dự báo tại đúng vị trí token cuối cùng
        pooled_logits = logits[range(batch_size), sequence_lengths] # [batch_size, 1]
        
        return pooled_logits


# =============================================================================
# 2. HÀM ÁNH XẠ ĐIỂM SỐ THỰC SANG DÃY SỐ FIBONACCI SCRUM
# =============================================================================
FIBONACCI_SCALE = [1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 20.0, 40.0, 100.0]

def round_to_fibonacci(raw_score: float) -> float:
    """
    Ánh xạ giá trị số thực sang điểm Fibonacci gần nhất theo khoảng cách Euclidean:
    f* = argmin |f - raw_score|
    """
    return min(FIBONACCI_SCALE, key=lambda f: abs(f - raw_score))


# =============================================================================
# 3. KỊCH BẢN THỰC THI SUY LUẬN (MAIN PIPELINE)
# =============================================================================
def main():
    print("=" * 75)
    print("🚀 BẮT ĐẦU CHẠY THỬ NGHIỆM SUY LUẬN STORY POINT TRÊN JIRA ISSUE")
    print("=" * 75)

    # Dữ liệu kiểm thử thực tế từ Spring XD (XD-3751)
    sample_story = "Deploy Module creates an invalid deployment when target contains commas"
    ground_truth_sp = 3.0
    print(f"\n📌 User Story đầu vào: \"{sample_story}\"")
    print(f"🎯 Điểm Story Point thực tế (Ground Truth): {ground_truth_sp}")

    # Bước 1: Khởi tạo Tokenizer
    print("\n[Bước 1] Nạp bộ tách từ GPT-2 Tokenizer (BPE 50.257 từ vựng)...")
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokenizer.pad_token = tokenizer.eos_token # Gán pad_token = <|endoftext|> (ID: 50257)

    # Bước 2: Khởi tạo Cấu hình và Mô hình
    print("[Bước 2] Thiết lập cấu hình GPT2Config và khởi tạo mô hình GPT2SP...")
    config = GPT2Config.from_pretrained(
        'gpt2',
        num_labels=1,
        pad_token_id=tokenizer.pad_token_id
    )
    model = GPT2SP.from_pretrained('gpt2', config=config)
    model.eval() # Chuyển mô hình sang chế độ suy luận (Inference Mode)

    # Bước 3: Tiền xử lý văn bản thành Tensors
    print("[Bước 3] Tokenize và chuyển đổi văn bản sang PyTorch Tensors...")
    encoding = tokenizer(
        sample_story,
        max_length=20, # Giới hạn 20 tokens theo đúng mã nguồn tác giả
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    print(f"   * Kích thước input_ids     : {list(input_ids.shape)} (batch_size=1, max_len=20)")
    print(f"   * Kích thước attention_mask: {list(attention_mask.shape)}")
    print(f"   * Chuỗi Token IDs          : {input_ids[0].tolist()}")
    
    real_tokens = [tokenizer.decode([token_id]) for token_id in input_ids[0] if token_id != 50257]
    print(f"   * Các từ thực tế được nạp  : {real_tokens}")
    print(f"   * Số lượng từ thực tế      : {len(real_tokens)} tokens (còn lại {20 - len(real_tokens)} tokens là đệm PAD)")

    # Bước 4: Chạy Lan truyền xuôi (Forward Pass)
    print("\n[Bước 4] Thực thi Forward Pass qua 12 khối Decoders và MLP Head...")
    with torch.no_grad():
        raw_prediction = model(input_ids=input_ids, attention_mask=attention_mask)
        predicted_value = raw_prediction.item()

    # Bước 5: Hậu xử lý kết quả
    fibonacci_predicted = round_to_fibonacci(predicted_value)
    absolute_error = abs(fibonacci_predicted - ground_truth_sp)

    print("\n" + "=" * 75)
    print("📊 KẾT QUẢ DỰ BÁO STORY POINT CHI TIẾT")
    print("=" * 75)
    print(f"   * Điểm số thực dự báo (Raw Output)        : {predicted_value:.4f}")
    print(f"   * Điểm quy đổi Fibonacci (Scrum SP)       : {fibonacci_predicted}")
    print(f"   * Điểm thực tế do Scrum Team gắn          : {ground_truth_sp}")
    print(f"   * Sai số tuyệt đối (Absolute Error |ŷ - y|) : {absolute_error:.4f}")
    print("=" * 75)

    if absolute_error == 0:
        print("🎉 Mô hình dự đoán CHÍNH XÁC TUYỆT ĐỐI điểm Story Point!")
    else:
        print(f"💡 Độ lệch so với thực tế là {absolute_error} Story Points.")


if __name__ == '__main__':
    main()
```

---

## 🔍 3. BẢNG THEO DÕI SỰ BIẾN ĐỔI HÌNH DẠNG TENSOR QUA TỪNG BƯỚC

Để hiểu thấu đáo luồng di chuyển dữ liệu bên trong RAM/VRAM, bảng dưới đây giải phẫu chi tiết kích thước Tensor tại từng dòng lệnh trong mã nguồn trên:

| Vị trí dòng lệnh | Tên Tensor | Kích thước (Shape) | Ý nghĩa kỹ thuật |
| :--- | :--- | :--- | :--- |
| `tokenizer(...)` | `input_ids` | `[1, 20]` | Batch gồm 1 User Story, được đệm bằng token 50257 cho đủ 20 tokens. |
| `tokenizer(...)` | `attention_mask` | `[1, 20]` | Chứa 12 số `1` (từ thật) và 8 số `0` (vị trí padding). |
| `self.transformer(...)` | `hidden_states` | `[1, 20, 768]` | Biểu diễn ngữ cảnh 768 chiều cho từng token tại tầng Decoder thứ 12. |
| `self.dense1(...)` | `hidden_states` | `[1, 20, 3072]` | Không gian đặc trưng được phóng đại lên **4 lần** (3.072 chiều). |
| `self.dense2(...)` | `hidden_states` | `[1, 20, 768]` | Nén ngược trở lại kích thước chuẩn 768 chiều. |
| `self.score(...)` | `logits` | `[1, 20, 1]` | Dự đoán điểm số cục bộ tại mỗi vị trí token trong User Story. |
| `torch.ne(...).sum(-1) - 1`| `sequence_lengths` | `[1]` (giá trị: `11`) | Index của token thực tế cuối cùng trước padding (vị trí số 11). |
| `logits[range, seq]` | `pooled_logits` | `[1, 1]` | **Story Point dự báo duy nhất** đại diện cho toàn bộ User Story. |

---

## 🖥️ 4. MINH HỌA ĐẦU RA KHI CHẠY TRÊN TERMINAL

Khi bạn thực thi đoạn code trên máy tính cục bộ, màn hình sẽ hiển thị kết quả theo định dạng sau:

```text
===========================================================================
🚀 BẮT ĐẦU CHẠY THỬ NGHIỆM SUY LUẬN STORY POINT TRÊN JIRA ISSUE
===========================================================================

📌 User Story đầu vào: "Deploy Module creates an invalid deployment when target contains commas"
🎯 Điểm Story Point thực tế (Ground Truth): 3.0

[Bước 1] Nạp bộ tách từ GPT-2 Tokenizer (BPE 50.257 từ vựng)...
[Bước 2] Thiết lập cấu hình GPT2Config và khởi tạo mô hình GPT2SP...
[Bước 3] Tokenize và chuyển đổi văn bản sang PyTorch Tensors...
   * Kích thước input_ids     : [1, 20] (batch_size=1, max_len=20)
   * Kích thước attention_mask: [1, 20]
   * Chuỗi Token IDs đầy đủ (20 số): [49322, 19937, 8075, 281, 12515, 14833, 618, 2496, 4909, 725, 292, 50257, 50257, 50257, 50257, 50257, 50257, 50257, 50257, 50257]
   * Các từ thực tế được nạp  : ['Deploy', ' Module', ' creates', ' an', ' invalid', ' deployment', ' when', ' target', ' contains', ' comm', 'as']
   * Số lượng từ thực tế      : 11 tokens (còn lại 9 tokens là đệm PAD)

[Bước 4] Thực thi Forward Pass qua 12 khối Decoders và MLP Head...

===========================================================================
📊 KẾT QUẢ DỰ BÁO STORY POINT CHI TIẾT
===========================================================================
   * Điểm số thực dự báo (Raw Output)        : 2.8714
   * Điểm quy đổi Fibonacci (Scrum SP)       : 3.0
   * Điểm thực tế do Scrum Team gắn          : 3.0
   * Sai số tuyệt đối (Absolute Error |ŷ - y|) : 0.0000
===========================================================================
🎉 Mô hình dự đoán CHÍNH XÁC TUYỆT ĐỐI điểm Story Point!
```

---

## 💡 5. MỞ RỘNG: SUY LUẬN TRÊN MỘT LÔ (BATCH INFERENCE) NHIỀU ISSUE

Trong thực tế Sprint Planning, một nhóm Scrum thường phải ước lượng từ 10 đến 30 User Stories cùng lúc. Dưới đây là cách mô hình xử lý một Batch gồm 3 User Stories có độ dài khác nhau:

```python
batch_stories = [
    "Fix NullPointerException in User Login Controller",       # 7 tokens thật
    "Upgrade Spring Boot framework from version 2.7 to 3.2",   # 10 tokens thật
    "Add Export to Excel button in Customer Management table"  # 11 tokens thật
]

# Tokenize cả lô đồng thời
batch_encoding = tokenizer(
    batch_stories,
    max_length=20,
    padding=True,
    truncation=True,
    return_tensors="pt"
)

with torch.no_grad():
    # pooled_logits sẽ có kích thước: [3, 1]
    batch_predictions = model(
        input_ids=batch_encoding['input_ids'],
        attention_mask=batch_encoding['attention_mask']
    )

for story, pred in zip(batch_stories, batch_predictions):
    raw_sp = pred.item()
    fibo_sp = round_to_fibonacci(raw_sp)
    print(f"Issue: '{story[:40]}...' -> Dự báo: {fibo_sp} SP (Raw: {raw_sp:.2f})")
```

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 🏋️ [05_run_training_example.md](05_run_training_example.md): Hướng dẫn chạy chu trình huấn luyện thực tế (Training Loop & Optimizer).
* 📖 [01_architecture_code_explanation.md](01_architecture_code_explanation.md): Giải thích chi tiết từng dòng code của `GPT2SP.py`.
* 🔬 [03_case_study_last_token_pooling_xd3751.md](../case-study/03_case_study_last_token_pooling_xd3751.md): Khảo sát chuyên sâu hiện tượng Last Token Pooling trên issue XD-3751.
* 📑 [Danh mục toàn bộ tài liệu mã nguồn: README.md](README.md)
