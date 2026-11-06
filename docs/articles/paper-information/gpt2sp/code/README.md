# 💻 THƯ MỤC MÃ NGUỒN & GIẢI MÃ SOURCE CODE BÀI BÁO GPT2SP (CODE REPOSITORY & EXPLANATION)

> **Kho mã nguồn gốc:** [`https://github.com/awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp) (Đại học Monash, Melbourne, Úc).  
> **Bài báo khoa học:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (Fu & Tantithamthavorn, IEEE Transactions on Software Engineering 2023).  
> **Mục tiêu thư mục:** Lưu trữ toàn bộ 100% mã nguồn thực tế của hệ thống GPT2SP, phân tích chi tiết từng khối lệnh tương ứng với các chương trong bài báo, và đối soát khách quan giữa lý thuyết công bố với code chạy thực tế.

---

## 🧭 CẤU TRÚC HỆ THỐNG TÀI LIỆU TRONG THƯ MỤC `code/`

Thư mục này được chia thành 7 tài liệu chuyên sâu, phục vụ đầy đủ từ việc lưu trữ mã nguồn thô đến mổ xẻ phương pháp luận, phản biện khoa học, các kịch bản chạy code thực tế, và quy trình tái lập thực nghiệm lấy bằng chứng khoa học:

| Thứ tự | Tên Tập Tin | Nội Dung Cốt Lõi | Chương Đối Ứng Trong Bài Báo |
| :---: | :--- | :--- | :--- |
| **00** | [`00_full_source_code.md`](00_full_source_code.md) | **Toàn bộ 100% mã nguồn gốc GPT2SP**<br>• Lưu trữ nguyên bản file mô hình `GPT2SP.py`.<br>• Toàn bộ các code cells trong notebook huấn luyện `model_training_notebook.ipynb`.<br>• Khai báo thư viện, siêu tham số, các hàm static và script chạy thực nghiệm RQ1, RQ2. | Nền tảng toàn bài |
| **01** | [`01_architecture_code_explanation.md`](01_architecture_code_explanation.md) | **Giải thích chi tiết mã nguồn kiến trúc mô hình (`GPT2SP.py`)**<br>• Mổ xẻ từng dòng code của class `GPT2ForSequenceClassification`.<br>• Cơ chế cắt bỏ LM Head để chuyển sang hồi quy.<br>• Khối MLP Regressor Head ($768 \rightarrow 3072 \rightarrow 768 \rightarrow 1$).<br>• Thuật toán Last Token Pooling bắt token cuối.<br>• Hàm mất mát $L_1$ Loss kháng ngoại lai. | **Section 3: The GPT2SP Architecture** (Trang 3 – 5, Hình 2) |
| **02** | [`02_training_pipeline_code_explanation.md`](02_training_pipeline_code_explanation.md) | **Giải thích chi tiết mã nguồn huấn luyện (`model_training_notebook.ipynb`)**<br>• Luồng xử lý dữ liệu và tạo DataLoader.<br>• Cấu hình Dynamic Batch Size theo tỷ lệ mẫu.<br>• Phân chia Chronological Split 60/20/20 trong hàm `within_project_split()`.<br>• Vòng lặp tối ưu hóa AdamW và bộ điều tốc Learning Rate Warmup.<br>• Cơ chế chọn Best Checkpoint theo Validation Loss và đánh giá MAE/MdAE. | **Section 4: Experimental Setup** & **Section 5: Results** (Trang 5 – 10) |
| **03** | [`03_code_vs_paper_discrepancies.md`](03_code_vs_paper_discrepancies.md) | **Mổ xẻ 4 điểm sai lệch cốt tử giữa Code thực tế và Bài báo**<br>• Phát hiện bài báo ghi dùng `Title + Description` nhưng code chỉ nạp `Title`.<br>• Phát hiện `SEQUENCE_LEN` bị ép cụt ngủn xuống 20 tokens.<br>• Lý giải bí mật tốc độ huấn luyện 14 giây.<br>• Lỗi tính MAE do nhóm nghiên cứu UCL vạch trần.<br>• Bằng chứng tái lập thực tế trên Spring XD: Checkpoint tác giả chỉ đạt MAE 1.7330 (thua Median Baseline 1.7153). | **Section 9: Threats to Validity** & **Phản biện NCKH Nhóm 3** |
| **04** | [`04_run_inference_example.md`](04_run_inference_example.md) | **Hướng dẫn chạy ví dụ suy luận thực tế trong code (`Inference`)**<br>• Mã nguồn Python hoàn chỉnh chạy dự báo trên Jira issue XD-3751.<br>• Bảng theo dõi biến đổi hình dạng Tensor qua từng tầng.<br>• Cơ chế ánh xạ Euclidean sang dãy số Fibonacci Scrum.<br>• Mô phỏng terminal output và mở rộng cho suy luận theo lô (Batch Inference). | **Section 3.3 & Section 5** |
| **05** | [`05_run_training_example.md`](05_run_training_example.md) | **Hướng dẫn chạy ví dụ huấn luyện thực tế trong code (`Training Loop`)**<br>• Mã nguồn Python hoàn chỉnh mô phỏng chu trình học máy.<br>• Lan truyền xuôi, tính $L_1$ Loss, lan truyền ngược (`backward`) và AdamW.<br>• Bảng so sánh kết quả dự báo trước vs sau khi cập nhật Gradient.<br>• Phân tích toán học tính kháng ngoại lai của $L_1$ Loss. | **Section 3.4 & Section 4** |
| **06** | [`06_end_to_end_reproduction_guide_github_to_metrics.md`](06_end_to_end_reproduction_guide_github_to_metrics.md) | **Hướng dẫn tái lập thực nghiệm từ GitHub đến thông số đầu ra làm bằng chứng**<br>• Quy trình 5 bước từ repo `awsm-research/gpt2sp` đến checkpoint Hugging Face.<br>• Phân chia Chronological Split 60/20/20 trên 3.526 issues của Spring XD.<br>• Script Python hoàn chỉnh tính MAE, MdAE, SA, và kiểm định Wilcoxon Signed-Rank Test.<br>• Xuất file CSV bằng chứng chi tiết 706 mẫu test làm minh chứng khoa học. | **Section 4 & Section 5 & Đề tài NCKH** |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 🧠 [Thư mục Phân tích phản biện chuyên sâu (Critical Thinking)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/README.md)
* 📖 [Thư mục Giải thích chi tiết từng chương bài báo (Explanation)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/README.md)
* 🔬 [Thư mục Nghiên cứu trường hợp điển hình trên Jira (Case Study)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/case-study/README.md)
* 👑 [Quy chuẩn vận hành nghiên cứu NCKH Nhóm 3](file:///d:/NCKH_3/AGENTS.md)
