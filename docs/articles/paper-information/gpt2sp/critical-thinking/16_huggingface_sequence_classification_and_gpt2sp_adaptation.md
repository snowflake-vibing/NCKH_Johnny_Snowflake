# 🧠 GIẢI PHẪU CODE HUGGING FACE CHO BÀI TOÁN PHÂN LOẠI CHUỖI VÀ CÁCH GPT2SP CẢI BIÊN (ADAPTATION)
## BẢN CHẤT KẾ THỪA TỪ `GPT2ForSequenceClassification`, SỰ KHÁC BIỆT GIỮA CHUẨN CÔNG NGHIỆP VÀ MÃ NGUỒN BÀI BÁO (IEEE TSE 2023)

> **Mã nguồn phân tích:**  
> 1. Mã nguồn gốc Hugging Face: [`transformers.models.gpt2.modeling_gpt2.GPT2ForSequenceClassification`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/gpt2/modeling_gpt2.py)  
> 2. Mã nguồn cải biên của tác giả: File [`GPT2SP.py`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py) trong Replication Package.  
> **Chương đối ứng trong bài báo:** Section 3: *The GPT2SP Architecture* (Trang 3 – 5, IEEE TSE 2023).

---

## 🎯 1. ĐẶT VẤN ĐỀ: NGUỒN GỐC MÃ NGUỒN `GPT2SP.py` THỰC SỰ TỪ ĐÂU RA?

Khi tiếp cận bài báo *"GPT2SP: Software Story Point Estimation with Generative Pre-trained Transformer 2"*, nhiều nhà nghiên cứu lầm tưởng rằng nhóm tác giả đã tự thiết kế và lập trình kiến trúc `GPT2SP` hoàn toàn mới từ con số 0 (`from scratch`) bằng PyTorch.

Tuy nhiên, khi đối soát trực tiếp mã nguồn trong kho lưu trữ GitHub của bài báo, **sự thật công nghệ là:**
> Nhóm tác giả đã **sao chép nguyên mẫu (fork / copy-paste)** lớp `GPT2ForSequenceClassification` từ thư viện mã nguồn mở tiêu chuẩn **Hugging Face Transformers**, sau đó chèn thêm một số tầng và tinh chỉnh lại một vài dòng lệnh phục vụ cho bài toán ước lượng Story Point.

Những "dấu vết" kỹ thuật chứng minh sự kế thừa nguyên khối này bao gồm:
1. **Biến `_keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]`**: Đây là khai báo đặc trưng của Hugging Face để triệt tiêu cảnh báo rác khi nạp checkpoint `gpt2`.
2. **Sử dụng biến `self.num_labels = config.num_labels`**: Mô hình không gán cứng số `1` mà vẫn giữ nguyên biến số của Hugging Face.
3. **Sự tồn tại của nhánh `else: loss_fct = CrossEntropyLoss()`**: Dù bài toán của tác giả là hồi quy đơn biến (Regression với `num_labels = 1`), nhánh mã nguồn phân loại đa lớp của Hugging Face vẫn nằm nguyên trong code mà không hề bị xóa!
4. **Đóng gói đầu ra qua lớp `SequenceClassifierOutputWithPast`**: Chuẩn dữ liệu trả về đặc thù của hệ sinh thái Hugging Face.

Tài liệu này sẽ giải phẫu chi tiết: **Hugging Face nguyên bản thiết kế lớp này như thế nào**, và **nhóm tác giả GPT2SP đã can thiệp, sửa đổi những gì?**

---

## 🏛️ 2. GIẢI PHẪU LỚP CHUẨN CỦA HUGGING FACE: `GPT2ForSequenceClassification`

Trong hệ sinh thái Hugging Face, mô hình ngôn ngữ gốc GPT-2 (`GPT2LMHeadModel`) được huấn luyện trước nhằm mục đích **sinh từ tiếp theo (Autoregressive Generation)** với đầu ra là phân phối từ vựng $50.257$ chiều. 

Để biến một mô hình sinh ngôn ngữ thành một mô hình làm nhiệm vụ ở cấp độ câu/chuỗi (như phân tích cảm xúc, phân loại chủ đề, hoặc hồi quy độ tương đồng), Hugging Face đã tạo ra lớp `GPT2ForSequenceClassification`.

### 2.1. Thiết kế nguyên mẫu trong Hugging Face

