# 🧠 PHÂN TÍCH PHẢN BIỆN 15: GIẢI MÃ KHO MÃ NGUỒN AWMS-RESEARCH/GPT2SP, NGUỒN GỐC TRÍCH XUẤT VÀ Ý NGHĨA TÁI LẬP

> **Câu hỏi phản biện của nhà nghiên cứu:**  
> 1. *"Kho mã nguồn GitHub `https://github.com/awsm-research/gpt2sp` thực chất lưu trữ những gì bên trong và cấu trúc của nó ra sao?"*  
> 2. *"Làm thế nào để biết được đường link này? Vị trí chính xác (Trang, Cột, Tọa độ, Ngữ cảnh văn bản) trong bài báo gốc IEEE TSE 2023 ở đâu?"*  
> 3. *"Khi mổ xẻ mã nguồn thực tế trong repository này, nhóm nghiên cứu đã phát hiện ra những bí mật phương pháp luận và sai lệch chấn động nào so với những gì bài báo công bố?"*  
> 4. *"Nhóm NCKH 3 (Johnny Snowflake) cần ứng xử như thế nào với repository này để phục vụ đề tài nghiên cứu?"*

---

## 🎯 1. NGUỒN GỐC ĐƯỜNG LINK: TÌM THẤY TỪ ĐÂU TRONG BÀI BÁO GỐC?

