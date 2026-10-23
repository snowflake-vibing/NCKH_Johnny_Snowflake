# 🧠 PHÂN TÍCH PHẢN BIỆN 02: NGUỒN GỐC VÀ BẢN CHẤT CỦA KHÔNG GIAN 768 CHIỀU ẨN (HIDDEN DIMENSION)

> **Câu hỏi phản biện mở rộng:**  
> 1. *"Tại sao chiều ẩn (hidden dimension - $d_{\text{model}}$) của GPT-2 và GPT2SP lại là con số lẻ 768 mà không phải là một số tròn chẵn như 500 hay 1000?"*  
> 2. *"768 tọa độ này thực chất chứa những gì bên trong? Có phải tọa độ 1 là danh từ, tọa độ 2 là lỗi phần mềm không?"*  
> 3. *"Có những bài báo khoa học nào chuyên nghiên cứu và giải mã không gian này? Có dataset và code thực nghiệm để tự kiểm chứng không?"*

---

## 🎯 1. NGUỒN GỐC TỪ CƠ CHẾ ĐA ĐẦU CHÚ Ý ($12 \times 64 = 768$)

Nguồn gốc trực tiếp nhất của con số **$768$** xuất phát từ công thức phân bổ kích thước trong cơ chế **Multi-Head Self-Attention** của kiến trúc Transformer.

Trong bài báo gốc của Google (*"Attention Is All You Need"*, Vaswani et al., 2017):
* Toàn bộ vector biểu diễn ẩn $d_{\text{model}}$ được chia đều cho $H$ đầu chú ý song song (Attention Heads):
  $$d_k = \frac{d_{\text{model}}}{H}$$
  *(Trong đó $d_k$ là số chiều vector mà mỗi đầu chú ý phụ trách).*

### Vì sao mỗi đầu lại chọn kích thước chuẩn $d_k = 64$?
* **Về mặt toán học:** Trong công thức Scaled Dot-Product Attention:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$
  Tích vô hướng $QK^T$ có phương sai tỷ lệ thuận với $d_k$. Nếu $d_k$ quá lớn (ví dụ $256$), tích vô hướng bùng nổ rất lớn khiến hàm Softmax rơi vào vùng bão hòa (gradient gần bằng $0$, gây triệt tiêu gradient).  
  Các tác giả thực nghiệm nhận thấy **$d_k = 64$** (kết hợp với hệ số chia $\frac{1}{\sqrt{64}} = \frac{1}{8}$) là điểm cân bằng vàng: đủ sức chứa đặc trưng ngôn ngữ mà gradient vẫn lan truyền cực kỳ ổn định.
* **Số lượng đầu chú ý ($H = 12$ heads):**  
  Để mô hình có thể quan sát $12$ khía cạnh ngữ nghĩa độc lập cùng một lúc (cú pháp câu, đối tượng gây lỗi, liên kết logic, dấu câu...), OpenAI thiết lập $H = 12$.

Từ đó, chiều ẩn tổng thể của mô hình bắt buộc phải là:
$$d_{\text{model}} = H \times d_k = 12 \times 64 = \mathbf{768}$$

---

## 💻 2. TỐI ƯU HÓA PHẦN CỨNG GPU (WARP ALIGNMENT & TENSOR CORES)

Trong kỹ thuật máy tính, các chip đồ họa GPU (đặc biệt là GPU NVIDIA) không xử lý dữ liệu theo từng luồng đơn lẻ, mà tính toán theo từng bó luồng song song gọi là **Warp**:
* Mỗi Warp của NVIDIA luôn luôn có đúng **$32$ luồng (threads)**.
* Các nhân tính toán ma trận chuyên dụng (**Tensor Cores**) được thiết kế để nạp và nhân các khối ma trận kích thước là bội số của **$16$**, **$32$**, và **$64$**.

Con số **$768$** là một con số "cực kỳ thân thiện với phần cứng" (Hardware-aligned number):

$$768 = 24 \times 32 \quad (\text{Chia hết cho 32 luồng của 1 Warp})$$
$$768 = 12 \times 64 \quad (\text{Khớp hoàn hảo với Tensor Core GEMM})$$
$$768 = 3 \times 256 \quad (\text{Căn chỉnh theo đường truyền bộ nhớ cache 256-bit})$$

> [!TIP]
> **Hệ quả phần cứng:** Nếu ta chọn một con số tròn trịa theo thói quen con người như $500$ hay $1000$, GPU sẽ không thể chia đều cho các Warp 32 luồng. Phần cứng buộc phải thực hiện kỹ thuật chèn thêm các số 0 (padding), gây lãng phí bộ nhớ đệm, chậm băng thông và xuất hiện hiện tượng xung đột hàng bộ nhớ (Bank Conflict). Con số $768$ giúp GPU chạy ở **100% công suất lý thuyết**.

