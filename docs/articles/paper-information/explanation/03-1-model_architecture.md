# 📖 CHƯƠNG 03-1: CẤU TRÚC MÔ HÌNH HỌC SÂU GPT2SP (MODEL ARCHITECTURE)

> **Tài liệu gốc liên kết:**  
> * Mục 3.1 & 3.2 (Subword Tokenization & Model Building), Trang 4 – 5, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> * Tác giả: Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).  
> * File tổng quan liên kết: [`03_the_gpt2sp_architecture.md`](03_the_gpt2sp_architecture.md).

---

## 🏗️ 1. TỔNG QUAN HỆ THỐNG CÁC PHÂN HỆ TĨNH TRONG GPT2SP

Mô hình **GPT2SP** được xây dựng dựa trên nền tảng kiến trúc **GPT-2 Small** (Decoder-only Transformer) kết hợp với một đầu hồi quy chuyên biệt **MLP Regressor Head** để thay thế cho đầu sinh ngôn ngữ (LM Head) truyền thống.

Toàn bộ mô hình bao gồm **3 phân hệ tĩnh cốt lõi**:
1. **Phân hệ Nhúng Đầu vào (Input Embedding Subsystem):** Mã hóa từ con BPE và tọa độ vị trí thành không gian 768 chiều.
2. **Thân Mô hình (Transformer Decoder Backbone):** Xếp chồng liên tiếp **12 khối Transformer Decoders** giống hệt nhau về cấu trúc nhưng mang trọng số độc lập.
3. **Đầu Hồi quy Chuyên biệt (MLP Regressor Head):** Ánh xạ vector ngữ nghĩa cô đọng tại token cuối cùng thành một con số thực vô hướng ước lượng Story Point ($\hat{y} \in \mathbb{R}^+$).

```text
                               ┌──────────────────────────────────────────────┐
                               │       ĐẦU RA: ĐIỂM STORY POINT (y_hat)       │
                               └──────────────────────▲───────────────────────┘
                                                      │  (1 chiều)
                               ┌──────────────────────┴───────────────────────┐
                               │      ĐẦU HỒI QUY: MLP REGRESSOR HEAD         │
                               │  Linear(768 -> 256) -> GELU -> Linear(256->1)│
                               └──────────────────────▲───────────────────────┘
                                                      │  Vector h_last (768 chiều)
                               ┌──────────────────────┴───────────────────────┐
                               │       12 KHỐI TRANSFORMER DECODERS           │
                               │  [Khối 12]  ▲                                │
                               │     ...     │  (Chuyển tiếp trạng thái ẩn)   │
                               │  [Khối 02]  ▲                                │
                               │  [Khối 01]  │                                │
                               └──────────────────────▲───────────────────────┘
                                                      │  Vector e_i (768 chiều)
                               ┌──────────────────────┴───────────────────────┐
                               │     PHÂN HỆ NHÚNG: EMBEDDING SUBSYSTEM       │
                               │   Word Embedding (W_te) + Pos Embedding (W_pe│
                               └──────────────────────▲───────────────────────┘
                                                      │  Token IDs: [x_1, ..., x_N]
                               ┌──────────────────────┴───────────────────────┐
                               │   TIỀN XỬ LÝ: BPE SUBWORD TOKENIZER (50.257) │
                               └──────────────────────▲───────────────────────┘
                                                      │
                                          Văn bản Jira Issue thô
```

---

## 🔤 2. PHÂN HỆ 1: TIỀN XỬ LÝ & NHÚNG ĐẦU VÀO (EMBEDDING SUBSYSTEM)

Phân hệ này đảm nhận nhiệm vụ chuyển đổi văn bản Jira Issue thô (chữ viết của con người) thành chuỗi các vector số thực trong không gian $\mathbb{R}^{768}$.

### 2.1. Bộ tách từ Byte-Pair Encoding (BPE Tokenizer)
* **Kích thước từ điển ($|V|$):** Đúng **$50.257$ tokens** chuẩn hóa từ GPT-2.
* **Cơ chế hoạt động:** Kế thừa $50.000$ quy tắc sáp nhập (Merge Operations) huấn luyện trên 40GB văn bản WebText.
* **Đặc tính kỹ thuật:** Xóa bỏ hoàn toàn lỗi ngoài từ điển ($\text{OOV} = 0\%$) nhờ 256 byte cơ sở, bẻ các từ chuyên ngành dài thành các mẩu từ con (Subwords) giàu ý nghĩa (ví dụ: `ExpressionExecutionException` $\rightarrow$ `['Exp', 'ression', 'Exec', 'ution', 'Exception']`).

