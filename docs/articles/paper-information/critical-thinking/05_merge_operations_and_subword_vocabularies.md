# 🧠 PHÂN TÍCH PHẢN BIỆN 05: BẢN CHẤT MERGE OPERATIONS & SUBWORD VOCABULARIES (DATASET, THUẬT TOÁN & MÃ NGUỒN THỰC THI)

> **Câu hỏi phản biện mở rộng:**  
> 1. *"Merge Operations (Quy tắc sáp nhập) và Subword Vocabularies (Từ điển từ con) thực chất là gì? Chúng nằm ở khâu nào trong quy trình Transformer?"*  
> 2. *"Làm sao cỗ máy biết cách ghép từng chữ cái để phân tách các từ chuyên ngành siêu dài như `ExpressionExecutionException` hay `NullPointerException`?"*  
> 3. *"Các file dataset gốc của chúng nằm ở đâu? Có mã nguồn Python thực tế để soi vào dữ liệu và tự huấn luyện thuật toán này từ con số 0 không?"*

---

## 🎯 1. VỊ TRÍ VÀ VAI TRÒ TRONG QUY TRÌNH KIẾN TRÚC TRANSFORMER

Trong quy trình xử lý của mô hình ngôn ngữ lớn (như GPT-2 và GPT2SP), **Merge Operations** và **Subword Vocabularies** nằm ở **Khung 1: Khâu Tiền xử lý (Tokenization)** — chiếc cổng kiểm soát đầu tiên biến văn bản chữ viết của con người thành danh sách các đơn vị số học trước khi đưa vào mạng nơ-ron:

```text
[Văn bản thô của Jira Issue]:
"ExpressionExecutionException when element that expects a DW starts with space"
                                   │
                                   ▼
 [KHÂU 1: MERGE OPERATIONS & SUBWORD TOKENIZATION]  <── ĐÂY LÀ NƠI XỬ LÝ!
 Áp dụng cuốn sổ tay quy tắc sáp nhập (merges.txt) để ghép các ký tự lại,
 tạo thành danh sách 15 mẩu Subwords có mặt trong từ điển 50.257 từ (vocab.json):
 ['Exp', 'ression', 'Exec', 'ution', 'Exception', 'when', ..., 'space']
                                   │
                                   ▼
 [KHÂU 2: TRA TỪ ĐIỂN & GẮN THẺ SỐ THỨ TỰ (POS-EMBEDDING)]
 - Từ thứ 1: 'Exp'   -> Nhận 768 số nghĩa (w_1)  + 768 số vị trí ghế 1 (p_1)
 - ...
 - Từ thứ 15: 'space' -> Nhận 768 số nghĩa (w_15) + 768 số vị trí ghế 15 (p_15)
                                   │
                                   ▼
 [KHÂU 3: ĐƯA VÀO 12 TẦNG TRANSFORMER DECODERS SUY NGẪM]
 15 tờ phiếu lần lượt đi xuôi từ Khối 1 -> Khối 12.
```

---

## 🧩 2. BẢN CHẤT CỦA SUBWORD & QUY TẮC SÁP NHẬP (MERGE OPERATIONS)

### 2.1. Subword (Từ con) là gì?
Trong các dự án phần mềm, các lập trình viên thường xuyên đặt tên biến, tên hàm hoặc tên lớp rất dài (kiểu CamelCase):
* Ví dụ: `ExpressionExecutionException` *(dài 27 ký tự)*, `NullPointerException`, `SimpleMessageListenerContainer`.

Nếu dùng cách xử lý văn bản truyền thống:
* **Theo từ nguyên vẹn (Word-level):** Từ điển tiếng Anh thông thường sẽ không có từ này. Mô hình sẽ gán cho nó nhãn `<UNK>` (Unknown - Không xác định). Mô hình hoàn toàn "mù tịt" về ý nghĩa của từ.
* **Theo từng chữ cái (Character-level):** Xé từ thành 27 ký tự đơn lẻ (`E`, `x`, `p`...). Chuỗi văn bản sẽ dài gấp hàng chục lần, làm bùng nổ chi phí tính toán Self-Attention $\mathcal{O}(L^2)$ và làm mất ngữ nghĩa của từ.
* **Giải pháp Subword (Từ con):** Tách từ ghép dài thành các **mẩu Lego trung gian có nghĩa**:
  $$\text{ExpressionExecutionException} \longrightarrow \mathbf{Exp} + \mathbf{ression} + \mathbf{Exec} + \mathbf{ution} + \mathbf{Exception}$$
  Mỗi mẩu Lego này được gọi là một **Subword**. Máy tính chỉ cần học ngữ nghĩa của các mẩu này là có thể hiểu được hàng triệu từ ghép kỹ thuật phức tạp khác nhau!

