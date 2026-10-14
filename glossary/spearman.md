# 📖 Thuật Ngữ: Spearman's Rank Correlation

- 📌 **Term (Thuật ngữ tiếng Anh):** Spearman's Rank Correlation Coefficient
- 🔤 **Acronym (Từ viết tắt):** Spearman's $\rho$ (rho)
- 🇻🇳 **Thuật ngữ tiếng Việt:** Hệ số tương quan thứ hạng Spearman / Thước đo độ ăn khớp về thứ tự xếp hạng
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một con số từ -1 đến +1 dùng để đo xem hai bảng xếp hạng có đồng thuận với nhau hay không. Điểm số cụ thể bao nhiêu không quan trọng, miễn là danh sách xếp từ khó đến dễ của máy tính có trùng trật tự với danh sách xếp của chuyên gia hay không.
  - Điểm $+1$: Hai bảng xếp hạng trùng khớp nhau từng vị trí.
  - Điểm $0$: Máy xếp thứ tự lộn xộn, không liên quan gì đến thực tế.
  - Điểm $-1$: Máy xếp hoàn toàn ngược lại (việc dễ nhất lại xếp thành khó nhất).
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như cuộc thi nấu ăn MasterChef: Hai vị giám khảo chấm điểm một món ăn có thể chênh nhau (giám khảo A chấm 8 điểm, giám khảo B chấm 9.5 điểm). Nhưng nếu cả hai cùng đồng ý rằng: *"Món của thí sinh An ngon nhất, thứ nhì là món của Bình, thứ ba là Chi"*, thì hai vị giám khảo có sự tương quan thứ hạng rất cao (Spearman $\rho \approx 1$).
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Đội phát triển đánh giá thực tế độ khó 3 task theo thứ tự: Task A (1 SP) $<$ Task B (3 SP) $<$ Task C (8 SP).
  - Mô hình AI dự đoán điểm số có thể bị lệch (đoán là 1.8; 4.2; 11.5). Nhưng vì thứ tự xếp hạng vẫn đúng là $A < B < C$, hệ số Spearman vẫn đạt trọn vẹn **+1.0**.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Khan et al. (arXiv 2025) — *Efficient Story Point Estimation With Comparative Learning*.
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - Spearman, C. (1904). *The proof and measurement of association between two things*. The American Journal of Psychology, 15(1), 72-101. DOI: https://doi.org/10.2307/1412159
  - Zar, J. H. (2005). *Spearman rank correlation*. Encyclopedia of Biostatistics, 7. DOI: https://doi.org/10.1002/0470011815.b2a15150

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
