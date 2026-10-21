# 🧠 PHÂN TÍCH PHẢN BIỆN 01: NGUỒN GỐC VÀ BẢN CHẤT KÍCH THƯỚC TỪ ĐIỂN BPE (50.257 TOKENS)

> **Câu hỏi phản biện:**  
> *"Tại sao từ điển từ con (Subword Vocabularies) của GPT-2 và GPT2SP lại có đúng 50.257 tokens? Con số này từ đâu ra, và người ta huấn luyện đến đó thôi à hay có thể huấn luyện thêm?"*

---

## 🎯 1. NGUỒN GỐC TOÁN HỌC CỦA CON SỐ 50.257

Con số **$50.257$** không phải là một con số ngẫu nhiên, mà là kết quả của một phép cộng đại số chuẩn xác gồm 3 thành phần trong thuật toán **Byte-level Byte-Pair Encoding (BPE)** do OpenAI đề xuất (Radford et al., 2019):

```text
  256 Ký tự Byte cơ sở ban đầu (Bytes 0x00 → 0xFF)
+ 50.000 Phép sáp nhập hình vị tần suất cao (Merge Operations)
+      1 Token đặc biệt báo hiệu kết thúc (<|endoftext|>)
-----------------------------------------------------------------
= 50.257 TOKENS TRONG BỘ TỪ ĐIỂN CHUẨN CỦA GPT-2
```

### Chi tiết 3 thành phần cấu tạo:

1. **256 Token Byte gốc ($256$ tokens — Chỉ số ID từ $0$ đến $255$):**
   * Trong máy tính, một byte bao gồm 8 bit, cho phép biểu diễn $2^8 = 256$ giá trị khả dĩ (từ `0x00` đến `0xFF`).
   * Thay vì bắt đầu từ bảng chữ cái tiếng Anh (Unicode characters), OpenAI bắt đầu thuật toán BPE trực tiếp ở **cấp độ Byte thô**.
   * *Hệ quả đột phá:* Bất kỳ chuỗi văn bản nào trên thế giới (kể cả tiếng Việt, tiếng Trung, emoji, hay mã nhị phân) đều được phân rã thành chuỗi các byte. Nhờ có 256 byte cơ sở này, mô hình **không bao giờ bị lỗi Out-of-Vocabulary (OOV)**.

2. **50.000 Phép sáp nhập BPE ($50.000$ tokens — Chỉ số ID từ $256$ đến $50.255$):**
   * OpenAI cho thuật toán quét qua kho ngữ liệu khổng lồ **WebText (40GB văn bản)**.
   * Thuật toán thống kê cặp byte/ký hiệu liền kề nào xuất hiện nhiều nhất và sáp nhập chúng thành một token mới (ví dụ: `t` + `h` $\rightarrow$ `th`; `th` + `e` $\rightarrow$ `the`).
   * Quá trình này được lặp lại chính xác **$50.000$ lần**, sinh ra $50.000$ từ con phổ biến nhất trong ngôn ngữ tự nhiên và lập trình.

3. **1 Token đặc biệt ($1$ special token — Chỉ số ID: $50.256$):**
   * OpenAI bổ sung đúng 1 token đặc biệt có tên là `<|endoftext|>`.
   * Token này đóng vai trò như dấu phân cách tài liệu (document delimiter) hoặc ký hiệu kết thúc sinh văn bản.

$$\text{Tổng số lượng từ vựng } |V| = 256 + 50.000 + 1 = \mathbf{50.257}$$

---

## 🤔 2. NGƯỜI TA HUẤN LUYỆN ĐẾN ĐÓ THÔI À? CÓ THỂ HUẤN LUYỆN THÊM KHÔNG?

**Câu trả lời ngắn gọn:** Đúng vậy, OpenAI đã **chủ động dừng lại ở $50.000$ phép merge**!  
$50.000$ là một **siêu tham số (hyperparameter)** được lựa chọn dựa trên bài toán tối ưu hóa đánh đổi (Trade-off).

Về mặt lý thuyết, người ta hoàn toàn có thể tiếp tục cho thuật toán chạy thêm $100.000$ hay $200.000$ phép merge nữa. Tuy nhiên, nếu làm vậy, mô hình sẽ phải đối mặt với **bài toán đánh đổi hai chiều (Dual Trade-off)**:

