# 🧠 PHÂN TÍCH PHẢN BIỆN 14: GIẢI PHÃU ĐẦU HỒI QUY MLP REGRESSOR HEAD TRONG GPT2SP
## BẢN CHẤT CẤU TRÚC 2 TẦNG (768 -> 768 -> 1), VÌ SAO DÙNG GELU VÀ ĐÁNH ĐỔI VỚI LINEAR PROBE

> **Chuyên mục:** Phân tích phản biện khoa học độc lập (Scientific Critical Thinking).  
> **Câu hỏi trọng tâm:** Tại sao tác giả GPT2SP (Fu et al., IEEE TSE 2023) không chiếu thẳng vector ngữ nghĩa về 1 con số bằng một tầng tuyến tính đơn giản ($768 \rightarrow 1$), mà lại thiết kế một mạng MLP 2 tầng ($768 \rightarrow 768 \rightarrow 1$) kết hợp hàm kích hoạt GELU? Cấu trúc này gồm bao nhiêu tham số và có những đánh đổi kỹ thuật (Trade-offs) nào?

---

## 🧭 1. ĐẶT VẤN ĐỀ: LINEAR PROBE HAY ĐẦU HỒI QUY PHI TUYẾN?

Sau khi chuỗi token của Jira issue chạy qua 12 khối Transformer Decoders và cơ chế Last Token Pooling, ta thu được một vector đại diện ngữ nghĩa:
$$h_{\text{last}} \in \mathbb{R}^{1 \times 768}$$

Tại thời điểm này, có 2 cách thiết kế để dự đoán giá trị Story Point ($\hat{y} \in \mathbb{R}^+$):

* **Phương án 1 (Linear Probe đơn giản):** Dùng duy nhất một tầng tuyến tính chiếu thẳng từ 768 chiều về 1 chiều:
  $$\hat{y} = h_{\text{last}} \cdot W + b \quad (W \in \mathbb{R}^{768 \times 1})$$
* **Phương án 2 (MLP Regressor Head - Lựa chọn của Fu et al.):** Xây dựng một mạng nơ-ron nhiều tầng (Multi-Layer Perceptron) với một tầng ẩn trung gian 768 chiều và hàm kích hoạt phi tuyến GELU:
  $$h_{\text{last}} \xrightarrow{\text{Linear}(768, 768)} z_1 \xrightarrow{\text{GELU}} a_1 \xrightarrow{\text{Linear}(768, 1)} \hat{y}$$

Tại sao tác giả lại chọn Phương án 2?

---

## 🔬 2. BẢN CHẤT TOÁN HỌC & CẤU TRÚC CỦA MLP REGRESSOR HEAD

### 2.1. Chi tiết 2 tầng tính toán
Đầu hồi quy MLP của GPT2SP nhận đầu vào là vector $h_{\text{last}} \in \mathbb{R}^{1 \times 768}$ và thực hiện 3 bước:

1. **Tầng ẩn biến đổi ngữ nghĩa (Dense Projection Layer):**
   $$z_1 = h_{\text{last}} W_1 + b_1$$
   * Ma trận trọng số: $W_1 \in \mathbb{R}^{768 \times 768}$
   * Vector độ chệch: $b_1 \in \mathbb{R}^{768}$
2. **Kích hoạt phi tuyến mượt (GELU Activation):**
   $$a_1 = \text{GELU}(z_1) = z_1 \cdot \Phi(z_1) = z_1 \cdot \frac{1}{2}\left[1 + \text{erf}\left(\frac{z_1}{\sqrt{2}}\right)\right]$$
3. **Tầng hồi quy dự đoán điểm số (Output Regression Layer):**
   $$\hat{y} = a_1 W_2 + b_2$$
   * Ma trận trọng số: $W_2 \in \mathbb{R}^{768 \times 1}$
   * Hệ số chệch vô hướng: $b_2 \in \mathbb{R}^1$

---

### 2.2. Bảng thống kê chi tiết tham số của MLP Regressor Head

| Tầng nơ-ron (Component) | Kích thước Tensor trọng số | Kích thước Bias | Tổng số tham số | Tỷ trọng |
| :--- | :---: | :---: | :---: | :---: |
| **Tầng 1 (Dense Linear)** | $768 \times 768 = 589.824$ | $768$ | **$590.592$** | $99.87\%$ |
| **Kích hoạt (GELU)** | Không có tham số | Không có | **$0$** | $0.00\%$ |
| **Tầng 2 (Regressor Linear)**| $768 \times 1 = 768$ | $1$ | **$769$** | $0.13\%$ |
| **TỔNG CỘNG ĐẦU MLP HEAD** | — | — | **$591.361$** | **$100\%$** |

> [!NOTE]
> Mặc dù $591.361$ tham số chỉ chiếm chưa đầy **$0.5\%$** trong tổng số 117 triệu tham số của GPT-2, nhưng đây là phân hệ duy nhất chịu trách nhiệm **chuyển hóa tri thức ngôn ngữ thành độ lớn công việc phần mềm**.

---

## 🧠 3. TẠI SAO LẠI LÀ 768 CHIỀU VÀ TẠI SAO LẠI DÙNG GELU?

### 3.1. Vì sao tầng ẩn trung gian lại có kích thước đúng bằng 768?
* **Bảo toàn chiều không gian đặc trưng (Isometric Representation):**  
  Chiều ẩn của phần thân GPT-2 Small là $d_{\text{model}} = 768$. Bằng cách giữ nguyên chiều $768 \rightarrow 768$, mô hình không bị "nghẽn cổ chai" (Bottleneck) làm mất mát thông tin đột ngột như khi ép xuống 128 hay 64 chiều.
