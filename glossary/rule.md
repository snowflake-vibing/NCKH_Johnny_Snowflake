# 📜 Quy Tắc & Mẫu Thuật Ngữ Nghiên Cứu (Glossary Rules & Template)

> **Mục tiêu:** Quy định chuẩn mực viết giải thích thuật ngữ trong đề tài nghiên cứu theo tiêu chí: trực quan, dễ hiểu nhất, dùng ngôn ngữ đời thường, hình ảnh ẩn dụ thực tế và kèm tài liệu tham chiếu có link DOI. Tuyệt đối **không** dùng một thuật ngữ khó khác để giải thích.

---

## 🚨 QUY TẮC BẮT BUỘC KHI TẠO THUẬT NGỮ MỚI (MANDATORY RULE)

> [!IMPORTANT]
> **Quy tắc Tự động Đồng bộ `overview.md`:**  
> Mỗi khi tạo mới hoặc cập nhật một file thuật ngữ trong thư mục `glossary/`, người viết (hoặc AI Agent) **bắt buộc phải cập nhật bảng danh mục thuật ngữ theo thứ tự A - Z trong file [overview.md](file:///d:/NCKH_3/glossary/overview.md)**, đồng thời cập nhật sơ đồ cây thư mục trong [README.md](file:///d:/NCKH_3/README.md).

---

## 📋 Mẫu Định Dạng Thuật Ngữ Chuẩn (Standard Glossary Template)

Mỗi file thuật ngữ mới trong `glossary/` phải tuân thủ đúng 8 trường thông tin sau:

- 📌 **Term (Thuật ngữ tiếng Anh):** [Tên thuật ngữ tiếng Anh gốc, ví dụ: Story Point, Data Leakage, Chronological Split]
- 🔤 **Acronym (Từ viết tắt):** [Viết tắt thường dùng, ví dụ: SP, MAE, LLM. Nếu không có thì ghi "Không có"]
- 🇻🇳 **Thuật ngữ tiếng Việt:** [Tên gọi tiếng Việt phổ biến, dễ hiểu nhất, ví dụ: Điểm độ khó công việc, Rò rỉ dữ liệu, Chia dữ liệu theo thời gian]
- 💡 **Definition (Định nghĩa dễ hiểu):** [Giải thích bản chất của khái niệm bằng từ ngữ giản dị, rõ ràng; tập trung vào ý nghĩa cốt lõi mà một người mới tiếp cận cũng hiểu được ngay]
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** [Ví von khái niệm này giống như một câu chuyện, tình huống quen thuộc nào trong cuộc sống hàng ngày (như nấu ăn, đi chợ, thi cử, xem phim,...)]
- 🔍 **Example (Ví dụ minh họa cụ thể):** [Một tình huống hoặc số liệu ví dụ cụ thể, thực tế gắn liền với dự án phần mềm Jira hoặc bài toán của nhóm]
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** [Tên bài báo, tác giả, năm hoặc liên kết tài liệu nơi thuật ngữ này xuất hiện tiêu biểu nhất]
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - [Tác giả A, et al. (Năm). *Tên bài báo khoa học*. Tên hội thảo/Tạp chí. DOI / Link: https://doi.org/...]
  - [Tác giả B, et al. (Năm). *Tên bài báo khoa học*. Tên hội thảo/Tạp chí. DOI / Link: https://doi.org/...]

---

### 🌟 Mẫu ví dụ minh họa cách ghi (Example Entry)

- 📌 **Term (Thuật ngữ tiếng Anh):** Story Point
- 🔤 **Acronym (Từ viết tắt):** SP
- 🇻🇳 **Thuật ngữ tiếng Việt:** Điểm ước lượng độ khó công việc
- 💡 **Definition (Định nghĩa dễ hiểu):** Là một con số quy ước (như 1, 2, 3, 5, 8...) do nhóm lập trình viên cùng nhau chấm cho một yêu cầu công việc, để thể hiện công việc đó khó hay dễ, tốn nhiều công sức hay ít công sức, thay vì tính bằng số giờ làm việc cụ thể.
- 🎭 **Ẩn dụ đời thực (Real-world Analogy):** Giống như khi bạn đi uống trà sữa có các cỡ ly: Size S (nhỏ - dễ uống hết), Size M (vừa), Size L (to - tốn nhiều thời gian uống hơn). Bạn không cần đo chính xác ly có bao nhiêu mililít nước, mà chỉ cần nhìn cỡ ly là biết mức độ "to hay nhỏ".
- 🔍 **Example (Ví dụ minh họa cụ thể):** 
  - Nhiệm vụ "Đổi màu nút Đăng nhập" rất dễ $\rightarrow$ Nhóm chấm **1 Story Point**.
  - Nhiệm vụ "Tích hợp cổng thanh toán ngân hàng bảo mật cao" rất phức tạp $\rightarrow$ Nhóm chấm **8 Story Points**.
- 📚 **Source bài báo (Nguồn tài liệu tham chiếu):** Choetkiertikul et al. (IEEE TSE 2019) — *A Deep Learning Model for Estimating Story Points*; Tawosi et al. (IEEE TSE 2022).
- 📑 **References (Tài liệu đọc thêm chi tiết kèm link DOI):**
  - Cohn, M. (2005). *Agile Estimating and Planning*. Prentice Hall. Link: https://www.scrumalliance.org/learn-about-scrum/agile-estimating-and-planning
  - Choetkiertikul, M., Dam, H. K., Tran, T., Pham, T., Ghose, A., & Menzies, T. (2019). *A deep learning model for estimating story points*. IEEE Transactions on Software Engineering, 45(7), 637-656. DOI: https://doi.org/10.1109/TSE.2018.2792473
  - Tawosi, V., Moussa, R., & Sarro, F. (2022). *Agile effort estimation: Have we solved the problem yet? Insights from a replication study*. IEEE Transactions on Software Engineering, 49(4), 2673-2691. DOI: https://doi.org/10.1109/TSE.2022.3204902

---
© 2026 **Nhóm 3 — Khoa Hệ thống Thông tin, Trường ĐH Công nghệ Thông tin, ĐHQG-HCM.**