### 2.2. Merge Operations (Quy tắc sáp nhập) là gì?
Làm sao máy tính biết phải ghép `E` với `x` rồi với `p` thành `Exp`, mà không ghép nhầm thành `Expre` hay `ssion`?

Đó chính là nhờ **Cuốn sổ tay quy tắc sáp nhập (Merge Operations)**:
1. **Khởi điểm:** Toàn bộ văn bản chỉ là các ký tự/byte rời rạc (`E`, `x`, `p`, `r`, `e`, `s`, `s`, `i`, `o`, `n`...).
2. **Học quy tắc ghép (Training Phase của BPE):** Thuật toán quét qua kho dữ liệu hàng chục gigabyte, đếm xem cặp ký tự nào hay đi liền kề nhau nhất để đặt ra luật sáp nhập:
   * *Luật 1:* Thấy `E` và `x` hay đi cùng nhau $\rightarrow$ Ghép `E` + `x` $\rightarrow$ `Ex`.
   * *Luật 2:* Thấy `Ex` và `p` hay đi cùng nhau $\rightarrow$ Ghép `Ex` + `p` $\rightarrow$ `Exp`.
   * *Luật 3:* Thấy `s` và `s` hay đi cùng nhau $\rightarrow$ Ghép `s` + `s` $\rightarrow$ `ss`.
   * *Luật 4:* Thấy `r` + `e` + `ss` + `i` + `o` + `n` $\rightarrow$ `ression`.
3. Quá trình này được lặp lại đúng **$50.000$ lần**, tạo ra một danh sách $50.000$ luật sáp nhập có thứ tự ưu tiên nghiêm ngặt.

---

## 📂 3. CÁC TẬP DỮ LIỆU & FILE ARTIFACT GỐC CỦA GPT-2

Thuật toán BPE được OpenAI huấn luyện trên kho ngữ liệu **WebText (khoảng 40 GB văn bản)** cào từ các bài viết Reddit có trên 3 upvotes. Kết quả xuất xưởng của quá trình huấn luyện này là **2 file dữ liệu chính thức**:

