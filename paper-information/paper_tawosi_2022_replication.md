# BÁO CÁO PHÂN TÍCH TÀI LIỆU KHOA HỌC (LITERATURE REVIEW NOTE)
**Bài báo:** Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study (arXiv:2201.05401v2)

---

## 📋 THƯỚC ĐO TIÊU CHUẨN (TABLE MATRIX)

| Citation | Year | Problem | Dataset | Ground truth | Method | Baseline | Split | Metrics | Main result | Điểm cần lưu ý | Nhóm có thể học/kế thừa gì? | Liên quan/giúp gì cho đề tài nhóm? |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tawosi et al.** (*IEEE TSE / arXiv:2201.05401v2*) | 2022 | Kiểm chứng (Replication & Extension) hiệu quả của mô hình Deep Learning (Deep-SE) trong ước lượng Agile Effort (Story Points) ở mức task; xác minh liệu tương đồng ngữ nghĩa có đủ để dự đoán effort. | 3 bộ dữ liệu: Choetkiertikul (16 dự án, 23.313 issues), Porru (8 dự án, 4.904 issues), và Tawosi (26 dự án, 31.960 issues mở rộng). | Story Point (SP) thực tế ghi nhận trong hệ thống Jira. | Replication & Extension study: Đánh giá Deep-SE (Word Embedding + LSTM + RHWN + Regressor) & TF/IDF-SVM. | Random Guessing (RG), Mean Effort, Median Effort. | Within-project: Chronological split (60% train / 20% val / 20% test). Cross-project: Strict Chronological split theo mốc thời gian tạo issue. | MAE (chính), MdAE, SA, Wilcoxon Rank-Sum test ($\alpha = 0.05$ & Bonferroni $0.025$), Vargha-Delaney $\hat{A}_{12}$ effect size. | Deep-SE **KHÔNG** vượt trội hơn Median baseline ở 58% dự án (within-project); chỉ hơn TF/IDF-SVM ở 19% dự án; Cross-project bị đè bẹp; Augmentation làm kém đi 67% dự án; Pre-training (~47h) không tăng độ chính xác hay tốc độ hội tụ. | 1. Nguy cơ rò rỉ dữ liệu (Future-Information Leakage) khi cap outlier 90th percentile lên cả test set.<br>2. 19.11% issue chứa code/stack trace làm nhiễu NLP.<br>3. Semantic similarity không phân biệt được nỗ lực thực tế.<br>4. Ground truth SP mang tính cảm quan chủ quan.<br>5. Giới hạn 100 token đầu của issue text. | 1. Bắt buộc dùng **Chronological Split**.<br>2. Không transform/cap outlier trên test set.<br>3. Bỏ qua bước pre-training đắt đỏ.<br>4. Tiền xử lý tách biệt code/stack trace khỏi natural text.<br>5. Bổ sung các đặc trưng effort drivers khác ngoài ngữ nghĩa thuần túy. | 1. Cung cấp căn cứ sắc bén phản biện việc lạm dụng NLP/LLM embedding cho bài toán ước lượng effort.<br>2. Cung cấp chuẩn mực thiết kế thực nghiệm (Chronological split, Median baseline, kiểm định Wilcoxon & $\hat{A}_{12}$).<br>3. Giúp nhóm lập luận né tránh Future-Information Leakage khi bảo vệ đề tài. |

---

## 📑 PHÂN TÍCH CHI TIẾT (DETAILED LITERATURE NOTE)

### 📄 Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study

#### 1. Thông tin trích dẫn (Citation & Metadata)
* **Citation:** Vali Tawosi, Rebecca Moussa, and Federica Sarro, *"Agile Effort Estimation: Have We Solved the Problem Yet? Insights From A Replication Study"*, IEEE Transactions on Software Engineering (TSE), 2022.
* **Year:** 2022 (arXiv:2201.05401v2, Dec 2022).
* **DOI / Link:** [arXiv:2201.05401v2](https://arxiv.org/abs/2201.05401) | Rep package: [GitHub SOLAR-group/AgileEffortEstimation](https://github.com/SOLAR-group/AgileEffortEstimation)

#### 2. Đặt bài toán & Mục tiêu nghiên cứu (Problem & Goal)
* **Problem:** 
  * Ước lượng nỗ lực trong các dự án Agile thường được thực hiện ở mức công việc thông qua **Story Point (SP)** dựa trên đánh giá cảm quan của chuyên gia, dẫn đến sự thiếu nhất quán.
  * Bài báo tiến hành nghiên cứu tái lặp nghiêm ngặt (close replication) và mở rộng (extension) đối với Deep-SE (Choetkiertikul et al., IEEE TSE 2019).
  * Câu hỏi cốt lõi: *"Liệu sự tương đồng ngữ nghĩa (semantic similarity) giữa các User Story có đủ để phân biệt và dự đoán chính xác Story Point hay chưa?"*
* **Ground truth:** Giá trị Story Point (SP) thực tế ghi nhận trên hệ thống Jira.

#### 3. Dữ liệu & Phương pháp thực nghiệm (Dataset & Methodology)
* **Dataset:** 3 bộ dữ liệu: Choetkiertikul (16 dự án, 23,313 issues), Porru (8 dự án, 4,904 issues), Tawosi (26 dự án, 31,960 issues mở rộng).
* **Method:** Deep-SE (Word Embedding + LSTM + Recurrent Highway Network) và TF/IDF-SVM.
* **Baseline:** Random Guessing (RG), Mean Effort, Median Effort.
* **Split:** Chronological split (60/20/20) cho within-project và Strict Chronological Split cho cross-project (triệt tiêu Future-Information Leakage).
* **Metrics:** MAE, MdAE, SA, Wilcoxon Rank-Sum Test, Vargha-Delaney $\hat{A}_{12}$ Effect Size.

#### 4. Kết quả & Đóng góp chính (Results & Takeaways)
* Deep-SE không vượt trội hơn Median baseline ở 58% dự án.
* Tự động điều chỉnh quy trình chống Data Leakage làm lộ ra các hạn chế thực tế của Deep Learning trên bài toán ước lượng Story Point.

#### 5. Giá trị thực tiễn cho Đề tài NCKH của Nhóm (Team Application)
* Cung cấp luận cứ sắc bén và thiết kế thực nghiệm chuẩn mực cho đề tài của Nhóm 3.

---
© 2026 **Nhóm 3 — NCKH Agile Story Point Estimation Project**
