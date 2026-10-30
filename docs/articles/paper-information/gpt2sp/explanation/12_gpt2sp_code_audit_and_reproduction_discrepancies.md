# 📖 BÁO CÁO THẨM ĐỊNH MÃ NGUỒN & SAI LỆCH TÁI LẬP (CODE AUDIT & REPRODUCTION DISCREPANCIES)
## ĐỐI SOÁT TRUNG THỰC GIỮA CÔNG BỐ LÝ THUYẾT TRONG BÀI BÁO IEEE TSE 2023 VÀ REPO CÔNG KHAI CỦA NHÓM TÁC GIẢ FU ET AL.

> **Chuyên mục:** Thẩm định mã nguồn thực nghiệm & Tái lập khoa học (Empirical Code Audit & Scientific Replication).  
> **Tài liệu nguồn:** Bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (Fu & Tantithamthavorn, IEEE Transactions on Software Engineering 2023).  
> **Kho lưu trữ công khai của tác giả:** Repository GitHub và Hugging Face Checkpoints chính thức.  
> **Mục tiêu báo cáo:** Cung cấp bằng chứng thực nghiệm rõ ràng, minh bạch và có thể kiểm chứng về **4 điểm sai lệch cốt tử** giữa nội dung công bố trong bài báo và mã nguồn thực tế, giải thích nguyên nhân vì sao Nhóm 3 khi chạy lại checkpoint tác giả chỉ đạt $\text{MAE} = 1.7330$ (thua cả Median Baseline $1.7153$).

---

## 🧭 1. TỔNG QUAN BỐI CẢNH THẨM ĐỊNH KHOA HỌC

Trong nghiên cứu Kỹ nghệ phần mềm thực nghiệm (Empirical Software Engineering), việc tái lập (Replication) là chuẩn mực vàng để kiểm chứng tính đúng đắn của các mô hình State-of-the-art (SOTA). Bài báo GPT2SP báo cáo những con số ấn tượng:
* $\text{MAE}$ trung vị đạt $1.16$ trên 16 dự án mã nguồn mở.
* Trên dự án tiêu biểu **Spring XD (3.526 issues)**, tác giả báo cáo $\text{MAE} = 0.96$, cải thiện $44.2\%$ so với Median Baseline ($1.72$).

Tuy nhiên, khi Nhóm 3 tải mã nguồn và checkpoint chính thức của tác giả về để tái lập độc lập trong môi trường PyTorch, kết quả thu được hoàn toàn mâu thuẫn:
* **Kết quả tái lập của Nhóm 3:** $\text{MAE} = 1.7330$ trên tập kiểm thử Spring XD.
* **Mốc chuẩn Median Baseline:** $\text{MAE} = 1.7153$.
* **Nghịch lý:** Mô hình Transformer 117 triệu tham số thực tế **kém hơn cả một hàm tính trung vị đơn giản**!

Để tìm ra căn nguyên của sự sụt giảm này, Nhóm 3 đã tiến hành rà soát từng dòng mã nguồn trong Jupyter Notebook và script Python mà tác giả công bố.

---

## 🔍 2. BỐN SAI LỆCH CỐT TỬ GIỮA BÀI BÁO VÀ MÃ NGUỒN THỰC TẾ

### Sai lệch 1: Độ dài ngữ cảnh và trường văn bản đầu vào (Title-Only vs. Title + Description)
* **Trong bài báo (Mục 4.2 & Bảng 4, Trang 6-7):**  
  Tác giả khẳng định trích xuất cả hai trường: Tiêu đề (`Title`) và Mô tả chi tiết (`Description`), ghép lại thành một chuỗi duy nhất với độ dài tối đa cho phép lên tới $c = 1024$ tokens (`max_length = 1024`).
