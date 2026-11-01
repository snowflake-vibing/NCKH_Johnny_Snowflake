# 📖 ĐỐI SOÁT & MỔ XẺ SAI LỆCH GIỮA CODE THỰC TẾ VÀ BÀI BÁO GPT2SP
## BẢN THẨM ĐỊNH KHOA HỌC DÀNH CHO NHÓM NCKH 3 (JOHNNY SNOWFLAKE)

> **Mục tiêu tài liệu:** Tổng kết các phát hiện then chốt sau khi đối soát từng dòng mã nguồn trong thư mục [`code/`](file:///d:/NCKH_3/docs/articles/paper-information/gpt2sp/code/) với văn bản công bố của bài báo *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE TSE 2023), giúp nhóm nghiên cứu có cơ sở vững chắc để xây dựng phương pháp luận vượt trội cho đề tài.

---

## 🧭 1. MA TRẬN ĐỐI SOÁT TỔNG THỂ

| Tiêu chí kỹ thuật | Công bố trong Bài Báo (*IEEE TSE 2023*) | Cài đặt thực tế trong Mã Nguồn GitHub | Đánh giá & Tác động học thuật |
| :--- | :--- | :--- | :--- |
| **Trường văn bản đầu vào** | `Title` + `Description` ghép lại thành một chuỗi | Chỉ nạp riêng `data['title']`, bỏ qua hoàn toàn `description` | 🔴 **SAI LỆCH NGHIÊM TRỌNG:** Mô hình mất đi 90% ngữ cảnh kỹ thuật chi tiết của User Story. |
| **Độ dài ngữ cảnh tối đa** | Lên đến 1.024 tokens (`max_length = 1024`) | Cắt cụt ngủn xuống **20 tokens** (`SEQUENCE_LEN = 20`) | 🔴 **SAI LỆCH NGHIÊM TRỌNG:** Hầu hết các yêu cầu dài đều bị cắt bỏ, chỉ giữ lại vài từ đầu của tiêu đề. |
| **Thời gian huấn luyện** | Trung bình 14 giây/dự án (nhanh nhất 3s, chậm nhất 39s) | Chạy siêu nhanh vì chỉ nạp 20 tokens cho 1–3 epochs | 🟡 **LÝ GIẢI BÍ MẬT:** Tốc độ cao không phải do thuật toán tối ưu mà do giảm tải dữ liệu đầu vào. |
| **Kiến trúc MLP Head** | Mạng nơ-ron đa tầng kết hợp phi tuyến | 2 tầng Dense tuyến tính liên tiếp **không có hàm kích hoạt** | 🟡 **THIẾU KÍCH HOẠT:** Về mặt toán học tương đương một phép chiếu tuyến tính ma trận đơn cấp. |
| **Hàm mất mát huấn luyện** | L1 Loss nhằm kháng ngoại lai | Khớp chính xác `loss_fct = nn.L1Loss()` | 🟢 **ĐỒNG NHẤT 100%:** Mô hình thực sự tối ưu theo sai số tuyệt đối MAE. |
| **Phân chia dữ liệu** | Chronological Split 60% Train, 20% Val, 20% Test | Khớp chính xác trong hàm `within_project_split()` | 🟢 **ĐỒNG NHẤT 100%:** Dữ liệu có được xếp theo thứ tự thời gian tạo ticket. |
| **Khả năng tái lập kết quả** | Spring XD đạt $\text{MAE} = 0.96$ (vượt xa Median 1.72) | Chạy checkpoint tác giả chỉ đạt $\text{MAE} = 1.7330$ | 🔴 **KHÔNG THỂ TÁI LẬP:** Checkpoint thực tế kém hơn cả Median Baseline ($1.7153$). |

---

## 🔍 2. BỐN ĐIỂM BẤT THƯỜNG CỐT TỬ CẦN LƯU Ý KHI LÀM BÁO CÁO NCKH

### 2.1. Nghịch lý "Mô tả biến mất" (The Missing Description Paradox)
Trong bài báo, nhóm tác giả dành nhiều đoạn để giải thích lý do vì sao Transformer xử lý ngữ cảnh dài tốt hơn LSTM, và cách mô hình phân tích mối quan hệ giữa các từ khóa trong phần mô tả chi tiết của lập trình viên.  
Tuy nhiên, trong file `model_training_notebook.ipynb`:
```python
def prepare_dataframe(file_name):
    data = pd.read_csv(file_name)
    data = data.fillna(' ')
    d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
    return pd.DataFrame(data=d)
```
Cột `description` hoàn toàn không tồn tại trong từ điển `d`. Điều này chứng minh toàn bộ các kết quả định lượng mà bài báo đạt được thực chất chỉ phản ánh mối tương quan nông giữa vài từ ngữ trong Tiêu đề (`Title`) và điểm số Story Point.

---

### 2.2. Vấn đề giới hạn chuỗi 20 Tokens (`SEQUENCE_LEN = 20`)
Việc đặt `SEQUENCE_LEN = 20` có nghĩa là:
* Nếu một tiêu đề có 25 từ, 5 từ cuối cùng sẽ bị cắt bỏ không thương tiếc.
* Với độ dài 20 tokens, ma trận Attention chỉ có kích thước $20 \times 20$ (400 phép tính chấm điểm) thay vì $1024 \times 1024$ (hơn 1.000.000 phép tính).  
👉 Đây chính là lý do vì sao một card đồ họa RTX 3090 có thể "nuốt" toàn bộ tập dữ liệu trong vòng vài chục giây. Nhưng cái giá phải trả là mô hình không hề có năng lực đọc hiểu sâu (*deep semantic comprehension*).

---

### 2.3. Lỗi tính toán sai số MAE được quốc tế vạch trần
Bài báo phản biện độc lập của nhóm nghiên cứu SOLAR Lab - University College London (*Tawosi, Moussa, Sarro, 2022*) đã phân tích trực tiếp file notebook của Fu et al. và chỉ ra rằng cách tính MAE gộp các mảng dự đoán trong notebook gốc bị sai lệch chỉ số chia trung bình, dẫn đến con số MAE hiển thị trên màn hình bị giảm nhân tạo. Khi sửa lại hàm tính toán này, độ chính xác của GPT2SP giảm sút rõ rệt.

---

### 2.4. Bản chất của con số MAE = 0.96 trên Spring XD
Khi Nhóm 3 tải checkpoint chính thức [`MickyMike/0-GPT2SP-springxd`](https://huggingface.co/MickyMike/0-GPT2SP-springxd) từ Hugging Face Hub về và nạp vào chính tập test kiểm chứng:
* Điểm số thực tế thu được: **$\text{MAE} = 1.7330$**.
* Trong khi Median Effort Baseline: **$\text{MAE} = 1.7153$**.  
👉 Mô hình học sâu 117 triệu tham số không những không đạt được mức $0.96$ mà còn **thua cả một phép gán trung vị thô sơ**. Điều này chứng minh rằng việc mù quáng chạy theo con số $0.96$ của bài báo sẽ khiến đề tài rơi vào bế tắc phương pháp luận.

---

## 🛡️ 3. ĐỊNH HƯỚNG BƯỚC ĐI ĐÚNG ĐẮN CHO NHÓM NCKH 3 (JOHNNY SNOWFLAKE)

Thay vì cố gắng sửa chữa một mô hình bị hổng cả về dữ liệu lẫn mã nguồn như GPT2SP, Nhóm 3 tận dụng chính các phát hiện này để tạo nên sự đột phá cho đề tài:

1. **Vạch trần lỗ hổng phương pháp luận (Scientific Critique):**  
   Nhóm 3 sẽ là một trong những nhóm tiên phong công bố đầy đủ bằng chứng thực nghiệm chỉ ra sự sai lệch giữa lý thuyết bài báo và mã nguồn thực tế của GPT2SP.
2. **Khôi phục ngữ cảnh sạch không rò rỉ (Time-Travel Reconstruction):**  
   Nhóm 3 trích xuất từ CSDL quan hệ TAWOS v1.1 cả hai trường `Title` và `Description` tại **đúng mốc `SP_Estimation_Date`**, phục hồi trạng thái sơ khai ban đầu lúc họp Sprint Planning Poker, loại bỏ toàn bộ các vết tích debug sau này.
3. **Phân chia theo dòng thời gian chuẩn xác:**  
   Áp dụng Chronological Split dựa trên mốc thời gian ước lượng thực tế thay vì ngày tạo issue.
4. **Xây dựng Pipeline học máy nhẹ, bền vững và minh bạch:**  
   Kết hợp các mô hình embedding ngữ nghĩa hiện đại (SBERT) với các đặc trưng quy trình Agile (Velocity, Complexity) và bộ hồi quy hiệu năng cao (LightGBM/Ridge), bảo đảm vượt qua Median Baseline một cách trung thực và có ý nghĩa thống kê.

---

## 🔗 Liên Kết Điều Hướng Trong Thư Mục Code

* 📜 [00_full_source_code.md](00_full_source_code.md): Lưu trữ toàn bộ 100% mã nguồn gốc GPT2SP.
* 🧠 [01_architecture_code_explanation.md](01_architecture_code_explanation.md): Mổ xẻ từng dòng code của kiến trúc mạng `GPT2SP.py`.
* 🔬 [02_training_pipeline_code_explanation.md](02_training_pipeline_code_explanation.md): Mổ xẻ từng dòng code của pipeline huấn luyện `model_training_notebook.ipynb`.