---

## ⚖️ 3. "ĐIỂM NGỌT" NGÂN SÁCH THAM SỐ TRÊN GPU 16GB VRAM

Vào thời điểm GPT-1 (2018) và GPT-2 (2019) ra đời, phần cứng mạnh mẽ nhất trong các phòng thí nghiệm AI là card đồ họa **NVIDIA Tesla V100 có 16GB VRAM**.

Với $d_{\text{model}} = 768$ và $12$ khối Transformer, tổng số tham số mô hình được tính như sau:
* **Ma trận nhúng từ & vị trí:** $(50.257 + 1024) \times 768 \approx 39.4\text{M}$
* **12 Khối Transformer Decoders:** $12 \times \approx 7.08\text{M} \approx 85\text{M}$
* **Tổng cộng:** $\approx \mathbf{124\text{M}}$ tham số (khoảng $117\text{M}$ trọng số biến đổi độc lập).

Quy mô 117M tham số cho phép huấn luyện mô hình với batch size đủ lớn (ví dụ: batch size = 64 hoặc 128) nằm trọn vẹn trong một card GPU 16GB VRAM mà không bị tràn bộ nhớ.

---

## 📊 4. MỌI BIẾN THỂ GPT-2 ĐỀU LÀ BỘI SỐ CỦA 64

Để chứng minh rằng con số $768$ bắt nguồn từ công thức $H \times 64$, hãy nhìn vào bảng thông số kỹ thuật của toàn bộ 4 phiên bản GPT-2 mà OpenAI công bố:

| Phiên bản GPT-2 | Số tầng ($L$) | Chiều ẩn ($d_{\text{model}}$) | Số đầu chú ý ($H$) | Kích thước 1 đầu ($d_k$) | Kiểm chứng toán học |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **GPT-2 Small** *(Dùng trong GPT2SP)* | **12** | **768** | **12** | **64** | $12 \times 64 = \mathbf{768}$ |
| **GPT-2 Medium** | 24 | **1024** | **16** | **64** | $16 \times 64 = \mathbf{1024}$ |
| **GPT-2 Large** | 36 | **1280** | **20** | **64** | $20 \times 64 = \mathbf{1280}$ |
| **GPT-2 XL** | 48 | **1600** | **25** | **64** | $25 \times 64 = \mathbf{1600}$ |

*Tất cả mọi biến thể đều giữ bất di bất dịch kích thước một đầu là $d_k = 64$ và tăng dần số đầu chú ý $H$, kéo theo chiều ẩn $d_{\text{model}}$ tăng lên tương ứng.*

---

## 🧬 5. 768 TỌA ĐỘ ĐÓ THỰC CHẤT CHỨA NHỮNG GÌ BÊN TRONG?

Khi in một vector trạng thái ẩn $\mathbf{h} \in \mathbb{R}^{768}$ ra màn hình, ta thấy một dãy gồm 768 số thực:
$$\mathbf{h} = [-0.1425, +0.8912, -0.0034, +1.2401, \dots, -0.5621]$$

Nhiều người mới tiếp cận thường đặt câu hỏi:  
*"Có phải tọa độ số 1 lưu thông tin từ loại (Danh từ/Động từ), tọa độ số 2 lưu thông tin thời gian, tọa độ số 3 lưu mức độ nghiêm trọng của Bug phần mềm không?"*

👉 **Câu trả lời dứt khoát là: KHÔNG! Không gian 768 chiều không hoạt động theo kiểu gán nhãn đơn lẻ như vậy.**

### 5.1. Bản chất 1: Biểu diễn phân tán (Distributed Representation)
Trong mạng nơ-ron học sâu:
* **Không có khái niệm nào nằm trọn vẹn ở một tọa độ đơn lẻ.** Một khái niệm như *"Lỗi sập ứng dụng NullPointerException"* không nằm ở chiều số 42, mà nó được **phân tán (distributed)** trải dài trên hàng trăm tọa độ cùng lúc.
* **Ngược lại, một tọa độ duy nhất không phục vụ riêng một khái niệm nào.** Tọa độ số 42 có thể vừa tham gia biểu diễn dấu câu, vừa tham gia thể hiện độ dài từ, vừa góp phần biểu đạt sắc thái lỗi kỹ thuật.

