# 🧠 PHÂN TÍCH PHẢN BIỆN 12: TỪ MÔ HÌNH SINH NGÔN NGỮ (GENERATIVE LLM) ĐẾN ĐẦU HỒI QUY STORY POINT (REGRESSION HEAD)
## GIẢI PHÃU CƠ CHẾ "PHẪU THUẬT" GPT-2 TỪ MÁY SINH CHỮ THÀNH MÁY ĐOÁN ĐIỂM SỐ THỰC

> **Chuyên mục:** Phân tích phản biện khoa học độc lập (Scientific Critical Thinking).  
> **Câu hỏi trọng tâm:** GPT-2 vốn được OpenAI sinh ra để dự đoán từ tiếp theo (Next Token Prediction / Causal Language Modeling) trong kho từ điển $50.257$ từ. Làm thế nào tác giả Fu et al. (IEEE TSE 2023) có thể "phẫu thuật" mô hình này để biến nó thành một công cụ dự đoán điểm số thực duy nhất (Story Point Regression: ví dụ $3.0, 5.0, 8.0$)?

---

## 🧭 1. NGHỊCH LÝ ĐẶT RA CHO NGƯỜI MỚI

Khi một sinh viên hoặc lập trình viên mới tiếp cận mô hình GPT-2, họ thường mặc định trong đầu:
* GPT-2 là một mô hình sinh ngôn ngữ tự hồi quy (Autoregressive Generative Model).
* Đầu ra của GPT-2 nguyên bản là một phân phối xác suất trên toàn bộ kho từ vựng $50.257$ tokens để trả lời câu hỏi: *"Từ tiếp theo nhiều khả năng xuất hiện nhất là từ nào?"*.

Tuy nhiên, bài toán ước lượng Story Point trong Agile hoàn toàn không phải là bài toán sinh chữ:
* Đầu vào: Một đoạn văn bản mô tả User Story hoặc Jira Bug.
* Đầu ra mong muốn: **Một con số thực vô hướng duy nhất** ($\hat{y} \in \mathbb{R}^+$), đại diện cho độ phức tạp và nỗ lực cần thiết (Story Point).

Để giải quyết nghịch lý này, nhóm tác giả GPT2SP đã thực hiện một cuộc "phẫu thuật kiến trúc" gồm 3 bước căn bản: Cắt bỏ LM Head, Thay thế bằng MLP Regressor Head, và Chuyển dịch hàm mất mát.

---

## 🔬 2. BA BƯỚC "PHẪU THUẬT" KIẾN TRÚC TRONG MÃ NGUỒN PYTORCH

### Bước 1: Vứt bỏ Language Modeling Head (LM Head)
Trong kiến trúc GPT-2 chuẩn của OpenAI (`GPT2LMHeadModel`), sau khi chuỗi token đi qua 12 khối Transformer Decoders, ta thu được tensor trạng thái ẩn cuối cùng có kích thước `[batch_size, sequence_length, 768]`:
$$H \in \mathbb{R}^{B \times S \times 768}$$

Ở mô hình gốc, tensor này sẽ được nhân với một ma trận chiếu tuyến tính khổng lồ gọi là **LM Head**:
$$W_{\text{lm}} \in \mathbb{R}^{768 \times 50.257}$$

Phép nhân ma trận này phóng đại vector 768 chiều thành 50.257 con số (logits), đại diện cho điểm số của 50.257 từ trong từ điển.  
👉 **Quyết định của Fu et al.:** Tác giả **vứt bỏ hoàn toàn ma trận $W_{\text{lm}}$ này**. Nhóm nghiên cứu chỉ giữ lại phần "thân" (Backbone) gồm 12 khối Transformer Decoders để biến GPT-2 thành một **Cỗ máy trích xuất đặc trưng ngữ nghĩa khổng lồ (Rich Semantic Feature Extractor)**.

---

### Bước 2: Ghép nối Đầu hồi quy Đa tầng (MLP Regressor Head)
Sau khi có được vector đại diện ngữ nghĩa của chuỗi văn bản $h_{\text{last}} \in \mathbb{R}^{1 \times 768}$ (thông qua cơ chế Last Token Pooling), tác giả gắn thêm một mạng nơ-ron nhiều tầng mới (Multi-Layer Perceptron):

```text
[Vector ngữ nghĩa Last Token] (1 x 768)
          │
          ▼
[Tầng Tuyến tính 1: Linear Layer] (768 -> 768)
          │
          ▼
[Hàm kích hoạt phi tuyến GELU]
          │
          ▼
[Tầng Tuyến tính 2: Linear Layer] (768 -> 1)
          │
          ▼
[Con số Story Point dự đoán: y_hat] (Giá trị vô hướng thực)
```

Công thức toán học của đầu hồi quy này:
$$z_1 = h_{\text{last}} \cdot W_1 + b_1 \quad (W_1 \in \mathbb{R}^{768 \times 768}, b_1 \in \mathbb{R}^{768})$$
$$a_1 = \text{GELU}(z_1)$$
$$\hat{y} = a_1 \cdot W_2 + b_2 \quad (W_2 \in \mathbb{R}^{768 \times 1}, b_2 \in \mathbb{R}^1)$$

