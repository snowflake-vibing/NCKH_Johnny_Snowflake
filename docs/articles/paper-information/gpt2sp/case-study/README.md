# 📂 DANH MỤC CÁC NGHIÊN CỨU TÌNH HUỐNG THỰC TẾ (CASE STUDIES)

> Thư mục này tập hợp các bài phân tích tình huống thực tế (Case Studies), minh họa chi tiết quy trình xử lý dữ liệu từ đầu vào Jira Issue thô đến kết quả dự đoán và giải thích XAI của các mô hình ước lượng Story Point.

> [!TIP]
> **🎧 BẢN THUYẾT MINH ÂM THANH TOÀN BỘ CASE STUDY (AUDIO WALKTHROUGH):**  
> Để nghe thuyết minh âm thanh toàn bộ 9 bài Case Study từ 00 đến 07 trên issue Spring XD-3751 (thời lượng $10.3$ phút, **giọng đọc nam AI tiếng Việt trầm ấm, tự nhiên kèm khoảng ngắt nghỉ chuẩn nhịp thở**, chỉ âm thanh không có video):  
> • **Tập tin MP4 (Audio-only container):** 🎙️ **[case_study_full_audio_walkthrough.mp4](case_study_full_audio_walkthrough.mp4)**.  
> • **Tập tin MP3 phụ trợ:** 🎧 **[case_study_full_audio_walkthrough.mp3](case_study_full_audio_walkthrough.mp3)**.

---

## 📑 Danh Sách Các Bài Case Study Chuyên Sâu

| STT | Tài liệu Case Study | Phạm vi chuyên đề | Dự án áp dụng | Nội dung kỹ thuật cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **00-A** | [00_case_study_jira_raw_to_token_pipeline.md](00_case_study_jira_raw_to_token_pipeline.md) | **Tiền Xử Lý: Jira Thô -> Tokens** | Spring XD (XD-3751) | Trích xuất Summary + Description, chuẩn hóa văn bản, thêm <|endoftext|>, cắt cụt Truncation và phân tách BPE thành tensor [1, 64]. |
| **00** | [case_study_gpt2sp_architecture.md](case_study_gpt2sp_architecture.md) | **Tổng quan Sơ đồ Kiến trúc** | Spring XD (`XD-3751`) | Minh họa trọn vẹn quy trình 2 pha (Huấn luyện vs Suy luận) theo sơ đồ Hình 2 bài báo gốc IEEE TSE 2023: từ BPE Tokenization đến MLP Regressor và XAI. |
| **01** | [01_case_study_12_transformer_decoders.md](01_case_study_12_transformer_decoders.md) | **12 Khối Transformer Decoders** | Spring XD (`XD-3751`) | Giải mã hành trình dữ liệu qua 12 khối: Sự phân tầng trừu tượng (Từ vựng $\rightarrow$ Quan hệ lỗi $\rightarrow$ Mức độ phức tạp), cơ chế Masked Multi-Head Attention, và hệ thống 24 đường tắt Residual Connections. |
| **02** | [02_case_study_mlp_regressor_head.md](02_case_study_mlp_regressor_head.md) | **Last Token Pooling & MLP Regressor** | Spring XD (`XD-3751`) | Giải mã cơ chế chuyển đổi từ Sinh từ (Text $\rightarrow$ Text) sang Hồi quy (Text $\rightarrow$ Number): Tại sao chọn token cuối cùng $\mathbf{h}_{15}$? Cấu trúc mạng MLP 3 tầng ($768 \rightarrow 256 \rightarrow 64 \rightarrow 1$) và quy đổi điểm Fibonacci. |
| **03** | [03_case_study_last_token_pooling_xd3751.md](03_case_study_last_token_pooling_xd3751.md) | **Mắt Xích Last Token Pooling** | Spring XD (XD-3751) | Cắt lát Tensor đầu ra 3 chiều [1, 48, 768] tại vị trí index 47 để lấy ra đúng vector 2 chiều [1, 768] nạp vào MLP Regressor Head. |
| **04** | [04_case_study_training_phase.md](04_case_study_training_phase.md) | **Chuyên đề Pha Huấn luyện (Training Phase)** | Spring XD (`XD-3751`) | Phân tích trực quan, dễ hình dung về nửa trên Hình 2: từ BPE, Embedding, 12 khối Decoder, Last Token Pooling đến $L_1$ Loss, Backpropagation và cập nhật trọng số AdamW (không dùng sơ đồ khối trừu tượng). |
| **05** | [05_case_study_inference_phase.md](05_case_study_inference_phase.md) | **Chuyên đề Pha Suy luận (Inference Phase)** | Spring XD (`XD-4012`) | Phân tích trực quan, dễ hình dung về nửa dưới Hình 2: Đóng băng mô hình (`torch.no_grad`), Cơ chế Đột phá Hai luồng song song (Ước lượng Fibonacci 5 SP + XAI tô sáng từ khóa & 3 Supporting Examples), mô phỏng buổi họp Sprint Planning. |
| **06** | [06_case_study_intra_issue_temporal_leakage_evidence.md](06_case_study_intra_issue_temporal_leakage_evidence.md) | **Bằng Chứng Rò Rỉ Nội Tại (Leakage Proof)** | Spring XD (`XD-3751`) | Bằng chứng bằng mắt đối chiếu 2 ảnh chụp: Trạng thái sạch tại Sprint Planning ($T_{\text{estimation}}$, 29 từ) vs Trạng thái rò rỉ lúc đóng ($T_{\text{closed}}$, 72 từ, stack trace, comments giải pháp) khiến mô hình Transformer gian lận tương lai. |
| **07** | [07_case_study_leakage_free_contextual_features_xd3751.md](07_case_study_leakage_free_contextual_features_xd3751.md) | **Tái Dựng Đặc Trưng Agile Sạch (Hướng 5)** | Spring XD (`XD-3751`) | Quy trình trích xuất CSDL TAWOS tại $t \le T_{\text{estimation}}$: Team Velocity, Workload, Component Churn kết hợp SBERT sạch nạp vào LightGBM (2.18s), đạt MAE 1.4120 đánh bại Median baseline hợp lệ. |

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📖 [Thư mục Giải thích chi tiết các chương bài báo GPT2SP (Explanation)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/README.md)
* 🧠 [Thư mục Phân tích phản biện chuyên sâu (Scientific Critical Thinking)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/critical-thinking/README.md)
* 📚 [Thư mục Tra cứu thuật ngữ chuyên ngành (Glossary)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/glossary/README.md)
* 📑 [Báo cáo Tổng hợp Bài báo GPT2SP (Fu & Tantithamthavorn 2023)](file:///d:/NCKH_3/docs/articles/paper-information/paper_fu_2023_gpt2sp.md)