Dưới đây là cấu trúc tối giản của lớp chuẩn từ thư viện Hugging Face `transformers`:

```python
# --- TRÍCH XUẤT TỪ HUGGING FACE TRANSFORMERS ---
class GPT2ForSequenceClassification(GPT2PreTrainedModel):
    _keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        # Hugging Face dùng trực tiếp một tầng Linear từ 768 -> num_labels
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)

        self.init_weights()
```

### 2.2. Khả năng đa nhiệm "3 trong 1" của Hugging Face

Hugging Face thiết kế lớp này theo phong cách **khung tổng quát (Generic Framework)**. Cùng một lớp mã nguồn, nó có thể tự động thích ứng với cả 3 bài toán chỉ thông qua tham số `config.num_labels`:

```text
                               ┌───> [num_labels = 1] ───> Bài toán HỒI QUY (Regression)
                               │                           Hàm mất mát mặc định: MSELoss()
                               │
[config.num_labels] ───────────┼───> [num_labels = 2] ───> PHÂN LOẠI NHỊ PHÂN (Binary Classification)
                               │                           Hàm mất mát: CrossEntropyLoss()
                               │
                               └───> [num_labels > 2] ───> PHÂN LOẠI ĐA LỚP (Multi-class Classification)
                                                           Hàm mất mát: CrossEntropyLoss()
```

### 2.3. Cơ chế Last Token Pooling nguyên bản của Hugging Face

Vì GPT-2 sử dụng mặt nạ nhân quả (**Causal Masking**), token ở vị trí thứ $t$ chỉ có thể chú ý (*attend*) đến các token từ $1$ đến $t$. Do đó, token cuối cùng trong chuỗi là vị trí duy nhất gom trọn ngữ cảnh của toàn bộ câu. 

Hugging Face xử lý việc trích xuất token này trong hàm `forward()` như sau:

```python
# 1. Trích xuất hidden_states tầng cuối: [batch_size, sequence_length, 768]
hidden_states = transformer_outputs[0]

# 2. Chiếu trực tiếp qua tầng score: [batch_size, sequence_length, num_labels]
logits = self.score(hidden_states)

# 3. Tìm vị trí của token thực sự cuối cùng (loại trừ các token đệm [PAD])
if self.config.pad_token_id is None:
    sequence_lengths = -1
else:
    if input_ids is not None:
        # Đếm số lượng token khác với pad_token_id, trừ 1 để ra index
        sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
    else:
        sequence_lengths = -1

# 4. Lấy logits tại đúng vị trí token cuối cùng
pooled_logits = logits[range(batch_size), sequence_lengths]
```

---

## 🛠️ 3. CÁCH GPT2SP CẢI BIÊN (ADAPTATION): 3 THAY ĐỔI & 2 DI SẢN SÓT LẠI

Nhóm tác giả GPT2SP đã lấy file mã nguồn trên của Hugging Face và thực hiện các điều chỉnh kỹ thuật để chuyển đổi nó thành công cụ dự báo Story Point.

```text
[Hugging Face Gốc]                                            [GPT2SP Cải Biên]
------------------                                            -----------------
Vector 768 chiều                                              Vector 768 chiều
       │                                                             │
       │                                                             ▼
       │                                                      self.dense1: 768 -> 3072
       │                                                             │
       │                                                             ▼
       │                                                      self.dense2: 3072 -> 768
       ▼                                                             │
self.score: 768 -> num_labels                                        ▼
       │                                                      self.score: 768 -> num_labels
       ▼                                                             │
Hàm Loss: MSELoss() (L2)                                             ▼
                                                              Hàm Loss: nn.L1Loss() (L1/MAE)
```

### 🔄 3.1. Ba điểm thay đổi kỹ thuật then chốt

#### Điểm 1: Chèn thêm 2 tầng `dense1` và `dense2` trước `score`
* **Trong Hugging Face:** Vector 768 chiều được đưa thẳng vào `self.score` ($768 \rightarrow \text{num\_labels}$).
* **Trong GPT2SP:** Tác giả chèn thêm một mạng MLP thu phóng kích thước:
  ```python
  self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)  # 768 -> 3072
  self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)  # 3072 -> 768
  self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)      # 768 -> num_labels
  ```