Như vậy, toàn bộ 117 triệu tham số ngôn ngữ được cô đọng lại thành một vector 768 chiều, và 2 tầng Linear nhỏ gọn này sẽ học cách ánh xạ tri thức ngôn ngữ thành con số nỗ lực phần mềm.

---

### Bước 3: Chuyển dịch hàm mất mát (Từ Cross-Entropy sang L1 Loss)
* **Trong mô hình sinh chữ (GPT-2 gốc):** Mô hình tối ưu hóa hàm Cross-Entropy Loss để ép phân phối xác suất đầu ra trùng với từ thực tế tiếp theo trong văn bản.
* **Trong mô hình dự đoán Story Point (GPT2SP):** Mô hình tối ưu hóa hàm mất mát khoảng cách tuyệt đối (**L1 Loss / Mean Absolute Error**):
$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$
Trong đó:
* $y_i$ là số điểm Story Point thực tế được ghi nhận trong Jira ticket.
* $\hat{y}_i$ là con số do mạng MLP Regressor dự đoán ra.

Đạo hàm của hàm mất mát này là hàm dấu $\text{sign}(\hat{y} - y)$, tạo ra độ dốc hằng số $\pm 1$ giúp gradient truyền ngược một cách ổn định qua toàn bộ 12 khối Transformer Decoders.

---

## 💻 3. MINH HỌA MÃ NGUỒN PYTORCH THỰC TẾ

Dưới đây là đoạn mã nguồn Python/PyTorch mô tả chính xác cách tác giả định nghĩa lớp `GPT2SPModel`:

```python
import torch
import torch.nn as nn
from transformers import GPT2Model

class GPT2SPRegressor(nn.Module):
    def __init__(self, pretrained_model_name='gpt2'):
        super(GPT2SPRegressor, self).__init__()
        # 1. Tải phần thân (Backbone) 12 khối của GPT-2, bỏ qua LM Head
        self.gpt2 = GPT2Model.from_pretrained(pretrained_model_name)
        
        # 2. Định nghĩa MLP Regressor Head (768 -> 768 -> 1)
        self.dense = nn.Linear(768, 768)
        self.gelu = nn.GELU()
        self.regressor = nn.Linear(768, 1)
        
    def forward(self, input_ids, attention_mask):
        # Cho chuỗi token đi qua 12 khối Transformer
        outputs = self.gpt2(input_ids=input_ids, attention_mask=attention_mask)
        hidden_states = outputs.last_hidden_state  # Shape: [batch_size, seq_len, 768]
        
        # 3. Last Token Pooling: Bốc vector của token cuối cùng trong chuỗi
        # Lấy vị trí token thực tế cuối cùng dựa vào attention_mask
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = input_ids.shape[0]
        last_token_repr = hidden_states[torch.arange(batch_size), sequence_lengths] # [batch, 768]
        
        # 4. Dự đoán qua MLP Regressor Head
        x = self.dense(last_token_repr)
        x = self.gelu(x)
        predicted_sp = self.regressor(x) # Shape: [batch, 1]
        
        return predicted_sp.squeeze(-1)
```

---

## ⚖️ 4. PHÂN TÍCH ĐÁNH ĐỔI & HẠN CHẾ (CRITICAL TRADE-OFFS)

1. **Lợi thế vượt bậc so với Deep-SE:**  
   Bằng cách giữ lại phần thân GPT-2 tiền huấn luyện, mô hình thừa hưởng vốn tri thức ngữ nghĩa khổng lồ từ Internet (Wikipedia, Reddit, GitHub). Khi đọc các từ chuyên ngành như *"SQL injection"*, *"NullPointerException"*, *"refactoring"*, mô hình đã hiểu sẵn mối liên hệ trừu tượng mà không cần học lại từ con số 0 như Word2Vec của Deep-SE.
2. **Cạm bẫy chi phí tính toán (Over-parameterization):**  
   Để dự đoán một con số thực đơn giản (Story Point), chúng ta phải mang theo toàn bộ cỗ máy cồng kềnh **117 triệu tham số**!  
   * Mỗi lượt suy luận (Inference) đòi hỏi hàng trăm triệu phép nhân ma trận.
   * Nguy cơ mô hình bị ghi nhớ vẹt (Over-fitting) rất cao nếu tập dữ liệu Jira chỉ có vài trăm ticket.
3. **Độ nhạy cảm với Token cuối:**  
   Toàn bộ nỗ lực dự đoán đặt hết lên vai của **duy nhất một vector 768 chiều của token cuối cùng**. Nếu quá trình tiền xử lý hoặc padding làm lệch token cuối, toàn bộ kết quả dự đoán sẽ sụp đổ.

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG HỆ THỐNG

* 🧠 [Phân tích 13: Bản chất toán học của Last Token Pooling (Vì sao lấy token cuối?)](13_why_last_token_pooling_not_first_or_mean.md)
* 🔬 [Case Study 02: Bóc tách cơ chế MLP Regressor Head](../case-study/02_case_study_mlp_regressor_head.md)
* 📖 [Chương 3: Kiến trúc mô hình GPT2SP](../explanation/03_the_gpt2sp_architecture.md)
* 📋 [Báo cáo Tổng quan Điều hành dành cho Partner](../explanation/00_executive_report_and_partner_briefing.md)
