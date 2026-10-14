# 📖 Thuật Ngữ: TF-IDF

- 📌 **Term (Thuật ngữ tiếng Anh):** TF-IDF (Term Frequency - Inverse Document Frequency)
- 🔤 **Acronym (Từ viết tắt):** TF-IDF
- 🇻🇳 **Thuật ngữ tiếng Việt:** Thước đo độ quan trọng của từ khóa trong văn bản
- 💡 **Definition (Định nghĩa dễ hiểu):** Là cách chấm điểm để máy tính nhận diện từ ngữ nào thực sự quan trọng và đặc trưng nhất cho một bài viết. Một từ sẽ được chấm điểm rất cao nếu nó xuất hiện lặp đi lặp lại nhiều lần trong bài viết này, nhưng lại rất hiếm khi xuất hiện ở các bài viết khác trong toàn bộ kho dữ liệu.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như manh mối trong một vụ án hình sự: Những từ thông thường như "người, nhà, đi, về" xuất hiện ở mọi câu chuyện nên vô giá trị. Nhưng nếu một biên bản thẩm vấn nhắc đi nhắc lại từ "vali đỏ", từ đó lập tức trở thành manh mối vàng và được điều tra viên chú ý nhất.
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Trong 10.000 công việc Jira, từ "hệ thống" xuất hiện ở khắp nơi $\rightarrow$ Điểm TF-IDF gần bằng 0 (vô nghĩa).
  - Nhưng cụm từ "deadlock_database" (nghẽn khóa cơ sở dữ liệu) chỉ xuất hiện trong đúng công việc này $\rightarrow$ Điểm TF-IDF cực kỳ cao, giúp mô hình biết ngay đây là một lỗi kỹ thuật nặng cần chấm nhiều Story Point.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Choetkiertikul et al. (IEEE TSE 2019); Fu & Tantithamthavorn (IEEE TSE 2023).
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. Information Processing & Management, 24(5), 513-523. DOI: https://doi.org/10.1016/0306-4573(88)90021-0
  - Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. DOI: https://doi.org/10.1017/CBO9780511809071

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