```mermaid
flowchart LR
    A["Số Phép Merge BPE (K)"] -->|K Quá Nhỏ\n(ví dụ: 10.000)| B["TỪ ĐIỂN NHỎ\n- Chuỗi token bị xé rất dài\n- Bùng nổ chi phí Attention O(L^2)\n- Tràn giới hạn ngữ cảnh 1024"]
    A -->|K Quá Lớn\n(ví dụ: 200.000)| C["TỪ ĐIỂN PHÌNH TO\n- Ma trận nhúng W_te ngốn VRAM\n- Nhiều token hiếm không học đủ dữ liệu\n- Tham số bị phân mảnh"]
    A -->|K = 50.000\n(Điểm Cân Bằng)| D["ĐIỂM NGỌT (SWEET SPOT)\n- Cân bằng tối ưu giữa độ dài câu và kích thước ma trận nhúng"]
```

### Bảng phân tích đánh đổi thực nghiệm:

| Tiêu chí kỹ thuật | Khi số Merges quá nhỏ ($K \approx 10.000$) | Điểm dừng tối ưu của GPT-2 ($K = 50.000$) | Khi số Merges quá lớn ($K \ge 150.000$) |
| :--- | :--- | :--- | :--- |
| **Kích thước từ điển $|V|$** | Rất nhỏ ($\approx 10.257$ tokens) | **$50.257$ tokens** | Rất lớn ($\ge 150.000$ tokens) |
| **Độ dài chuỗi token ($L$)** | Bị xé vụn thành quá nhiều mẩu nhỏ. | Độ dài trung bình, giữ nguyên phần lớn các từ kỹ thuật thông dụng. | Rất ngắn (nhiều cụm từ dài được gộp thành 1 token duy nhất). |
| **Chi phí tính toán Self-Attention** | Bùng nổ dữ dội vì độ phức tạp là $\mathcal{O}(L^2)$. Rất dễ vượt quá giới hạn 1024 tokens. | Tối ưu, vừa vặn trong phạm vi tính toán của GPU. | Rất thấp ở tầng Attention do chuỗi $L$ ngắn. |
| **Kích thước ma trận nhúng ($W_{te}$)** | Rất nhỏ ($10.257 \times 768 \approx 7.8\text{M}$ tham số). | **$50.257 \times 768 \approx 38.6\text{M}$ tham số** (chiếm $\approx 33\%$ mô hình GPT-2 Small). | Bùng nổ khổng lồ ($200.000 \times 768 \approx 153.6\text{M}$ tham số, lớn hơn toàn bộ phần còn lại của mô hình!). |
| **Khả năng học trọng số (Generalization)** | Tốt (mỗi token xuất hiện rất nhiều lần). | Cân bằng hoàn hảo. | Kém (nhiều từ con cực hiếm, chỉ xuất hiện 1-2 lần trong toàn bộ 40GB văn bản, không học được vector ngữ nghĩa chuẩn). |

---

## 🔬 3. TÁC ĐỘNG THỰC NGHIỆM TRONG BÀI BÁO GPT2SP

Trong bài báo *GPT2SP* (IEEE TSE 2023), quyết định kế thừa bộ từ điển $50.257$ tokens của GPT-2 đã mang lại bước nhảy vọt có tính quyết định trước đối thủ **Deep-SE**:

1. **Thu hẹp $73\%$ kích thước từ vựng so với Deep-SE:**  
   * Deep-SE dùng Word-level Tokenization, tích lũy tới **$185.625$ từ duy nhất**. Ma trận từ của Deep-SE vừa khổng lồ, vừa thưa thớt, vừa không thể chia sẻ giữa các dự án.
   * GPT2SP giảm xuống còn **$50.257$ tokens**, gọn hơn $73\%$ nhưng lại biểu diễn được phạm vi ngôn ngữ rộng hơn gấp nhiều lần.
2. **Khắc phục hoàn toàn lỗi Out-of-Vocabulary (OOV):**  
   * Trong Deep-SE, các thuật ngữ kỹ thuật ghép như `ExpressionExecutionException` bị gán nhãn `<UNK>` do chưa từng thấy trong tập train.
   * Trong GPT2SP, từ điển $50.257$ tokens phân tách khéo léo thành:
     $$\left[\text{"Exp"}, \text{"ression"}, \text{"Exec"}, \text{"ution"}, \text{"Exception"}\right]$$
     Tất cả 5 mảnh này đều nằm sẵn trong $50.257$ tokens và đều có vector nhúng giàu ý nghĩa.

---

## 📌 4. TỔNG KẾT

* **Con số 50.257** = $256$ byte cơ sở + $50.000$ phép merge BPE + $1$ token `<|endoftext|>`.
* **Người ta dừng ở 50.000** vì đây là **"điểm ngọt" (Sweet Spot)** toán học: đủ lớn để câu văn không bị xé vụn (tránh bùng nổ chi phí tính toán $\mathcal{O}(L^2)$ của Attention), nhưng cũng đủ nhỏ để ma trận nhúng từ không phình to đè bẹp dung lượng VRAM của GPU.