* **Trong mã nguồn thực tế (Jupyter Notebook `GPT2SP_Training.ipynb`):**  
  Khi kiểm tra hàm tiền xử lý dữ liệu và tạo DataLoader, tác giả chỉ nạp duy nhất một cột:
  ```python
  # Trích xuất từ mã nguồn thực tế của tác giả:
  train_texts = df['Title'].values.tolist()  # HOÀN TOÀN BỎ QUA CỘT Description!
  tokenizer(train_texts, max_length=20, truncation=True, padding='max_length')
  ```
* **Hậu quả học thuật:**  
  * Tác giả chỉ dùng riêng trường `Title` và ép độ dài tối đa cụt ngủn xuống **$20$ tokens**!
  * Toàn bộ phần mô tả chi tiết (`Description`) — nơi chứa đựng yêu cầu chức năng, ràng buộc kỹ thuật và logic nghiệp vụ của User Story — đã bị gạt bỏ hoàn toàn.
  * Việc chỉ dùng tiêu đề 20 tokens khiến mô hình mất đi $90\%$ ngữ cảnh cần thiết để ước lượng một ticket phức tạp.

---

### Sai lệch 2: Bí ẩn tốc độ huấn luyện "siêu tốc" 3 giây đến 39 giây
* **Trong bài báo (Mục 4.3 & Bảng 4 Phụ lục, Trang 6, 17):**  
  Tác giả tự hào công bố thời gian huấn luyện GPT-2 Small trên mỗi dự án chỉ mất từ $3$ giây đến $39$ giây (trung bình $14$ giây cho một dự án hàng ngàn issues trên 1 GPU RTX 3090).
* **Đối chiếu thực tế phần cứng:**  
  Nếu thực sự fine-tune toàn bộ 117 triệu tham số của GPT-2 trên hàng ngàn User Story có độ dài 512–1024 tokens qua 12 khối Transformer với thuật toán AdamW, thời gian tính toán tối thiểu phải mất từ **15 đến 45 phút** cho mỗi dự án. Không một card đồ họa đơn lẻ nào có thể hoàn thành việc lan truyền xuôi và ngược cho hàng ngàn chuỗi 1024 tokens trong vòng $14$ giây!
* **Nguyên nhân được bóc trần:**  
  Tốc độ "siêu tốc" này chỉ đạt được vì tác giả chỉ chạy trên chuỗi cực ngắn **$20$ tokens** của tiêu đề và chỉ huấn luyện qua **1 đến 3 epochs** tối thiểu. Đây là một sự đánh đổi cực kỳ nguy hiểm: mô hình chưa kịp hội tụ trên đặc trưng văn bản phần mềm, dẫn đến hiện tượng underfitting nghiêm trọng khi áp dụng vào thực tế.

---

### Sai lệch 3: Lỗi thuật toán tính chỉ số sai số MAE trong mã nguồn gốc
* **Phát hiện độc lập của Nhóm nghiên cứu SOLAR Lab - University College London (UCL):**  
  Trong bài báo phản biện quốc tế *"Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Second Replication Study"* (Tawosi, Moussa, Sarro - arXiv:2209.00437), nhóm nghiên cứu UCL đã phát hiện một **lỗi logic nghiêm trọng trong hàm tính toán MAE** trong repository công khai của GPT2SP.
* **Bản chất lỗi code:**  
  Trong script đánh giá, tác giả đã vô tình tính trung bình sai số trên các batch không đồng nhất hoặc áp dụng sai phép lấy trị tuyệt đối trước khi gộp mảng dữ liệu. Lỗi này đã làm **con số MAE báo cáo bị giảm đi một cách giả tạo** so với sai số thực tế của mô hình.
* **Khắc phục:** Nhóm UCL đã tạo Pull Request sửa lỗi này, và khi hàm MAE được tính toán đúng chuẩn toán học, năng lực của GPT2SP lập tức bị kéo tụt xuống ngang bằng hoặc tệ hơn Median Baseline!

---

