# 📖 CHƯƠNG 03-3: LAN TRUYỀN NGƯỢC VÀ TỐI ƯU HÓA TRỌNG SỐ (BACKPROPAGATION & OPTIMIZATION)

> **Tài liệu gốc liên kết:**  
> * Mục 3.2 (Model Building) & Mục 4.3 (Model Training), Trang 4 – 6, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> * Tác giả: Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).  
> * File cấu trúc mô hình: [`03-1-model_architecture.md`](03-1-model_architecture.md).  
> * File lan truyền xuôi: [`03-2-forward_pass.md`](03-2-forward_pass.md).

---

## 🎯 1. BẢN CHẤT CỦA PHA LAN TRUYỀN NGƯỢC (BACKPROPAGATION)

Nếu như **Lan truyền Xuôi (Forward Pass)** là quá trình mô hình đưa ra dự đoán điểm nỗ lực ($\hat{y}$), thì **Lan truyền Ngược (Backward Propagation)** là quá trình **sửa sai và rút kinh nghiệm**:

> ⚠️ **LƯU Ý CỐT TỬ:**  
> **Lan truyền ngược CHỈ TỒN TẠI trong Pha Huấn luyện (Training Phase)!**  
> Khi bước sang Pha Suy luận (Inference Phase) tại các buổi họp Sprint Planning thực tế, quá trình lan truyền ngược bị khóa hoàn toàn (`torch.no_grad()`, `model.eval()`), toàn bộ 117M trọng số được giữ nguyên cố định.

Mục tiêu của lan truyền ngược là tính toán đạo hàm riêng của hàm mất mát đối với từng trọng số trong mô hình:

$$\nabla_{\theta} \mathcal{L} = \frac{\partial \mathcal{L}}{\partial \theta} \quad (\theta \in \{W_{\text{mlp}}, W_{\text{ffn}}, W_{QKV}, W^O, W_{te}, W_{pe}\})$$

Từ đó, thuật toán tối ưu hóa **AdamW** sẽ điều chỉnh các trọng số $\theta$ để ở lượt học tiếp theo, sai số dự đoán sẽ giảm đi.

```text
[HÀM MẤT MÁT L1 LOSS]  L = |y - y_hat|
           │
           ▼  (Đạo hàm: dL/dy_hat = sign(y_hat - y))
[MLP REGRESSOR HEAD]   Linear 2 -> GELU -> Linear 1
           │
           ▼  (dL/dh_last: Gradient tại vector 768 chiều token cuối cùng)
[12 KHỐI TRANSFORMER DECODERS] (Lội ngược từ Khối 12 -> Khối 1)
           │  • Nhờ 24 Residual Connections: Gradient truyền thẳng tắp không bị triệt tiêu!
           │  • Tính đạo hàm qua FFN (W2, GELU, W1) & LayerNorm 2
           │  • Tính đạo hàm qua Attention (W^O, Softmax, W_QKV) & LayerNorm 1
           ▼
[MA TRẬN NHÚNG ĐẦU VÀO] W_te (50.257 x 768) & W_pe (1024 x 768)
           │
           ▼
[THUẬT TOÁN ADAMW]     Cập nhật trọng số: W_(t+1) = W_t - alpha * m_hat / sqrt(v_hat) - Weight Decay
```

---

## 📏 2. BƯỚC 1: HÀM MẤT MÁT $L_1$ LOSS VÀ ĐẠO HÀM KHỞI NGUỒN

Trong mỗi mini-batch gồm $B$ User Stories, mô hình đối chiếu điểm số dự đoán $\hat{y}_b$ với điểm Story Point thực tế $y_b$ do đội ngũ lập trình viên chốt trong quá khứ.

### 2.1. Công thức hàm mất mát $L_1$ Loss (MAE Loss)

$$\mathcal{L}_{L_1} = \frac{1}{B} \sum_{b=1}^{B} |y_b - \hat{y}_b|$$

### 2.2. Đạo hàm khởi nguồn của hàm mất mát theo dự đoán $\hat{y}$
Đạo hàm của hàm mất mát $L_1$ đối với đầu ra dự đoán của mỗi mẫu $b$ là hàm dấu (sign function):

$$\frac{\partial \mathcal{L}}{\partial \hat{y}_b} = \frac{1}{B} \cdot \text{sign}(\hat{y}_b - y_b) = \begin{cases} +\frac{1}{B} & \text{khi } \hat{y}_b > y_b \quad (\text{Mô hình đoán già điểm}) \\ -\frac{1}{B} & \text{khi } \hat{y}_b < y_b \quad (\text{Mô hình đoán non điểm}) \\ 0 & \text{khi } \hat{y}_b = y_b \quad (\text{Mô hình đoán trúng tuyệt đối}) \end{cases}$$

