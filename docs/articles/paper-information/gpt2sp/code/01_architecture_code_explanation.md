# 📖 GIẢI THÍCH CHI TIẾT TỪNG DÒNG MÃ NGUỒN KIẾN TRÚC MÔ HÌNH (`GPT2SP.py`)
## ĐỐI SOÁT TỪNG BIẾN, TỪNG DÒNG CODE VÀ BẢN CHẤT LOGIC TOÁN HỌC BÊN DƯỚI (SECTION 3 THE GPT2SP ARCHITECTURE)

> **Mã nguồn phân tích:** File [`GPT2SP.py`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py) trong Replication Package.  
> **Chương đối ứng trong bài báo gốc:** **Section 3: The GPT2SP Architecture** (Trang 3 – 5, IEEE TSE 2023).  
> **Tôn chỉ phân tích:** Bóc tách chi tiết từng dòng lệnh, giải mã bản chất các tham số nhập vào, cấu trúc trả về của `transformer_outputs`, lý do cắt bỏ `lm_head.weight`, và cơ chế tính toán thực tế bên trong PyTorch.

---

## 🧭 1. LOGIC THIẾT KẾ CỐT LÕI: TỪ GENERATIVE LLM SANG REGRESSION MODEL

Trong bài toán xử lý ngôn ngữ tự nhiên thông thường, mô hình GPT-2 được sinh ra để làm nhiệm vụ **Sinh văn bản tự hồi quy (Autoregressive Causal Language Modeling)**: từ chuỗi token đầu vào $x_1, x_2, \dots, x_t$, mô hình dự đoán xác suất token tiếp theo $x_{t+1}$ thông qua tầng phân loại ngôn ngữ `lm_head` có kích thước ma trận `[768, 50257]`.

Tuy nhiên, bài toán ước lượng Story Point trong Agile là một **bài toán hồi quy số thực (Continuous Regression)**:
$$\text{Input: Văn bản User Story} \longrightarrow \text{Output: Một số thực duy nhất } \hat{y} \in \mathbb{R}^+$$

Để biến GPT-2 thành GPT2SP, tác giả thực hiện 3 bước logic can thiệp vào mã nguồn:
1. **Phẫu thuật loại bỏ đầu sinh từ vựng (`lm_head`):** Triệt tiêu 38,5 triệu tham số sinh từ không cần thiết.
2. **Kế thừa 12 khối giải mã Transformer Decoders:** Sử dụng lại toàn bộ tri thức biểu diễn ngôn ngữ đã được tiền huấn luyện trên WebText.
3. **Gắn thêm đầu hồi quy MLP Regressor Head & Cơ chế Last Token Pooling:** Chuyển hóa vector ẩn của token cuối cùng thành một con số dự đoán điểm nỗ lực.

---

## 🔍 2. GIẢI PHẪU CHI TIẾT TỪNG DÒNG LỆNH TRONG `GPT2SP.py`

### 2.1. Phần 1: Khai báo thư viện và định nghĩa lớp

```python
from transformers.modeling_outputs import SequenceClassifierOutputWithPast
import torch.nn as nn
from transformers import GPT2Model, GPT2PreTrainedModel
import torch
```

* `from transformers.modeling_outputs import SequenceClassifierOutputWithPast`:
  * **Ý nghĩa:** Nạp lớp dữ liệu trả về chuẩn (Data Class) của Hugging Face cho các bài toán phân loại / hồi quy chuỗi.
  * **Tại sao cần?** Giúp mô hình đóng gói kết quả đầu ra thành một đối tượng đồng nhất chứa `loss`, `logits`, `hidden_states`, và `attentions` tương thích với toàn bộ hệ sinh thái Hugging Face (như Trainer, Pipelines, hay Transformers-Interpret).
* `from transformers import GPT2Model, GPT2PreTrainedModel`:
  * `GPT2Model`: Lớp chứa phần thân chính (backbone) của GPT-2, gồm tầng nhúng từ ngữ, nhúng vị trí và 12 khối Transformer Decoders (nhưng **không bao gồm** tầng sinh từ vựng `lm_head`).
  * `GPT2PreTrainedModel`: Lớp cơ sở trừu tượng cung cấp các tiện ích nạp trọng số tiền huấn luyện (`from_pretrained`), lưu mô hình (`save_pretrained`) và quản lý cấu hình kiến trúc (`config`).

