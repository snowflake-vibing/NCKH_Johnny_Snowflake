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
| **04** | [04_origin_of_layers_heads_and_head_dimension.md](04_origin_of_layers_heads_and_head_dimension.md) | **Cội nguồn học thuật: $L=12$, $H=12$, $d_k=64$** | • Các con số số tầng ($12$), số đầu ($12$), kích thước đầu ($64$) từ bài báo nào sinh ra?<br>• Link DOI và vị trí cụ thể (Trang, Cột, Bảng) trong các bài báo kinh điển (*Vaswani 2017*, *GPT-1 2018*, *BERT 2018*, *GPT-2 2019*, *GPT2SP 2023*). |
| **05** | [05_merge_operations_and_subword_vocabularies.md](05_merge_operations_and_subword_vocabularies.md) | **Bản chất Merge Operations & Subword Vocabularies** | • Subword và Merge Operations thực chất là gì, nằm ở khâu nào trong Transformer?<br>• File dataset gốc `merges.txt` và `vocab.json` từ OpenAI / HuggingFace.<br>• 3 kịch bản mã nguồn Python thực thi: Soi file gốc, tách từ bằng `tiktoken`, và tự viết thuật toán BPE từ con số 0. |
| **06** | [06_why_4x_expansion_triggers_neuron_activation.md](06_why_4x_expansion_triggers_neuron_activation.md) | **Tại sao phóng đại $4\times$ ($3072$) nơ-ron mới bừng sáng?** | • Tại sao ở 768 chiều nơ-ron không thể bừng sáng độc lập?<br>• Bản chất toán học của "bừng sáng": Cổng kích hoạt GELU và tính thưa (Sparsity).<br>• Định lý Cover (1965) về tính phân tách tuyến tính và lý thuyết Key-Value Memory (*Geva et al.*).<br>• Code PyTorch đo trực tiếp độ thưa và sự kích hoạt của 3.072 nơ-ron trên GPT-2. |
| **07** | [07_why_12_transformer_decoder_blocks.md](07_why_12_transformer_decoder_blocks.md) | **Tại sao cần 12 khối Transformer Decoders?** | • Tại sao cần 12 khối mà không dùng 1 khối rộng 10.000 chiều?<br>• Tại sao lại là con số 12 (So sánh với 6 khối và 24-48 khối, giới hạn VRAM 16GB, tránh overfit trên Jira).<br>• 4 bài báo khoa học kinh điển mổ xẻ 12 khối: Google (*Tenney 2019*), Inria (*Jawahar 2019*), MIT (*Meng 2022 ROME*), Harvard (*Rogers 2020*).<br>• Code Python trích xuất và đo lường sự tiến hóa tri thức qua cả 12 khối bằng Cosine Similarity. |
| **08** | [08_streamlit_gpt2sp_tool_and_experimental_workflow.md](08_streamlit_gpt2sp_tool_and_experimental_workflow.md) | **Giải mã Công cụ Streamlit GPT2SP & Quy trình Thực nghiệm** | • Bản chất công cụ Web Streamlit: Chuyển AI từ "Hộp đen" sang "Hộp kính" (tăng độ tin cậy từ $19\%$ lên $75\%$).<br>• Kiến trúc 4 tầng: UI $\rightarrow$ Inference $\rightarrow$ Integrated Gradients $\rightarrow$ Historical Retrieval.<br>• Đánh đổi kỹ thuật: Độ trễ tính toán 50 bước đạo hàm của Integrated Gradients và rủi ro thiên kiến xác nhận.<br>• Mã nguồn hoàn chỉnh `app.py` và hướng dẫn chạy thực nghiệm cục bộ (`streamlit run`). |
| **09** | [09_data_leakage_analysis_and_action_plan.md](09_data_leakage_analysis_and_action_plan.md) | **GPT2SP đã giải quyết Data Leakage chưa & Kế hoạch Nhóm 3** | • Đối chiếu sự thật: GPT2SP có dùng TAWOS v1.1 không? (Không, dùng CSV Choetkiertikul 2016) và có Chronological Split không? (Có, nhưng chỉ ở cấp độ chia issue).<br>• Giải phẫu vì sao Chronological Split vẫn bị Data Leakage nặng nề: Rò rỉ văn bản Final Snapshot bên trong từng issue (Intra-issue Post-planning Leakage) và lệch mốc thời gian ước lượng.<br>• Kế hoạch hành động 5 trụ cột của Nhóm 3: Khai thác CSDL TAWOS v1.1, phục hồi trạng thái tại `SP_Estimation_Date`, và bài toán thực nghiệm đối chứng. |
| **10** | [10_research_directions_critical_evaluation.md](10_research_directions_critical_evaluation.md) | **Đánh giá Đa Tiêu chí & Xếp hạng 5 Hướng Nghiên cứu cho Hội nghị WSESE (1 tháng)** | • Đặt lên bàn cân 5 hướng nghiên cứu nhắm thẳng vào **Hội nghị Quốc tế WSESE** (Workshop on Methodological Issues with Empirical Studies in Software Engineering).<br>• Khung đánh giá MCDA 9 tiêu chí mở rộng: Khả thi trong 1 tháng, Độ khớp tôn chỉ WSESE & Tỷ lệ duyệt, Bằng chứng phương pháp luận, Tính xây dựng, Thực tế Scrum, Phản biện WSESE, Replication Package, Green AI, Kể chuyện số liệu.<br>• Ma trận điểm số định lượng: Hướng 5 ($9.53/10$), Hướng 4 ($9.37/10$), Hướng 3 ($8.83/10$), Hướng 2 ($8.68/10$), Hướng 1 ($4.10/10$).<br>• Chiến lược Tổ hợp Kim cương (Grand Hybrid Blueprint) và kế hoạch 4 tuần hoàn thành bài báo nộp WSESE với tỷ lệ duyệt cao nhất. |
| **11** | [11_implementation_guide_for_research_directions.md](11_implementation_guide_for_research_directions.md) | **Cẩm nang Thực thi Chi tiết Từng Hướng Nghiên cứu (Nộp WSESE)** | • Sổ tay kỹ thuật toàn diện hiện thực hóa các hướng nghiên cứu nộp Hội nghị WSESE trong 1 tháng.<br>• Truy vấn SQL CSDL TAWOS phục hồi trạng thái tại `SP_Estimation_Date`.<br>• Code Python mẫu: Baselines (Median, TF-IDF + Ridge), Phẫu thuật bóc tách 4 lát cắt rò rỉ (Waterfall plot), Mô hình tiến trình Agile sạch (SBERT + Velocity + LightGBM).<br>• Quy trình kiểm định phi tham số Wilcoxon & Cliff's Delta và cấu trúc đóng gói Replication Package đạt chuẩn Artifact Evaluation. |

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

* 📖 [Chương 3: Kiến trúc mô hình GPT2SP](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/explanation/03_the_gpt2sp_architecture.md)
* 🔬 [Case Study: Thực tế áp dụng kiến trúc trên Jira Issue XD-3751](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/case-study/case_study_gpt2sp_architecture.md)
* 📚 [Thuật ngữ chuyên ngành GPT2SP (Glossary)](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/glossary/README.md)
* 📑 [Báo cáo Tổng hợp Bài báo GPT2SP (IEEE TSE 2023)](file:///d:/NCKH_3/docs/articles/paper-information/paper_fu_2023_gpt2sp.md)