* **Tương thích hoàn hảo với GPU Tensor Cores:**  
  Con số $768 = 32 \times 24$, chia hết cho kích thước Warp (32 threads) và phù hợp với các phép nhân ma trận FP16/BF16 tối ưu hóa trên kiến trúc GPU NVIDIA.

### 3.2. Vì sao dùng GELU mà không dùng ReLU?
* **Không bị chết nơ-ron (Dying ReLU):**  
  ReLU triệt tiêu toàn bộ gradient khi giá trị đầu vào âm ($x < 0 \rightarrow f'(x) = 0$). Với dữ liệu Jira có phương sai lớn, ReLU rất dễ làm "chết" hàng loạt nơ-ron trong quá trình lan truyền ngược. GELU cho phép một lượng nhỏ gradient âm đi qua, giữ cho mạng nơ-ron luôn sống.
* **Đồng nhất với kiến trúc bên trong GPT-2:**  
  Toàn bộ 12 khối Transformer Decoders của GPT-2 đều dùng hàm kích hoạt GELU. Việc tiếp tục sử dụng GELU ở đầu hồi quy giúp duy trì tính liên tục của hàm vi phân trên toàn bộ mạng.

---

## ⚖️ 4. PHÂN TÍCH ĐÁNH ĐỔI KỸ THUẬT (TRADE-OFF ANALYSIS)

### Ưu điểm của MLP Head so với Linear Probe:
* **Học được mối quan hệ phi tuyến phức tạp:**  
  Trong quản lý dự án Agile, nỗ lực phát triển không tăng tuyến tính. Ví dụ: Một ticket có chữ *"Database Migration"* kết hợp với chữ *"Security Vulnerability"* sẽ có Story Point tăng theo hàm mũ chứ không phải phép cộng đơn giản. Tầng phi tuyến GELU ở giữa giúp mô hình nắm bắt được các tương tác chéo giữa các đặc trưng ngữ nghĩa.

### Nhược điểm & Rủi ro chết người trong thực tế:
* **Nguy cơ Overfitting (Học vẹt) rất cao:**  
  Đầu MLP với gần $600.000$ tham số là một mạng rất lớn so với kích thước tập dữ liệu Jira thông thường. Nếu một dự án chỉ có $500$ đến $1.000$ issues, số lượng tham số cần học gấp hàng trăm lần số lượng mẫu huấn luyện!  
  Nếu không áp dụng kỹ thuật ngắt giảm nơ-ron (Dropout) và suy giảm trọng số (Weight Decay trong AdamW), đầu MLP này sẽ ghi nhớ từng ticket cụ thể thay vì học quy luật ước lượng tổng quát.

---

## 🔢 5. QUY ĐỔI TỪ SỐ THỰC SANG DÃY SỐ FIBONACCI

Sau khi tầng hồi quy xuất ra con số thực $\hat{y}$ (ví dụ $\hat{y} = 4.82$), các Agile Teams trong thực tế không bao giờ dùng điểm $4.82$. Họ sử dụng dãy số Fibonacci:
$$\mathcal{F} = \{1, 2, 3, 5, 8, 13, 21, \dots\}$$

Tác giả áp dụng quy tắc khoảng cách Euclidean gần nhất để làm tròn:
$$\text{SP}_{\text{final}} = \arg\min_{f \in \mathcal{F}} |f - \hat{y}|$$
Ví dụ:
* $\hat{y} = 2.4 \rightarrow \text{làm tròn thành } 2$
* $\hat{y} = 4.82 \rightarrow \text{làm tròn thành } 5$
* $\hat{y} = 7.1 \rightarrow \text{làm tròn thành } 8$

---

## 💻 6. MÃ NGUỒN PYTORCH XÂY DỰNG MLP REGRESSOR HEAD

```python
import torch
import torch.nn as nn

class MLPRegressorHead(nn.Module):
    def __init__(self, hidden_dim=768):
        super(MLPRegressorHead, self).__init__()
        # Tầng 1: Phóng chiếu phi tuyến giữ nguyên 768 chiều
        self.dense = nn.Linear(hidden_dim, hidden_dim, bias=True)
        self.gelu = nn.GELU()
        
        # Tầng 2: Chiếu về 1 giá trị Story Point thực
        self.regressor = nn.Linear(hidden_dim, 1, bias=True)
        
    def forward(self, last_token_vector):
        # last_token_vector shape: [batch_size, 768]
        x = self.dense(last_token_vector)      # [batch_size, 768]
        x = self.gelu(x)                       # [batch_size, 768]
        out = self.regressor(x)                # [batch_size, 1]
        return out.squeeze(-1)                 # [batch_size]

# Kiểm tra số lượng tham số
head = MLPRegressorHead(768)
total_params = sum(p.numel() for p in head.parameters() if p.requires_grad)
print(f"Tổng số tham số của MLP Regressor Head: {total_params:,}")
# Output: Tổng số tham số của MLP Regressor Head: 591,361
```

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG HỆ THỐNG

* 🔬 [Case Study 02: Bóc tách cơ chế MLP Regressor Head trên XD-3751](../case-study/02_case_study_mlp_regressor_head.md)
* 🧠 [Phân tích 12: Từ Generative LLM đến Regression Head](12_from_generative_llm_to_regression_head.md)
* 🧠 [Phân tích 13: Bản chất toán học của Last Token Pooling](13_why_last_token_pooling_not_first_or_mean.md)
* 📖 [Chương 3: Kiến trúc mô hình GPT2SP (Tổng quan)](../explanation/03_the_gpt2sp_architecture.md)
* 📋 [Báo cáo Tổng quan Điều hành dành cho Partner](../explanation/00_executive_report_and_partner_briefing.md)