---

### 2.2. Phần 2: Khởi tạo mô hình và loại bỏ trọng số thừa (`__init__`)

```python
class GPT2ForSequenceClassification(GPT2PreTrainedModel):
    _keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)

        self.init_weights()

        # Model parallel
        self.model_parallel = False
        self.device_map = None
```

#### 💡 Bóc tách từng dòng code:

1. `_keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]`:
   * **`lm_head.weight` là cung cấp cái gì trong GPT-2 gốc?**  
     Trong kiến trúc nguyên bản của OpenAI GPT-2, `lm_head` là một tầng tuyến tính `nn.Linear(768, 50257)` có trọng số là ma trận $W_{\text{lm}} \in \mathbb{R}^{768 \times 50.257}$ (thường dùng chung trọng số với ma trận nhúng từ $W_{te}$ qua kỹ thuật Weight Tying). Nhiệm vụ của `lm_head.weight` là nhận vector ẩn 768 chiều từ decoder cuối cùng và nhân với từng vector trong 50.257 từ vựng để tính ra 50.257 điểm số logits. Sau đó qua hàm Softmax sẽ cho ra xác suất từ tiếp theo:
     $$P(w_{t+1} \mid w_{1:t}) = \text{Softmax}(h_t \cdot W_{\text{lm}})$$
   * **Vì sao trong GPT2SP BẮT BUỘC PHẢI BỎ NÓ?**  
     Bài toán ước lượng Story Point **không phải là bài toán sinh văn bản** (chúng ta không cần mô hình viết tiếp User Story), mà là bài toán **dự đoán một giá trị độ khó thực $\hat{y} \in \mathbb{R}^+$**. Nếu giữ lại `lm_head.weight`, mô hình sẽ lãng phí hơn 38,5 triệu tham số (chiếm gần 1/3 tổng số tham số của GPT-2 Small) vào một việc hoàn toàn vô nghĩa. Do đó, tác giả phẫu thuật cắt bỏ nó và khai báo `_keys_to_ignore_on_load_missing` để khi gọi lệnh `from_pretrained('gpt2')`, PyTorch hiểu rằng việc thiếu ma trận `lm_head.weight` là chủ đích thiết kế, không báo lỗi thiếu trọng số.
   * `r"h\.\d+\.attn\.masked_bias"`: Bỏ qua các giá trị mặt nạ đệm chú ý tĩnh trong các phiên bản Hugging Face cũ để tránh cảnh báo rác.
2. `self.num_labels = config.num_labels`:
   * **Bản chất kỹ thuật:** Lấy số lượng nhãn/đầu ra mong muốn từ đối tượng cấu hình `config`.
   * **Tại sao không gán cứng luôn `self.num_labels = 1` mà phải dùng biến `config.num_labels`?**
     * **1. Nguồn gốc mã nguồn (Thừa hưởng từ Hugging Face):** Nhóm tác giả bài báo sao chép và cải biên từ lớp chuẩn `GPT2ForSequenceClassification` của thư viện Hugging Face. Lớp chuẩn này được thiết kế để giải quyết cả 3 bài toán:
       * **Hồi quy (Regression):** `num_labels = 1` $\rightarrow$ Tầng output ra 1 số thực duy nhất, dùng hàm mất mát L1 hoặc MSE.
       * **Phân loại nhị phân (Binary Classification):** `num_labels = 2` $\rightarrow$ Tầng output ra 2 logits, dùng Cross-Entropy.
       * **Phân loại đa lớp (Multi-class Classification):** `num_labels = C` $\rightarrow$ Tầng output ra $C$ logits.
       Vì thế trong code có cả đoạn `if self.num_labels == 1: loss_fct = nn.L1Loss() else: loss_fct = CrossEntropyLoss()`.
     * **2. Nguyên lý Đóng gói & Tách biệt Cấu hình (Decoupling Architecture & Config):** Theo chuẩn kiến trúc của Hugging Face (`PreTrainedModel`), mã nguồn mô hình **tuyệt đối không được hardcode số chiều**. Tham số này được truyền từ bên ngoài vào qua lệnh cấu hình:
       ```python
       config = GPT2Config.from_pretrained('gpt2', num_labels=1, pad_token_id=50257)
       ```
       Khi lưu mô hình (`model.save_pretrained()`), PyTorch sẽ ghi `num_labels: 1` vào file `config.json`. Nhờ vậy, khi ai đó nạp lại mô hình đã huấn luyện, hệ thống tự biết mô hình này có 1 đầu ra hồi quy mà không sợ xung đột kích thước ma trận.
     * **3. Khả năng mở rộng cho các nghiên cứu Agile khác:** Trong lĩnh vực Story Point, bên cạnh bài toán *Hồi quy liên tục* (Continuous Regression: điểm số là số thực bất kỳ), nhiều nghiên cứu coi Story Point là bài toán *Phân loại đa lớp* theo thang Fibonacci rời rạc $\{1, 2, 3, 5, 8, 13, 20\}$ (`num_labels = 7`) hoặc cỡ áo T-shirt $\{S, M, L, XL\}$ (`num_labels = 4`). Việc giữ nguyên `config.num_labels` cho phép tái sử dụng toàn bộ khung mô hình này cho bài toán phân loại mà không phải sửa lại code bên trong lớp.
