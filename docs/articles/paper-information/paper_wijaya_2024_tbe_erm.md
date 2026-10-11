# 📑 Báo Cáo Phân Tích Tài Liệu Khoa Học (Literature Review Note)

> **Tên bài báo:** Enhancing Story Point Estimation in Software Projects Using Transformer-Based Embeddings and Ensemble Regression Models (TBE & ERM)  
> **Nguồn công bố:** IEEE Access (2024)

---

## 📋 1. Bảng Tổng hợp Ma trận Tài liệu (Literature Matrix Table)

|  STT   | Trường thông tin (Field) | Nội dung trích xuất & Đánh giá |
| :----: | :----------------------- | :----------------------------- |
| **1**  | **Title**                | Enhancing Story Point Estimation in Software Projects Using Transformer-Based Embeddings and Ensemble Regression Models |
| **2**  | **Cite Key**             | `wijaya2024tbe` |
| **3**  | **Authors**              | Darren Cornelius Citra Wijaya, Auryn Larissa Sabrina, Meiliana |
| **4**  | **Year**                 | 2024 |
| **5**  | **Venue**                | IEEE Access |
| **6**  | **Files & media**        | [docs/articles/paper_TBE&ERM.pdf](docs/articles/paper_TBE&ERM.pdf) \| [DOI Link](https://doi.org/10.1109/ACCESS.2024.3418576) |
| **7**  | **Venue Type**           | Journal |
| **8**  | **SJR Quartile**         | Q1 |
| **9**  | **CORE Rank**            | N/A (Journal) |
| **10** | **Rank**                 | Q1 (Open Access Multidisciplinary / Computer Science) |
| **11** | **Problem**              | Tìm kiếm sự kết hợp tối ưu giữa biểu diễn ngữ nghĩa hiện đại từ Transformer (Transformer-Based Embeddings) và các thuật toán học máy hồi quy tổ hợp (Ensemble Regression Models) để nâng cao độ chính xác dự báo Story Point mà không cần chi phí huấn luyện quá lớn. |
| **12** | **Dataset**              | Dữ liệu Jira công khai từ các tập dữ liệu chuẩn TAWOS và Choetkiertikul (hàng chục nghìn issues từ các dự án mã nguồn mở). |
| **13** | **Ground Truth**         | Giá trị Story Point (SP) số thực ghi nhận trong hệ thống Jira (Final Snapshot). |
| **14** | **Method**               | **TBE + ERM**: Trích xuất vector nhúng đặc trưng từ các mô hình ngôn ngữ pre-trained (BERT, RoBERTa, DistilBERT), sau đó nạp vào các mô hình Ensemble Regressors (Random Forest, Extra Trees, Gradient Boosting, AdaBoost). |
| **15** | **Baseline**             | Linear Regression, Ridge Regression, Single Decision Tree, Deep-SE. |
| **16** | **Split**                | K-Fold Cross-Validation và Train/Test Split (80% Train / 20% Test). |
| **17** | **Metrics**              | MAE (Mean Absolute Error), MdAE (Median Absolute Error), RMSE, $R^2$ Score. |
| **18** | **Main Result**          | Kết hợp RoBERTa embedding với Extra Trees / Random Forest regressor đạt hiệu quả vượt trội, giảm thiểu MAE và tăng chỉ số $R^2$ rõ rệt so với các mô hình hồi quy tuyến tính cổ điển. |
| **19** | **Critical Notes**       | 1. **Chưa kiểm soát Temporal Leakage:** Nghiên cứu tập trung thuần túy vào mô hình trên dữ liệu tĩnh (Final Snapshot).<br>2. **Chiến lược phân chia dữ liệu:** Việc sử dụng K-Fold và Random Split có thể gây rò rỉ kiến thức giữa các issue trong tương lai về quá khứ.<br>3. Thiếu kiểm tra tái dựng trạng thái ban đầu của issue. |
| **20** | **Takeaways**            | 1. Tách biệt giai đoạn trích xuất đặc trưng (Feature Extraction) và hồi quy (Downstream Regression) giúp tối ưu hóa hiệu năng tính toán.<br>2. Các thuật toán Ensemble Tree thích ứng tốt với không gian vector dày đặc của Transformer. |
| **21** | **Relevance to Topic**   | Đóng vai trò là phương pháp tiếp cận đại diện cho hướng tiếp cận kết hợp (Hybrid / Two-Stage Architecture). Nhóm tham khảo kiến trúc này để đưa vào danh mục mô hình mở rộng trong Roadmap thực nghiệm. |

---

## 🔬 2. Phân Tích Chuyên Sâu (Deep-Dive Analysis)

### 2.1. Bối cảnh & Động lực Nghiên cứu (Motivation & Problem Formulation)
- **Vấn đề thực tiễn:** Việc fine-tune toàn bộ một mô hình ngôn ngữ lớn (như GPT2SP) đòi hỏi tài nguyên tính toán rất lớn và dễ gặp hiện tượng quá khớp (overfitting) trên các dự án có số lượng issue nhỏ.
- **Mục tiêu khoa học:** Đánh giá tính khả thi của phương pháp tiếp cận hai giai đoạn: dùng Transformer pre-trained làm bộ trích xuất đặc trưng đông cứng (frozen feature extractor) kết hợp với các thuật toán học máy tổ hợp (Ensemble Learning) nhẹ và mạnh mẽ.

### 2.2. Dữ liệu & Quy trình Tiền xử lý (Data & Preprocessing Pipeline)
- **Nguồn dữ liệu:** Khai thác các kho dữ liệu phần mềm mã nguồn mở chuẩn từ TAWOS và Choetkiertikul.
- **Đặc trưng đầu vào:** Chuỗi văn bản User Story được làm sạch cơ bản (loại bỏ ký tự đặc biệt, chuẩn hóa chữ thường) và đưa qua tokenizer của BERT / RoBERTa.
- **Mốc thời gian lấy dữ liệu:** Dữ liệu được trích xuất tĩnh ở thời điểm sau khi issue đã hoàn tất (Final Snapshot).

### 2.3. Phương pháp Đề xuất & Kiến trúc Mô hình (Methodology & Architecture)
- **Kiến trúc hai giai đoạn (Two-Stage Pipeline):**
  - *Giai đoạn 1 (TBE):* Sử dụng các mô hình Transformer đã được huấn luyện sẵn (BERT-base, RoBERTa-base, DistilBERT) để ánh xạ văn bản thành vector nhúng ngữ nghĩa chiều cao (ví dụ: vector 768 chiều từ token `[CLS]` hoặc mean-pooling).
  - *Giai đoạn 2 (ERM):* Sử dụng vector nhúng làm đầu vào huấn luyện các mô hình cây hồi quy tổ hợp: Random Forest (RF), Extremely Randomized Trees (ET), Gradient Boosting Regressor (GBR).
- **Tối ưu siêu tham số:** Sử dụng Grid Search hoặc Random Search trên tập validation để tinh chỉnh số lượng cây (n_estimators), độ sâu tối đa (max_depth).

### 2.4. Kết quả Thực nghiệm & Đối chứng (Empirical Evaluation)
- **Hiệu năng:** RoBERTa kết hợp Extra Trees mang lại kết quả tốt nhất, vượt qua các mô hình hồi quy tuyến tính cổ điển và Decision Tree đơn lẻ trên toàn bộ các thước đo sai số (MAE, RMSE).
- **Mức độ tương thích:** Mô hình Ensemble Tree thể hiện khả năng nắm bắt phi tuyến tính xuất sắc trên các vector biểu diễn dày đặc do Transformer tạo ra.

### 2.5. Đánh giá Phản biện & Nguy cơ Rò rỉ Thông tin (Critical Assessment & Leakage Risks)
- **Rò rỉ thông tin tương lai (Temporal Leakage):**
  - Tương tự như các công trình tiền nhiệm, nghiên cứu này không kiểm soát sự thay đổi của Title và Description sau thời điểm Sprint Planning.
  - Sử dụng Random Split trong một số kịch bản thực nghiệm, dẫn đến việc dùng dữ liệu của năm sau để dự đoán cho các task của năm trước, vi phạm nghiêm trọng tính nhân quả thời gian trong Agile.
- **Chưa chuẩn hóa Median Baseline:** Bài báo so sánh chủ yếu với Linear Regression thay vì Median Effort baseline như khuyến nghị của Tawosi et al. (2022).

### 2.6. Định hướng Kế thừa & Đóng góp cho Đề tài Nhóm (Actionable Takeaways)
- **Kế thừa kiến trúc:** Nhóm có thể áp dụng mô hình Two-Stage (RoBERTa/SBERT Embedding + GBT/Random Forest) vì tính ổn định cao và thời gian huấn luyện nhanh hơn GPT2SP.
- **Cải tiến của nhóm:** Đưa mô hình này vào kiểm thử trong cả hai môi trường: Final Snapshot vs Planning-Time Snapshot với phân chia Chronological Split nghiêm ngặt để đo lường mức độ ảnh hưởng của Temporal Leakage.
