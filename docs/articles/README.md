# 📚 Quản lý Tài liệu Khoa học (Literature Review Management)

> Thư mục này chịu trách nhiệm quản lý, phân loại và số hóa tri thức từ các bài báo khoa học (Scientific Papers) phục vụ đề tài nghiên cứu:  
> **"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"**.

---

## 📂 1. Cấu trúc Phân mục

```text
docs/articles/
├── paper-information/        # Thư mục chứa các file phân tích chi tiết từng bài báo (*.md)
├── *.pdf                     # Bản sao file PDF gốc của các bài báo khoa học
└── README.md                 # Hướng dẫn quy trình & Mẫu chuẩn phân tích
```

---

## 🎯 2. Quy ước & Hướng dẫn cho AI / Người đọc (Guidelines)

Khi đọc một bài báo PDF mới và tạo file phân tích trong thư mục `paper-information/`, bắt buộc phải tuân thủ các quy tắc sau:

### 🏷️ Quy tắc đặt tên file:

- **Cú pháp:** `paper_<tác_giả_chính_lowercase>_<năm>_<từ_khóa_chính>.md`
- **Ví dụ:**
  - `paper_fu_2023_gpt2sp.md`
  - `paper_tawosi_2022_replication.md`
  - `paper_choetkiertikul_2019_deep_se.md`

### 🔍 Quy tắc thẩm định & Điền 21 trường dữ liệu:

Tất cả các bản phân tích đều phục vụ trực tiếp cho **Literature Matrix** của đề tài với đầy đủ 21 trường thông tin:

