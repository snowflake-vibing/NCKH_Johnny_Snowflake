# 📖 GIẢI THÍCH CHI TIẾT MÃ NGUỒN KIẾN TRÚC MÔ HÌNH (`GPT2SP.py`)
## ĐỐI SOÁT TỪNG DÒNG CODE VÀ BẢN CHẤT LOGIC ĐẰNG SAU KIẾN TRÚC

> **Mã nguồn phân tích:** File [`GPT2SP.py`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py) trong Replication Package.  
> **Chương đối ứng trong bài báo gốc:** **Section 3: The GPT2SP Architecture** (Trang 3 – 5, IEEE TSE 2023).

---

## 🧭 1. LOGIC THIẾT KẾ CỐT LÕI: TỪ GENERATIVE LLM SANG REGRESSION MODEL

Trong bài toán xử lý ngôn ngữ tự nhiên thông thường, mô hình GPT-2 được sinh ra để làm nhiệm vụ **Sinh văn bản tự hồi quy (Autoregressive Text Generation)**: từ chuỗi token đầu vào $x_1, x_2, \dots, x_t$, mô hình dự đoán xác suất token tiếp theo $x_{t+1}$ thông qua tầng phân loại ngôn ngữ `lm_head` có kích thước `[768, 50257]`.

Tuy nhiên, bài toán ước lượng Story Point trong Agile là một **bài toán hồi quy số thực (Continuous Regression)**:
$$\text{Input: Văn bản User Story} \longrightarrow \text{Output: Một số thực duy nhất } \hat{y} \in \mathbb{R}^+$$

Để biến GPT-2 thành GPT2SP, tác giả thực hiện 3 bước logic can thiệp vào mã nguồn:
1. **Phẫu thuật loại bỏ đầu sinh từ vựng (`lm_head`):** Triệt tiêu 38,5 triệu tham số sinh từ không cần thiết.
2. **Kế thừa 12 khối giải mã Transformer Decoders:** Sử dụng lại toàn bộ tri thức biểu diễn ngôn ngữ đã được tiền huấn luyện trên WebText.
3. **Gắn thêm đầu hồi quy MLP Regressor Head & Cơ chế Last Token Pooling:** Chuyển hóa vector ẩn của token cuối cùng thành một con số dự đoán điểm nỗ lực.

---

## 🔍 2. GIẢI PHẪU TỪNG DÒNG CODE VÀ LOGIC ĐẰNG SAU

### 2.1. Khởi tạo mô hình và loại bỏ trọng số thừa (`__init__`)

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
```

#### 💡 Logic đằng sau từng câu lệnh:
1. `class GPT2ForSequenceClassification(GPT2PreTrainedModel)`:
   * **Tại sao không viết `nn.Module` thuần?** Kế thừa `GPT2PreTrainedModel` cho phép mô hình tận dụng cơ chế `from_pretrained('gpt2')` của Hugging Face để tự động tải các checkpoint trọng số 117M tham số đã được huấn luyện sẵn, đồng thời hỗ trợ quản lý cấu hình `GPT2Config`.
2. `_keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]`:
   * **Bản chất logic:** Báo cho PyTorch biết khi tải trọng số GPT-2 chính thức từ Hugging Face Hub, nếu không thấy `lm_head.weight` thì **không được báo lỗi**. Vì GPT2SP đã cố tình vứt bỏ ma trận này để thay thế bằng đầu hồi quy.
3. `self.transformer = GPT2Model(config)`:
   * Giữ nguyên xương sống của GPT-2: Ma trận nhúng từ $W_{te}$ ($50.257 \times 768$), ma trận nhúng vị trí $W_{pe}$ ($1024 \times 768$) và 12 khối Transformer Decoders liên tiếp.
4. `self.dense1 = nn.Linear(768, 3072, bias=False)` & `self.dense2 = nn.Linear(3072, 768, bias=False)`:
   * **Tại sao lại phóng đại 4 lần (từ 768 lên 3072 rồi ép về 768)?**  
     Đây là thiết kế mô phỏng lại tầng Feed-Forward Network (FFN) kinh điển của Transformer. Theo lý thuyết bộ nhớ tri thức (*Key-Value Memory Theory*), việc chiếu vector biểu diễn lên không gian 3.072 chiều giúp các mẫu tổ hợp từ ngữ kỹ thuật phức tạp trong User Story phân tách tuyến tính tốt hơn trước khi cô đọng lại.
   * **Tại sao `bias=False`?** Việc bỏ toàn bộ hệ số điều chỉnh bias giúp giảm thiểu số lượng tham số tự do, hạn chế nguy cơ mạng nơ-ron học vẹt (overfitting) trên các bộ dữ liệu Jira vốn chỉ có vài ngàn mẫu.
5. `self.score = nn.Linear(768, 1, bias=False)`:
   * Vì `config.num_labels = 1`, tầng này thực hiện phép tích vô hướng giữa vector ngữ cảnh 768 chiều của User Story với 768 trọng số để sinh ra một giá trị scalar duy nhất: điểm Story Point dự báo.

---

### 2.2. Luồng tính toán lan truyền xuôi (`forward pass`)

```python
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
                
        # MLP Layer
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        
        logits = self.score(hidden_states)