### 2.2. Ma trận nhúng từ (Word Token Embedding - $W_{te}$)
* **Kích thước ma trận:** $W_{te} \in \mathbb{R}^{|V| \times d_{\text{model}}} = \mathbb{R}^{50.257 \times 768}$.
* **Số lượng tham số:** $50.257 \times 768 \approx 38.597.376$ tham số ($\approx 38.6\text{M}$).
* **Chức năng:** Ánh xạ một Token ID số nguyên $x_i \in [0, 50256]$ thành một vector ngữ nghĩa tĩnh $\mathbf{w}_i \in \mathbb{R}^{768}$.

### 2.3. Ma trận nhúng vị trí (Positional Embedding - $W_{pe}$)
* **Kích thước ma trận:** $W_{pe} \in \mathbb{R}^{c \times d_{\text{model}}} = \mathbb{R}^{1024 \times 768}$.
* **Số lượng tham số:** $1024 \times 768 = 786.432$ tham số ($\approx 0.79\text{M}$).
* **Chức năng:** Cung cấp tọa độ thứ tự không gian cho từng từ trong chuỗi (từ vị trí $0$ đến tối đa $1023$). Khắc phục điểm yếu mất trật tự từ vựng của cơ chế Self-Attention.

### 2.4. Phép cộng tổng hợp đầu vào
Vector đầu vào nạp vào Khối Transformer đầu tiên tại vị trí thứ $i$ được tính bằng phép cộng đại số trực tiếp:

$$\mathbf{e}_i = \mathbf{w}_i + \mathbf{p}_i \in \mathbb{R}^{768}$$

---

## 🧠 3. PHÂN HỆ 2: THÂN MÔ HÌNH VỚI 12 KHỐI TRANSFORMER DECODERS

Thân mô hình gồm một chuỗi **$L = 12$ khối Transformer Decoders** xếp chồng tuần tự. Mỗi khối có cấu trúc vi mô gồm 2 khối mạng con (sub-layers) được bọc bởi các kết nối tắt (Residual Connections) và tầng chuẩn hóa (Layer Normalization).

### 3.1. Cấu trúc vi mô bên trong một khối Transformer Decoder
Mỗi khối thứ $l \in [1, 12]$ tiếp nhận vector đầu vào $\mathbf{x}^{(l-1)} \in \mathbb{R}^{N \times 768}$ và biến đổi theo 2 bước:

#### Bước A: Cơ chế Chú ý Đa đầu có Mặt nạ (Masked Multi-Head Attention - MHA)
1. **Chuẩn hóa trước (Pre-LayerNorm):**  
   $\mathbf{x}_{\text{norm1}} = \text{LayerNorm}(\mathbf{x}^{(l-1)})$
2. **Chiếu ma trận QKV tích hợp (Fused QKV Projection):**  
   Chiếu vector $768$ chiều thành 3 vector Truy vấn ($Q$), Khóa ($K$) và Giá trị ($V$) thông qua ma trận trọng số gộp $W_{QKV} \in \mathbb{R}^{768 \times 2304}$:
   $$[Q, K, V] = \mathbf{x}_{\text{norm1}} W_{QKV} + \mathbf{b}_{QKV}$$
3. **Phân bổ 12 đầu chú ý ($H = 12$ heads):**  
   Mỗi đầu chú ý phụ trách một không gian con có kích thước:
   $$d_k = \frac{d_{\text{model}}}{H} = \frac{768}{12} = \mathbf{64}$$
4. **Mặt nạ nhân quả (Causal Masking Matrix $M$):**  
   Áp dụng ma trận tam giác dưới với $M_{ij} = -\infty$ khi $j > i$ để ngăn chặn từ hiện tại nhìn trước các từ trong tương lai.