| Tên File | Quy mô | Vai trò kỹ thuật cốt lõi | Link tải chính thức |
| :--- | :---: | :--- | :--- |
| **`merges.txt`** | $50.000$ dòng ($\approx 450\text{ KB}$) | **Merge Operations:** Lưu trữ danh sách $50.000$ phép ghép cặp theo thứ tự ưu tiên từ cao xuống thấp. | [HuggingFace merges.txt](https://huggingface.co/gpt2/resolve/main/merges.txt) |
| **`vocab.json`** | $50.257$ mục ($\approx 1.0\text{ MB}$) | **Subword Vocabularies:** Bảng tra cứu ánh xạ từng từ con (Subword) sang một mã số nguyên duy nhất (Token ID từ $0$ đến $50256$). | [HuggingFace vocab.json](https://huggingface.co/gpt2/resolve/main/vocab.json) |

> [!NOTE]
> **Ký hiệu đặc biệt `Ġ` trong file:**  
> Trong file `merges.txt` và `vocab.json` của GPT-2, ký tự lạ `Ġ` (Unicode `\u0120`) được dùng để đại diện cho **ký tự khoảng trắng (Space)**.  
> Ví dụ: Token `Ġthe` nghĩa là từ `"the"` có một khoảng trắng đứng trước; trong khi `the` là chuỗi không có khoảng trắng đứng trước. Nhờ vậy, GPT-2 bảo toàn nguyên vẹn cấu trúc thụt lề và khoảng cách của mã nguồn!

---

## 💻 4. MÃ NGUỒN PYTHON THỰC NGHIỆM

Dưới đây là 3 kịch bản mã nguồn hoàn chỉnh giúp bạn kiểm chứng và tự thực thi toàn bộ quy trình:

### Thực nghiệm 1: Tải trực tiếp và "soi" vào file `merges.txt` & `vocab.json` gốc

```python
import requests
import json

# 1. Tải và đọc 10 quy tắc sáp nhập hàng đầu trong merges.txt
merges_url = "https://huggingface.co/gpt2/resolve/main/merges.txt"
res_merges = requests.get(merges_url)
merges_lines = res_merges.text.splitlines()

print("=== 10 QUY TẮC SÁP NHẬP ĐẦU TIÊN TRONG merges.txt ===")
for i, line in enumerate(merges_lines[1:11], start=1):
    print(f"Quy tắc {i:02d}: {line}")

# 2. Tải và tra cứu ID của các Subword trong Issue XD-3751 từ vocab.json
vocab_url = "https://huggingface.co/gpt2/resolve/main/vocab.json"
vocab = requests.get(vocab_url).json()

print(f"\nTổng số Subword trong từ điển: {len(vocab)} tokens")

subwords_case_study = ["Exp", "ression", "Exec", "ution", "Exception", "Ġwhen", "Ġspace"]
print("\n=== TRA CỨU ID CỦA CÁC SUBWORD (SPRING XD) ===")
for sw in subwords_case_study:
    token_id = vocab.get(sw)
    print(f"Subword: '{sw}' \t--> Token ID: {token_id}")
```

---

### Thực nghiệm 2: Tách từ BPE bằng thư viện `tiktoken` trên User Story thực tế

Thư viện `tiktoken` là công cụ triển khai BPE chuẩn hóa bằng ngôn ngữ Rust của OpenAI, cho tốc độ xử lý nhanh gấp hàng chục lần so với Python thuần:

```python
import tiktoken

# 1. Nạp bộ mã hóa BPE r50k_base (dành riêng cho GPT-2, 50.257 tokens)
enc = tiktoken.get_encoding("r50k_base")

# 2. Kiểm tra từ ghép kỹ thuật siêu dài
word = "ExpressionExecutionException"
tokens = enc.encode(word)
subwords = [enc.decode([t]) for t in tokens]

print(f"Từ kỹ thuật gốc: {word}")
print(f"Mã Token IDs: {tokens}")
print(f"Các Subwords sau khi áp dụng Merge Operations: {subwords}")

# 3. Phân tách toàn bộ tiêu đề Issue XD-3751
title = "ExpressionExecutionException when element that expects a DW starts with space"
all_tokens = enc.encode(title)

print(f"\nTiêu đề Issue: '{title}'")
print(f"Tổng số mẩu Subword tạo thành: {len(all_tokens)}")
for idx, t in enumerate(all_tokens, start=1):
    print(f"Vị trí {idx:02d}: Token ID={t:<5} | Subword='{enc.decode([t])}'")
```

---

### Thực nghiệm 3: Tự xây dựng thuật toán BPE từ con số 0 (Vanilla BPE Training)

Đoạn code sau mô phỏng chính xác thuật toán đếm tần suất và sáp nhập cặp ký tự mà OpenAI đã chạy trên 40 GB văn bản:

```python
import collections

# Kho ngữ liệu đồ chơi mô phỏng các từ và tần suất xuất hiện
corpus = {
    'l o w </w>': 5,
    'l o w e r </w>': 2,
    'n e w e s t </w>': 6,
    'w i d e s t </w>': 3
}

def get_stats(corpus):
    """Đếm tần suất xuất hiện của tất cả các cặp ký hiệu liền kề"""
    pairs = collections.defaultdict(int)
    for word, freq in corpus.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, corpus):
    """Sáp nhập cặp ký hiệu có tần suất cao nhất thành một token mới"""
    new_corpus = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word in corpus:
        new_word = word.replace(bigram, replacement)
        new_corpus[new_word] = corpus[word]
    return new_corpus

# Huấn luyện tìm 5 quy tắc sáp nhập (Merge Operations) đầu tiên
num_merges = 5
print("=== TIẾN TRÌNH HỌC QUY TẮC SÁP NHẬP BPE ===")
for step in range(num_merges):
    pairs = get_stats(corpus)
    if not pairs:
        break
    best_pair = max(pairs, key=pairs.get)
    corpus = merge_vocab(best_pair, corpus)
    print(f"Bước {step + 1}: Ghép cặp '{best_pair[0]}' + '{best_pair[1]}' (Tần suất xuất hiện: {pairs[best_pair]} lần)")

print("\nKho từ vựng sau khi áp dụng các quy tắc sáp nhập:")
for word, freq in corpus.items():
    print(f"  {word} : {freq}")
```

---

## 🏆 5. TÁC ĐỘNG QUYẾT ĐỊNH ĐỐI VỚI ĐỀ TÀI ƯỚC LƯỢNG STORY POINT (GPT2SP VS. DEEP-SE)

Sự kết hợp giữa **Merge Operations** và **Subword Vocabularies** chính là "vũ khí bí mật" giúp GPT2SP đánh bại hoàn toàn các mô hình truyền thống (như Deep-SE):

1. **Khắc phục triệt để lỗi Out-Of-Vocabulary (OOV):**  
   Trong các dự án phần mềm mới, liên tục xuất hiện các thư viện, framework và tên biến mới lạ. Mô hình Deep-SE (sử dụng Word2Vec/FastText cố định) coi các từ này là `<UNK>`, làm mất toàn bộ ngữ cảnh kỹ thuật. Trong khi đó, GPT2SP nhờ có $50.000$ quy tắc sáp nhập sẽ dễ dàng xẻ nhỏ bất kỳ từ mới nào thành các mẩu Subwords quen thuộc để hiểu trọn vẹn ý nghĩa.
2. **Bảo toàn ngữ nghĩa trong giới hạn chiều dài:**  
   Bằng cách nén các cụm ký tự phổ biến thành từ con, chuỗi văn bản không bị xé quá dài, giúp toàn bộ User Story nằm gọn trong phạm vi ngữ cảnh $1024$ tokens của GPT-2 mà không cần cắt xén (truncation).
