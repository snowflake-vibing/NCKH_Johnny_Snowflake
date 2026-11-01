# 🤖 HỆ TRI THỨC VÀ PHÂN TÍCH CHUYÊN SÂU MÔ HÌNH GPT2SP
## "GPT2SP: A Transformer-Based Agile Story Point Estimation Approach" (IEEE TSE 2023)

> Thư mục này tập hợp toàn bộ tri thức số hóa, giải phẫu kiến trúc, nghiên cứu tình huống thực tế và các phân tích phản biện khoa học chuyên sâu về mô hình **GPT2SP** (Fu & Tantithamthavorn, *IEEE Transactions on Software Engineering 2023*).

---

## 📂 Cấu Trúc Hệ Tri Thức GPT2SP

```text
docs/articles/paper-information/gpt2sp/
├── code/               # Toàn bộ mã nguồn gốc GPT2SP và giải thích chi tiết đối ứng bài báo
├── explanation/        # Phân tích chi tiết từng chương (Chương 1 - 10 & Phụ lục của bài báo)
├── case-study/          # Nghiên cứu tình huống thực tế trên Jira Issue XD-3751 & các khối kiến trúc
├── critical-thinking/   # 15 bài phân tích phản biện chuyên sâu, toán học, rò rỉ dữ liệu & hướng đi WSESE
├── glossary/            # Từ điển tra cứu thuật ngữ chuyên ngành (BPE, Self-Attention, GELU, Regressor...)
└── README.md            # Mục lục điều hướng tổng quan (Tài liệu này)
```

---

## 💻 0. [code/](code/README.md) — Toàn Bộ Mã Nguồn & Giải Mã Source Code
* **[00_full_source_code.md](code/00_full_source_code.md):** Lưu trữ 100% nguyên văn toàn bộ mã nguồn gốc GPT2SP (GPT2SP.py và model_training_notebook.ipynb).
* **[01_architecture_code_explanation.md](code/01_architecture_code_explanation.md):** Giải thích chi tiết mã nguồn kiến trúc mô hình (GPT2SP.py) đối ứng với Section 3 bài báo.
* **[02_training_pipeline_code_explanation.md](code/02_training_pipeline_code_explanation.md):** Giải thích chi tiết mã nguồn pipeline huấn luyện và đánh giá thực nghiệm RQ1, RQ2.
* **[03_code_vs_paper_discrepancies.md](code/03_code_vs_paper_discrepancies.md):** Mổ xẻ 4 điểm sai lệch cốt tử giữa code thực tế và công bố trong bài báo IEEE TSE 2023.

---

## 📑 1. [explanation/](explanation/README.md) — Phân Tích Chi Tiết Từng Chương
* **[00_executive_report_and_partner_briefing.md](explanation/00_executive_report_and_partner_briefing.md):** **Báo cáo điều hành & Kế hoạch hành động tổng thể (Dành cho Partner)**.
* **[01_introduction.md](explanation/01_introduction.md):** Đặt vấn đề, bối cảnh ước lượng Agile và đóng góp của bài báo.
* **[02_background.md](explanation/02_background.md):** Kiến thức nền tảng về Story Point và Transformer Decoders.
* **[03_the_gpt2sp_architecture.md](explanation/03_the_gpt2sp_architecture.md):** Kiến trúc tổng thể mô hình GPT2SP.
  * [03-1-model_architecture.md](explanation/03-1-model_architecture.md): Cấu tạo chi tiết các tầng nơ-ron.
  * [03-2-forward_pass.md](explanation/03-2-forward_pass.md): Dòng chảy dữ liệu xuôi (Forward Pass).
  * [03-3-backpropagation_and_optimization.md](explanation/03-3-backpropagation_and_optimization.md): Lan truyền ngược và tối ưu hóa AdamW.
* **[04_experimental_setup.md](explanation/04_experimental_setup.md):** Tập dữ liệu và thiết lập phân chia Chronological Split.
* **[05_experimental_design_and_results.md](explanation/05_experimental_design_and_results.md):** 4 câu hỏi nghiên cứu (RQ1 - RQ4) và kết quả.
* **[06_xai_tool_and_practitioner_survey.md](explanation/06_xai_tool_and_practitioner_survey.md):** Công cụ Web Streamlit XAI và khảo sát 16 chuyên gia Agile.
* **[07_discussion.md](explanation/07_discussion.md) - [11_appendix.md](explanation/11_appendix.md):** Thảo luận, nghiên cứu liên quan, các mối đe dọa giá trị và phụ lục.
* **[12_gpt2sp_code_audit_and_reproduction_discrepancies.md](explanation/12_gpt2sp_code_audit_and_reproduction_discrepancies.md):** Báo cáo thẩm định mã nguồn & 4 sai lệch thực nghiệm giữa bài báo và repo GitHub.

---