1. **Title:** Tiêu đề bài báo chính xác theo bản công bố.
2. **Cite Key:** Khóa trích dẫn BibTeX chuẩn (`FirstAuthorYearKeyword`, vd: `fu2023gpt2sp`).
3. **Authors:** Danh sách tác giả đầy đủ.
4. **Year:** Năm công bố chính thức.
5. **Venue:** Tên đầy đủ và viết tắt của Journal / Conference (vd: _IEEE Transactions on Software Engineering (TSE)_, _ICSE_, _MSR_).
6. **Files & media:** Đường dẫn tới file PDF nội bộ trong kho lưu trữ (vd: `docs/articles/paper_gpt2sp.pdf`) hoặc DOI/link bài báo.
7. **Venue Type:** Loại ấn phẩm (`Journal`, `Conference`, `Workshop`, `Preprint`).
8. **SJR Quartile:** Phân hạng Scimago Journal Rank (`Q1`, `Q2`, `Q3`, `Q4`, hoặc `N/A` nếu là Conference).
9. **CORE Rank:** Phân hạng theo Hội nghị CORE Ranking (`A*`, `A`, `B`, `C`, hoặc `N/A` nếu là Journal).
10. **Rank:** Đánh giá tổng hợp uy tín (`Q1`, `CORE A*`, v.v.).
11. **Problem:** Vấn đề và mục tiêu cốt lõi mà bài báo đặt ra cần giải quyết.
12. **Dataset:** Tập dữ liệu nghiên cứu sử dụng (Tên dataset, số lượng issues/dự án, nguồn gốc Jira/GitHub).
13. **Ground Truth:** Định nghĩa nhãn mục tiêu (Final SP, Initial SP, Actual Effort, v.v.).
14. **Method:** Kiến trúc mô hình / Thuật toán đề xuất (Transformer, Deep-SE, SBERT, Ensemble, v.v.).
15. **Baseline:** Danh sách mô hình nền tảng đối chứng (Random, Mean, Median, TF-IDF + Ridge, v.v.).
16. **Split:** Chiến lược chia tập dữ liệu (Chronological split 60/20/20, Cross-project, K-fold).
17. **Metrics:** Thước đo định lượng (MAE, MdAE, SA, RMSE, Wilcoxon test, Cliff's delta).
18. **Main Result:** Kết quả thực nghiệm trọng tâm và mức độ cải thiện được báo cáo.
19. **Critical Notes:** **(Rất quan trọng)** Phân tích phản biện, điểm hạn chế, nguy cơ rò rỉ dữ liệu tương lai (_Temporal/Future-Information Leakage_), hoặc khác biệt giữa mã nguồn công khai và bài báo.
20. **Takeaways:** Bài học rút ra, kinh nghiệm thực nghiệm hoặc kỹ thuật nhóm có thể học tập/kế thừa.
21. **Relevance to Topic:** Đóng góp và vị trí của bài báo đối với đề tài nghiên cứu của nhóm (_Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control_).

---

## 🤖 3. Prompt Mẫu dành cho AI Assistant (Prompt Template)

Khi cung cấp một file PDF cho AI, hãy sử dụng đoạn prompt sau để AI trích xuất và tạo file đúng cấu trúc:

```markdown
Bạn là chuyên gia nghiên cứu khoa học trong lĩnh vực Software Engineering và Machine Learning.
Hãy đọc kỹ tài liệu PDF đính kèm và tạo một bài phân tích chuyên sâu định dạng Markdown tuân thủ tuyệt đối cấu trúc mẫu dưới đây.

Lưu ý đặc biệt:

- Trích xuất chính xác 21 trường dữ liệu thuộc Literature Matrix.
- Phân tích sâu sắc khía cạnh "Temporal / Future-Information Leakage": Xem xét dữ liệu tác giả sử dụng được lấy tại thời điểm nào (Sprint Planning hay Final Snapshot sau khi đóng issue)? Có hiện tượng sửa title/description làm rò rỉ thông tin tương lai không?
- Đối chiếu trung thực giữa công bố lý thuyết và mã nguồn/artifact công khai (nếu bài báo có đề cập).
```

---

## 📄 4. MẪU CHUẨN TẠO FILE PHÂN TÍCH (LITERATURE REVIEW TEMPLATE)

_Dưới đây là nội dung mẫu để tạo một file `docs/articles/paper-information/paper_<author>_<year>_<keyword>.md`:_

```markdown
# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** [Điền tiêu đề bài báo đầy đủ ở đây]  
> **Nguồn công bố:** [Tên Hội nghị / Tạp chí] ([Năm])

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá                                                              |
| :----: | :----------------------- | :------------------------------------------------------------------------------------------ |
| **1**  | **Title**                | [Tên bài báo chính thức]                                                                    |
| **2**  | **Cite Key**             | `[FirstAuthorYearKeyword]`                                                                  |
| **3**  | **Authors**              | [Danh sách tác giả]                                                                         |
| **4**  | **Year**                 | [Năm công bố]                                                                               |
| **5**  | **Venue**                | [Tên Tạp chí / Hội nghị (Viết tắt)]                                                         |
| **6**  | **Files & media**        | [docs/articles/tên_file.pdf](docs/articles/tên_file.pdf) \| [DOI Link](https://doi.org/...) |
| **7**  | **Venue Type**           | [Journal / Conference / Preprint]                                                           |
| **8**  | **SJR Quartile**         | [Q1 / Q2 / Q3 / Q4 / N/A]                                                                   |
| **9**  | **CORE Rank**            | [A* / A / B / C / N/A]                                                                      |
| **10** | **Rank**                 | [Q1 / CORE A* / ...]                                                                        |
| **11** | **Problem**              | [Mô tả ngắn gọn bài toán nghiên cứu]                                                        |
| **12** | **Dataset**              | [Tên dataset, quy mô, số issue, số dự án]                                                   |
| **13** | **Ground Truth**         | [Định nghĩa nhãn Story Point mục tiêu]                                                      |
| **14** | **Method**               | [Phương pháp / Kiến trúc mô hình cốt lõi]                                                   |
| **15** | **Baseline**             | [Các mô hình đối chứng (Median, Mean, TF-IDF, v.v.)]                                        |
| **16** | **Split**                | [Chiến lược phân chia tập dữ liệu (Chronological, Random, v.v.)]                            |
| **17** | **Metrics**              | [Các độ đo: MAE, MdAE, SA, Wilcoxon, Cliff's delta]                                         |
| **18** | **Main Result**          | [Kết quả định lượng nổi bật nhất]                                                           |
| **19** | **Critical Notes**       | [Điểm hạn chế, nghi vấn rò rỉ dữ liệu, code vs paper]                                       |
| **20** | **Takeaways**            | [Bài học kinh nghiệm, phương pháp có thể kế thừa]                                           |
| **21** | **Relevance to Topic**   | [Vai trò và ý nghĩa đối với đề tài NCKH của nhóm]                                           |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)

- **Vấn đề thực tiễn:** [Tại sao tác giả lại thực hiện nghiên cứu này? Hạn chế của các nghiên cứu trước đó là gì?]
- **Mục tiêu khoa học:** [Câu hỏi nghiên cứu (Research Questions - RQs) bài báo đặt ra là gì?]

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)

- **Nguồn dữ liệu:** [Chi tiết về cách thu thập dữ liệu Jira/GitHub, các bộ lọc đã áp dụng].
- **Đặc trưng đầu vào (Input Features):** [Sử dụng Title, Description, Components, Issue Type hay các trường nào khác?].
- **Mốc thời gian lấy dữ liệu:** [Dữ liệu được trích xuất tại mốc Planning hay Final Snapshot sau khi đóng issue?].

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)

- **Kiến trúc mô hình:** [Mô tả chi tiết luồng xử lý của mô hình, trích xuất vector embedding, pooling, regression head].
- **Kỹ thuật huấn luyện:** [Loss function, Optimizer, Hyperparameters, Tokenizer length, v.v.].

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)

- **Bảng tóm tắt kết quả:** [So sánh hiệu năng giữa mô hình đề xuất và các baselines].
- **Kiểm định thống kê:** [Ý nghĩa thống kê qua Wilcoxon Signed-Rank Test, Cliff's Delta Effect Size].

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)

- **Temporal / Future-Information Leakage:**
  - _Bài báo có kiểm soát việc sửa đổi text sau thời điểm planning không?_
  - _Có sử dụng các trường tương lai như Resolution Date, Comments sau planning, Status closed không?_
- **Tính minh bạch & Khả năng tái lập (Reproducibility):**
  - _Mã nguồn và dữ liệu công khai có khớp hoàn toàn với mô tả trong bài báo không?_
  - _Có gặp bẫy môi trường hay thiếu sót chi tiết cài đặt không?_

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)

- **Ý tưởng có thể áp dụng:** [Các kiến trúc, hàm mất mát hoặc cách xử lý văn bản có thể tái sử dụng].
- **Điểm nhóm cần cải tiến/vượt qua:** [Cách đề tài của nhóm giải quyết triệt để các lỗ hổng mà bài báo này chưa khắc phục].
```

---

## 📊 5. Danh mục Tổng hợp Literature Review Hiện có

| Cite Key                 | Tác giả & Năm                | Venue       | Phân hạng | Phương pháp chính                 | Đóng góp & Vị trí đối với Đề tài                                          | File phân tích chi tiết                                                                          |
| :----------------------- | :--------------------------- | :---------- | :-------: | :-------------------------------- | :------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------- |
| `tawosi2022agile`        | Tawosi et al. (2022)         | IEEE TSE    |    Q1     | TAWOS Dataset & Replication Study | Nền tảng dữ liệu thực nghiệm (TAWOS v1.1) và chuẩn hóa độ đo (MAE, SA).   | [`paper_tawosi_2022_replication.md`](paper-information/paper_tawosi_2022_replication.md)         |
| `fu2023gpt2sp`           | Fu & Tantithamthavorn (2023) | IEEE TSE    |    Q1     | GPT2SP (GPT-2 Fine-tuning)        | Đối tượng tái lập thực nghiệm chính (Reproduction target) của nhóm.       | [`paper_fu_2023_gpt2sp.md`](paper-information/paper_fu_2023_gpt2sp.md)                           |
| `choetkiertikul2019deep` | Choetkiertikul et al. (2019) | IEEE TSE    |    Q1     | Deep-SE (Word2Vec + LSTM + RNN)   | Nghiên cứu nền tảng đầu tiên áp dụng Deep Learning cho Story Point.       | [`paper_choetkiertikul_2019_deep_se.md`](paper-information/paper_choetkiertikul_2019_deep_se.md) |
| `yalciner2024sbert`      | Yalciner et al. (2024)       | IEEE Access |    Q1     | SBERT + GBT                       | Hướng tiếp cận kết hợp Sentence-BERT embedding và Gradient Boosted Trees. | [`paper_yalciner_2024_sbert_gbt.md`](paper-information/paper_yalciner_2024_sbert_gbt.md)         |
| `wijaya2024tbe`          | Wijaya et al. (2024)         | IEEE Access |    Q1     | TBE & ERM                         | Mô hình khai thác Temporal Behavior và Effort Ratio Modeling.             | [`paper_wijaya_2024_tbe_erm.md`](paper-information/paper_wijaya_2024_tbe_erm.md)                 |
| `khan2025comparative`    | Khan et al. (2025)           | arXiv / ESEM| CORE Rank A | Pairwise Comparative Learning     | Mô hình học so sánh cặp User Story với Sentence-BERT và suy diễn thứ hạng.| [`paper_khan_2025_comparative_learning.md`](paper-information/paper_khan_2025_comparative_learning.md) |
