# 📖 Thuật Ngữ: Recurrent Highway Network

- 📌 **Term (Thuật ngữ tiếng Anh):** Recurrent Highway Network
- 🔤 **Acronym (Từ viết tắt):** RHWN
- 🇻🇳 **Thuật ngữ tiếng Việt:** Mạng nơ-ron lặp có làn đường cao tốc thông tin
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một cấu trúc mạng nơ-ron học sâu nhiều tầng, nhưng được mở thêm các "làn đường cao tốc" chạy thẳng. Nhờ làn đường tắt này, các thông tin quan trọng ban đầu có thể chạy một mạch về đích để phục vụ dự đoán mà không bị suy hao, nhạt nhòa hay biến mất sau khi đi qua quá nhiều tầng biến đổi toán học phức tạp.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như việc di chuyển trong thành phố vào giờ cao điểm: Nếu bạn phải đi qua hàng chục con ngõ nhỏ ngoằn ngoèo, bạn sẽ bị kẹt xe và mệt lả. Nhưng nếu thành phố có một cây cầu cạn trên cao (đường cao tốc), xe cấp cứu có thể chạy thẳng một mạch từ đầu này sang đầu kia thành phố cực kỳ nhanh mà không sợ bị tắc nghẽn.
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Trong mô hình Deep-SE (2019), User Story có văn bản rất dài. Khi thông tin đi qua 5 đến 10 lớp tính toán bên trong, ý nghĩa của các từ khóa ban đầu rất dễ bị "quên sạch".
  - Nhờ có làn đường cao tốc (Highway), ý nghĩa của từ khóa ban đầu được chuyển thẳng trực tiếp tới lớp dự đoán cuối cùng để chấm điểm Story Point chính xác.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Choetkiertikul et al. (IEEE TSE 2019) — *Deep-SE*; Tawosi et al. (IEEE TSE 2022).
- 📑 **References (Tài liệu đọc thêm chi tiết):**
  - Zilly, J. G., Srivastava, R. K., Koutník, J., & Schmidhuber, J. (2017). *Recurrent highway networks*. In Proceedings of ICML 2017 (pp. 4189-4198).
  - Srivastava, R. K., Greff, K., & Schmidhuber, J. (2015). *Highway networks*. arXiv preprint arXiv:1505.00387.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