## 🔬 2. [case-study/](case-study/README.md) — Nghiên Cứu Tình Huống Thực Tế
* **[00_case_study_jira_raw_to_token_pipeline.md](case-study/00_case_study_jira_raw_to_token_pipeline.md):** Từ Jira ticket thô đến chuỗi tokens và padding tensor.
* **[case_study_gpt2sp_architecture.md](case-study/case_study_gpt2sp_architecture.md):** Giải mã dòng chảy dữ liệu trên Jira Issue cụ thể **XD-3751** (Spring XD).
* **[01_case_study_12_transformer_decoders.md](case-study/01_case_study_12_transformer_decoders.md):** Dòng chảy tính toán qua 12 khối Transformer Decoders.
* **[03_case_study_last_token_pooling_xd3751.md](case-study/03_case_study_last_token_pooling_xd3751.md):** Cắt lát tensor [1, 48, 768] trích xuất vector token thứ 48.
* **[02_case_study_mlp_regressor_head.md](case-study/02_case_study_mlp_regressor_head.md):** Trích xuất Last Token Embedding và dự đoán qua đầu hồi quy MLP.
* **[04_case_study_training_phase.md](case-study/04_case_study_training_phase.md):** Quá trình huấn luyện, tính hàm mất mát MSE và cập nhật trọng số.
* **[05_case_study_inference_phase.md](case-study/05_case_study_inference_phase.md):** Quy trình suy luận thực tế khi người dùng nhập User Story mới.
* **[06_case_study_intra_issue_temporal_leakage_evidence.md](case-study/06_case_study_intra_issue_temporal_leakage_evidence.md):** Bằng chứng thực nghiệm bằng mắt về rò rỉ nội tại: Planning vs Lúc đóng ticket XD-3751.
* **[07_case_study_leakage_free_contextual_features_xd3751.md](case-study/07_case_study_leakage_free_contextual_features_xd3751.md):** Tái dựng đặc trưng tiến trình Agile sạch tại mốc planning nạp vào LightGBM.

---

## 🧠 3. [critical-thinking/](critical-thinking/README.md) — Phân Tích Phản Biện Khoa Học Chuyên Sâu
* **[01_subword_vocabularies_50257.md](critical-thinking/01_subword_vocabularies_50257.md):** Nguồn gốc kích thước từ điển BPE $50.257$.
* **[02_why_hidden_dimension_768.md](critical-thinking/02_why_hidden_dimension_768.md):** Bản chất phần cứng GPU và con số 768 chiều ẩn.
* **[03_why_qkv_2304_and_ffn_3072.md](critical-thinking/03_why_qkv_2304_and_ffn_3072.md):** Ma trận Fused QKV 2304 và tầng FFN $4\times$ (3072).
* **[04_origin_of_layers_heads_and_head_dimension.md](critical-thinking/04_origin_of_layers_heads_and_head_dimension.md):** Cội nguồn học thuật của $L=12$, $H=12$, $d_k=64$ từ các bài báo kinh điển.
* **[05_merge_operations_and_subword_vocabularies.md](critical-thinking/05_merge_operations_and_subword_vocabularies.md):** Cơ chế Merge Operations và thuật toán BPE từ con số 0.
* **[06_why_4x_expansion_triggers_neuron_activation.md](critical-thinking/06_why_4x_expansion_triggers_neuron_activation.md):** Định lý Cover và lý do nơ-ron bừng sáng ở tầng FFN.
* **[07_why_12_transformer_decoder_blocks.md](critical-thinking/07_why_12_transformer_decoder_blocks.md):** Sự tiến hóa tri thức qua 12 khối giải mã.
* **[08_streamlit_gpt2sp_tool_and_experimental_workflow.md](critical-thinking/08_streamlit_gpt2sp_tool_and_experimental_workflow.md):** Giải mã kiến trúc công cụ Web Streamlit XAI.
* **[09_data_leakage_analysis_and_action_plan.md](critical-thinking/09_data_leakage_analysis_and_action_plan.md):** Phân tích rò rỉ dữ liệu (Intra-issue Temporal Leakage) trong GPT2SP & Kế hoạch Nhóm 3.
* **[10_research_directions_critical_evaluation.md](critical-thinking/10_research_directions_critical_evaluation.md):** Đánh giá đa tiêu chí 9 trục MCDA & xếp hạng các hướng nghiên cứu nhắm đến **Hội nghị WSESE**.
* **[11_implementation_guide_for_research_directions.md](critical-thinking/11_implementation_guide_for_research_directions.md):** Sổ tay kỹ thuật thực thi chi tiết từ CSDL TAWOS, bóc tách kênh rò rỉ đến mô hình tiến trình Agile sạch.
* **[12_from_generative_llm_to_regression_head.md](critical-thinking/12_from_generative_llm_to_regression_head.md):** Giải phẫu cơ chế biến GPT-2 từ mô hình sinh chữ thành đầu hồi quy số thực.
* **[13_why_last_token_pooling_not_first_or_mean.md](critical-thinking/13_why_last_token_pooling_not_first_or_mean.md):** Bản chất toán học của Causal Masking và lý do bắt buộc lấy Last Token.
* **[14_why_mlp_regressor_head_architecture.md](critical-thinking/14_why_mlp_regressor_head_architecture.md):** Giải phẫu cấu trúc 2 tầng của MLP Regressor Head ( \rightarrow 768 \rightarrow 1$) và hàm kích hoạt GELU.

---

## 📚 4. [glossary/](glossary/README.md) — Từ Điển Thuật Ngữ Chuyên Ngành
* Tra cứu nhanh hơn 20 thuật ngữ cốt lõi: Byte-Pair Encoding, Self-Attention, GELU, Residual Connection, MLP Regressor Head, Backpropagation, Cliff's Delta, Wilcoxon Test...

---

## 🔗 Liên Kết Điều Hướng Hệ Thống
* 📄 [Báo cáo Tổng hợp Bài báo GPT2SP (Literature Matrix)](../paper_fu_2023_gpt2sp.md)
* 📜 [Quy chế vận hành Agent (AGENTS.md)](file:///d:/NCKH_3/AGENTS.md)
* 🛡️ [Quy tắc Chống Rò rỉ Dữ liệu (RULE.md)](file:///d:/NCKH_3/docs/draft/RULE.md)