* **Phản biện học thuật (Critical Discrepancy):**  
  Trong bài báo công bố trên IEEE TSE 2023 (Mục 3.3, Trang 4), tác giả tuyên bố đây là một mạng **MLP 2 tầng có hàm kích hoạt phi tuyến GELU**. Tuy nhiên, trong mã nguồn thực tế ở file `GPT2SP.py`, tác giả **quên không gọi hàm kích hoạt** giữa 2 tầng:
  ```python
  # Trong forward() của GPT2SP.py:
  hidden_states = self.dense1(hidden_states)
  hidden_states = self.dense2(hidden_states) # Không có nn.functional.gelu()!
  ```
  Về mặt đại số tuyến tính, nhân hai ma trận liên tiếp mà không có phi tuyến tương đương với một phép nhân ma trận đơn lẻ:
  $$W_{\text{eff}} = W_2 \times W_1 \in \mathbb{R}^{768 \times 768}$$

#### Điểm 2: Thay đổi Hàm Mất mát từ MSE ($L_2$) sang MAE ($L_1$)
* **Trong Hugging Face:** Nhánh hồi quy mặc định tính theo Mean Squared Error:
  ```python
  loss_fct = MSELoss()
  loss = loss_fct(pooled_logits.view(-1), labels.view(-1))
  ```
* **Trong GPT2SP:** Tác giả đổi sang tính bằng Sai số tuyệt đối ($L_1$ Loss / MAE):
  ```python
  if self.num_labels == 1:
      # We are doing regression
      loss_fct = nn.L1Loss()
      loss = loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))
  ```
* **Lý do toán học:** Phân phối Story Point trong các dự án Jira bị lệch phải rất mạnh (nhiều task 1, 2, 3 nhưng có task 40, 100). Đạo hàm của hàm bậc hai $L_2$ tỷ lệ thuận với sai số khiến gradient bùng nổ khi gặp ngoại lai. Ngược lại, đạo hàm của $L_1$ luôn là $\pm 1$, giúp mô hình hội tụ ổn định và kháng điểm ngoại lai (*robust to outliers*).

#### Điểm 3: Tách biệt cấu hình điều khiển (`GPT2Config`)
Trong file huấn luyện `run_all.py` hoặc `data_processing.py`, tác giả truyền cấu hình điều khiển vào mô hình:
```python
config = GPT2Config.from_pretrained(
    'gpt2',
    num_labels=1,          # Ép mô hình chỉ dự báo 1 số thực duy nhất (Regression)
    pad_token_id=50257     # Gán token EOS (<|endoftext|>) làm token đệm PAD
)
MODEL = GPT2SP.from_pretrained('gpt2', config=config)
```

---

### 🏛️ 3.2. Hai "di sản" còn sót lại chứng minh nguồn gốc copy-paste

#### Di sản 1: Nhánh mã nguồn chết `CrossEntropyLoss()`
Trong hàm `forward()` của file `GPT2SP.py`, chúng ta thấy khối code:
```python
        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = nn.L1Loss()
                loss = loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(pooled_logits.view(-1, self.num_labels), labels.view(-1))
```
* Vì tác giả luôn khởi tạo `num_labels = 1` trong toàn bộ bài báo và toàn bộ thực nghiệm, điều kiện `self.num_labels == 1` luôn luôn đúng (`True`).
* Nhánh `else: loss_fct = CrossEntropyLoss()` **không bao giờ được thực thi một lần nào** trong suốt toàn bộ nghiên cứu! Nó tồn tại đơn giản vì tác giả sao chép nguyên mẫu từ Hugging Face và không xóa đoạn code thừa.

#### Di sản 2: Khai báo `_keys_to_ignore_on_load_missing`
```python
_keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]
```
* Trong GPT-2 nguyên bản, checkpoint 117M tham số tải từ OpenAI có chứa ma trận `lm_head.weight` ($768 \times 50.257$).
* Khi kế thừa `GPT2PreTrainedModel` và gọi `from_pretrained('gpt2')`, PyTorch kiểm tra các trọng số trong checkpoint so với các tầng được khai báo trong class. Nếu không khai báo `_keys_to_ignore_on_load_missing`, PyTorch sẽ in ra cảnh báo đỏ:
  `RuntimeError: Missing key(s) in state_dict: "lm_head.weight"`.
* Bằng cách giữ nguyên danh sách bỏ qua này của Hugging Face, mô hình âm thầm bỏ qua 38,5 triệu tham số của `lm_head` mà không gây lỗi runtime.