### 5.2. Bản chất 2: Hiện tượng Chồng chập đa nghĩa (Polysemanticity & Superposition)
Tại sao mô hình lại làm như vậy?  
Công trình nghiên cứu đột phá của nhóm nghiên cứu Anthropic (*"Toy Models of Superposition"*, Elhage et al., 2022) đã chỉ ra:
* Thế giới thực có hàng triệu khái niệm và thuộc tính ngữ nghĩa khác nhau (từ vựng, cú pháp, quan hệ phụ thuộc, ngữ cảnh phần mềm...).
* Nhưng mô hình chỉ có **$768$ chiều vật lý**.
* Để biểu diễn được hàng chục ngàn khái niệm trong một không gian chỉ có 768 trục tọa độ, mạng nơ-ron thực hiện cơ chế **chồng chập (Superposition)**: Nó nén các khái niệm vào các hướng hình học giao nhau gần như trực giao (almost-orthogonal directions). Các khái niệm không nằm theo các trục tọa độ chính ($x, y, z...$), mà nằm ở các **vector phương hướng (directions)** trong không gian 768 chiều!

### 5.3. Sự tiến hóa ngữ nghĩa của 768 chiều qua từng tầng (Layer Hierarchy)
Mặc dù ở mỗi tầng đều là 768 con số, nhưng nội dung thông tin chứa bên trong 768 chiều này **thay đổi hoàn toàn** khi đi từ Tầng 1 đến Tầng 12:

1. **Ở các tầng đầu (Tầng 1 – 3):** 768 tọa độ lưu trữ thông tin bề mặt (Surface features): hình thái từ vựng, tiền tố, hậu tố, dấu câu, từ loại (Noun, Verb, Adj).
2. **Ở các tầng giữa (Tầng 4 – 8):** 768 tọa độ mã hóa cấu trúc cú pháp (Syntactic features): cây phụ thuộc cú pháp, mối quan hệ chủ ngữ - vị ngữ, phạm vi ảnh hưởng của mệnh đề điều kiện (`if ... then ...`).
3. **Ở các tầng sâu (Tầng 9 – 12):** 768 tọa độ lưu trữ tri thức ngữ nghĩa trừu tượng cao cấp (High-level Semantic features): bản chất của nghiệp vụ phần mềm, độ phức tạp của logic nghiệp vụ, sự phối hợp giữa các module (`DataWeave` kết hợp với `ExpressionExecution`).

---

## 📚 6. CÁC BÀI BÁO KHOA HỌC GIẢI MÃ BÊN TRONG 768 CHIỀU (PROBING & INTERPRETABILITY)

Các nhà khoa học không chấp nhận để 768 chiều này là "chiếc hộp đen". Lĩnh vực nghiên cứu chuyên mổ xẻ các vector ẩn này được gọi là **Probing (Thăm dò biểu diễn)** và **Mechanistic Interpretability (Khả năng giải thích cơ chế)**.

Dưới đây là các công trình kinh điển thế giới đã công bố về cách giải mã 768 chiều này:

### 1. Bài báo "BERT Rediscovers the Classical NLP Pipeline" (ACL 2019)
* **Tác giả:** Ian Tenney, Dipanjan Das, Ellie Pavlick (Google Research).
* **Nội dung:** Bài báo sử dụng kỹ thuật *Edge Probing* trên không gian 768 chiều của Transformer. Nhóm tác giả phát hiện một điều kinh ngạc: mô hình nơ-ron tự động "tái phát minh" lại toàn bộ quy trình xử lý ngôn ngữ truyền thống trong 768 chiều theo đúng thứ tự các tầng: từ loại (POS) $\rightarrow$ thành phần câu (Constituents) $\rightarrow$ quan hệ cú pháp (Dependencies) $\rightarrow$ thực thể có tên (NER) $\rightarrow$ gán nhãn vai trò ngữ nghĩa (Semantic Roles).
* **Link bài báo:** [arXiv:1905.05950](https://arxiv.org/abs/1905.05950).

### 2. Bài báo "A Structural Probe for Finding Syntax in Word Representations" (NAACL 2019)
* **Tác giả:** John Hewitt, Christopher D. Manning (Stanford University).
* **Nội dung:** Bài báo chứng minh rằng cây cú pháp chuẩn của ngôn ngữ tự nhiên được mã hóa bằng **hình học khoảng cách** trong không gian 768 chiều. Cụ thể: khoảng cách Euclid bình phương giữa hai vector trong không gian 768 chiều phản ánh chính xác khoảng cách giữa hai từ trên cây cú pháp.
* **Link bài báo:** [ACL Anthology N19-1419](https://aclanthology.org/N19-1419/).

### 3. Bài báo "A Primer in BERTology: What We Know About How BERT Works" (TACL 2020)
* **Tác giả:** Anna Rogers, Olga Kovaleva, Anna Rumshisky.
* **Nội dung:** Bản tổng hợp đồ sộ hơn 150 công trình nghiên cứu mổ xẻ không gian 768 chiều của Transformer: khảo sát từng đầu chú ý trong 12 heads, phân bố giá trị trong 768 chiều, hiện tượng hình học (anisotropy) và cách tri thức thế giới được lưu trữ trong các vector này.
* **Link bài báo:** [arXiv:2002.12327](https://arxiv.org/abs/2002.12327).

### 4. Chuỗi công trình "Toy Models of Superposition" & "Towards Monosemanticity" (Anthropic 2022, 2023)
* **Tác giả:** Nelson Elhage, Trenton Bricken et al. (Anthropic Research).
* **Nội dung:** Giải thích lý do cốt lõi vì sao các tọa độ nơ-ron đơn lẻ lại không thể giải thích trực tiếp (Polysemantic). Nhóm nghiên cứu huấn luyện các mạng tự mã hóa thưa (Sparse Autoencoders - SAE) để phân tách vector 768 chiều thành hàng chục ngàn đặc trưng đơn nghĩa (monosemantic features), chứng minh rằng 768 chiều là một không gian nén tối ưu.
* **Link công trình:** [Anthropic Transformer Circuits](https://transformer-circuits.pub/2023/monosemantic-features/index.html).

---

## 🗂️ 7. CÁC BỘ DỮ LIỆU CHUẨN (DATASETS) DÙNG ĐỂ THĂM DÒ 768 CHIỀU

Để kiểm tra xem 768 chiều của một token đang chứa thông tin gì, cộng đồng nghiên cứu sử dụng các bộ dữ liệu thăm dò (Probing Datasets) sau:

1. **SentEval Benchmark (Facebook AI Research / Meta):**  
   * Bao gồm 10 bài toán thăm dò (Probing tasks) chuẩn hóa: kiểm tra độ dài câu (`Length`), thứ tự từ (`WordContent`), từ loại (`TreeDepth`), thì động từ (`Tense`), số ít/số nhiều (`SubjNum`, `ObjNum`).
   * *Nguồn:* [github.com/facebookresearch/SentEval](https://github.com/facebookresearch/SentEval).
2. **Universal Dependencies (UD) Treebanks:**  
   * Bộ dữ liệu ngôn ngữ học gán nhãn chuẩn hóa cho hơn 100 ngôn ngữ, cung cấp cây phụ thuộc cú pháp để kiểm chứng xem các phép toán trên 768 chiều có dựng lại được cấu trúc câu hay không.
   * *Nguồn:* [universaldependencies.org](https://universaldependencies.org/).
3. **Bộ dữ liệu Jira Open-Source (TAWOS Dataset):**  
   * Trong đề tài Story Point của chúng ta, tập dữ liệu gồm hàng ngàn issue từ Spring XD, Apache, Jira... Dữ liệu này được dùng để thăm dò xem 768 chiều của GPT2SP có phân biệt được độ nghiêm trọng (Severity), loại task (Bug vs. Feature) và mức nỗ lực (Story Point) hay không.

---

## 💻 8. MÃ NGUỒN PYTHON THỰC NGHIỆM: TRÍCH XUẤT, MỔ XẺ & LINEAR PROBE

Bạn hoàn toàn có thể tự chạy thử các đoạn code Python dưới đây bằng thư viện `transformers` và `torch` để trực tiếp "sờ tận tay" vào không gian 768 chiều này.

### Thực nghiệm 1: Trích xuất và mổ xẻ vector 768 chiều của một từ
Đoạn code sau nạp mô hình GPT-2, đưa vào một User Story và in ra cấu trúc thực tế của vector 768 chiều:

```python
import torch
from transformers import GPT2Tokenizer, GPT2Model

# 1. Nạp Tokenizer và Mô hình GPT-2 gốc (12 tầng, d_model = 768)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2', output_hidden_states=True)
model.eval()  # Chuyển sang chế độ Inference

# 2. Đầu vào là một câu văn kỹ thuật (tương tự issue Jira XD-4012)
text = "NullPointerException in ExpressionExecution"
inputs = tokenizer(text, return_tensors="pt")

# 3. Chạy qua mô hình mà không cần tính đạo hàm (torch.no_grad)
with torch.no_grad():
    outputs = model(**inputs)

# outputs.last_hidden_state có kích thước: [batch_size, sequence_length, 768]
hidden_states = outputs.last_hidden_state
seq_len = hidden_states.shape[1]

print(f"Kích thước ma trận biểu diễn: {hidden_states.shape}")
print(f"Số lượng tokens: {seq_len}")
print(f"Số chiều ẩn của mỗi token: {hidden_states.shape[2]} (Đúng bằng 768!)")

# 4. Trích xuất vector 768 chiều của token cuối cùng
token_last_vec = hidden_states[0, -1, :].numpy()

print("\n--- 10 TỌA ĐỘ ĐẦU TIÊN CỦA TOKEN CUỐI CÙNG TRONG 768 CHIỀU ---")
print(token_last_vec[:10])

print("\n--- THỐNG KÊ TOÁN HỌC TRÊN 768 TỌA ĐỘ ---")
print(f"Giá trị nhỏ nhất (Min): {token_last_vec.min():.4f}")
print(f"Giá trị lớn nhất (Max): {token_last_vec.max():.4f}")
print(f"Trung bình cộng (Mean): {token_last_vec.mean():.4f}")
print(f"Độ lệch chuẩn (Std):    {token_last_vec.std():.4f}")
```

---

### Thực nghiệm 2: Kỹ thuật Thăm dò Tuyến tính (Linear Probing) trên 768 chiều
Để chứng minh khoa học rằng: *"Liệu 768 chiều này có thể cho ta biết task này là Bug hay Feature hay không?"*, các nhà khoa học không đọc từng số, mà huấn luyện một **bộ phân loại tuyến tính đơn giản (Linear Probe)** trên vector 768 chiều:

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Giả sử ta có 4 vector 768 chiều được trích xuất từ 4 User Story khác nhau
# X mang kích thước [4, 768]
torch.manual_seed(42)
X_hidden_vectors = torch.randn(4, 768)

# Nhãn thực tế: 1 = Lỗi phần mềm (Bug), 0 = Tính năng mới (Feature)
y_labels = torch.tensor([1.0, 1.0, 0.0, 0.0]).unsqueeze(1)

# Thiết lập một Linear Probe: Chỉ gồm ĐÚNG 1 tầng tuyến tính 768 -> 1
probe = nn.Linear(768, 1)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.SGD(probe.parameters(), lr=0.1)

# Huấn luyện thăm dò trong 50 bước
for epoch in range(50):
    optimizer.zero_grad()
    predictions = probe(X_hidden_vectors)
    loss = criterion(predictions, y_labels)
    loss.backward()
    optimizer.step()

print("Huấn luyện Linear Probe hoàn tất!")
# Nếu probe học được với độ chính xác cao mà không cần mạng nơ-ron phức tạp,
# điều đó chứng minh: Khái niệm "Bug vs Feature" đã được phân tách tuyến tính
# một cách tự nhiên ngay bên trong không gian 768 chiều này!
```

> [!NOTE]
> **Ý nghĩa khoa học của Probing:**  
> Nếu một bộ phân loại tuyến tính đơn giản ($y = Wx + b$) có thể đoán đúng nhãn từ vector 768 chiều, điều đó chứng minh rằng **thông tin đó đã được mô hình tự động tổ chức và trích xuất sẵn** trong quá trình đọc văn bản, chứ không phải do ta ép buộc nó!

---

## 📌 9. TỔNG KẾT BẢN CHẤT CỦA CON SỐ 768

| Khía cạnh | Bản chất giải thích | Ý nghĩa thực tiễn |
| :--- | :--- | :--- |
| **Nguồn gốc công thức** | $H \times d_k = 12 \times 64 = 768$ | Phù hợp với công thức scaled dot-product attention và gradient ổn định. |
| **Khớp nối phần cứng** | Bội số của 32 threads (NVIDIA Warp) và 64 (Tensor Cores) | Khai thác 100% hiệu năng GPU, tránh lãng phí bộ nhớ đệm do padding. |
| **Dung lượng biểu diễn** | Điểm ngọt cân bằng ngân sách 117M tham số trên GPU 16GB | Đủ sâu để học ngữ nghĩa mà không gây quá tải tài nguyên máy tính. |
| **Nội dung 768 tọa độ** | Không phải nhãn đơn lẻ, mà là Biểu diễn phân tán (Distributed) | Nén hàng chục ngàn khái niệm vào không gian hình học trực giao (Superposition). |
| **Phương pháp giải mã** | Thăm dò tuyến tính (Probing) & Phân tích cơ chế (SAEs) | Được kiểm chứng qua hàng loạt bài báo uy tín thế giới (Google ACL 2019, Stanford NAACL 2019, Anthropic 2023). |
