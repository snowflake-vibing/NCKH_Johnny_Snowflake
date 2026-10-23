# 📂 DANH MỤC CÁC NGHIÊN CỨU TÌNH HUỐNG THỰC TẾ (CASE STUDIES)

> Thư mục này tập hợp các bài phân tích tình huống thực tế (Case Studies), minh họa chi tiết quy trình xử lý dữ liệu từ đầu vào Jira Issue thô đến kết quả dự đoán và giải thích XAI của các mô hình ước lượng Story Point.

---

## 📑 Danh Sách Các Bài Case Study Chuyên Sâu

| STT | Tài liệu Case Study | Phạm vi chuyên đề | Dự án áp dụng | Nội dung kỹ thuật cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **00** | [case_study_gpt2sp_architecture.md](case_study_gpt2sp_architecture.md) | **Tổng quan Sơ đồ Kiến trúc** | Spring XD (`XD-3751`) | Minh họa trọn vẹn quy trình 2 pha (Huấn luyện vs Suy luận) theo sơ đồ Hình 2 bài báo gốc IEEE TSE 2023: từ BPE Tokenization đến MLP Regressor và XAI. |
| **01** | [01_case_study_12_transformer_decoders.md](01_case_study_12_transformer_decoders.md) | **12 Khối Transformer Decoders** | Spring XD (`XD-3751`) | Giải mã hành trình dữ liệu qua 12 khối: Sự phân tầng trừu tượng (Từ vựng $\rightarrow$ Quan hệ lỗi $\rightarrow$ Mức độ phức tạp), cơ chế Masked Multi-Head Attention, và hệ thống 24 đường tắt Residual Connections. |
| **02** | [02_case_study_mlp_regressor_head.md](02_case_study_mlp_regressor_head.md) | **Last Token Pooling & MLP Regressor** | Spring XD (`XD-3751`) | Giải mã cơ chế chuyển đổi từ Sinh từ (Text $\rightarrow$ Text) sang Hồi quy (Text $\rightarrow$ Number): Tại sao chọn token cuối cùng $\mathbf{h}_{15}$? Cấu trúc mạng MLP 3 tầng ($768 \rightarrow 256 \rightarrow 64 \rightarrow 1$) và quy đổi điểm Fibonacci. |
| **04** | [04_case_study_training_phase.md](04_case_study_training_phase.md) | **Chuyên đề Pha Huấn luyện (Training Phase)** | Spring XD (`XD-3751`) | Phân tích trực quan, dễ hình dung về nửa trên Hình 2: từ BPE, Embedding, 12 khối Decoder, Last Token Pooling đến $L_1$ Loss, Backpropagation và cập nhật trọng số AdamW (không dùng sơ đồ khối trừu tượng). |
| **05** | [05_case_study_inference_phase.md](05_case_study_inference_phase.md) | **Chuyên đề Pha Suy luận (Inference Phase)** | Spring XD (`XD-4012`) | Phân tích trực quan, dễ hình dung về nửa dưới Hình 2: Đóng băng mô hình (`torch.no_grad`), Cơ chế Đột phá Hai luồng song song (Ước lượng Fibonacci 5 SP + XAI tô sáng từ khóa & 3 Supporting Examples), mô phỏng buổi họp Sprint Planning. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📖 [Thư mục Giải thích chi tiết các chương bài báo GPT2SP (Explanation)](file:///d:/NCKH_3/docs/articles/paper-information/explanation/README.md)
* 🧠 [Thư mục Phân tích phản biện chuyên sâu (Scientific Critical Thinking)](file:///d:/NCKH_3/docs/articles/paper-information/critical-thinking/README.md)
* 📚 [Thư mục Tra cứu thuật ngữ chuyên ngành (Glossary)](file:///d:/NCKH_3/docs/articles/paper-information/glossary/README.md)
* 📑 [Báo cáo Tổng hợp Bài báo GPT2SP (Fu & Tantithamthavorn 2023)](file:///d:/NCKH_3/docs/articles/paper-information/paper_fu_2023_gpt2sp.md)
