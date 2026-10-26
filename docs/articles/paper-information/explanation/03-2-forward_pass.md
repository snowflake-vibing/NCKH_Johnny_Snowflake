# 📖 CHƯƠNG 03-2: QUY TRÌNH LAN TRUYỀN XUÔI (FORWARD PASS FLOW)

> **Tài liệu gốc liên kết:**  
> * Mục 3.2 (Model Building) & Hình 2 (Fig. 2: An overview architecture of our GPT2SP), Trang 4 – 5, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> * Tác giả: Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).  
> * File cấu trúc mô hình: [`03-1-model_architecture.md`](03-1-model_architecture.md).  
> * File lan truyền ngược liên kết: [`03-3-backpropagation_and_optimization.md`](03-3-backpropagation_and_optimization.md).

---

## 🎯 1. BẢN CHẤT CỦA PHA LAN TRUYỀN XUÔI (FORWARD PASS)

**Pha Lan truyền Xuôi (Forward Pass)** là quy trình tính toán một chiều duy nhất, đưa dữ liệu từ văn bản Jira Issue thô đi xuyên suốt qua toàn bộ mạng nơ-ron GPT2SP để xuất ra con số điểm ước lượng Story Point cuối cùng ($\hat{y}$):

$$\text{Jira Issue Text} \xrightarrow{\text{Tokenize}} [x_1, \dots, x_N] \xrightarrow{\text{Embedding}} \mathbf{E} \xrightarrow{\text{12 Blocks}} \mathbf{H}^{(12)} \xrightarrow{\text{Pooling}} \mathbf{h}_{\text{last}} \xrightarrow{\text{MLP}} \hat{y} \in \mathbb{R}^+$$

Dưới đây là hành trình toán học chi tiết của một mini-batch gồm $B$ issues, mỗi issue có độ dài $N$ tokens.

```text
  [Văn bản Jira Issue]: "ExpressionExecutionException when element that expects a DW..."
                                         │
                                         ▼ (Bước 1: BPE Tokenization)
  Ma trận Token IDs:                     [B × N]
                                         │
                                         ▼ (Bước 2: Tra cứu Word & Pos Embedding)
  Ma trận Đầu vào E_0:                   [B × N × 768]
                                         │
                                         ▼ (Bước 3: Chạy qua 12 Khối Transformer Decoders)
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  LẶP TỪ KHỐI 1 ĐẾN KHỐI 12:                                                 │
  │  • Pre-LayerNorm 1 -> Fused QKV (768->2304) -> Masked Attention 12 Heads    │
  │  • Chiếu W^O (768->768) + Residual 1: x_mid = x + MHA(x)                    │
  │  • Pre-LayerNorm 2 -> FFN (768->3072 qua GELU -> 768)                       │
  │  • Residual 2: x_out = x_mid + FFN(x_mid)                                   │
  └─────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
  Ma trận Trạng thái Ẩn Khối 12:         [B × N × 768]
                                         │
                                         ▼ (Bước 4: Last Token Pooling tại vị trí N)
  Vector Ngữ cảnh Cô đọng h_last:        [B × 768]
                                         │
                                         ▼ (Bước 5: MLP Regressor Head: 768 -> 256 -> 1)
  ĐIỂM SỐ DỰ ĐOÁN CUỐI CÙNG:             y_hat ∈ [B × 1] (Ví dụ: 2.45 hoặc 4.82 SP)
```

---

## 🔤 2. BƯỚC 1 & 2: TIỀN XỬ LÝ & NHÚNG ĐẦU VÀO (INPUT EMBEDDING)

### 2.1. Phân tách từ con BPE Tokenization
* Văn bản tiêu đề và mô tả của Jira issue được đưa qua bộ BPE Tokenizer chuẩn hóa 50.257 vocabs.
* Ví dụ với issue `XD-3751`, câu văn được bẻ thành chuỗi $N = 15$ tokens:
  $$\text{Tokens} = [\text{"Exp"}, \text{"ression"}, \text{"Exec"}, \text{"ution"}, \text{"Exception"}, \dots, \text{"space"}]$$