---

## 📊 4. BẢNG SO SÁNH ĐỐI CHIẾU TRỰC DIỆN (SIDE-BY-SIDE DIFF)

Bảng tổng hợp chi tiết sự khác biệt từng dòng giữa nguyên mẫu Hugging Face và bản cải biên GPT2SP:

| Tiêu chí kỹ thuật | Hugging Face Nguyên Bản (`GPT2ForSequenceClassification`) | Bản Cải Biên GPT2SP (`GPT2SP.py`) | Ý nghĩa và Tác động Kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Lớp cơ sở kế thừa** | `GPT2PreTrainedModel` | `GPT2PreTrainedModel` | Giữ nguyên để tận dụng cơ chế tải trọng số tự động `from_pretrained('gpt2')`. |
| **Phần thân Backbone** | `self.transformer = GPT2Model(config)` | `self.transformer = GPT2Model(config)` | 12 khối Transformer Decoders (117M params) giữ nguyên $100\%$. |
| **Tầng trung gian MLP** | **Không có** (Đi thẳng từ 768 vào tầng output) | Có 2 tầng `dense1` ($768 \rightarrow 3072$) và `dense2` ($3072 \rightarrow 768$) | Nhằm tăng tham số học đặc trưng, nhưng thiếu kích hoạt phi tuyến trong code thực tế. |
| **Tầng điểm số cuối** | `nn.Linear(768, num_labels, bias=False)` | `nn.Linear(768, num_labels, bias=False)` | Chiếu vector ngữ cảnh thành số chiều mong muốn. |
| **Số nhãn cấu hình** | Linh hoạt: $1, 2, \dots, C$ tùy bài toán | Cố định qua config: `num_labels = 1` | Biến GPT-2 thành mô hình Hồi quy đơn biến (Story Point). |
| **Thuật toán Pooling** | Last Token Pooling (tìm vị trí token thật cuối cùng) | Last Token Pooling (sao chép nguyên mẫu logic) | Bắt buộc đối với kiến trúc Causal Mask để gom đủ ngữ cảnh User Story. |
| **Hàm mất mát hồi quy** | `MSELoss()` (Sai số toàn phương trung bình - $L_2$) | `nn.L1Loss()` (Sai số tuyệt đối trung bình - $L_1$) | Tránh bùng nổ gradient khi gặp task ngoại lai trong dữ liệu Jira. |
| **Nhánh phân loại thừa** | Đang được sử dụng cho phân loại | **Mã chết (Dead Code)**, không bao giờ chạy | Dấu tích còn lại của việc copy-paste từ Hugging Face. |

---

## 💡 5. TẠI SAO HUGGING FACE DÙNG `config.num_labels` MÀ KHÔNG GÁN CỨNG SỐ 1?

Nhiều lập trình viên khi đọc code đặt câu hỏi: *"Nếu chỉ làm bài toán hồi quy ước lượng Story Point (chắc chắn luôn ra 1 con số), tại sao không viết cứng `self.num_labels = 1` hoặc `self.score = nn.Linear(768, 1)` cho gọn?"*

Việc sử dụng đối tượng cấu hình `config` tuân thủ các nguyên lý thiết kế công nghiệp sau:

### 1. Nguyên lý Tách biệt Kiến trúc và Siêu tham số (Decoupling)
Mô hình toán học (`GPT2SP.py`) là một bản thiết kế chung, còn bài toán thực thi cụ thể do `GPT2Config` kiểm soát. Khi đóng gói mô hình:
```python
# Lưu mô hình:
model.save_pretrained("./my_story_point_model")
```
Hệ thống sẽ tự sinh ra file `config.json` chứa:
```json
{
  "model_type": "gpt2",
  "n_embd": 768,
  "n_layer": 12,
  "n_head": 12,
  "num_labels": 1,
  "pad_token_id": 50257
}
```
Nhờ vậy, khi bất kỳ ai tải lại mô hình:
```python
model = AutoModelForSequenceClassification.from_pretrained("./my_story_point_model")
```
PyTorch sẽ đọc file `config.json` và biết chính xác mô hình có đúng 1 đầu ra hồi quy, không lo bị lỗi lệch số chiều hay thiếu trọng số.