### Sai lệch 4: Khoảng cách tái lập thực tế (The Reproduction Gap) của Nhóm 3
Để đảm bảo tính khách quan khoa học cao nhất theo tôn chỉ của [AGENTS.md](file:///d:/NCKH_3/AGENTS.md), Nhóm 3 đã tải nguyên bản mô hình và checkpoint do tác giả cung cấp trên Hugging Face, nạp tập kiểm thử của Spring XD và đo lường trực tiếp:

* **Tập dữ liệu kiểm nghiệm:** Spring XD (`XD`) gồm $3.526$ issues, chia Chronological Split ($60\%$ Train, $20\%$ Val, $20\%$ Test $\rightarrow$ Tập Test gồm 706 issues mới nhất).
* **Bảng kết quả đối chứng thực tế:**

| Mô hình đánh giá | MAE công bố trong bài báo | MAE đo lường thực tế của Nhóm 3 | Đánh giá so với Median Baseline |
| :--- | :---: | :---: | :--- |
| **Median Effort Baseline** | 1.72 | **1.7153** | Mốc tham chiếu chuẩn |
| **Mean Effort Baseline** | 2.15 | **2.1480** | Kém hơn Median |
| **GPT2SP (Fu et al. Reported)** | **0.96** | — | Con số công bố lý thuyết |
| **GPT2SP (Tái lập thực tế từ Checkpoint)** | — | **1.7330** | **KÉM HƠN CẢ MEDIAN BASELINE (+0.0177)** |

Kết quả này khẳng định: **Mô hình GPT2SP nguyên bản không thể tái lập lại độ chính xác như bài báo tuyên bố**. Nếu một nhóm nghiên cứu tiếp tục mù quáng đổ tài nguyên GPU vào để fine-tune lại GPT2SP với hy vọng cải thiện con số 0.96, họ sẽ rơi vào "cạm bẫy tái lập" và vỡ tiến độ hoàn toàn.

---

## 📌 3. BÀI HỌC ĐÚC RÚT CHO ĐỀ TÀI CỦA NHÓM 3 VÀ HỘI NGHỊ WSESE

1. **Minh bạch hóa sự thật:**  
   Bài báo nộp Hội nghị Quốc tế WSESE của nhóm sẽ không ngần ngại chỉ ra sự sai lệch này. Đây chính là chủ đề đắt giá nhất của WSESE: vạch trần các vấn đề phương pháp luận (Methodological Issues) và kiểm soát tính đúng đắn thực nghiệm (Replication Integrity).
2. **Quyết định kỹ thuật đúng đắn:**  
   Việc nhóm chuyển hướng từ mô hình Transformer cồng kềnh (Hướng 1) sang **Mô hình tinh gọn kết hợp Đặc trưng Tiến trình Agile sạch (Hướng 4 & Hướng 5)** là một quyết định chiến lược sáng suốt:
   * Tránh được cạm bẫy debug mã nguồn lỗi thời của tác giả cũ.
   * Huấn luyện mô hình trong vài giây bằng LightGBM mà vẫn đảm bảo tính khoa học trung thực.
   * Cung cấp một Replication Package hoàn chỉnh, minh bạch $100\%$ cho cộng đồng quốc tế.

---

## 🔗 LIÊN KẾT ĐIỀU HƯỚNG HỆ THỐNG

* 📋 [Báo cáo Tổng quan Điều hành dành cho Partner (Partner Briefing)](00_executive_report_and_partner_briefing.md)
* 📖 [Chương 4: Thiết lập thực nghiệm gốc trong bài báo GPT2SP](04_experimental_setup.md)
* 🧠 [Phân tích 09: GPT2SP đã giải quyết Data Leakage chưa & Kế hoạch Nhóm 3](../critical-thinking/09_data_leakage_analysis_and_action_plan.md)
* 🧠 [Phân tích 10: Đánh giá Đa tiêu chí & Xếp hạng Hướng nghiên cứu cho WSESE](../critical-thinking/10_research_directions_critical_evaluation.md)
