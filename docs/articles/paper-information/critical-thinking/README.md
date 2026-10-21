# 🧠 DANH MỤC CÁC PHÂN TÍCH PHẢN BIỆN CHUYÊN SÂU (CRITICAL THINKING)
# VỀ KIẾN TRÚC VÀ BẢN CHẤT MÔ HÌNH GPT2SP

> Thư mục này tập hợp các bài phân tích phản biện khoa học (Scientific Critical Thinking), giải phẫu tận gốc các quyết định thiết kế kiến trúc, các hằng số siêu tham số ("magic numbers"), và các cơ chế toán học ngầm định trong mô hình GPT2SP và Transformer.

---

## 🎯 Mục Tiêu Của Chuyên Mục Critical Thinking

Khác với các tài liệu mô tả thuần túy (Explanation), chuyên mục này trả lời cho câu hỏi:
* **"Tại sao lại là con số đó mà không phải con số khác?"** (Why these exact hyperparameters?)
* **"Bản chất vật lý và phần cứng bên dưới các công thức toán là gì?"** (Hardware alignment & Tensor optimization)
* **"Đánh đổi (trade-offs) tiềm ẩn và giới hạn kỹ thuật của tác giả là gì?"** (Ablation boundaries & Architectural trade-offs)

---

## 📑 Danh Sách Các Bài Phân Tích Phản Biện

| STT | Bài phân tích phản biện | Chủ đề cốt lõi | Các câu hỏi phản biện then chốt được giải đáp |
| :-: | :--- | :--- | :--- |
| **01** | [01_subword_vocabularies_50257.md](01_subword_vocabularies_50257.md) | **Kích thước từ điển BPE ($50.257$)** | • Tại sao từ điển BPE có đúng $50.257$ tokens?<br>• Người ta huấn luyện đến đó thôi hay có thể train thêm?<br>• Nguồn gốc phép cộng $256 + 50.000 + 1$ và bài toán đánh đổi giữa chiều dài chuỗi ($O(n^2)$) và dung lượng ma trận nhúng ($W_{te}$). |
| **02** | [02_why_hidden_dimension_768.md](02_why_hidden_dimension_768.md) | **Nguồn gốc chiều ẩn ($d_{\text{model}} = 768$)** | • Con số 768 thực sự từ đâu sinh ra?<br>• Tại sao lại là $12 \text{ heads} \times 64 = 768$?<br>• Ràng buộc kiến trúc GPU NVIDIA (Warp 32 threads, Tensor Cores) và điểm ngọt 117M tham số trên card 16GB VRAM. |
| **03** | [03_why_qkv_2304_and_ffn_3072.md](03_why_qkv_2304_and_ffn_3072.md) | **Kích thước ma trận QKV ($2304$) và FFN ($3072$)** | • Tại sao ma trận Query/Key/Value lại là $768 \times 2304$ rồi chiếu về $768 \times 768$?<br>• Kỹ thuật Fused Attention Matrix tối ưu GPU kernel calls.<br>• Tại sao tầng FFN lại mở rộng đúng $4$ lần lên $768 \times 3072$ (Bản chất bộ nhớ tri thức Key-Value Memory)? |

---

## 🧭 Khung Hướng Dẫn Bổ Sung Câu Hỏi Phản Biện Mới (Cho các nghiên cứu sau này)

Khi xuất hiện các câu hỏi phản biện mới trong quá trình thảo luận hoặc tái lập thực nghiệm, cấu trúc một bài viết phản biện cần tuân thủ 5 bước chuẩn hóa:

```text
[1. Đặt Vấn Đề] ──> Nêu câu hỏi trực diện, chỉ rõ con số / cơ chế gây thắc mắc.
       │
       ▼
[2. Bản Chất Toán Học & Phần Cứng] ──> Mổ xẻ công thức, kích thước ma trận, sự tương thích với GPU.
       │
       ▼
[3. Phân Tích Đánh Đổi (Trade-off Analysis)] ──> Nếu tăng/giảm tham số này thì hậu quả là gì?
       │
       ▼
[4. Liên Hệ Thực Tế GPT2SP & Đề Tài NCKH] ──> Tác động cụ thể đến bài toán ước lượng Story Point.
       │
       ▼
[5. Tổng Kết & Bài Học Đúc Rút] ──> Kết luận ngắn gọn, súc tích và dễ nhớ.
```

---

## 🔗 Liên Kết Điều Hướng Hệ Thống

* 📖 [Chương 3: Kiến trúc mô hình GPT2SP](file:///d:/NCKH_3/docs/articles/paper-information/explanation/03_the_gpt2sp_architecture.md)
* 🔬 [Case Study: Thực tế áp dụng kiến trúc trên Jira Issue XD-3751](file:///d:/NCKH_3/docs/articles/paper-information/case-study/case_study_gpt2sp_architecture.md)
* 📚 [Thuật ngữ chuyên ngành GPT2SP (Glossary)](file:///d:/NCKH_3/docs/articles/paper-information/glossary/README.md)
* 📑 [Báo cáo Tổng hợp Bài báo GPT2SP (IEEE TSE 2023)](file:///d:/NCKH_3/docs/articles/paper-information/paper_fu_2023_gpt2sp.md)