### 2. Mở rộng linh hoạt cho các bài toán Agile khác
Dù tác giả bài báo chọn cách tiếp cận Story Point là **Hồi quy điểm liên tục** ($\hat{y} \in \mathbb{R}^+$), trong cộng đồng nghiên cứu Kỹ nghệ phần mềm (SE) có hai trường phái lớn:
1. **Trường phái Hồi quy (Regression):** Coi Story Point là số thực liên tục $\rightarrow$ `num_labels = 1`.
2. **Trường phái Phân loại đa lớp (Multi-class Classification):** Coi Story Point là các nhãn phân loại rời rạc theo thang Fibonacci chuẩn Scrum $\{1, 2, 3, 5, 8, 13, 20\}$ $\rightarrow$ Cần `num_labels = 7`. Hoặc phân loại theo cỡ áo T-shirt $\{S, M, L, XL\}$ $\rightarrow$ Cần `num_labels = 4`.

Nhờ việc giữ nguyên biến `config.num_labels`, bất kỳ nhà nghiên cứu nào sau này cũng có thể tái sử dụng file `GPT2SP.py` cho bài toán phân loại đa lớp chỉ bằng cách truyền `num_labels = 7` vào `GPT2Config`, tầng `self.score` sẽ tự động thành `nn.Linear(768, 7)` và hàm mất mát tự động chuyển sang `CrossEntropyLoss()` mà không phải sửa một dòng mã nguồn nào!

---

## 🎯 6. BÀI HỌC ĐÚC RÚT CHO ĐỀ TÀI NGHIÊN CỨU CỦA NHÓM 3

Từ việc bóc tách cội nguồn mã nguồn Hugging Face và cách GPT2SP cải biên, Nhóm 3 rút ra 3 bài học thực tiễn then chốt cho đề tài nghiên cứu:

1. **Hiểu rõ giới hạn để không "thần thánh hóa" mô hình:**  
   GPT2SP không phải là một phát minh kiến trúc hoàn toàn mới, mà là một sự tinh chỉnh nhỏ (*minor adaptation*) trên lớp phân loại chuỗi có sẵn của Hugging Face. Việc tác giả bỏ quên hàm kích hoạt phi tuyến giữa `dense1` và `dense2` cho thấy khoảng cách giữa bài báo lý thuyết và mã nguồn thực tế.
2. **Cơ hội tối ưu hóa kiến trúc sạch hơn:**  
   Trong các thử nghiệm đối chứng của Nhóm 3:
   - Nếu áp dụng mô hình ngôn ngữ 2 chiều (Bidirectional) như **RoBERTa** hay **Sentence-BERT (SBERT)**, ta có thể dùng `[CLS]` token hoặc Mean Pooling thay vì bị ràng buộc vào Last Token Pooling của GPT-2.
   - Thử nghiệm cả 2 hướng tiếp cận: Hồi quy $L_1$ Loss (`num_labels = 1`) và Phân loại đa lớp Cross-Entropy (`num_labels = K` theo dãy Fibonacci) một cách bài bản.
3. **Tránh bẫy Data Leakage mà GPT2SP mắc phải:**  
   Mặc dù tầng phân loại và hàm mất mát của GPT2SP được thiết kế hợp lý, điểm yếu chí tử của nghiên cứu gốc nằm ở khâu **dữ liệu đầu vào**: sử dụng văn bản Jira sau planning và bỏ qua `Description`. Nhóm 3 tập trung khắc phục triệt để vấn đề này bằng việc phục hồi dữ liệu tại mốc thời gian thực `SP_Estimation_Date`.

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 💻 [File mã nguồn hoàn chỉnh: 00_full_source_code.md](../code/00_full_source_code.md)
* 📖 [Giải thích từng dòng code kiến trúc: 01_architecture_code_explanation.md](../code/01_architecture_code_explanation.md)
* 🧠 [Tại sao Last Token Pooling chứ không phải Mean hay First: 13_why_last_token_pooling_not_first_or_mean.md](13_why_last_token_pooling_not_first_or_mean.md)
* 🧠 [Giải phẫu MLP Regressor Head: 14_why_mlp_regressor_head_architecture.md](14_why_mlp_regressor_head_architecture.md)
* 🧠 [Phân tích kho mã nguồn awsm-research/gpt2sp: 15_awsm_research_gpt2sp_repository_analysis.md](15_awsm_research_gpt2sp_repository_analysis.md)
* 📑 [Danh mục toàn bộ bài phân tích phản biện: README.md](README.md)
