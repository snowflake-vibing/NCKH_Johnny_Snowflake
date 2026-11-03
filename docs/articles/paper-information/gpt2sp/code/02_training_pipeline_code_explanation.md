# 📖 GIẢI THÍCH CHI TIẾT MÃ NGUỒN HUẤN LUYỆN & THỰC NGHIỆM (`model_training_notebook.ipynb`)
## ĐỐI SOÁT TỪNG DÒNG CODE VÀ BẢN CHẤT LOGIC CỦA PIPELINE THỰC NGHIỆM

> **Mã nguồn phân tích:** File [`model_training_notebook.ipynb`](https://github.com/awsm-research/gpt2sp/blob/main/model_training_notebook.ipynb) trong Replication Package.  
> **Chương đối ứng trong bài báo gốc:** **Section 4: Experimental Setup** & **Section 5: Results** (Trang 5 – 10, IEEE TSE 2023).

---

## 🧭 1. LOGIC TỔNG THỂ CỦA PIPELINE THỰC NGHIỆM

Toàn bộ quy trình thực nghiệm trong notebook gốc được xây dựng nhằm giải quyết hai câu hỏi nghiên cứu cốt lõi:
* **RQ1 (Within-Project):** Huấn luyện trên $60\%$ dữ liệu quá khứ của một dự án, tinh chỉnh trên $20\%$ xác thực, và kiểm thử trên $20\%$ công việc tương lai của chính dự án đó.
* **RQ2 (Cross-Project):** Huấn luyện trên toàn bộ một hoặc nhiều dự án nguồn (Source Projects) và kiểm thử khả năng chuyển giao tri thức sang một dự án đích (Target Project) hoàn toàn mới.

Để hiện thực hóa điều này, nhóm tác giả chia nhỏ mã nguồn thành 5 khối logic xử lý dữ liệu và mô hình liên hoàn:

---

## 🔍 2. GIẢI PHẪU TỪNG KHỐI CODE VÀ LOGIC ĐẰNG SAU

### 2.1. Logic cấu hình siêu tham số toàn cục (Cell 4)

```python
EPOCHS = 20
BATCH_SIZE_RATIO = 0.3 # within proj: 0.3 / cross proj: 0.4
SEQUENCE_LEN = 20
LEARNING_RATE = 5e-4
TOKENIZER = 'gpt2'
MODEL_NAME = 'gpt2sp'
DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
```

#### 💡 Logic kỹ thuật đằng sau từng tham số:
1. `SEQUENCE_LEN = 20`:
   * **Bản chất logic:** Giới hạn độ dài tối đa của câu văn bản đưa vào mô hình là 20 tokens.
   * **Đánh đổi phương pháp luận:** Việc chọn con số 20 là nguyên nhân trực tiếp khiến mô hình chỉ đọc được vài từ đầu tiên của tiêu đề User Story và loại bỏ hoàn toàn phần mô tả chi tiết (`Description`). Tuy nhiên, nó giúp giảm chi phí tính toán ma trận Attention từ $\mathcal{O}(1024^2) \approx 10^6$ xuống $\mathcal{O}(20^2) = 400$ phép tính (nhanh hơn $2.500$ lần).
2. `BATCH_SIZE_RATIO = 0.3`:
   * **Cơ chế Dynamic Batch Size:** Thay vì cố định kích thước lô là 16 hay 32 mẫu, tác giả lấy batch size bằng $30\%$ quy mô tập train.
   * **Hệ quả logic:** Một epoch huấn luyện chỉ có vỏn vẹn khoảng $3$ đến $4$ bước cập nhật gradient (`steps`), giúp quá trình huấn luyện hoàn thành chớp nhoáng trong vài giây.
3. `LEARNING_RATE = 5e-4`:
   * Tốc độ học lớn gấp 10 đến 25 lần so với mức chuẩn khi tinh chỉnh Transformer ($2\times 10^{-5}$), giúp đầu hồi quy MLP mới khởi tạo ngẫu nhiên nhanh chóng bắt kịp quy mô điểm Story Point.

---

### 2.2. Logic nạp dữ liệu và lọc đặc trưng (`prepare_dataframe`)

```python
def prepare_dataframe(file_name):
    data = pd.read_csv(file_name)
    # some rows have no description, fill blank to avoid Null
    data = data.fillna(' ')
    d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
    return pd.DataFrame(data=d)
```

#### 💡 Logic đằng sau từng câu lệnh:
1. `data = pd.read_csv(file_name)`: Nạp các file CSV tĩnh được trích xuất từ Jira (mỗi dòng gồm `issuekey`, `title`, `description`, `storypoint`, `split_mark`).
2. `data = data.fillna(' ')`: Thay thế các giá trị khuyết (NaN) bằng khoảng trắng để tránh lỗi crash khi nạp vào bộ tách từ BPE.
3. `d = {'text': (data['title']).tolist(), 'label': data['storypoint']}`:
   * **Điểm then chốt:** Tác giả gán trường `data['title']` vào cột `text`. Cột `data['description']` hoàn toàn bị bỏ quên và không hề xuất hiện trong DataFrame đầu ra!
   * Điều này chứng minh 100% dữ liệu thực nghiệm thực tế chỉ dựa trên Tiêu đề của User Story.

---

### 2.3. Logic phân chia tập dữ liệu nhân quả theo thời gian (`within_project_split`)

```python
def within_project_split(data):
    print('within project split!')
    train_val_split_point = int(len(data) * 0.6)
    val_test_split_point = int(len(data) * 0.8)
    train_text = data['text'][:train_val_split_point]
    train_labels = data['label'][:train_val_split_point]
    val_text = data['text'][train_val_split_point:val_test_split_point]
    val_labels = data['label'][train_val_split_point:val_test_split_point]
    test_text = data['text'][val_test_split_point:]
    test_labels = data['label'][val_test_split_point:]
    return train_text, train_labels, val_text, val_labels, test_text, test_labels   
```

#### 💡 Logic phân tách không gian thời gian (Chronological Splitting):
* **Tại sao không dùng `train_test_split(..., shuffle=True)` ngẫu nhiên?**
  * Trong kỹ nghệ phần mềm, công việc phát triển diễn ra theo trình tự thời gian liên tục. Nếu xới tung ngẫu nhiên (Random Split), mô hình sẽ lấy kiến thức của năm 2016 để đi dự đoán Story Point của năm 2013 (vi phạm nguyên lý nhân quả).
* **Cơ chế cắt lát tuần tự:**
  * Dữ liệu trong CSV đã được sắp xếp tăng dần theo thời gian tạo ticket (`created_date`).
  * $60\%$ đầu tiên: Quá khứ xa nhất $\rightarrow$ Tập Huấn luyện (`Train`).
  * $20\%$ tiếp theo ($60\% \rightarrow 80\%$): Quá khứ gần $\rightarrow$ Tập Xác thực (`Validation`) dùng để chọn epoch tối ưu.
  * $20\%$ cuối cùng ($80\% \rightarrow 100\%$): Tương lai $\rightarrow$ Tập Kiểm thử độc lập (`Test`) mô phỏng các Sprint sắp tới.

---

### 2.4. Logic phân tách từ con Byte-Pair Encoding (`tokenization`)

```python
    elif TOKENIZER == 'gpt2':
        print('using pretrained gpt-2 tokenizer')
        tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER)
        tokenizer.pad_token = '[PAD]'
        return tokenizer.batch_encode_plus(
            text_list, 
            truncation=True, 
            max_length=SEQUENCE_LEN, 
            padding='max_length'
        )
```

#### 💡 Logic xử lý ngôn ngữ tự nhiên:
1. `tokenizer.pad_token = '[PAD]'`:
   * Vì GPT-2 được huấn luyện không có token đệm đặc biệt, tác giả gán nhãn chuỗi `[PAD]` làm pad token để các câu ngắn có cùng chiều dài vector với các câu dài trong lô.
2. `truncation=True, max_length=20, padding='max_length'`:
   * Đảm bảo mọi mẫu văn bản khi chuyển thành ma trận số nguyên (token IDs) đều có chiều dài cố định đúng $20$ phần tử:
     * Câu dài hơn 20 tokens: Bị cắt cụt ở token thứ 20.
     * Câu ngắn hơn 20 tokens: Được bổ sung các ID tương ứng của `[PAD]` ở phía sau.

---

### 2.5. Logic vòng lặp huấn luyện, chọn mô hình và đánh giá sai số (`train_eval_test`)

```python
    optimizer = AdamW(MODEL.parameters(), lr=LEARNING_RATE)    
    total_steps = len(train_dataloader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
```

#### 💡 Logic tối ưu hóa:
* `AdamW`: Tách biệt việc suy giảm trọng số (Weight Decay) ra khỏi cập nhật gradient, giúp ổn định quá trình học của mạng Transformer.
* `get_linear_schedule_with_warmup`: Giảm dần tốc độ học theo hàm bậc nhất từ $5\times 10^{-4}$ về $0$, giúp mô hình hội tụ êm ái ở các epoch cuối mà không bị dao động quanh điểm cực trị.

```python
        # Kiểm tra loss trên tập Validation để chọn Checkpoint tốt nhất
        if avg_eval_loss <= min_eval_loss_epoch[0]:
            min_eval_loss_epoch[0] = avg_eval_loss
            min_eval_loss_epoch[1] = e
        
        torch.save(model.state_dict(), './models/' + 'epo_' + str(e))
```

#### 💡 Logic lựa chọn mô hình khách quan (Early Stopping / Checkpoint Selection):
* Mô hình được đánh giá trên tập **Validation** ở mỗi epoch.
* Epoch nào đạt mức sai số tuyệt đối trung bình $L_1$ thấp nhất trên tập Validation (`min_eval_loss_epoch[0]`) sẽ được chọn làm đại diện cuối cùng.
* **Nguyên tắc khoa học:** Hoàn toàn không dùng tập Test để chọn mô hình, tránh hiện tượng thiên kiến xác nhận (*Data Snooping Bias*).

```python
            # Đo lường sai số trên tập kiểm thử Test
            distance_records = []
            for i in range(len(predictions)):
                for j in range(len(predictions[i])):
                    distance = abs(predictions[i][j] - true_labels[i][j])
                    distance_records.append(distance)

            MAE = np.mean(np.array(distance_records)) 
            MdAE = np.median(np.array(distance_records)) 
```

#### 💡 Logic tính toán thước đo sai số:
* Với mỗi mẫu kiểm thử, tính khoảng cách tuyệt đối giữa điểm Story Point dự đoán và nhãn thực tế:
  $$\text{distance}_k = |\hat{y}_k - y_k|$$
* `MAE = np.mean(...)`: Đo lường độ lớn sai số trung bình (Mean Absolute Error).
* `MdAE = np.median(...)`: Đo lường sai số trung vị (Median Absolute Error), bỏ qua các ngoại lai quá lớn.

---

## 📋 3. BẢNG TỔNG KẾT LOGIC PIPELINE HUẤN LUYỆN

| Bước kỹ thuật | Lệnh thực thi trong Notebook | Logic nghiệp vụ & Bản chất khoa học |
| :--- | :--- | :--- |
| **Cấu hình siêu tham số** | `SEQUENCE_LEN = 20`, `RATIO = 0.3` | Thu hẹp ngữ cảnh để đẩy tốc độ tính toán lên cực đại trên 1 GPU. |
| **Tiền xử lý văn bản** | `d = {'text': data['title']}` | Chỉ trích xuất tiêu đề; toàn bộ mô tả chi tiết bị loại bỏ khỏi luồng học. |
| **Phân chia dữ liệu** | `within_project_split()` | Phân chia nhân quả thời gian 60/20/20 bảo toàn trật tự quá khứ $\rightarrow$ tương lai. |
| **Bộ nạp DataLoader** | `RandomSampler` vs `SequentialSampler` | Xáo trộn ngẫu nhiên khi train để phá vỡ tương quan chuỗi; giữ nguyên khi test. |
| **Chọn Checkpoint** | `min_eval_loss_epoch` | Chọn epoch có sai số validation nhỏ nhất để kiểm thử độc lập. |
| **Đánh giá hiệu năng** | `np.mean(distance_records)` | Tính chỉ số MAE làm thước đo trung tâm so sánh với 9 mô hình baseline. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📜 [00_full_source_code.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/00_full_source_code.md): Toàn bộ mã nguồn gốc GPT2SP.
* 🧠 [01_architecture_code_explanation.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/01_architecture_code_explanation.md): Giải thích chi tiết mã nguồn kiến trúc mô hình `GPT2SP.py`.
* ⚠️ [03_code_vs_paper_discrepancies.md](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/03_code_vs_paper_discrepancies.md): Mổ xẻ 4 điểm sai lệch cốt tử giữa code thực tế và bài báo.
* 📖 [Chương 4: Thiết lập thực nghiệm (Explanation)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/04_experimental_setup.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
