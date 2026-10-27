# 🔬 CASE STUDY 03: TRÍCH XUẤT ĐẶC TRƯNG VÀ LAST TOKEN POOLING TRÊN ISSUE XD-3751
## MẮT XÍCH KẾT NỐI: TỪ TENSOR 3 CHIỀU [1, 48, 768] ĐẾN VECTOR ĐẠI DIỆN [1, 768]

> **Chuyên mục:** Nghiên cứu tình huống thực tế (Practical Case Study).  
> **Dự án thực nghiệm:** Spring XD (Jira Repository).  
> **Issue mục tiêu:** **XD-3751** — *"Trigger job should not fail when job name does not exist"*.  
> **Vị trí mắt xích:** Nằm chính giữa [Case Study 01 (12 Decoders)](01_case_study_12_transformer_decoders.md) và [Case Study 02 (MLP Regressor Head)](02_case_study_mlp_regressor_head.md).  
> **Câu hỏi trọng tâm:** Sau khi chuỗi 48 tokens của issue XD-3751 đi qua khối Transformer thứ 12, ta có một khối tensor 3 chiều kích thước `[1, 48, 768]`. Làm thế nào mô hình bóc tách được đúng vector 768 chiều đại diện cho toàn bộ issue để chuyển giao sang cho đầu hồi quy MLP?

---

## 🧭 1. HIỆN TRẠNG TENSOR SAU TẦNG GIẢI MÃ THỨ 12

Sau khi tính toán xong toàn bộ 12 khối giải mã, tensor đầu ra tại tầng LayerNorm cuối cùng (`ln_f`) của GPT-2 có dạng:
$$H_{12} \in \mathbb{R}^{1 \times 48 \times 768}$$

Trong đó:
* Số chiều thứ 1 ($1$): Kích thước lô (Batch Size $= 1$ issue XD-3751).
* Số chiều thứ 2 ($48$): Chiều dài chuỗi token (Sequence Length $= 48$ tokens từ `'Tr'` đến `'<|endoftext|>'`).
* Số chiều thứ 3 ($768$): Chiều sâu không gian ẩn (Hidden Dimension $= 768$ nơ-ron).

Mỗi token trong chuỗi $48$ tokens này lúc này đều sở hữu riêng một vector trạng thái $768$ chiều:
* Vector $h_0 \in \mathbb{R}^{768}$: Đại diện cho token `'Tr'` (chỉ chứa thông tin cục bộ của chính nó).
* Vector $h_1 \in \mathbb{R}^{768}$: Đại diện cho token `'igger'`.
* ...
* Vector $h_{47} \in \mathbb{R}^{768}$: Đại diện cho token thứ 48 — token kết thúc chuỗi `'<|endoftext|>'`.

---

## 🔍 2. BẢN CHẤT SỰ TÍCH TỤ NGỮ CẢNH CỦA TOKEN THỨ 48

Tại sao vector $h_{47}$ lại là "tinh hoa" của toàn bộ ticket XD-3751?
Do cơ chế Mặt nạ Chú ý Nhân quả (Causal Mask), ma trận trọng số chú ý tại tầng 12 của token thứ 48 đã thực hiện phép tổng hợp có trọng số trên toàn bộ 47 token đứng trước:

$$h_{47} = \sum_{j=0}^{47} \alpha_{47, j} \cdot V_j$$

* Token thứ 48 đã "nhìn thấy" từ khóa `'NullPointerException'` (vị trí token 35-37) và gán trọng số chú ý cao ($\alpha \approx 0.18$).
* Nó đã nhìn thấy cụm từ `'job does not exist'` (vị trí token 7-11) và gán trọng số ($\alpha \approx 0.22$).
* Nó đã nhìn thấy yêu cầu `'gracefully catch'` (vị trí token 40-42) với trọng số ($\alpha \approx 0.15$).

Do đó, vector $h_{47}$ không còn là một ký tự kết thúc vô nghĩa, mà đã trở thành một **vector ngữ nghĩa cô đặc (Dense Semantic Representation)** đại diện trọn vẹn cho toàn bộ bối cảnh lỗi và nỗ lực sửa lỗi của ticket XD-3751.

---

## ✂️ 3. THAO TÁC CẮT LÁT TENSOR TRONG PYTORCH (SLICING OPERATION)

Để lấy được vector này, mã nguồn thực hiện phép cắt lát tensor (Tensor Slicing) như sau:

```python
import torch

# Giả lập hidden_states từ tầng 12 của issue XD-3751
# batch_size = 1, seq_len = 48, hidden_dim = 768
hidden_states = torch.randn(1, 48, 768)

# Vị trí của token cuối cùng là index 47 (tức seq_len - 1)
last_token_index = 47

# Phép bóc tách Last Token Pooling:
# Trích xuất hàng thứ 47 dọc theo trục sequence_length
last_token_vector = hidden_states[:, last_token_index, :] # Shape: [1, 768]

print("Kích thước tensor sau khi pooling:", last_token_vector.shape)
# Output: torch.Size([1, 768])
```

Từ một khối lập phương $1 \times 48 \times 768$ (gồm $36.864$ con số thực), phép Last Token Pooling đã gạn lọc lại đúng **$768$ con số thực** tinh túy nhất.

---

## 🚀 4. CHUYỂN GIAO SANG ĐẦU HỒI QUY (MLP REGRESSOR HEAD)

Vector $h_{47} \in \mathbb{R}^{1 \times 768}$ vừa bóc tách xong sẽ lập tức được làm đầu vào trực tiếp cho mạng nơ-ron MLP Regressor Head:

```text
Tensor đầu ra tầng 12: [1, 48, 768]
               │
               ▼ (Last Token Pooling tại vị trí index 47)
Vector đại diện: [1, 768]
               │
               ▼ (Nạp vào MLP Dense Layer: Linear 768 -> 768 + GELU)
Vector phi tuyến: [1, 768]
               │
               ▼ (Nạp vào Regressor Layer: Linear 768 -> 1)
Dự đoán Story Point: y_hat = 3.12 (Gần sát ground-truth 3.0 của XD-3751!)
```

Nhờ mắt xích kết nối này, toàn bộ dòng chảy thông tin từ chữ viết thô của Jira ticket XD-3751 đã được chuyển hóa thành một giá trị Story Point định lượng cụ thể.

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG HỆ THỐNG

* 🔬 [Case Study 01: Dòng chảy qua 12 khối Transformer Decoders](01_case_study_12_transformer_decoders.md)
* 🔬 [Case Study 02: Bóc tách cơ chế MLP Regressor Head](02_case_study_mlp_regressor_head.md)
* 🧠 [Phân tích 13: Bản chất toán học của Last Token Pooling](../critical-thinking/13_why_last_token_pooling_not_first_or_mean.md)
* 📋 [Báo cáo Tổng quan Điều hành dành cho Partner](../explanation/00_executive_report_and_partner_briefing.md)