### 💡 Vì sao bài báo GPT2SP dùng $L_1$ Loss thay vì $L_2$ Loss (MSE)?
* Trong các dự án phần mềm Jira, thỉnh thoảng xuất hiện các User Story bất thường (outliers) được chấm điểm rất cao (ví dụ $40$ hay $100$ SP).
* Nếu dùng **$L_2$ Loss ($(\hat{y} - y)^2$)**: Đạo hàm tỷ lệ thuận với độ lệch $2(\hat{y} - y)$. Một sai số lệch $30$ điểm sẽ tạo ra gradient khổng lồ gấp 60 lần, làm rung chuyển và phá hỏng toàn bộ các trọng số mô hình đã học ổn định từ các task thông thường.
* Dùng **$L_1$ Loss**: Gradient luôn luôn có độ lớn cố định bằng $\pm 1/B$, bất kể sai số lệch $0.5$ hay lệch $50$ điểm. Điều này giúp mô hình **cực kỳ bền bỉ và không bị nhiễu bởi các task ngoại lai (Robust to Outliers)**.

---

## 🔙 3. BƯỚC 2: LAN TRUYỀN NGƯỢC QUA ĐẦU HỒI QUY MLP REGRESSOR HEAD

Dòng tín hiệu gradient $\frac{\partial \mathcal{L}}{\partial \hat{y}}$ chảy ngược qua mạng MLP Regressor 2 tầng:

1. **Đạo hàm tại Tầng Tuyến tính Đầu ra (Linear Layer 2):**  
   Với $\hat{y} = \mathbf{a}_1 W_{\text{mlp2}} + b_{\text{mlp2}}$, ta tính gradient của trọng số:
   $$\frac{\partial \mathcal{L}}{\partial W_{\text{mlp2}}} = \mathbf{a}_1^T \frac{\partial \mathcal{L}}{\partial \hat{y}} \in \mathbb{R}^{256 \times 1}$$
   $$\frac{\partial \mathcal{L}}{\partial b_{\text{mlp2}}} = \sum_{b=1}^{B} \frac{\partial \mathcal{L}}{\partial \hat{y}_b} \in \mathbb{R}$$
   Và gradient truyền ngược về tầng ẩn:
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{a}_1} = \frac{\partial \mathcal{L}}{\partial \hat{y}} W_{\text{mlp2}}^T \in \mathbb{R}^{B \times 256}$$

2. **Đạo hàm qua Tầng Kích hoạt Phi tuyến GELU & Dropout:**  
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{z}_1} = \frac{\partial \mathcal{L}}{\partial \mathbf{a}_1} \odot \text{Dropout\_Mask} \odot \text{GELU}'(\mathbf{z}_1) \in \mathbb{R}^{B \times 256}$$
   *(Nhờ GELU là hàm trơn khả vi liên tục trên toàn trục số, đạo hàm $\text{GELU}'(\mathbf{z}_1)$ không bao giờ bị cắt đột ngột về 0 như ReLU, bảo đảm dòng gradient luôn được lưu thông êm ái).*

3. **Đạo hàm tại Tầng Tuyến tính Thứ nhất (Linear Layer 1):**  
   Với $\mathbf{z}_1 = \mathbf{h}_{\text{last}} W_{\text{mlp1}} + \mathbf{b}_{\text{mlp1}}$, gradient trọng số được tính:
   $$\frac{\partial \mathcal{L}}{\partial W_{\text{mlp1}}} = \mathbf{h}_{\text{last}}^T \frac{\partial \mathcal{L}}{\partial \mathbf{z}_1} \in \mathbb{R}^{768 \times 256}$$
   $$\frac{\partial \mathcal{L}}{\partial \mathbf{b}_{\text{mlp1}}} = \sum_{b=1}^{B} \frac{\partial \mathcal{L}}{\partial \mathbf{z}_{1, b}} \in \mathbb{R}^{256}$$

4. **Tín hiệu Gradient tại Đỉnh Token Cuối cùng:**  
   Tín hiệu gradient truyền về vector ngữ nghĩa của token cuối cùng là:
   $$\mathbf{g}_{\text{last}} = \frac{\partial \mathcal{L}}{\partial \mathbf{h}_{\text{last}}} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}_1} W_{\text{mlp1}}^T \in \mathbb{R}^{B \times 768}$$

---

## 🌊 4. BƯỚC 3: DÒNG THÁC GRADIENT LỘI NGƯỢC QUA 12 KHỐI TRANSFORMER

Đây là giai đoạn phức tạp nhất: gradient $\mathbf{g}_{\text{last}}$ phải lội ngược từ Khối 12 về Khối 1.