* Tensor Token IDs đầu vào: $\mathbf{X}_{\text{ids}} \in \mathbb{Z}^{B \times N}$ với giá trị nguyên nằm trong đoạn $[0, 50256]$.

### 2.2. Tra cứu ma trận nhúng Word & Positional Embedding
Tại mỗi vị trí $i \in [0, N-1]$ trong chuỗi:
1. **Tra cứu từ ma trận từ $W_{te} \in \mathbb{R}^{50257 \times 768}$:** Lấy ra vector $\mathbf{w}_i = W_{te}[\mathbf{X}_{\text{ids}}[b, i]] \in \mathbb{R}^{768}$.
2. **Tra cứu từ ma trận vị trí $W_{pe} \in \mathbb{R}^{1024 \times 768}$:** Lấy ra vector vị trí $\mathbf{p}_i = W_{pe}[i] \in \mathbb{R}^{768}$.
3. **Phép cộng nhúng đầu vào:**
   $$\mathbf{e}_i = \mathbf{w}_i + \mathbf{p}_i \in \mathbb{R}^{768}$$
4. **Áp dụng Dropout đầu vào ($p = 0.1$):**  
   $$\mathbf{E}^{(0)} = \text{Dropout}(\mathbf{e}) \in \mathbb{R}^{B \times N \times 768}$$

---

## ⚙️ 3. BƯỚC 3: LAN TRUYỀN QUA 12 KHỐI TRANSFORMER DECODERS

Dữ liệu $\mathbf{E}^{(0)}$ lần lượt đi qua Khối $l = 1, 2, \dots, 12$. Tại mỗi khối $l$, quy trình lan truyền diễn ra như sau:

### 3.1. Phân hệ Masked Multi-Head Self-Attention

#### 1. Chuẩn hóa lớp trước (Pre-LayerNorm 1):
$$\mathbf{X}_{\text{norm1}} = \text{LayerNorm}(\mathbf{X}^{(l-1)}) = \frac{\mathbf{X}^{(l-1)} - \mu}{\sqrt{\sigma^2 + \epsilon}} \odot \gamma_1 + \beta_1 \in \mathbb{R}^{B \times N \times 768}$$

#### 2. Chiếu ma trận Fused QKV (Một phép nhân duy nhất):
$$\mathbf{QKV} = \mathbf{X}_{\text{norm1}} W_{QKV} + \mathbf{b}_{QKV} \in \mathbb{R}^{B \times N \times 2304}$$
Sau đó cắt mảng thành 3 tensor độc lập kích thước $[B \times N \times 768]$:
$$Q, K, V = \text{split}(\mathbf{QKV}, 768, \text{dim}=-1)$$

#### 3. Phân chia không gian thành 12 đầu chú ý ($H = 12, d_k = 64$):
Định dạng lại tensor sang kích thước $[B \times 12 \times N \times 64]$ để tính toán song song:
$$Q_h, K_h, V_h \in \mathbb{R}^{B \times 12 \times N \times 64} \quad (h = 1, \dots, 12)$$

#### 4. Tính toán Ma trận Chú ý có Mặt nạ (Masked Attention Scores):
Điểm tương đồng giữa các từ được tính bằng tích vô hướng chia tỷ lệ:
$$S_h = \frac{Q_h K_h^T}{\sqrt{64}} \in \mathbb{R}^{B \times 12 \times N \times N}$$

Cộng ma trận mặt nạ nhân quả $M \in \mathbb{R}^{N \times N}$ (trong đó $M_{ij} = -\infty$ nếu $j > i$ và $M_{ij} = 0$ nếu $j \le i$):
$$\tilde{S}_h = S_h + M$$

