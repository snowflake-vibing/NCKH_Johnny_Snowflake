# 📂 DANH MỤC CÁC NGHIÊN CỨU TÌNH HUỐNG THỰC TẾ (CASE STUDIES)

> Thư mục này tập hợp các bài phân tích tình huống thực tế (Case Studies), minh họa chi tiết quy trình xử lý dữ liệu từ đầu vào Jira Issue thô đến kết quả dự đoán và giải thích XAI của các mô hình ước lượng Story Point.

---

## 📑 Danh Sách Các Bài Case Study Chuyên Sâu

| STT | Tài liệu Case Study | Phạm vi chuyên đề | Dự án áp dụng | Nội dung kỹ thuật cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **00** | [case_study_gpt2sp_architecture.md](case_study_gpt2sp_architecture.md) | **Tổng quan Sơ đồ Kiến trúc** | Spring XD (`XD-3751`) | Minh họa trọn vẹn quy trình 2 pha (Huấn luyện vs Suy luận) theo sơ đồ Hình 2 bài báo gốc IEEE TSE 2023: từ BPE Tokenization đến MLP Regressor và XAI. |
| **01** | [01_case_study_12_transformer_decoders.md](01_case_study_12_transformer_decoders.md) | **12 Khối Transformer Decoders** | Spring XD (`XD-3751`) | Giải mã hành trình dữ liệu qua 12 khối: Sự phân tầng trừu tượng (Từ vựng $\rightarrow$ Quan hệ lỗi $\rightarrow$ Mức độ phức tạp), cơ chế Masked Multi-Head Attention, và hệ thống 24 đường tắt Residual Connections. |
| **02** | [02_case_study_mlp_regressor_head.md](02_case_study_mlp_regressor_head.md) | **Last Token Pooling & MLP Regressor** | Spring XD (`XD-3751`) | Giải mã cơ chế chuyển đổi từ Sinh từ (Text $\rightarrow$ Text) sang Hồi quy (Text $\rightarrow$ Number): Tại sao chọn token cuối cùng $\mathbf{h}_{15}$? Cấu trúc mạng MLP 3 tầng ($768 \rightarrow 256 \rightarrow 64 \rightarrow 1$) và quy đổi điểm Fibonacci. |
| **03** | [03_case_study_training_vs_inference_phases.md](03_case_study_training_vs_inference_phases.md) | **Training Phase vs. Inference Phase** | Spring XD (`XD-3751`) | Đối chứng toàn diện hai pha: Pha Huấn luyện ($L_1$ Loss, Backprop, AdamW) và Pha Suy luận (Đóng băng mô hình, Đột phá Hai luồng song song, XAI Integrated Gradients & 3 Supporting Examples), kèm cảnh báo Temporal Leakage. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📖 [Thư mục Giải thích chi tiết các chương bài báo GPT2SP (Explanation)](file:///d:/NCKH_3/docs/articles/paper-information/explanation/README.md)
* 🧠 [Thư mục Phân tích phản biện chuyên sâu (Scientific Critical Thinking)](file:///d:/NCKH_3/docs/articles/paper-information/critical-thinking/README.md)
* 📚 [Thư mục Tra cứu thuật ngữ chuyên ngành (Glossary)](file:///d:/NCKH_3/docs/articles/paper-information/glossary/README.md)
* 📑 [Báo cáo Tổng hợp Bài báo GPT2SP (Fu & Tantithamthavorn 2023)](file:///d:/NCKH_3/docs/articles/paper-information/paper_fu_2023_gpt2sp.md)