### 4.1. Sự mở rộng từ 1 token sang toàn bộ chuỗi
Tại đầu ra Khối 12, chỉ có token cuối cùng $N$ nhận tín hiệu gradient trực tiếp $\mathbf{g}_{\text{last}}$, các vị trí token khác $1 \dots N-1$ ban đầu có gradient bằng 0:
$$\frac{\partial \mathcal{L}}{\partial \mathbf{H}^{(12)}} = [0, 0, \dots, \mathbf{g}_{\text{last}}] \in \mathbb{R}^{B \times N \times 768}$$

Tuy nhiên, khi đi ngược qua **Cơ chế Attention**, vì token cuối cùng đã chú ý đến tất cả các từ phía trước trong câu trong pha Forward, nên tín hiệu gradient của nó sẽ **tự động phân bổ ngược lại cho tất cả các token phía trước**! Nhờ đó, mọi từ trong câu đều được điều chỉnh trọng số nhúng tương ứng với mức độ đóng góp vào sai số dự đoán.

### 4.2. Vai trò cứu mạng của 24 Kết nối tắt (Residual Connections)
Trong mạng sâu 12 tầng, nếu không có kết nối tắt, gradient sẽ phải nhân liên tiếp qua 12 ma trận trọng số, dẫn đến hiện tượng **Triệt tiêu Gradient (Vanishing Gradient)** khiến các tầng đầu tiên không thể học được.

Nhờ công thức kết nối tắt: $\mathbf{X}_{\text{out}} = \mathbf{X}_{\text{in}} + F(\mathbf{X}_{\text{in}})$, đạo hàm được tính theo công thức:

$$\frac{\partial \mathcal{L}}{\partial \mathbf{X}_{\text{in}}} = \frac{\partial \mathcal{L}}{\partial \mathbf{X}_{\text{out}}} \cdot \frac{\partial \mathbf{X}_{\text{out}}}{\partial \mathbf{X}_{\text{in}}} = \mathbf{\frac{\partial \mathcal{L}}{\partial \mathbf{X}_{\text{out}}}} + \frac{\partial \mathcal{L}}{\partial \mathbf{X}_{\text{out}}} \cdot \frac{\partial F(\mathbf{X}_{\text{in}})}{\partial \mathbf{X}_{\text{in}}}$$

> ⭐ **ĐƯỜNG CAO TỐC GRADIENT (GRADIENT HIGHWAY):**  
> Số hạng $\frac{\partial \mathcal{L}}{\partial \mathbf{X}_{\text{out}}}$ đứng độc lập trong công thức trên đóng vai trò là một "đường cao tốc" truyền thẳng tín hiệu gradient từ tầng trên xuống tầng dưới mà **không hề bị suy giảm hay nhân nhỏ đi**! Nhờ 24 kết nối tắt này, cả 12 khối Transformer của GPT2SP đều được cập nhật trọng số mạnh mẽ và đồng đều.

### 4.3. Đạo hàm qua từng khối Transformer
Tại mỗi khối từ 12 về 1:
1. **Qua FFN:** Tính gradient đối với ma trận $W_2$ ($3072 \times 768$), hàm phi tuyến GELU, và ma trận $W_1$ ($768 \times 3072$).
2. **Qua Pre-LayerNorm 2:** Tính gradient đối với hệ số tỉ lệ $\gamma_2$ và độ lệch $\beta_2$.
3. **Cộng nhánh tắt 2:** Cộng trực tiếp gradient vào luồng tín hiệu chính.
4. **Qua Masked Attention:**
   * Tính gradient đối với ma trận chiếu đầu ra $W^O$ ($768 \times 768$).
   * Tách gradient về 3 nhánh $Q, K, V$.
   * Tính gradient đối với ma trận gộp $W_{QKV}$ ($768 \times 2304$).
5. **Qua Pre-LayerNorm 1:** Tính gradient đối với $\gamma_1$ và $\beta_1$.
6. **Cộng nhánh tắt 1:** Truyền tiếp gradient xuống khối phía trước.

---

## 🔤 5. BƯỚC 4: LAN TRUYỀN VỀ CÁC MA TRẬN NHÚNG ĐẦU VÀO

Khi dòng gradient vượt qua Khối 1 về đến chân mô hình:
* **Gradient ma trận nhúng vị trí ($W_{pe}$):**
  $$\frac{\partial \mathcal{L}}{\partial W_{pe}[i]} = \sum_{b=1}^{B} \frac{\partial \mathcal{L}}{\partial \mathbf{e}_{b, i}} \in \mathbb{R}^{768}$$
