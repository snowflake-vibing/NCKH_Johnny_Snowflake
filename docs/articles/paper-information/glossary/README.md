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
| **OOV (Out-Of-Vocabulary)** | NLP & Tokenization | Tử huyệt "từ ngoài từ điển" khiến Deep-SE thất bại và cách BPE của GPT-2 xóa sổ triệt để lỗi này. | [oov.md](oov.md) |
| **Word Encoding** | Representation Learning | Ánh xạ chỉ số token vào không gian vector ngữ nghĩa $d=768$, thừa hưởng tri thức khổng lồ của GPT-2. | [word_encoding.md](word_encoding.md) |
| **Positional Encoding** | Transformers Architecture | Vector mã hóa thứ tự vị trí, giúp cơ chế Self-Attention song song không bị "mù thứ tự cú pháp". | [positional_encoding.md](positional_encoding.md) |
| **Transformer Decoder** | Deep Learning Models | Khối giải mã nhân quả một chiều (Masked Causal Attention), chắt lọc ngữ cảnh toàn bài vào token cuối để hồi quy Story Point. | [transformer_decoder.md](transformer_decoder.md) |
| **Feed-Forward Network (FFN)** | Deep Learning Models | Mạng truyền thẳng mở rộng $768 \rightarrow 3072 \rightarrow 768$ chiều, chiếm 66% tham số đóng vai trò bộ nhớ tri thức của GPT-2. | [feed_forward_neural_network.md](feed_forward_neural_network.md) |
| **GELU Activation** | Deep Learning Math | Hàm kích hoạt phân phối chuẩn Gauss trơn mượt, loại bỏ triệt để hiện tượng chết nơ-ron của ReLU. | [gelu.md](gelu.md) |
| **Linear Layers** | Deep Learning Core | Lớp biến đổi tuyến tính $y = Wx + b$, nền móng kết nối đầy đủ của các khối chiếu Attention và MLP. | [linear_layers.md](linear_layers.md) |
| **Residual Connection** | Deep Learning Architecture | Con đường tắt phần dư $y = x + F(x)$, siêu dẫn đạo hàm không ma sát giúp huấn luyện ổn định 12 tầng Transformer. | [residual_connection.md](residual_connection.md) |
| **MLP Regressor Head** | Specialized Prediction Heads | Đầu hồi quy đa tầng ($768 \rightarrow 256 \rightarrow 1$) gắn trên đỉnh GPT-2 thay thế đầu sinh từ vựng để dự đoán Story Point. | [mlp_regressor_head.md](mlp_regressor_head.md) |
| **Regressor** | Predictive Modeling | Bản chất toán học của bài toán hồi quy liên tục so với phân loại rời rạc trong ước lượng nỗ lực phần mềm. | [regressor.md](regressor.md) |
| **Weight Decay** | Optimization & Regularization | Cơ chế bào mòn trọng số tách rời trong AdamW ($\text{LR} = 5 \times 10^{-4}$), chống quá khớp khi fine-tuning trên dữ liệu Jira nhỏ. | [weight_decay.md](weight_decay.md) |
| **Back-propagation** | Optimization Calculus | Thuật toán lan truyền ngược đạo hàm theo quy tắc chuỗi (Chain Rule) dẫn dắt bởi L1 Loss trong huấn luyện đầu-cuối. | [backpropagation.md](backpropagation.md) |
| **Word2Vec** | Representation Learning | Mô hình nhúng từ tĩnh dựa trên ngữ cảnh lân cận (CBOW / Skip-gram) trong Deep-SE và các hạn chế OOV. | [word2vec.md](word2vec.md) |
| **LSTM** | Recurrent Neural Networks | Mạng bộ nhớ dài-ngắn với 3 cổng kiểm soát và cell state, giải quyết triệt tiêu đạo hàm trong Deep-SE. | [lstm.md](lstm.md) |
| **RHWN** | Deep Recurrent Networks | Mạng đường cao tốc hồi quy với Carry Gate & Transform Gate, tăng độ sâu biểu diễn trừu tượng. | [rhwn.md](rhwn.md) |
| **Random Forest** | Traditional ML & Ensemble | Rừng cây quyết định ngẫu nhiên, lấy trung bình dự đoán của 100 cây, làm bộ hồi quy baseline (LSTM+RF, BoW+RF). | [random_forest.md](random_forest.md) |
| **TF-IDF** | Traditional NLP & Mining | Tần suất từ kết hợp nghịch đảo tần suất văn bản, chấm điểm từ khóa đặc thù cho baseline TF-IDF + SVM [36]. | [tf_idf.md](tf_idf.md) |
| **Support Vector Machine (SVM)** | Traditional ML & Convex Opt | Máy vector hỗ trợ với dải hành lang an toàn biên cực đại và hàm mất mát $\epsilon$-insensitive loss trong SVR. | [support_vector_machine.md](support_vector_machine.md) |
| **Bag-of-Words (BoW)** | Traditional NLP | Mô hình túi từ đếm tần suất thô, ném bỏ hoàn toàn ngữ pháp và thứ tự câu cú trong baseline BoW + RF. | [bag_of_words.md](bag_of_words.md) |

---

## 🧭 HƯỚNG DẪN TRA CỨU

1. **Quy chuẩn biên soạn thuật ngữ:** Xem file [`RULE.md`](RULE.md).
2. **Khái niệm cơ bản về Agile & Story Point:** Xem Mục 1 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
3. **Kiến trúc Transformer & GPT-2:** Xem các chuyên đề [`transformer_decoder.md`](transformer_decoder.md), [`feed_forward_neural_network.md`](feed_forward_neural_network.md), [`residual_connection.md`](residual_connection.md), [`linear_layers.md`](linear_layers.md), [`gelu.md`](gelu.md).
4. **Cơ chế Tokenization & Biểu diễn:** Xem [`byte_pair_encoding.md`](byte_pair_encoding.md), [`subword_tokens.md`](subword_tokens.md), [`oov.md`](oov.md), [`word_encoding.md`](word_encoding.md), [`positional_encoding.md`](positional_encoding.md).
5. **Cơ chế Tối ưu hóa & Đầu hồi quy GPT2SP:** Xem [`mlp_regressor_head.md`](mlp_regressor_head.md), [`regressor.md`](regressor.md), [`weight_decay.md`](weight_decay.md), [`backpropagation.md`](backpropagation.md).
6. **Kiến trúc Deep-SE cổ điển (Word2Vec + LSTM + RHWN):** Xem các file chuyên đề [`word2vec.md`](word2vec.md), [`lstm.md`](lstm.md), [`rhwn.md`](rhwn.md).
7. **Các mô hình máy học đối chứng (Baselines):** Xem [`random_forest.md`](random_forest.md), [`tf_idf.md`](tf_idf.md), [`support_vector_machine.md`](support_vector_machine.md), [`bag_of_words.md`](bag_of_words.md).
8. **Thang đo sai số & Kiểm định phi tham số:** Xem Mục 5 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
9. **Trí tuệ nhân tạo có thể giải thích (XAI):** Xem Mục 6 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
10. **Ràng buộc chống rò rỉ dữ liệu (NCKH Nhóm 3):** Xem Mục 7 trong [`glossary_gpt2sp.md`](glossary_gpt2sp.md).
