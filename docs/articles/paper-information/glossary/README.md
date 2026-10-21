# 📚 THƯ MỤC THUẬT NGỮ CHUYÊN NGÀNH (GLOSSARY)

Thư mục này chứa hệ thống từ điển thuật ngữ chuyên sâu, đối chiếu Anh - Việt và giải thích toán học/khoa học phục vụ các nghiên cứu về Ước lượng Nỗ lực trong Agile (Agile Effort Estimation), Mô hình Ngôn ngữ Lớn (LLMs), và Kiểm định Chống Rò rỉ Dữ liệu.

---

## 🗂️ CÁC TÀI LIỆU CHÍNH TRONG THƯ MỤC

| Tên tài liệu | Chủ đề & Phạm vi | Liên kết |
| :--- | :--- | :--- |
| **`RULE.md`** | **Quy chuẩn xây dựng từ điển thuật ngữ**: Triết lý kỹ thuật Feynman (giải thích cho đứa trẻ 10 tuổi), cấu trúc khung chuẩn 6 phần, quy tắc sơ đồ Mermaid và tiếng Việt có dấu. | [Xem chi tiết](RULE.md) |
| **`glossary_gpt2sp.md`** | Tổng hợp nhanh toàn bộ thuật ngữ trong bài báo **GPT2SP (Fu & Tantithamthavorn, IEEE TSE 2023)**: Phân loại theo 7 nhóm chuyên sâu. | [Xem chi tiết](glossary_gpt2sp.md) |

---

## 🔬 TỪ ĐIỂN THUẬT NGỮ CHUYÊN SÂU (CHUẨN FEYNMAN 6 PHẦN)

Các thuật ngữ dưới đây được biên soạn chi tiết theo **quy chuẩn `RULE.md`** (Giải thích cho đứa trẻ 10 tuổi, Bóc tách chiết tự, Trực quan hóa bảng dữ liệu, Thách thức kỹ thuật, Giải pháp đối sánh giữa Deep-SE và GPT2SP, và Bản đúc kết 30 giây):

| Thuật ngữ chuyên sâu | Nhóm kỹ thuật | Khái niệm trọng tâm giải quyết | Liên kết tài liệu |
| :--- | :--- | :--- | :--- |
| **Byte-Pair Encoding (BPE)** | NLP & Tokenization | Thuật toán ghép cặp byte/ký tự theo tần suất, xóa bỏ 100% lỗi Out-Of-Vocabulary (`OOV = 0%`). | [byte_pair_encoding.md](byte_pair_encoding.md) |
| **Subword Tokens** | NLP & Tokenization | Đơn vị từ con trung gian, giải quyết hoàn hảo tên hàm mã nguồn và biệt ngữ ghép trong Jira. | [subword_tokens.md](subword_tokens.md) |
| **Word Encoding** | Representation Learning | Ánh xạ chỉ số token vào không gian vector ngữ nghĩa $d=768$, thừa hưởng tri thức khổng lồ của GPT-2. | [word_encoding.md](word_encoding.md) |
| **Positional Encoding** | Transformers Architecture | Vector mã hóa thứ tự vị trí, giúp cơ chế Self-Attention song song không bị "mù thứ tự cú pháp". | [positional_encoding.md](positional_encoding.md) |
| **Transformer Decoder** | Deep Learning Models | Khối giải mã nhân quả một chiều (Masked Causal Attention), chắt lọc ngữ cảnh toàn bài vào token cuối để hồi quy Story Point. | [transformer_decoder.md](transformer_decoder.md) |
| **Word2Vec** | Representation Learning | Mô hình nhúng từ tĩnh dựa trên ngữ cảnh lân cận (CBOW / Skip-gram) trong Deep-SE và các hạn chế OOV. | [word2vec.md](word2vec.md) |
| **LSTM** | Recurrent Neural Networks | Mạng bộ nhớ dài-ngắn với 3 cổng kiểm soát và cell state, giải quyết triệt tiêu đạo hàm trong Deep-SE. | [lstm.md](lstm.md) |
| **RHWN** | Deep Recurrent Networks | Mạng đường cao tốc hồi quy với Carry Gate & Transform Gate, tăng độ sâu biểu diễn trừu tượng. | [rhwn.md](rhwn.md) |
| **Regressor** | Predictive Modeling | Khối nơ-ron hồi quy đầu ra (MLP Regressor Head) kết hợp L1 Loss để dự đoán số thực Story Point kháng ngoại lai. | [regressor.md](regressor.md) |

---

## 🧭 HƯỚNG DẪN TRA CỨU

1. **Quy chuẩn biên soạn thuật ngữ:** Xem file [`RULE.md`](RULE.md).
2. **Khái niệm cơ bản về Agile & Story Point:** Xem Mục 1 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
3. **Kiến trúc GPT-2 & Quy trình Tối ưu:** Xem Mục 2 & Mục 3 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
4. **Kiến trúc Deep-SE cổ điển (Word2Vec + LSTM + RHWN):** Xem các file chuyên đề [`word2vec.md`](word2vec.md), [`lstm.md`](lstm.md), [`rhwn.md`](rhwn.md).
5. **Thang đo sai số & Kiểm định phi tham số:** Xem Mục 5 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
6. **Trí tuệ nhân tạo có thể giải thích (XAI):** Xem Mục 6 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
7. **Ràng buộc chống rò rỉ dữ liệu (NCKH Nhóm 3):** Xem Mục 7 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