* **Gradient ma trận nhúng từ ($W_{te}$):**  
  Chỉ những từ con nào thực sự xuất hiện trong câu của mini-batch đó mới nhận được gradient để cập nhật hàng vector tương ứng trong cuốn từ điển $50.257$ từ:
  $$\frac{\partial \mathcal{L}}{\partial W_{te}[\text{token\_id}]} += \frac{\partial \mathcal{L}}{\partial \mathbf{e}_{b, i}} \in \mathbb{R}^{768}$$

---

## ⚙️ 6. BƯỚC 5: THUẬT TOÁN TỐI ƯU HÓA ADAMW CẬP NHẬT TRỌNG SỐ

Sau khi đã thu thập đủ gradient $\mathbf{g}_t = \nabla_{\theta} \mathcal{L}$ cho toàn bộ $117\text{M}$ tham số, thuật toán tối ưu **AdamW (Adam with Decoupled Weight Decay)** thực hiện cập nhật theo 4 bước toán học:

### 6.1. Cấu hình siêu tham số của GPT2SP (Theo Mục 4.3 bài báo gốc)
* **Tốc độ học (Learning Rate):** $\alpha = 5 \times 10^{-4}$.
* **Hệ số suy giảm trọng số (Weight Decay):** $\lambda = 0.01$.
* **Hệ số quán tính bậc 1:** $\beta_1 = 0.9$ (Momentum).
* **Hệ số quán tính bậc 2:** $\beta_2 = 0.999$ (RMSprop variance).
* **Hằng số ổn định số học:** $\epsilon = 10^{-8}$.
* **Quy mô mini-batch:** $B = 64$ issues.

### 6.2. Các bước cập nhật toán học tại thời điểm $t$:

1. **Cập nhật ước lượng kỳ vọng quán tính bậc 1 (Momentum Vector):**
   $$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{g}_t$$
2. **Cập nhật ước lượng phương sai quán tính bậc 2 (Variance Vector):**
   $$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2$$
3. **Hiệu chỉnh thiên lệch cho các bước đầu (Bias Correction):**
   $$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$
4. **Cập nhật trọng số với cơ chế Tách rời Weight Decay (Decoupled Weight Decay):**
   $$\theta_{t+1} = \theta_t - \underbrace{\alpha \lambda \theta_t}_{\text{Weight Decay trực tiếp}} - \underbrace{\frac{\alpha}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon} \hat{\mathbf{m}}_t}_{\text{Bước nhảy thích nghi theo Gradient}}$$

> 💡 **Điểm đột phá của AdamW so với Adam cổ điển:**  
> AdamW tách riêng phép phạt $L_2$ (Weight Decay) ra khỏi việc tính toán gradient thích nghi. Điều này ngăn chặn hiện tượng các trọng số thường xuyên được kích hoạt bị thu nhỏ quá mức, giúp mô hình GPT2SP duy trì khả năng tổng quát hóa xuất sắc và không bao giờ bị quá khớp (overfitting) trên dữ liệu Jira.

---

## 📈 7. TOÀN CẢNH MỘT VÒNG HUẤN LUYỆN (EPOCH SUMMARY)

Một chu kỳ học hoàn chỉnh của GPT2SP diễn ra tuần hoàn:

```text
[DỮ LIỆU JIRA] ──> [FORWARD PASS] ──> [L1 LOSS] ──> [BACKPROPAGATION] ──> [ADAMW UPDATE]
      ▲                                                                         │
      └──────────────────────────── Lặp lại cho Batch tiếp theo ────────────────┘
```

* Sau hàng ngàn lượt lặp qua nhiều Epochs, hàm mất mát $L_1$ Loss giảm dần đều và hội tụ ổn định.
* Khi kết thúc huấn luyện, mô hình đạt mức sai số kỷ lục: **$\text{MAE} = 0.96$ Story Points trên dự án Spring XD** (và trung bình $1.16$ MAE trên toàn bộ 16 dự án mã nguồn mở).
* Lúc này, toàn bộ 117M tham số được đóng băng để đưa vào phục vụ Pha Suy luận tại các buổi họp Sprint Planning!

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG

* ⬅️ [Chương 03-1: Cấu trúc Mô hình Học sâu GPT2SP (Model Architecture)](03-1-model_architecture.md)
* ⬅️ [Chương 03-2: Chi tiết Pha Lan truyền Xuôi (Forward Pass Flow)](03-2-forward_pass.md)
* 📖 [File tổng quan Chương 3: Kiến trúc GPT2SP](03_the_gpt2sp_architecture.md)
* 🔬 [Case Study 04: Hình dung trực quan Pha Huấn luyện qua ví dụ XD-3751](../case-study/04_case_study_training_phase.md)
* 📚 [Thuật ngữ: Backpropagation (Lan truyền ngược)](../glossary/backpropagation.md)
* 📚 [Thuật ngữ: Weight Decay](../glossary/weight_decay.md)