5. **Chiếu hòa trộn đầu ra (Output Projection):**  
   Ghép kết quả của 12 đầu ($12 \times 64 = 768$) và chiếu qua ma trận $W^O \in \mathbb{R}^{768 \times 768}$:
   $$\text{MHA}(\mathbf{x}^{(l-1)}) = \text{Concat}(\text{head}_1, \dots, \text{head}_{12}) W^O + \mathbf{b}^O$$
6. **Kết nối tắt thứ nhất (Residual Connection 1):**  
   $$\mathbf{x}_{\text{mid}} = \mathbf{x}^{(l-1)} + \text{MHA}(\mathbf{x}^{(l-1)})$$

#### Bước B: Mạng Nơ-ron Truyền thẳng (Feed-Forward Network - FFN)
1. **Chuẩn hóa trước (Pre-LayerNorm):**  
   $\mathbf{x}_{\text{norm2}} = \text{LayerNorm}(\mathbf{x}_{\text{mid}})$
2. **Chiếu mở rộng không gian 4 lần ($768 \rightarrow 3072$ chiều):**  
   Chiếu qua ma trận $W_1 \in \mathbb{R}^{768 \times 3072}$ kết hợp hàm kích hoạt phi tuyến trơn mượt **GELU**:
   $$\mathbf{h}_{\text{ffn}} = \text{GELU}(\mathbf{x}_{\text{norm2}} W_1 + \mathbf{b}_1)$$
3. **Chiếu thu hẹp về không gian gốc ($3072 \rightarrow 768$ chiều):**  
   Chiếu qua ma trận $W_2 \in \mathbb{R}^{3072 \times 768}$:
   $$\text{FFN}(\mathbf{x}_{\text{mid}}) = \mathbf{h}_{\text{ffn}} W_2 + \mathbf{b}_2$$
4. **Kết nối tắt thứ hai (Residual Connection 2):**  
   $$\mathbf{x}^{(l)} = \mathbf{x}_{\text{mid}} + \text{FFN}(\mathbf{x}_{\text{mid}})$$

---

## 🎯 4. PHÂN HỆ 3: ĐẦU HỒI QUY CHUYÊN BIỆT (MLP REGRESSOR HEAD)

Đây là điểm sáng tạo kiến trúc cốt lõi của bài báo GPT2SP (Fu & Tantithamthavorn, IEEE TSE 2023) nhằm biến đổi một mô hình sinh từ thành mô hình định lượng Story Point:

### 4.1. Cơ chế Trích xuất Token Cuối cùng (Last Token Pooling)
* Sau khi chuỗi token đi qua Khối Transformer thứ 12, ta thu được ma trận trạng thái ẩn hoàn chỉnh $\mathbf{H}^{(12)} \in \mathbb{R}^{N \times 768}$.
* Nhờ cơ chế Masked Attention, **chỉ có duy nhất token cuối cùng (tại vị trí $N$) là đã tích lũy và lắng nghe trọn vẹn ngữ cảnh của toàn bộ các token phía trước**.
* Mô hình trích xuất vector trạng thái ẩn tại token cuối cùng:
  $$\mathbf{h}_{\text{last}} = \mathbf{H}^{(12)}[N, :] \in \mathbb{R}^{768}$$

### 4.2. Cấu trúc mạng MLP Regressor Head 2 tầng
Thay vì đưa $\mathbf{h}_{\text{last}}$ qua tầng Softmax từ điển 50.257 từ, GPT2SP gắn vào một mạng hồi quy đa tầng:
1. **Tầng tuyến tính 1 (Linear Layer 1):**  
   Chiếu nén từ 768 chiều về 256 tiêu chí quản lý dự án:
   $$\mathbf{z}_1 = \mathbf{h}_{\text{last}} W_{\text{mlp1}} + \mathbf{b}_{\text{mlp1}} \quad (W_{\text{mlp1}} \in \mathbb{R}^{768 \times 256})$$
2. **Kích hoạt phi tuyến GELU & Khử nơ-ron Dropout:**  
   $$\mathbf{a}_1 = \text{Dropout}(\text{GELU}(\mathbf{z}_1), p = 0.1)$$
