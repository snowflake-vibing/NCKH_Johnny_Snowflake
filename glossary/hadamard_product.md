# 📖 Thuật Ngữ: Hadamard Product

- 📌 **Term (Thuật ngữ tiếng Anh):** Hadamard Product (Element-wise Product)
- 🔤 **Acronym (Từ viết tắt):** Ký hiệu là dấu chấm tròn có vòng bao quanh $\odot$ hoặc nhân từng phần tử
- 🇻🇳 **Thuật ngữ tiếng Việt:** Phép nhân từng phần tử tương ứng / Phép nhân đối xứng từng vị trí
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một phép tính toán học giữa hai danh sách số có cùng độ dài: Bạn chỉ việc lấy con số ở vị trí số 1 của danh sách này nhân với con số ở vị trí số 1 của danh sách kia; số ở vị trí 2 nhân với số ở vị trí 2,... tạo ra một danh sách mới cùng chiều dài. Phép tính này giúp máy tính đo xem hai vật thể có cùng "sáng" hoặc cùng "tắt" ở những đặc điểm nào.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như so khớp hai bài trắc nghiệm của hai học sinh: Bạn so từng câu một: Câu 1 đúng nhân với đúng (ra điểm cao), câu 2 sai nhân với sai (ra điểm thấp). Nó giúp thầy cô giáo biết ngay hai học sinh này có "tâm đầu ý hợp" cùng làm đúng hoặc cùng làm sai ở những câu hỏi nào.
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Giả sử đặc trưng của Task A là vector: $[2, 0, 5]$
  - Đặc trưng của Task B là vector: $[3, 4, 2]$
  - Phép nhân Hadamard $A \odot B$ tính cực kỳ đơn giản:
    $$[2 \times 3, 0 \times 4, 5 \times 2] = [6, 0, 10]$$
  - Trong bài báo Khan et al. (2025), phép tính $v_i \odot v_j$ giúp mạng nơ-ron nhận diện được các khía cạnh ngữ nghĩa mà cả hai User Story cùng quan tâm (ví dụ cùng liên quan đến bảo mật hoặc cùng liên quan đến giao diện).
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Khan et al. (arXiv 2025) — *Efficient Story Point Estimation With Comparative Learning*.
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - Horn, R. A. (1990). *The Hadamard product*. In Proc. Symp. Appl. Math (Vol. 40, pp. 87-169). DOI: https://doi.org/10.1090/psapm/040/1053123
  - Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press. Link: https://www.press.jhu.edu/books/title/10424/matrix-computations

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