Tính xác suất phân bổ chú ý qua hàm Softmax:
$$A_h = \text{softmax}(\tilde{S}_h) \in \mathbb{R}^{B \times 12 \times N \times N}$$
*(Tại các vị trí tương lai, $\text{softmax}(-\infty) = 0$, ngăn chặn triệt để rò rỉ thông tin tương lai).*

#### 5. Tổng hợp đặc trưng và chiếu đầu ra:
Nhân ma trận xác suất với ma trận Giá trị $V_h$:
$$\text{head}_h = A_h V_h \in \mathbb{R}^{B \times 12 \times N \times 64}$$

Ghép 12 đầu lại với nhau thành tensor $[B \times N \times 768]$ và chiếu qua ma trận $W^O$:
$$\mathbf{X}_{\text{mha}} = \text{Concat}(\text{head}_1, \dots, \text{head}_{12}) W^O + \mathbf{b}^O \in \mathbb{R}^{B \times N \times 768}$$

#### 6. Kết nối tắt thứ nhất (Residual Connection 1):
$$\mathbf{X}_{\text{mid}} = \mathbf{X}^{(l-1)} + \text{Dropout}(\mathbf{X}_{\text{mha}}, p=0.1) \in \mathbb{R}^{B \times N \times 768}$$

---

### 3.2. Phân hệ Mạng Nơ-ron Truyền thẳng (Feed-Forward Network - FFN)

#### 1. Chuẩn hóa lớp trước (Pre-LayerNorm 2):
$$\mathbf{X}_{\text{norm2}} = \text{LayerNorm}(\mathbf{X}_{\text{mid}}) \in \mathbb{R}^{B \times N \times 768}$$

#### 2. Chiếu mở rộng không gian 4 lần ($768 \rightarrow 3072$ chiều):
Chiếu qua ma trận $W_1 \in \mathbb{R}^{768 \times 3072}$ kết hợp hàm kích hoạt phi tuyến GELU:
$$\mathbf{H}_{\text{ffn}} = \text{GELU}(\mathbf{X}_{\text{norm2}} W_1 + \mathbf{b}_1) \in \mathbb{R}^{B \times N \times 3072}$$

#### 3. Chiếu thu hẹp về không gian gốc ($3072 \rightarrow 768$ chiều):
$$\mathbf{X}_{\text{ffn\_out}} = \mathbf{H}_{\text{ffn}} W_2 + \mathbf{b}_2 \in \mathbb{R}^{B \times N \times 768}$$

#### 4. Kết nối tắt thứ hai (Residual Connection 2):
$$\mathbf{X}^{(l)} = \mathbf{X}_{\text{mid}} + \text{Dropout}(\mathbf{X}_{\text{ffn\_out}}, p=0.1) \in \mathbb{R}^{B \times N \times 768}$$

👉 Kết thúc Khối thứ 12, ta cho toàn bộ ma trận đi qua tầng chuẩn hóa cuối cùng:
$$\mathbf{H}^{(12)} = \text{Final\_LayerNorm}(\mathbf{X}^{(12)}) \in \mathbb{R}^{B \times N \times 768}$$

---

## 🎯 4. BƯỚC 4: TRÍCH XUẤT TOKEN CUỐI CÙNG (LAST TOKEN POOLING)

* Khác với bài toán phân loại thông thường (vốn dùng token đầu câu `[CLS]`), GPT-2 là mô hình Decoder có mặt nạ nhân quả:
  - Token số 1 chỉ nhìn thấy chính nó.
  - Token số 2 nhìn thấy token 1 và 2.
  - **Token số $N$ (token cuối cùng của câu) nhìn thấy toàn bộ từ token $1$ đến token $N$!**
* Do đó, vector trạng thái ẩn tại vị trí $N$ là nơi duy nhất chứa đựng toàn bộ bức tranh tổng thể về ngữ pháp, module phần mềm và nguyên nhân lỗi của User Story.
* Phép trích xuất được thực hiện tức thì với chi phí $\mathcal{O}(1)$:
  $$\mathbf{h}_{\text{last}} = \mathbf{H}^{(12)}[:, N-1, :] \in \mathbb{R}^{B \times 768}$$