3. `self.transformer = GPT2Model(config)`:
   * Khởi tạo phần thân 12 khối Transformer Decoders kế thừa toàn bộ tri thức biểu diễn ngôn ngữ đã học từ WebText.
4. `self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)`:
   * `config.n_embd = 768`. Tầng này nhân vector 768 chiều với ma trận trọng số $W_1 \in \mathbb{R}^{768 \times 3072}$ để phóng đại không gian biểu diễn lên **4 lần** (3.072 chiều).
   * **Tại sao phóng đại 4 lần?** Đây là thiết kế phỏng theo tầng FFN của Transformer. Không gian chiều cao 3.072 chiều giúp các đặc trưng ngữ nghĩa phức tạp phân tách tuyến tính tốt hơn (*Cover's Theorem*).
   * `bias=False`: Bỏ hệ số tự do bias để giảm bớt số tham số cần cập nhật, chống hiện tượng học vẹt (overfitting) trên tập Jira nhỏ.
5. `self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)`:
   * Tầng thu hẹp kích thước: nhân vector 3.072 chiều với ma trận trọng số $W_2 \in \mathbb{R}^{3072 \times 768}$ để nén thông tin trở về chiều chuẩn 768.
6. `self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)`:
   * Tầng tính điểm cuối cùng: nhân ma trận $W_3 \in \mathbb{R}^{768 \times 1}$ để ánh xạ vector ngữ cảnh 768 chiều thành 1 số thực duy nhất đại diện cho điểm Story Point dự báo.
7. `self.init_weights()`:
   * Khởi tạo các trọng số mới (`dense1`, `dense2`, `score`) theo phân phối chuẩn cụt (*Truncated Normal Distribution*) với độ lệch chuẩn $\sigma = 0.02$.

---

### 2.3. Phần 3: Khai báo tham số của hàm Lan truyền Xuôi (`forward`)

```python
    def forward(
        self,
        input_ids=None,
        past_key_values=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
```

#### 💡 Bóc tách chi tiết từng tham số đầu vào:
* `input_ids` (`torch.LongTensor`, kích thước `[batch_size, sequence_length]`):  
  Chuỗi các chỉ số ID của từ vựng sau khi đi qua BPE Tokenizer (ví dụ: `[40, 1101, 247, 50257, 50257]`).
* `attention_mask` (`torch.FloatTensor`, kích thước `[batch_size, sequence_length]`):  
  Mặt nạ nhị phân đánh dấu vị trí: giá trị `1` cho token thật cần tính toán, và `0` cho token đệm `[PAD]` cần bỏ qua trong Self-Attention.
* `labels` (`torch.FloatTensor` hoặc `torch.LongTensor`, kích thước `[batch_size]`):  
  Nhãn mục tiêu thực tế (Ground-Truth Story Point) dùng để tính toán hàm mất mát trong quá trình huấn luyện.
* `past_key_values`: Bộ nhớ đệm KV Cache lưu các vector Key/Value từ các bước trước (dùng trong sinh từ tuần tự, trong bài toán hồi quy GPT2SP không dùng).
* `position_ids`: Chỉ số vị trí thứ tự của token trong câu ($0, 1, 2, \dots$). Nếu truyền `None`, mô hình tự động sinh từ $0$ đến $\text{len} - 1$.
* `inputs_embeds`: Truyền trực tiếp vector nhúng thay vì truyền ID từ vựng `input_ids` (hữu ích khi làm giải thích mô hình XAI bằng Integrated Gradients).
* `return_dict`: Cờ boolean quy định kết quả trả về là đối tượng chuẩn `SequenceClassifierOutputWithPast` (`True`) hay là dạng tuple thuần túy (`False`).

---

### 2.4. Phần 4: Thực thi Transformer Backbone và Cấu trúc của `transformer_outputs`

```python
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        transformer_outputs = self.transformer(
            input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        hidden_states = transformer_outputs[0]
```

#### 💡 `transformer_outputs` bao gồm những gì bên trong?
Khi gọi `self.transformer(...)`, dữ liệu đầu vào chạy qua tầng Word & Positional Embedding, sau đó lần lượt xuyên qua cả 12 khối Transformer Decoders. Đối tượng `transformer_outputs` trả về là một `BaseModelOutputWithPastAndCrossAttentions` gồm các thành phần sau:

| Chỉ mục / Thuộc tính | Tên trường | Kiểu dữ liệu & Kích thước Tensor | Ý nghĩa bản chất trong Transformer |
| :---: | :--- | :--- | :--- |
| **`[0]`** | **`last_hidden_state`** | `Tensor [batch_size, sequence_length, 768]` | **Trạng thái ẩn ở tầng cuối cùng (Khối thứ 12):** Đây là thành phần quan trọng nhất! Mỗi token trong câu lúc này sở hữu một vector 768 chiều mang đầy đủ ngữ cảnh phong phú của câu. |
| **`[1]`** | `past_key_values` | `Tuple` 12 phần tử (tương ứng 12 tầng) | Lưu các tensor Key và Value của từng khối Attention để phục vụ suy luận nhanh (trong GPT2SP không sử dụng). |
| **`[2]`** *(nếu bật)* | `hidden_states` | `Tuple` 13 tensor `[batch_size, seq_len, 768]` | Toàn bộ vector trạng thái ẩn từ tầng Embedding ban đầu (tầng 0) cho đến hết cả 12 khối Decoders. |
| **`[3]`** *(nếu bật)* | `attentions` | `Tuple` 12 tensor `[batch, 12, seq_len, seq_len]` | Ma trận trọng số Attention Weights của 12 đầu tại 12 khối (được trích xuất để làm XAI trong Chương 6). |

👉 Do mục tiêu của mô hình là lấy vector đặc trưng cuối cùng để ước lượng Story Point, dòng lệnh:
```python
hidden_states = transformer_outputs[0]
```
đã trích xuất chính xác tensor `last_hidden_state` kích thước `[batch_size, sequence_length, 768]`.

---

### 2.5. Phần 5: Tính toán qua MLP Regressor Head

```python
        # MLP Layer
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        
        logits = self.score(hidden_states)
```

#### 💡 Bóc tách từng bước biến đổi hình dạng Tensor:
1. `hidden_states = self.dense1(hidden_states)`:
   * **Phép toán:** Nhân ma trận giữa `hidden_states` `[B, S, 768]` và trọng số $W_1^T$ `[768, 3072]`.
   * **Hình dạng mới:** `[batch_size, sequence_length, 3072]`.
2. `hidden_states = self.dense2(hidden_states)`:
   * **Phép toán:** Nhân ma trận giữa tensor trên `[B, S, 3072]` và trọng số $W_2^T$ `[3072, 768]`.
   * **Hình dạng mới:** `[batch_size, sequence_length, 768]`.
   * ⚠️ **Phát hiện phản biện:** Tác giả không chèn hàm kích hoạt phi tuyến nào (như GELU hay ReLU) giữa `dense1` và `dense2`. Về mặt toán học:
     $$h_{\text{out}} = (h_{\text{in}} \cdot W_1) \cdot W_2 = h_{\text{in}} \cdot (W_1 \cdot W_2) = h_{\text{in}} \cdot W_{\text{eff}}$$
     Hai tầng Dense liên tiếp này tương đương với một tầng tuyến tính duy nhất $W_{\text{eff}} \in \mathbb{R}^{768 \times 768}$.
3. `logits = self.score(hidden_states)`:
   * **Phép toán:** Nhân ma trận giữa `[B, S, 768]` và trọng số $W_3^T$ `[768, 1]`.
   * **Hình dạng mới:** `[batch_size, sequence_length, 1]`. Tại mỗi vị trí token trong User Story đều có một điểm số cục bộ.

---

### 2.6. Phần 6: Cơ chế Last Token Pooling (Trích xuất điểm số đại diện chuỗi)

```python
        if input_ids is not None:
            batch_size, sequence_length = input_ids.shape[:2]
        else:
            batch_size, sequence_length = inputs_embeds.shape[:2]

        assert (
            self.config.pad_token_id is not None or batch_size == 1
        ), "Cannot handle batch sizes > 1 if no padding token is defined."
        if self.config.pad_token_id is None:
            sequence_lengths = -1
        else:
            if input_ids is not None:
                sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
            else:
                sequence_lengths = -1
                logger.warning(
                    f"{self.__class__.__name__} will not detect padding tokens in `inputs_embeds`. Results may be "
                    f"unexpected if using padding tokens in conjunction with `inputs_embeds.`"
                )

        pooled_logits = logits[range(batch_size), sequence_lengths]
```

#### 💡 Bóc tách logic từng dòng lệnh:
1. `batch_size, sequence_length = input_ids.shape[:2]`:
   * Lấy số lượng mẫu trong lô (`batch_size`) và độ dài chuỗi tối đa (`sequence_length`).
2. `torch.ne(input_ids, self.config.pad_token_id)`:
   * Hàm `torch.ne` (Not Equal) so sánh từng phần tử với ID của token `[PAD]` (trong code tác giả gán pad_token_id = 50257).
   * Trả về ma trận boolean: vị trí nào chứa từ thật trả về `True` (tương đương 1), vị trí nào là padding trả về `False` (0).
   * Ví dụ câu có 3 từ thật và 2 từ đệm: `[True, True, True, False, False]`.
3. `.sum(-1) - 1`:
   * `.sum(-1)`: Cộng dồn theo hàng ngang để đếm tổng số token có nghĩa thực tế (ví dụ: $3$).
   * `- 1`: Vì chỉ số mảng trong lập trình bắt đầu từ $0$, nên từ cuối cùng có nghĩa nằm ở chỉ số $3 - 1 = 2$.
   * Biến `sequence_lengths` lúc này chứa một vector 1 chiều lưu vị trí index của token cuối cùng cho từng mẫu trong batch.
4. `pooled_logits = logits[range(batch_size), sequence_lengths]`:
   * Thực hiện phép cắt lát tensor nhiều chiều: với mỗi hàng $i$ trong batch (`0 <= i < batch_size`), lấy giá trị tại cột `sequence_lengths[i]`.
   * **Kết quả:** `pooled_logits` có hình dạng `[batch_size, 1]` — chính là điểm Story Point dự đoán đại diện cho toàn bộ User Story.
   * **Bản chất kiến trúc:** Vì GPT-2 dùng mặt nạ nhân quả (Causal Masking), từ phía trước không nhìn thấy từ phía sau, do đó chỉ có token cuối cùng mới tổng hợp được tri thức của toàn bộ câu.

---

### 2.7. Phần 7: Tính toán Hàm Mất mát và Đóng gói Kết quả Đầu ra

```python
        loss = None
        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = nn.L1Loss()
                loss = loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(pooled_logits.view(-1, self.num_labels), labels.view(-1))

        if not return_dict:
            output = (pooled_logits,) + transformer_outputs[1:]
            return ((loss,) + output) if loss is not None else output

        return SequenceClassifierOutputWithPast(
            loss=loss,
            logits=pooled_logits,
            past_key_values=transformer_outputs.past_key_values,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
```

#### 💡 Bóc tách từng dòng code:
1. `if labels is not None:`:
   * Nếu có nhãn truyền vào (chế độ Training hoặc Evaluation), mô hình sẽ tự động tính hàm mất mát `loss`. Nếu không truyền nhãn (chế độ Inference / Production), `loss = None`.
2. `if self.num_labels == 1: loss_fct = nn.L1Loss()`:
   * **Tại sao tác giả chọn $L_1$ Loss (MAE)?**  
     Trong dữ liệu Jira, phần lớn User Story có điểm số nhỏ ($1, 2, 3, 5$), nhưng có những task ngoại lai cực lớn ($40, 100$). Hàm $L_2$ Loss ($(\hat{y} - y)^2$) có đạo hàm tỷ lệ thuận với độ lệch sai số, khi gặp ngoại lai gradient sẽ bùng nổ và làm hỏng toàn bộ các trọng số đã học. Hàm $L_1$ Loss ($|\hat{y} - y|$) có đạo hàm luôn là hằng số $\pm 1$, giúp quá trình cập nhật gradient cực kỳ ổn định và kháng ngoại lai.
3. `loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))`:
   * Dùng `.view(-1)` để kéo phẳng cả 2 tensor về vector 1 chiều có độ dài `[batch_size]` trước khi đưa vào hàm mất mát $L_1$.
4. `return SequenceClassifierOutputWithPast(...)`:
   * Đóng gói toàn bộ kết quả gồm giá trị mất mát `loss`, điểm số dự báo `logits`, bộ nhớ đệm `past_key_values`, trạng thái các tầng `hidden_states` và trọng số chú ý `attentions` vào đối tượng chuẩn, hoàn tất một chu trình lan truyền xuôi hoàn hảo.

---

## 📋 3. BẢNG TỔNG HỢP ÁNH XẠ TOÀN DIỆN: DÒNG CODE VS. BÀI BÁO GỐC

| Dòng code trong `GPT2SP.py` | Thành phần trong bài báo (IEEE TSE 2023) | Vai trò kỹ thuật & Bản chất toán học |
| :--- | :--- | :--- |
| `_keys_to_ignore_on_load_missing` | Bỏ qua `lm_head.weight` | Cắt bỏ 38,5 triệu tham số sinh từ, chuyển GPT-2 thành mô hình hồi quy. |
| `self.transformer = GPT2Model(config)` | 12 Blocks Transformer Decoders (Mục 3.2) | 12 tầng Masked Self-Attention biểu diễn ngữ cảnh User Story (117M params). |
| `self.dense1` & `self.dense2` | MLP Regressor Head (Mục 3.3) | Phóng đại $768 \rightarrow 3072 \rightarrow 768$ (thiếu phi tuyến trong code thực tế). |
| `self.score` | Regression Linear Score | Tích vô hướng rút gọn 768 chiều thành 1 số thực duy nhất $\hat{y}$. |
| `transformer_outputs[0]` | `last_hidden_state` từ Decoders | Tensor `[B, S, 768]` chứa biểu diễn ngữ cảnh ở tầng 12 của tất cả tokens. |
| `torch.ne(...).sum(-1) - 1` | Last Token Pooling Strategy (Mục 3.3) | Bắt vị trí token thật cuối cùng trước padding `[PAD]`. |
| `pooled_logits = logits[range, seq]` | Vector Token cuối cùng đại diện User Story | Token duy nhất gom trọn ngữ cảnh toàn câu do cơ chế Causal Mask. |
| `loss_fct = nn.L1Loss()` | L1 Loss Optimization (Mục 3.4) | Kháng ngoại lai, trực tiếp tối ưu hóa hàm mục tiêu MAE. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📜 [00_full_source_code.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/00_full_source_code.md): Toàn bộ mã nguồn gốc GPT2SP.
* 🔬 [02_training_pipeline_code_explanation.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/02_training_pipeline_code_explanation.md): Giải thích chi tiết mã nguồn pipeline huấn luyện và đánh giá thực nghiệm.
* ⚠️ [03_code_vs_paper_discrepancies.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/03_code_vs_paper_discrepancies.md): Mổ xẻ 4 điểm sai lệch cốt tử giữa code thực tế và bài báo.
* 🧠 [Chuyên mục Critical Thinking tổng quan](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/README.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
