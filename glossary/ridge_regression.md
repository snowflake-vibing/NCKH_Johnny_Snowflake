# 📖 Thuật Ngữ: Ridge Regression

- 📌 **Term (Thuật ngữ tiếng Anh):** Ridge Regression
- 🔤 **Acronym (Từ viết tắt):** Không có (Đôi khi gọi là $L_2$ Regularization)
- 🇻🇳 **Thuật ngữ tiếng Việt:** Hồi quy phạt co cụm / Hồi quy đường thẳng chống đoán vống
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một thuật toán tìm đường thẳng dự đoán tốt nhất, nhưng có gắn thêm một "sợi dây kéo ghìm lại". Sợi dây này phạt nặng các mô hình quá tin tưởng mù quáng vào một vài đặc trưng riêng lẻ, giúp mô hình luôn giữ sự khiêm tốn và không bị sai lầm ngớ ngẩn khi gặp dữ liệu thực tế mới.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như một chuyên gia định giá nhà giàu kinh nghiệm: Một người mới vào nghề có thể thấy nhà có cái ban công sơn màu đẹp mà vội đoán giá nhà tăng vọt lên gấp đôi. Chuyên gia sẽ nhắc nhở: "Ban công đẹp thì có cộng thêm điểm, nhưng chỉ cộng một khoản nhỏ thôi, không được để một chi tiết phụ làm đảo lộn toàn bộ giá trị ngôi nhà".
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Khi thấy trong mô tả công việc có chữ "nguy hiểm", nếu dùng hồi quy thông thường, mô hình có thể bị thổi phồng điểm số từ 2 lên 50 Story Points.
  - Khi dùng Ridge Regression, thuật toán sẽ ghìm hệ số ảnh hưởng của từ "nguy hiểm" lại ở mức vừa phải, chỉ tăng lên mức hợp lý như 5 hoặc 8 điểm.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Choetkiertikul et al. (IEEE TSE 2019); Fu & Tantithamthavorn (IEEE TSE 2023).
- 📑 **References (Tài liệu đọc thêm chi tiết):**
  - Hoerl, A. E., & Kennard, R. W. (1970). *Ridge regression: Biased estimation for nonorthogonal problems*. Technometrics, 12(1), 55-67.
  - Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. Springer.

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
