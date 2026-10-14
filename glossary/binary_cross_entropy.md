# 📖 Thuật Ngữ: Binary Cross-Entropy

- 📌 **Term (Thuật ngữ tiếng Anh):** Binary Cross-Entropy Loss
- 🔤 **Acronym (Từ viết tắt):** BCE Loss / Log Loss
- 🇻🇳 **Thuật ngữ tiếng Việt:** Thước đo mức độ đoán sai bài toán Đúng/Sai / Hàm phạt đoán lệch xác suất
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một thước đo chấm điểm xem máy tính đoán một sự việc có đúng hay không (chỉ có 2 khả năng: Đúng hoặc Sai, 1 hoặc 0). Nếu máy đoán rất tự tin (99%) nhưng thực tế lại sai bét, thước đo này sẽ "phạt" mô hình điểm phạt cực kỳ nặng để ép mô hình phải sửa sai.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như chơi trò cá cược bóng đá có hai lựa chọn Thắng/Thua: Nếu bạn tự tin cá cược 100 triệu rằng đội A thắng, nhưng kết quả đội A thua tan nát, bạn sẽ mất trắng số tiền cược khổng lồ đó (bị phạt nặng vì quá tự tin vào điều sai trái).
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Máy tính so sánh hai công việc: Task A và Task B.
  - Thực tế: Task A tốn nhiều nỗ lực hơn Task B (Nhãn thật = 1).
  - Nếu máy tính dự đoán xác suất Task A nặng hơn chỉ có **5%** (nghĩa là máy đoán chắc nịch Task B nặng hơn) $\rightarrow$ Điểm phạt Binary Cross-Entropy sẽ vọt lên rất cao, buộc mạng nơ-ron phải đảo ngược lại trọng số học tập.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Khan et al. (arXiv 2025) — *Efficient Story Point Estimation With Comparative Learning*.
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning* (Chapter 5: Machine Learning Basics). MIT Press. Link: https://www.deeplearningbook.org/
  - Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective* (Section 5.7). MIT Press. Link: https://mitpress.mit.edu/9780262018029/

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