Đường dẫn [`https://github.com/awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp) **không phải do phỏng đoán hay tìm kiếm bên ngoài**, mà được **chính nhóm tác giả công bố chính thức ngay trong bài báo khoa học gốc** trên tạp chí *IEEE Transactions on Software Engineering (TSE 2023)*:
* **Tên bài báo:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach*.
* **Tác giả:** Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Melbourne, Úc).
* **Tập tin PDF trong repo:** [`docs/articles/paper_gpt2sp.pdf`](file:///d:/NCKH_3/docs/articles/paper_gpt2sp.pdf).

### 📍 Tọa độ & Vị trí văn bản cụ thể trong PDF:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ VỊ TRÍ 1: TRANG 2, CỘT 2 (DÒNG CUỐI CÙNG CỦA PHẦN ĐẶT VẤN ĐỀ - SECTION 1 INTRODUCTION)│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Tọa độ PDF Box: (x: 312.0, y: 703.4) đến (x: 563.0, y: 749.4)                        │
│ • Đoạn văn bản nguyên văn:                                                             │
│   "Open Science. To facilitate future work, we publish the studied dataset, scripts,   │
│   and experimental results (e.g., raw predictions) in GitHub (https://github.com/      │
│   awsm-research/gpt2sp)."                                                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

Ngoài ra, link này còn được củng cố tại hai vị trí khác trong bài báo:
* **Trang 2, Cột 2 (y: 658.1 - 692.0):** Công bố link ứng dụng Web Streamlit đi kèm:  
  `https://share.streamlit.io/awsm-research/gpt2sp_webapp/main/app.py`.
* **Trang 15, Cột 1 (y: 455.8 - 573.4 - Mục Lời Cảm Ơn / Acknowledgments):**  
  Tác giả tái khẳng định việc công bố toàn diện Replication Package gồm: tập dữ liệu, scripts cài đặt, raw predictions, web tool và các mô hình checkpoint trên Hugging Face.

---

## 🏗️ 2. BÊN TRONG REPOSITORY `awsm-research/gpt2sp` CÓ NHỮNG GÌ?

Tổ chức **`awsm-research`** (viết tắt của *Analytics for Workflow, Software and Machines* — phòng thí nghiệm nghiên cứu của GS. Chakkrit Tantithamthavorn tại Monash University) đã tổ chức repository theo cấu trúc cây thư mục sau:

```text
awsm-research/gpt2sp/
├── .DS_Store
├── LICENSE                              # Giấy phép mã nguồn mở (MIT License)
├── README.md                            # Hướng dẫn tái lập thực nghiệm và tài liệu mô tả
├── GPT2SP.py                            # Module PyTorch định nghĩa kiến trúc lớp GPT2SP
├── model_training_notebook.ipynb        # Jupyter Notebook huấn luyện mô hình GPT2SP & Baselines
├── tokenizer_training_notebook.ipynb    # Notebook huấn luyện 4 bộ Tokenizer (BPE, WordPiece...)
├── vocab_and_tokenization_comparison.ipynb # Notebook đối chiếu hiệu quả tokenization
├── GPT2SP_inspection_notebook.ipynb     # Notebook trích xuất giải thích XAI (Integrated Gradients)
│
├── sp_dataset/                          # Thư mục chứa dữ liệu nghiên cứu
│   └── marked_data/                     # 16 file CSV của 16 dự án mã nguồn mở (Choetkiertikul 2016)
│                                        # Mỗi file có 5 cột: issuekey, title, description,
│                                        # storypoint, split_mark (TRAIN / VAL / TEST)
├── all_tokenizers/                      # Checkpoints từ điển: BPE, WordPiece, SentencePiece, WordLevel
├── custom_transformers_interpret/       # Thư viện tính Integrated Gradients tùy biến
├── data_model_analysis/                 # Kết quả phân tích thống kê phân phối điểm Story Point
├── abe0/                                # Mã nguồn baseline tương đồng ABE0 + Hyperopt
├── xai_tokens/                          # Danh sách các từ khóa quan trọng được trích xuất
└── logo/                                # Logo hiển thị của dự án
```

---

## 🔍 3. MỔ XẺ MÃ NGUỒN: BÓC TRẦN 4 BÍ MẬT & SAI LỆCH SO VỚI BÀI BÁO

Khi nhóm nghiên cứu NCKH Johnny Snowflake trực tiếp rà soát và tải mã nguồn từ repo này về chạy thử, chúng tôi đã phát hiện **4 sự thật gây chấn động về mặt phương pháp luận**:

### 3.1. Bí mật 1: Lớp `GPT2SP.py` thực chất kế thừa `GPT2PreTrainedModel`
Trong file [`GPT2SP.py`](https://github.com/awsm-research/gpt2sp/blob/main/GPT2SP.py), mô hình được định nghĩa với tên lớp `GPT2ForSequenceClassification` kế thừa từ Hugging Face:
```python
class GPT2ForSequenceClassification(GPT2PreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)
        self.init_weights()
```
* Tác giả không dùng cơ chế sinh từ (Causal LM Head) mà thay thế bằng **MLP Regressor Head 2 tầng** với kích thước $768 \rightarrow 3072 \rightarrow 768 \rightarrow 1$.
* Điều này xác nhận mô hình hoàn toàn là một mạng hồi quy (Regression Network).

---

### 3.2. Sai lệch 2 (Chí mạng): Tác giả chỉ huấn luyện trên `Title` (Bỏ rơi toàn bộ `Description`)
* **Trong bài báo (Mục 4.2, Trang 6):** Tác giả khẳng định ghép cả tiêu đề và mô tả chi tiết: `text = Title + " " + Description` với độ dài tối đa lên tới $1024$ tokens.
* **Nhưng trong file `model_training_notebook.ipynb` (Cell 6):**
  ```python
  # TRÍCH XUẤT TỪ CODE GỐC CỦA TÁC GIẢ TẠI CELL 6:
  d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
  return tokenizer.batch_encode_plus(text_list, truncation=True, max_length=SEQUENCE_LEN, padding='max_length')
  ```
  👉 **Sự thật bộc lộ:** Biến `data['description']` hoàn toàn bị bỏ qua! Tác giả chỉ nạp duy nhất một cột `data['title']` và ép `max_length` xuống vỏn vẹn **20 tokens**!  
  Toàn bộ các logic nghiệp vụ, yêu cầu kỹ thuật và chi tiết lỗi nằm trong phần mô tả đã bị vứt bỏ trong mã nguồn huấn luyện thực tế.

---

### 3.3. Bí ẩn 3: Lý do thời gian huấn luyện "siêu tốc" 3 giây – 39 giây
Tại Bảng 4 của bài báo, tác giả công bố thời gian train trên 1 GPU RTX 3090 cực nhanh: `Jira` mất 3s, `Spring XD` mất 35s.
* **Bản chất phần cứng:** Không một card GPU nào có thể tính forward/backward cho 117M tham số qua 12 khối Transformer với chuỗi 1024 tokens trong 35 giây cho 3.526 issues.
* **Nguyên nhân thực sự từ code:** Vì tác giả chỉ đưa vào chuỗi tiêu đề **20 tokens** và chạy số epochs tối thiểu (1 đến 3 epochs)! Mô hình chưa hề kịp học sâu ngữ nghĩa phần mềm.

---

### 3.4. Sai lệch 4: Lỗi tính toán MAE được nhóm nghiên cứu UCL vạch trần
Trong bài báo phản biện độc lập công bố trên arXiv (*arXiv:2209.00437*), nhóm tác giả Vali Tawosi & Federica Sarro (SOLAR Lab - University College London) đã chỉ ra một **lỗi logic tính MAE trong notebook gốc**:
* Do cách tính trung bình không đồng đều giữa các batch trong quá trình tính loss, con số MAE hiển thị trong notebook bị **giảm đi một cách giả tạo**.
* Khi sửa lại đúng công thức MAE chuẩn tắc, sai số của GPT2SP tăng vọt.

---

## ⚖️ 4. BẢNG ĐỐI SOÁT TÁI LẬP: BÀI BÁO VS. CHECKPOINT THỰC TẾ TRÊN SPRING XD

Để kiểm chứng tính trung thực khoa học theo đúng nguyên tắc của [AGENTS.md](file:///d:/NCKH_3/AGENTS.md), Nhóm 3 đã tải trực tiếp checkpoint chính thức của tác giả từ Hugging Face Hub ([`MickyMike/0-GPT2SP-springxd`](https://huggingface.co/MickyMike/0-GPT2SP-springxd)) về và chạy đánh giá trên tập kiểm thử:

| Phương pháp đánh giá | MAE công bố trong bài báo (*IEEE TSE*) | MAE đo lường thực tế từ Checkpoint tác giả | Đánh giá so với Baseline |
| :--- | :---: | :---: | :--- |
| **Median Effort Baseline** | 1.72 | **1.7153** | Mốc chuẩn tham chiếu |
| **Mean Effort Baseline** | 2.15 | **2.1480** | Thua Median |
| **GPT2SP (Fu et al. Công bố)** | **0.96** | — | Con số lý thuyết trên bài báo |
| **GPT2SP (Checkpoint tác giả chạy thực tế)** | — | **1.7330** | ❌ **THUA CẢ MEDIAN BASELINE (+0.0177)** |

> [!CAUTION]
> **KẾT LUẬN THẨM ĐỊNH KHOA HỌC:**  
> Mô hình GPT2SP nguyên bản trong repository `awsm-research/gpt2sp` **hoàn toàn không thể tái lập lại kết quả $\text{MAE} = 0.96$ như bài báo tuyên bố**. Kết quả thực tế thua cả hàm tính trung vị đơn giản.

---

## 🚀 5. NHÓM NCKH 3 (JOHNNY SNOWFLAKE) CẦN ỨNG XỬ NHƯ THẾ NÀO VỚI REPO NÀY?

1. **Kế thừa có chọn lọc:**
   * Sử dụng cấu trúc lớp `GPT2ForSequenceClassification` trong file `GPT2SP.py` làm mô hình đại diện cho kiến trúc Transformer Decoder SOTA.
   * Kế thừa tập nhãn và các quy ước dữ liệu thô để làm đối chứng.
2. **Khắc phục toàn diện các lỗ hổng của repo:**
   * Thay vì chỉ lấy `Title` cụt ngủn 20 tokens, nhóm sẽ trích xuất cả `Title + Description` được **tái dựng nguyên bản tại thời điểm `SP_Estimation_Date`** từ CSDL TAWOS v1.1 (*Time-Travel Reconstruction*).
   * Thay vì dùng tập CSV tĩnh bị rò rỉ lời giải của tương lai (Final Snapshot), nhóm dùng dữ liệu sạch không rò rỉ (*Leakage-Free Dataset*).
3. **Giá trị đóng góp vào bài báo khoa học của Nhóm 3:**
   * Việc đối soát và chỉ ra các điểm sai lệch của repository `awsm-research/gpt2sp` chính là một **luận điểm phản biện cực kỳ đắt giá (Strong Academic Critique)**, chứng minh sự am hiểu sâu sắc mã nguồn và tính trung thực khoa học của đề tài Nhóm 3 trước hội đồng đánh giá.

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📄 [Báo cáo chi tiết thẩm định mã nguồn GPT2SP](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/12_gpt2sp_code_audit_and_reproduction_discrepancies.md)
* 🧠 [Phân tích phản biện 09: Rò rỉ dữ liệu trong GPT2SP và Kế hoạch Nhóm 3](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/09_data_leakage_analysis_and_action_plan.md)
* 📖 [Chương 10: Kết luận và cam kết Open Science của Fu et al.](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/10_conclusion.md)
* 📚 [Mục lục chuyên mục Critical Thinking](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/README.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