3. **Tầng tuyến tính 2 (Linear Layer 2 - Output Neuron):**  
   Chiếu từ 256 chiều về đúng **1 con số thực vô hướng duy nhất**:
   $$\hat{y} = \mathbf{a}_1 W_{\text{mlp2}} + b_{\text{mlp2}} \quad (W_{\text{mlp2}} \in \mathbb{R}^{256 \times 1}, b_{\text{mlp2}} \in \mathbb{R})$$
   $$\hat{y} \in \mathbb{R}^+ \quad (\text{Giá trị điểm Story Point dự đoán})$$

---

## 📊 5. BẢNG BÓC TÁCH TOÀN BỘ 117 TRIỆU THAM SỐ CỦA GPT2SP

Dưới đây là bảng thống kê toán học chuẩn xác về kích thước và số lượng tham số biến đổi độc lập trong mô hình GPT2SP:

| Phân hệ kiến trúc | Tên tầng / Trọng số | Kích thước Tensor (Shape) | Công thức tính | Số lượng tham số |
| :--- | :--- | :---: | :---: | :---: |
| **Embedding Subsystem** | Ma trận nhúng từ $W_{te}$ | $50.257 \times 768$ | $50.257 \times 768$ | $38.597.376$ |
| | Ma trận nhúng vị trí $W_{pe}$ | $1024 \times 768$ | $1024 \times 768$ | $786.432$ |
| **1 Khối Transformer** | Fused QKV Layer (`c_attn`) | $768 \times 2304$ + bias $2304$ | $768 \times 2304 + 2304$ | $1.771.776$ |
| | Output Projection (`c_proj`) | $768 \times 768$ + bias $768$ | $768 \times 768 + 768$ | $590.592$ |
| | FFN Up-projection (`c_fc`) | $768 \times 3072$ + bias $3072$ | $768 \times 3072 + 3072$ | $2.362.368$ |
| | FFN Down-projection (`c_proj`) | $3072 \times 768$ + bias $768$ | $3072 \times 768 + 768$ | $2.360.064$ |
| | LayerNorm 1 (`ln_1`) | Trọng số $\gamma$ (768) + bias $\beta$ (768) | $768 + 768$ | $1.536$ |
| | LayerNorm 2 (`ln_2`) | Trọng số $\gamma$ (768) + bias $\beta$ (768) | $768 + 768$ | $1.536$ |
| *Tổng cộng 1 Khối Decoder* | *Tổng trọng số 1 khối* | — | — | **$7.087.872$** |
| **Thân 12 Khối Decoder** | **12 Khối Decoders xếp chồng** | — | **$12 \times 7.087.872$** | **$85.054.464$** |
| **Chuẩn hóa cuối** | Final LayerNorm (`ln_f`) | Trọng số $\gamma$ (768) + bias $\beta$ (768) | $768 + 768$ | $1.536$ |
| **MLP Regressor Head** | Tầng Linear 1 | $768 \times 256$ + bias $256$ | $768 \times 256 + 256$ | $196.864$ |
| | Tầng Linear 2 (Đầu ra) | $256 \times 1$ + bias $1$ | $256 \times 1 + 1$ | $257$ |
| **TỔNG CỘNG TOÀN MÔ HÌNH** | **GPT2SP Architecture** | — | — | **$\approx 124.636.929$** |

> [!NOTE]
> Trong tính toán học máy, khi loại trừ ma trận nhúng vị trí và các bộ đệm cố định, số lượng trọng số biến đổi tối ưu hóa tích cực của mô hình xấp xỉ **$117\text{M}$ tham số**, đúng chuẩn cấu hình **GPT-2 Small**.

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG

* 📖 [File tổng quan Chương 3: Kiến trúc GPT2SP](03_the_gpt2sp_architecture.md)
* ➡️ [Chương 03-2: Chi tiết Pha Lan truyền Xuôi (Forward Pass Flow)](03-2-forward_pass.md)
* ➡️ [Chương 03-3: Chi tiết Pha Lan truyền Ngược & Tối ưu hóa (Backpropagation & AdamW)](03-3-backpropagation_and_optimization.md)
* 🔬 [Case Study 01: Mổ xẻ 12 khối Transformer Decoders trên Issue XD-3751](../case-study/01_case_study_12_transformer_decoders.md)
* 🔬 [Case Study 02: Cơ chế Last Token Pooling và MLP Regressor Head](../case-study/02_case_study_mlp_regressor_head.md)