---

## ⚖️ 5. BƯỚC 5: ĐẦU HỒI QUY MLP REGRESSOR HEAD TÍNH ĐIỂM SỐ THỰC

Vector $\mathbf{h}_{\text{last}}$ được đưa qua mạng hồi quy đa tầng để ánh xạ từ biểu diễn ngôn ngữ sang điểm số Story Point:

1. **Chiếu nén qua tầng ẩn thứ nhất ($768 \rightarrow 256$ chiều):**
   $$\mathbf{z}_1 = \mathbf{h}_{\text{last}} W_{\text{mlp1}} + \mathbf{b}_{\text{mlp1}} \in \mathbb{R}^{B \times 256}$$
2. **Kích hoạt GELU & Dropout:**
   $$\mathbf{a}_1 = \text{Dropout}(\text{GELU}(\mathbf{z}_1), p = 0.1) \in \mathbb{R}^{B \times 256}$$
3. **Chiếu về điểm số vô hướng (Linear Output Layer):**
   $$\hat{y} = \mathbf{a}_1 W_{\text{mlp2}} + b_{\text{mlp2}} \in \mathbb{R}^{B \times 1}$$

👉 Kết quả thu được là một giá trị số thực liên tục $\hat{y}$ (ví dụ: $\hat{y} = 2.45$ SP đối với `XD-3751` hoặc $\hat{y} = 4.82$ SP đối với `XD-4012`).

---

## 🔄 6. SỰ KHÁC BIỆT CỐT LÕI: FORWARD TRONG HUẤN LUYỆN VS. SUY LUẬN

| Tiêu chí kỹ thuật | Forward trong Pha Huấn luyện (Training) | Forward trong Pha Suy luận (Inference) |
| :--- | :--- | :--- |
| **Trạng thái mô hình** | `model.train()` | `model.eval()` |
| **Xây dựng đồ thị tính toán** | `requires_grad = True` (Lưu toàn bộ tensor trung gian để chuẩn bị Backprop). | `torch.no_grad()` (Vứt bỏ đồ thị tính toán, tiết kiệm $>70\%$ VRAM GPU). |
| **Hành vi Dropout ($p=0.1$)** | Bật ngẫu nhiên tắt $10\%$ nơ-ron để chống học vẹt (Stochastic). | Tắt hoàn toàn ($p=0$), 100% nơ-ron hoạt động, kết quả xác định 100% (Deterministic). |
| **Tốc độ thực thi** | Mất từ $50 - 80\text{ ms}$ cho mỗi batch (do phải lưu graph). | Siêu nhanh: chỉ mất **$15 - 30\text{ ms}$** cho một issue. |
| **Đích đến của kết quả $\hat{y}$** | Đưa vào hàm mất mát **$L_1$ Loss** để so sánh với điểm thật $y$ và kích hoạt Backpropagation. | 1. Làm tròn về thang điểm **Fibonacci** ($1, 2, 3, 5, 8, 13$).<br>2. Kích hoạt luồng giải thích **XAI Integrated Gradients**. |

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG

* ⬅️ [Chương 03-1: Cấu trúc Mô hình Học sâu GPT2SP (Model Architecture)](03-1-model_architecture.md)
* ➡️ [Chương 03-3: Chi tiết Pha Lan truyền Ngược & Tối ưu hóa (Backpropagation & AdamW)](03-3-backpropagation_and_optimization.md)
* 🔬 [Case Study 04: Hình dung trực quan Pha Huấn luyện qua ví dụ XD-3751](../case-study/04_case_study_training_phase.md)
* 🔬 [Case Study 05: Hình dung trực quan Pha Suy luận tại Sprint Planning qua XD-4012](../case-study/05_case_study_inference_phase.md)
