# 📖 CHƯƠNG 10: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN (CONCLUSION & FUTURE WORK)

> **Tài liệu gốc:** Trang 15, bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023).  
> **Tác giả:** Michael Fu, Chakkrit Tantithamthavorn (Đại học Monash, Úc).

---

## 🏁 1. TỔNG KẾT TOÀN BỘ CÔNG TRÌNH NGHIÊN CỨU

Bài báo khoa học của Fu & Tantithamthavorn (2023) đã giải quyết thành công 3 hạn chế căn bản của mô hình học sâu SOTA tiền nhiệm (Deep-SE) bằng việc đề xuất phương pháp **GPT2SP**:

1. **Khắc phục triệt để bài toán Out-of-Vocabulary (OOV):** Khai thác giải thuật phân tách từ con **Byte-Pair Encoding (BPE)**, cho phép xử lý mượt mà mọi thuật ngữ kỹ thuật, định danh biến và từ vựng mới mà không bị giới hạn trong kho ngữ liệu cục bộ.
2. **Nâng tầm năng lực biểu diễn ngữ cảnh dài hạn:** Ứng dụng mô hình nền tảng **GPT-2** với các khối giải mã **Transformer Decoders** và cơ chế **Masked Multi-Head Self-Attention**, loại bỏ hoàn toàn nút thắt cổ chai về bộ nhớ ngắn hạn của mạng nơ-ron hồi quy LSTM.
3. **Minh bạch hóa quá trình suy luận (Explainable AI):** Trích xuất trọng số Attention và thuật toán Gradient Tích phân để tô sáng các từ ngữ quyết định độ khó của task và truy hồi các ví dụ minh chứng trong lịch sử.

---

## 📊 2. CÁC CON SỐ MINH CHỨNG THỰC NGHIỆM ĐÁNG NHỚ

Qua chiến dịch thực nghiệm khổng lồ trên **23.313 Jira issues** thuộc **16 dự án mã nguồn mở lớn**:
* **Ước lượng Nội dự án (Within-Project):** Đạt sai số tuyệt đối trung vị $\text{MAE} = 1,16$, chính xác hơn từ **$34\%$ đến $57\%$** so với 9 mô hình baseline hiện có (trong đó giảm sai số của Deep-SE từ $6\%$ đến $47\%$).
* **Ước lượng Chuyển giao Liên dự án (Cross-Project):** Đạt $\text{MAE} = 2,14$, vượt trội **$39\%$ so với Deep-SE** và **$49\%$ so với phương pháp tương đồng ABE0**.
* **Hiệu năng huấn luyện vượt bậc:** Thời gian huấn luyện mô hình cực kỳ tối ưu, chỉ mất từ **3 đến 39 giây** (trung bình 14 giây/dự án) trên một GPU thương mại duy nhất (RTX 3090).
* **Khảo sát chuyên gia Agile thực tế:**
  * Mô hình có giải thích (XAI) đạt mức độ hữu ích **$88\%$** (so với $31\%$ khi không có giải thích) và mức độ tin cậy **$75\%$** (so với $19\%$).
  * **$69\%$** chuyên gia khẳng định sẵn sàng tích hợp công cụ vào Jira để hỗ trợ các buổi Sprint Planning.

---

## 🌐 3. CAM KẾT KHOA HỌC MỞ (OPEN SCIENCE ARTIFACTS)

Để thúc đẩy tính minh bạch và khả năng tái lập trong cộng đồng nghiên cứu Kỹ nghệ Phần mềm thế giới, nhóm tác giả đã công khai toàn bộ tài nguyên:
* **Mã nguồn và Dữ liệu thực nghiệm trên GitHub:**  
  👉 [`https://github.com/awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp)  
  Bao gồm toàn bộ các script huấn luyện PyTorch, dữ liệu 16 file CSV gốc và bảng kết quả dự đoán thô (raw predictions).
* **Mô hình tiền huấn luyện trên Hugging Face:**  
  👉 Checkpoint các mô hình đã tinh chỉnh cho từng dự án (đặc biệt là mô hình cho `Spring XD`).
* **Ứng dụng Web trực quan Streamlit:**  
  👉 [`https://share.streamlit.io/awsm-research/gpt2sp_webapp/main/app.py`](https://share.streamlit.io/awsm-research/gpt2sp_webapp/main/app.py)

---

## 🚀 4. CÁC HƯỚNG NGHIÊN CỨU MỞ RỘNG TRONG TƯƠNG LAI (FUTURE WORK)

Nhóm tác giả đề xuất 3 định hướng phát triển tiếp theo cho cộng đồng nghiên cứu:
1. **Nghiên cứu hiện trường trên quy mô doanh nghiệp (Field User Studies):** Triển khai thử nghiệm thực tế trong các môi trường phát triển phần mềm thương mại khép kín nhằm đo lường mức độ tiết kiệm thời gian họp Sprint Planning và sự cải thiện độ chính xác nỗ lực trong các chu kỳ Sprint dài hạn.
2. **Khai thác dữ liệu đa phương thức (Multimodal Information Fusion):** Tích hợp thêm các dữ liệu phi văn bản trong Jira Issue như: hình ảnh chụp màn hình đính kèm (screenshots), đoạn mã nguồn mẫu đính kèm trong mô tả, đồ thị phụ thuộc giữa các issue (Issue Link Graph) và thông tin thành viên (assignee, reporter).
3. **Thử nghiệm các kiến trúc LLM tiên tiến hơn:** Khảo sát năng lực của các mô hình ngôn ngữ lớn mạnh mẽ hơn (như RoBERTa, CodeBERT, T5, LLaMA) và các phương pháp tinh chỉnh tham số hiệu quả (PEFT / LoRA).