```

#### 💡 Logic đằng sau từng câu lệnh:
1. `hidden_states = transformer_outputs[0]`:
   * Vector đầu ra từ khối Transformer Decoder thứ 12 có hình dạng tensor là `[batch_size, sequence_length, 768]`. Mỗi vị trí token trong câu hiện đang mang một vector 768 chiều đại diện cho ngữ cảnh của nó.
2. `hidden_states = self.dense1(hidden_states)` $\rightarrow$ `self.dense2(hidden_states)`:
   * Tensor được chiếu qua `dense1` thành `[batch_size, sequence_length, 3072]`.
   * Sau đó chiếu qua `dense2` trở lại `[batch_size, sequence_length, 768]`.
   * **Phát hiện logic bất thường trong code của tác giả:** Ở đây tác giả thực hiện hai phép nhân ma trận liên tiếp mà **hoàn toàn không có hàm kích hoạt phi tuyến (như GELU hay ReLU) ở giữa**. Về mặt toán học:
     $$W_{\text{eff}} = W_2 \times W_1$$
     Hai tầng tuyến tính ghép liền nhau thực chất chỉ tương đương với một tầng tuyến tính đơn cấp! Điều này cho thấy kiến trúc MLP Head trong mã nguồn thực tế đơn giản và thô sơ hơn rất nhiều so với mô tả lý thuyết trong bài báo.
3. `logits = self.score(hidden_states)`:
   * Đưa tensor về kích thước `[batch_size, sequence_length, 1]`. Lúc này, tại mỗi vị trí token trong câu đều có một điểm số tạm thời.

---

### 2.3. Logic cốt tử: Tại sao bắt buộc dùng Last Token Pooling?

```python
        if self.config.pad_token_id is None:
            sequence_lengths = -1
        else:
            if input_ids is not None:
                sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
            else:
                sequence_lengths = -1

        pooled_logits = logits[range(batch_size), sequence_lengths]
```

#### 💡 Logic toán học và kiến trúc:
* **Tại sao không lấy token đầu tiên giống BERT (token `[CLS]`)?**
  * BERT là mô hình **Transformer Encoder**: Cơ chế Attention là hai chiều (Bidirectional Attention), token đầu tiên `[CLS]` được phép nhìn thấy tất cả các từ phía sau, do đó vector `[CLS]` gom đủ ý nghĩa cả câu.
  * GPT-2 là mô hình **Transformer Decoder**: Cơ chế Attention là **nhân quả một chiều có mặt nạ (Causal Masked Self-Attention)**. Token đứng trước không bao giờ được nhìn thấy token đứng sau.
  * Vì vậy:
    * Token 1 chỉ thấy chính nó.
    * Token 2 chỉ thấy Token 1 và 2.
    * **Chỉ duy nhất Token CUỐI CÙNG mới được phép nhìn thấy toàn bộ các từ từ đầu đến cuối câu!**
* **Giải mã dòng code trích xuất:**
  * Do trong một batch huấn luyện, các User Story có độ dài ngắn khác nhau và được chèn thêm token đệm `[PAD]` ở phía sau để bằng độ dài cố định.
  * `torch.ne(input_ids, self.config.pad_token_id)`: Trả về `True` cho các từ thực tế và `False` cho token `[PAD]`.
  * `.sum(-1) - 1`: Đếm tổng số token thật trừ đi 1 để tìm ra đúng vị trí chỉ số (index) của từ cuối cùng có nghĩa.
  * `logits[range(batch_size), sequence_lengths]`: Cắt lát tensor (tensor slicing) lấy đúng giá trị dự đoán tại vị trí token cuối cùng này.

---

### 2.4. Hàm mất mát huấn luyện: Tại sao tác giả dùng L1 Loss thay vì L2 Loss?

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
```

