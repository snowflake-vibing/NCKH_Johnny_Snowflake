# 📊 Thư mục Dữ liệu & Notebook Phân tích EDA (Data & EDA Workflows)

> **Thư mục này chứa các kịch bản Notebook thực hiện Phân tích Khám phá Dữ liệu (Exploratory Data Analysis - EDA) trên bộ dữ liệu TAWOS (The Agile World of Software).**

---

## 📁 1. Danh sách File trong Thư mục `data/`

* **`README.md`**: File tài liệu hướng dẫn và mô tả quy trình làm việc trong thư mục `data/`.
* **`EDA_TAWOS.ipynb`**: Notebook phân tích trực quan hóa dữ liệu EDA chi tiết, thống kê đếm Story Point, missing values, phân bố dự án, rò rỉ thông tin tương lai (*Future-Information Leakage*) và các case history trích xuất từ Change Log.

---

## 🛑 2. Cấu hình Đường dẫn Dataset & Lưu trữ Local

> [!IMPORTANT]
> **Bộ dữ liệu TAWOS (`tawos_eda.db` ~3.46GB, `TAWOS.sql` ~4.3GB) có dung lượng rất lớn nên KHÔNG được push lên GitHub.**
> Dữ liệu được lưu trữ trực tiếp trên ổ đĩa local tại thư mục cố định: `C:/tawos/`.

* **Đường dẫn CSDL SQLite:** `C:/tawos/tawos_eda.db`
* Trong file `EDA_TAWOS.ipynb`, biến kết nối CSDL đã được thiết lập mặc định:
  ```python
  db_path = 'C:/tawos/tawos_eda.db'
  conn = sqlite3.connect(db_path)
  ```

---

## 🚀 3. Hướng dẫn Thực hiện Quy trình (Step-by-Step Workflow)

Để chạy notebook `EDA_TAWOS.ipynb`, bạn thực hiện theo các bước sau:

### Bước 1: Chuẩn bị Bộ dữ liệu Local
Đảm bảo file CSDL SQLite `tawos_eda.db` đã có sẵn tại đường dẫn local:
```text
C:\tawos\tawos_eda.db
```

### Bước 2: Cài đặt Môi trường Python
Cài đặt các thư viện phân tích dữ liệu cần thiết (nếu chưa có):
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### Bước 3: Khởi chạy Jupyter Notebook
Mở VS Code hoặc Jupyter Lab/Notebook và chọn kernel Python đã cài đủ thư viện:
```bash
jupyter notebook data/EDA_TAWOS.ipynb
```

### Bước 4: Thực thi Quy trình Phân tích theo Thứ tự
Chạy các Cell code trong `EDA_TAWOS.ipynb` theo thứ tự từ trên xuống dưới:
1. **Cell 1 — Khởi tạo:** Thư viện (`pandas`, `sqlite3`, `seaborn`) và thiết lập kết nối tới `C:/tawos/tawos_eda.db`.
2. **Cell 2 — Thống kê Tổng quan:** Tổng số 39 Dự án và 458.232 Issues.
3. **Cell 3 — Story Point Distribution:** Đếm số lượng issue thực sự có Story Point (`63.011 issues` ~ `13,75%`).
4. **Cell 4 — Missing Data:** Thống kê tỷ lệ khuyết trường `Description`.
5. **Cell 5 — Project Distribution:** Phân bố số lượng issue theo từng project.
6. **Cell 6 — Timeline Statistics:** Thống kê khoảng thời gian thu thập dữ liệu (Time Range).
7. **Cell 7 — Change Log & Leakage Analysis:** Thống kê 11.969 issues bị sửa đổi title/description sau thời điểm estimation (minh chứng rò rỉ thông tin tương lai).
8. **Cell 8 — Time Delta:** Thống kê độ trễ thời gian thay đổi văn bản (trung vị `2.3 ngày`).
9. **Cell 9 — Case Studies:** Trích xuất chi tiết các lịch sử sửa đổi thực tế.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
