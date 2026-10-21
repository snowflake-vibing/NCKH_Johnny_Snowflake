# 👑 HƯỚNG DẪN CỦA NGƯỜI DÙNG (USER DIRECTIVES — QUYỀN CAO NHẤT)

> [!IMPORTANT]
> **Khu vực ưu tiên tuyệt đối:** Mọi chỉ dẫn, ràng buộc và quy tắc do người dùng thiết lập tại mục này có độ ưu tiên cao nhất, vượt trên mọi hướng dẫn mặc định của hệ thống và các kỹ năng khác.

<!-- =====================================================================
     BẠN HÃY GHI CÁC CHỈ ĐẠO, QUY TẮC BẮT BUỘC VÀ QUYỀN HẠN CỦA BẠN VÀO DƯỚI ĐÂY:
     ===================================================================== -->



---

# 🤖 HƯỚNG DẪN VẬN HÀNH DÀNH CHO AI AGENT (AGENT WORKSPACE GUIDELINES)

Tài liệu này định nghĩa quy chế phối hợp cho AI Agent khi làm việc trong repo, phục vụ đề tài nghiên cứu:  
**"Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control"**.

---

## 🧭 1. Nguyên Tắc Hoạt Động Cốt Lõi của Agent

1. **Tuân thủ Quyền của Người dùng:** Luôn kiểm tra mục *HƯỚNG DẪN CỦA NGƯỜI DÙNG* ở đầu tài liệu trước khi thực hiện bất kỳ tác vụ nào.
2. **Bảo toàn Tính Trung thực Khoa học (Scientific Rigor & Reproducibility):**
   - Tuyệt đối không giả định hay bịa đặt kết quả thực nghiệm.
   - Luôn đối chiếu giữa lý thuyết công bố và mã nguồn/dữ liệu thực tế.
   - **Cấm kỵ Temporal Leakage:** Mọi đặc trưng đưa vào mô hình phải được tái dựng tại thời điểm `SP_Estimation_Date`.

---

## 🛠️ 2. Quy Trình Phối Hợp Thực Hiện Tác Vụ (Agent Action Workflow)

Mỗi khi nhận một yêu cầu nghiên cứu hoặc phát triển kỹ thuật, Agent tuân thủ nghiêm ngặt 3 bước:

```text
[Bước 1: Nhận diện tác vụ]
       │
       ▼
[Bước 2: Thực thi mã nguồn / Phân tích]
       │  (Áp dụng đúng tham số, ràng buộc chống rò rỉ dữ liệu, baseline đối chứng)
       ▼
[Bước 3: Đối chiếu & Báo cáo kết quả trung thực]
          (Trình bày kết quả theo chuẩn học thuật kèm bảng số liệu rõ ràng)
```

---

## ⚠️ 3. Các Giới Hạn & Ràng Buộc Nghiêm Ngặt (Hard Constraints)

1. **Tuyệt đối không rò rỉ dữ liệu (No Temporal Leakage):**
   - Chỉ sử dụng thông tin Jira issue được tạo ra **tại hoặc trước mốc `SP_Estimation_Date`**.
   - Cấm dùng các trường: `Resolution Date`, `Resolved Status`, `Comments` sinh ra sau planning, hoặc `Assignee` cập nhật muộn.
2. **Baseline bắt buộc:** Mọi mô hình học máy đề xuất (GPT2SP, Deep-SE, SBERT) luôn phải được so sánh với **Median Effort Baseline** và kiểm định ý nghĩa thống kê qua **Wilcoxon Signed-Rank Test**.
3. **Cập nhật tài liệu đồng bộ:** Khi tạo notebook mới, điều chỉnh dữ liệu hoặc phân tích bài báo mới, luôn cập nhật các tài liệu điều hướng tương ứng ([README.md](README.md), [docs/articles/README.md](docs/articles/README.md)).