#### 💡 Logic toán học đằng sau:
1. `self.num_labels == 1`:
   * Xác nhận mô hình đang chạy chế độ hồi quy đơn biến (Single-target Regression).
2. `loss_fct = nn.L1Loss()`:
   * **Bản chất của dữ liệu Story Point trong thực tế:** Điểm Story Point có phân phối lệch phải cực mạnh (*Right-skewed Distribution*). Đa số task là 1, 2, 3, 5 điểm, nhưng thỉnh thoảng có những task ngoại lai cực lớn như 40, 100 điểm.
   * **Nếu dùng $L_2$ Loss (MSE - Sai số bình phương):**
     $$\mathcal{L}_{L2} = (\hat{y} - y)^2$$
     Khi gặp một task 100 điểm mà mô hình đoán 10 điểm, độ lệch là 90, bình phương lên là $8.100$. Gradient bùng nổ sẽ kéo toàn bộ trọng số của mô hình chạy theo điểm ngoại lai này, làm sai lệch việc dự đoán của hàng ngàn task nhỏ khác.
   * **Dùng $L_1$ Loss (MAE - Sai số tuyệt đối):**
     $$\mathcal{L}_{L1} = |\hat{y} - y|$$
     Đạo hàm của $L_1$ chỉ là $+1$ hoặc $-1$ (hàm dấu $\text{sign}$), không phụ thuộc vào độ lớn của sai số. Điều này giúp mô hình cực kỳ **vững chắc trước các điểm ngoại lai (Robust to Outliers)**.
3. `loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))`:
   * Kéo phẳng tensor dự đoán và nhãn thực tế về vector 1 chiều để tính sai số trung bình trên toàn batch.

---

## 📋 3. BẢNG TỔNG KẾT BẢN CHẤT LOGIC CỦA TỪNG KHỐI LỆNH

| Khối mã nguồn | Tác vụ lập trình thực tế | Logic toán học & Kỹ thuật bên dưới |
| :--- | :--- | :--- |
| `_keys_to_ignore_on_load_missing` | Bỏ qua `lm_head.weight` | Chuyển đổi công năng từ sinh ngôn ngữ tự do sang bộ ước lượng nỗ lực. |
| `dense1` & `dense2` | Nhân ma trận $768 \rightarrow 3072 \rightarrow 768$ | Tái cấu trúc đặc trưng nhưng thiếu phi tuyến, tương đương phép chiếu tuyến tính. |
| `score` | Chiếu $768 \rightarrow 1$ không có bias | Tích vô hướng rút gọn không gian ngữ cảnh thành điểm số thực $\hat{y}$. |
| `sequence_lengths` | Tính vị trí token thực cuối cùng | Thích ứng với mặt nạ nhân quả Causal Mask của GPT-2; chỉ token cuối gom đủ ngữ cảnh. |
| `nn.L1Loss()` | Tính trung bình trị tuyệt đối sai số | Kháng ngoại lai, chống bùng nổ gradient trên phân phối điểm lệch phải của Jira. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📜 [00_full_source_code.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/00_full_source_code.md): Toàn bộ mã nguồn gốc GPT2SP.
* 🔬 [02_training_pipeline_code_explanation.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/02_training_pipeline_code_explanation.md): Giải thích chi tiết mã nguồn pipeline huấn luyện và đánh giá thực nghiệm.
* ⚠️ [03_code_vs_paper_discrepancies.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/03_code_vs_paper_discrepancies.md): Mổ xẻ 4 điểm sai lệch cốt tử giữa code thực tế và bài báo.
* 🧠 [Chuyên mục Critical Thinking tổng quan](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/README.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
