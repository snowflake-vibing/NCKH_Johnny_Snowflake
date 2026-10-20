# 📖 CHƯƠNG 1: GIỚI THIỆU (INTRODUCTION)

> **Tài liệu gốc:** Trang 1 – 3, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả:** Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).

---

## 🎯 1. BỐI CẢNH & TẦM QUAN TRỌNG CỦA ƯỚC LƯỢNG STORY POINT

> *"Good estimation helps product owners optimize for efficiency and impact."*  
> — Một Giám đốc Sản phẩm tại Atlassian khẳng định [1].

Trong quy trình phát triển phần mềm theo phương pháp linh hoạt (Agile Software Development), **ước lượng điểm câu chuyện (Story Point Estimation)** là một trong những tác vụ khó khăn, phức tạp và mang tính quyết định nhất:
* **Khái niệm Story Point:** Là đơn vị đo lường nỗ lực tương đối (relative effort) cần thiết để hoàn thành trọn vẹn một hạng mục công việc trong sản phẩm (Product Backlog Item - PBI hoặc Issue).
* **Bốn yếu tố cấu thành nỗ lực:** Đội ngũ phát triển khi chấm điểm Story Point phải cân nhắc tổng hòa 4 khía cạnh:
  1. Khối lượng công việc dự kiến (*Amount of work*).
  2. Độ phức tạp kỹ thuật (*Technical complexity*).
  3. Các yếu tố rủi ro tiềm ẩn (*Risk*).
  4. Mức độ bất định hoặc thiếu thông tin ban đầu (*Uncertainty*).

### Thực trạng phương pháp truyền thống & Hệ quả tiêu cực
Hiện nay, các đội ngũ Agile chủ yếu sử dụng các kỹ thuật dựa trên sự đồng thuận nhóm như **Planning Poker**, phương pháp tương tự (**Analogy**) hoặc phán đoán của chuyên gia (**Expert Judgment**). Tuy nhiên, nghiên cứu của Usman et al. [53] đã chỉ ra rằng:
* Phán đoán mang nặng tính chủ quan của con người rất dễ đưa vào **thiên kiến nhận thức (cognitive bias)** và áp lực tâm lý từ các thành viên có tiếng nói lớn trong nhóm.
* **Hậu quả của ước lượng sai lệch:**
  * **Ước lượng quá cao (Overestimation):** Dẫn đến lãng phí thời gian nhàn rỗi của lập trình viên, suy giảm năng suất tổng thể và đẩy chi phí dự án lên cao (*cost overruns*).
  * **Ước lượng quá thấp (Underestimation):** Gây vỡ kế hoạch Sprint, trễ hạn bàn giao, kiệt sức (burnout) cho đội ngũ phát triển, giảm sút lòng tin của khách hàng và thậm chí làm thất bại toàn bộ dự án phần mềm.

---

## 🔍 2. SỰ TIẾN HÓA CỦA CÁC GIẢI PHÁP AI VÀ 3 HẠN CHẾ CHÍ TỬ CỦA DEEP-SE

Nhằm khắc phục tính chủ quan của con người, Trí tuệ nhân tạo (AI) và Học máy (ML) đã dần được áp dụng:
* **Giai đoạn đầu (Machine Learning cổ điển):** Porru et al. [36] sử dụng biểu diễn văn bản dạng túi từ (Bag-of-Words - BoW) kết hợp với các thuật toán học máy như Support Vector Machine (SVM). Nhược điểm: Phải thiết kế và trích xuất đặc trưng thủ công (hand-crafted features), tốn rất nhiều công sức và không nắm bắt được ngữ cảnh câu.
* **Giai đoạn học sâu (Deep Learning SOTA - Deep-SE):** Choetkiertikul et al. [7] công bố **Deep-SE**, mô hình học sâu đầu-cuối (end-to-end) sử dụng mạng Word2Vec kết hợp **Long Short-Term Memory (LSTM)** và **Recurrent Highway Network (RHWN)** để tự động học biểu diễn phân tán của từ vựng từ mô tả issue và dự đoán Story Point.

Tuy nhiên, bài báo GPT2SP vạch trần **3 giới hạn nghiêm trọng** khiến Deep-SE không thể ứng dụng hiệu quả trong thực tế:

| Giới hạn của Deep-SE | Nguyên nhân kỹ thuật | Hậu quả thực nghiệm |
| :--- | :--- | :--- |
| **1. Tốn thời gian & Không thể chuyển giao tri thức (Not Transferable)** | Deep-SE phải tự tiền huấn luyện một mô hình ngôn ngữ riêng biệt (project-specific) từ dữ liệu issue của từng dự án. | Mất **2 đến 7 giờ** chỉ để tiền huấn luyện cho mỗi dự án. Kho từ vựng bị bó hẹp trong các từ đã biết của dự án đó; khi mang sang dự án khác (cross-project), mô hình hoàn toàn thất bại. |
| **2. Bị giới hạn bộ nhớ ngắn hạn & Bỏ sót ngữ cảnh toàn cục** | Deep-SE dùng mạng hồi quy LSTM. Bộ nhớ ngắn hạn (short-term memory cell) của LSTM buộc phải làm mới (refresh) sau mỗi bước thời gian, khiến thông tin xa bị trôi mất. | Không thể nắm bắt mối quan hệ phụ thuộc dài hạn giữa các từ xa nhau trong mô tả issue dài; không chú ý đầy đủ đến vị trí từ trong ngữ cảnh toàn câu. |
| **3. Mô hình hộp đen, hoàn toàn không thể giải thích (Not Interpretable)** | Kiến trúc xếp chồng phức tạp của LSTM + RHWN không cung cấp bất kỳ manh mối nào về việc từ ngữ nào dẫn đến điểm số dự đoán. | Lập trình viên và Scrum Master không hiểu vì sao AI lại đưa ra con số đó, dẫn đến sự nghi ngờ, mất niềm tin và từ chối áp dụng trong các buổi Sprint Planning thực tế. |

---

## 💡 3. KIẾN TRÚC ĐỀ XUẤT: GPT2SP (TRANSFORMER-BASED)

Để giải quyết triệt để 3 rào cản trên, Fu & Tantithamthavorn đề xuất **GPT2SP**:
1. **Khai thác Mô hình Ngôn ngữ Nền tảng (Foundation Model):** Tận dụng mô hình **GPT-2** đã được tiền huấn luyện trên quy mô khổng lồ (40GB văn bản từ 8 triệu trang web). Nhờ vốn tri thức ngôn ngữ bao quát, mô hình hiểu sâu sắc quan hệ ngữ nghĩa của từ ngữ kỹ thuật mà **không cần tiền huấn luyện lại từ đầu cho từng dự án** (tiết kiệm 2-7 giờ tính toán).
2. **Cơ chế Masked Multi-Head Self-Attention:** Cho phép từng từ trong mô tả issue "chú ý" đồng thời đến mọi từ khác trong câu cùng vị trí chính xác của nó (Positional Encoding), giúp nắm bắt trọn vẹn ngữ cảnh kỹ thuật phức tạp của yêu cầu phần mềm.
3. **Phân tách từ con Byte-Pair Encoding (BPE):** Giữ nguyên các từ vựng phổ biến và phân rã các thuật ngữ lập trình hiếm gặp thành các mẩu subword thông dụng, giải quyết triệt để vấn đề từ mới ngoài từ điển (Out-of-Vocabulary - OOV).
4. **Trí tuệ nhân tạo có thể giải thích (XAI):** Tận dụng trực tiếp trọng số chú ý (Attention Weights) và thuật toán Gradient Tích phân (Integrated Gradients) để tô sáng chính xác những từ ngữ then chốt (keywords) chi phối quyết định Story Point, kèm ví dụ đối chứng trong quá khứ.

---

## 📊 4. TÓM TẮT KẾT QUẢ THỰC NGHIỆM ĐỘT PHÁ

Nghiên cứu tiến hành đánh giá quy mô lớn trên **23.313 issues** thuộc **16 dự án mã nguồn mở lớn** với 10 mô hình baseline đối chứng:

```mermaid
flowchart LR
    A["Tập Dữ Liệu Thực Nghiệm\n23.313 Jira Issues (16 Projects)"] --> B["Thực Nghiệm 1: RQ1\nƯớc lượng Nội dự án (Within-Project)"]
    A --> C["Thực Nghiệm 2: RQ2\nƯớc lượng Liên dự án (Cross-Project)"]
    A --> D["Thực Nghiệm 3: RQ3\nPhân tích Triệt tiêu (Ablation Study)"]

    B --> B1["GPT2SP đạt Median MAE = 1.16\nChính xác hơn 34% - 57% so với 9 baselines"]
    C --> C1["GPT2SP đạt Median MAE = 2.14\nVượt trội Deep-SE 39%, ABE0 49%"]
    D --> D1["Kiến trúc Transformer giúp cải thiện\nDeep-SE từ 6% đến 47%"]
```

### Các phát hiện thực nghiệm then chốt:
* **RQ1 (Ước lượng Nội dự án):** GPT2SP đạt sai số tuyệt đối trung vị $\text{MAE} = 1.16$, vượt trội vượt bậc so với Deep-SE ($\text{MAE} = 2.08$) và các phương pháp học máy truyền thống (Doc2Vec, Random Forest, SVM, Mean/Median Baseline).
* **RQ2 (Ước lượng Liên dự án):** Trong kịch bản chuyển giao giữa các tổ chức khác biệt (Cross-Repository), GPT2SP đạt $\text{MAE} = 2.14$, vượt Deep-SE (3.82) tới **$39\%$** và phương pháp tương đồng kinh điển ABE0 (4.55) tới **$49\%$**.
* **RQ3 (Nghiên cứu triệt tiêu thành phần - Ablation Study):** Việc thay thế LSTM bằng khối Transformer Decoder giúp cải thiện hiệu năng của Deep-SE từ **$6\%$ đến $47\%$** (trung vị $34\%$), khẳng định kiến trúc Transformer là nhân tố cốt lõi tạo nên bước nhảy vọt.
* **Khảo sát thực tế với 16 chuyên gia Agile:**
  * Đa số chuyên gia nhận định việc ước lượng Story Point là tác vụ "cực kỳ thách thức" (*extremely challenging*).
  * Mô hình AI có kèm giải thích minh chứng (Explainable AI) được đánh giá là **đáng tin cậy hơn và hữu ích hơn vượt trội** so với mô hình hộp đen.
  * **$69\%$** chuyên gia sẵn sàng tích hợp công cụ GPT2SP vào các nền tảng quản trị công việc hàng ngày như Atlassian Jira.

---

## 🏆 5. NĂM ĐÓNG GÓP KHOA HỌC CHÍNH (CONTRIBUTIONS)

Theo tuyên bố của tác giả, bài báo mang lại 5 đóng góp học thuật đầu tiên trong lĩnh vực Kỹ nghệ Phần mềm (SE):
1. **Tiên phong áp dụng Transformer cho Story Point:** Là công trình đầu tiên ứng dụng mô hình nền tảng ngôn ngữ Transformer (GPT-2) để giải quyết bài toán hồi quy ước lượng Story Point trong Agile.
2. **Đánh giá thực nghiệm toàn diện nhất:** Khảo sát trên 23.313 issues của 16 dự án, so sánh đối chứng chặt chẽ với 10 phương pháp baseline trên cả hai kịch bản trong nội bộ dự án và liên dự án.
3. **Phân tích bóc tách thành phần (Ablation Study):** Định lượng rành mạch đóng góp riêng biệt của bộ phân tách từ con (BPE) và các khối chú ý Transformer.
4. **Phát triển công cụ minh chứng XAI thực tế:** Xây dựng ứng dụng web Streamlit trực quan, hỗ trợ lập trình viên tra cứu từ ngữ quan trọng và các ví dụ tương đồng trong lịch sử.
5. **Khoa học mở (Open Science):** Toàn bộ mã nguồn, dữ liệu huấn luyện, checkpoint mô hình trên Hugging Face và kết quả dự đoán thô đều được công khai tại:
   * GitHub: [awsm-research/gpt2sp](https://github.com/awsm-research/gpt2sp)
   * Demo Web App: [awsm-research/gpt2sp_webapp](https://share.streamlit.io/awsm-research/gpt2sp_webapp/main/app.py)
