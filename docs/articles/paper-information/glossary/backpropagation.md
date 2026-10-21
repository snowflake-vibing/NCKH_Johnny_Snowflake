# 🧩 THUẬT NGỮ: BACK-PROPAGATION (LAN TRUYỀN NGƯỢC ĐẠO HÀM)

> **Thuật toán lan truyền ngược (Back-propagation / Error Backpropagation)**  
> *Thuộc nhóm:* Nền Tảng Tối Ưu Hóa & Giải Tích Học Sâu (Deep Learning Optimization & Calculus)  
> *Áp dụng trong:* Quá trình huấn luyện tinh chỉnh toàn diện (End-to-End Fine-Tuning) của cả **Deep-SE** và **GPT2SP** (IEEE TSE 2023).

---

## 🧒 PHẦN 1: GIẢI THÍCH CHO ĐỨA TRẺ 10 TUỔI (THE 10-YEAR-OLD EXPLANATION)

Hãy tưởng tượng một dây chuyền làm bánh kem gồm 12 người thợ đứng nối tiếp nhau trong một xưởng bánh:
1. **Lượt đi xuôi (Lan truyền tiến - Forward Pass):**  
   Bác thợ thứ nhất đập trứng, chuyển cho bác thứ hai trộn bột, chuyển cho bác thứ ba nướng bánh... đến bác thợ thứ 12 ở cuối dây chuyền trang trí dâu tây lên trên. Chiếc bánh hoàn thành được mang ra bàn tiệc.
2. **Khách hàng chấm điểm và phàn nàn (Tính sai số - Loss Calculation):**  
   Khách hàng nếm thử và lắc đầu chê: *"Bánh này bị quá ngọt và hơi khét!"* (sai số giữa mong muốn và thực tế).
3. **Lượt đi ngược (Lan truyền ngược - Back-propagation):**  
   Người giám sát bước từ cuối xưởng đi ngược trở lại đầu xưởng:
   * Ông đến gặp bác thợ thứ 12: *"Bác cho hơi nhiều mứt dâu tây rồi, lần sau giảm bớt 1 thìa nhé!"* (cập nhật trọng số tầng 12).
   * Ông đi lùi lại gặp bác thợ nướng bánh: *"Lò nướng hơi quá nhiệt 5 độ, lần sau chỉnh nhỏ lại nhé!"* (cập nhật trọng số tầng 11).
   * ... Cứ thế, ông đi lùi dần từng bước cho đến bác thợ thứ nhất đập trứng ở đầu dây chuyền!

Nhờ có chuyến đi ngược chỉ rõ lỗi lầm của từng người như vậy, ngày hôm sau cả 12 người thợ đều tiến bộ và làm ra một chiếc bánh kem thơm ngon chuẩn vị hơn hẳn!

> 💡 **Định nghĩa bình dân:**  
> **Back-propagation (Lan truyền ngược)** là thuật toán "rút kinh nghiệm từ sai lầm", đi ngược từ kết quả dự đoán sai ở đầu ra quay trở về từng tầng nơ-ron ở đầu vào, dùng toán học để chỉ rõ mỗi tầng đã góp bao nhiêu phần lỗi, từ đó điều chỉnh các nút vặn (trọng số) để lần sau đoán chính xác hơn.

---

## 🔍 PHẦN 2: BÓC TÁCH TỪNG TỪ NGỮ CHUYÊN NGÀNH (DECONSTRUCTING THE JARGON)

Thuật ngữ **Back-propagation** là cách viết tắt của cụm từ *"Backward Propagation of Errors"*:

| Thành tố | Gốc từ tiếng Anh | Ý nghĩa đời thường | Ý nghĩa trong Toán học & Machine Learning | Khái niệm đối lập (Antonym) |
| :--- | :--- | :--- | :--- | :--- |
| **Back-** | *Backward* (đi lùi, hướng ngược lại) | Đi ngược chiều kim đồng hồ hoặc đi lùi về phía sau. | Hướng truyền dòng thông tin đạo hàm: từ hàm mất mát $\mathcal{L}$ tại đầu ra quay ngược về đầu vào của mạng nơ-ron. | **Forward (Lan truyền tiến từ đầu vào ra đầu ra).** |
| **Propagation** | *Propagate* (lan tỏa, truyền bá) | Sự lan truyền của sóng âm thanh hoặc tin tức trong đám đông. | Dòng chảy liên tục của các giá trị đạo hàm riêng qua đồ thị tính toán toán học. | *Absorption / Blockade* (bị hấp thụ, chặn đứng). |
| **Chain Rule** | *Quy tắc chuỗi vi phân* | Dây chuyền bánh răng ăn khớp với nhau. | Công thức giải tích vi phân của hàm hợp: đạo hàm của hàm tổng thể bằng tích các đạo hàm thành phần: $\frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} \cdot \frac{\partial y}{\partial x}$. | *Direct differentiation* (đạo hàm trực tiếp không qua trung gian). |

---

## 📊 PHẦN 3: TRỰC QUAN HÓA BẰNG BẢNG DỮ LIỆU & SƠ ĐỒ (THE "AHA!" MOMENT)

```mermaid
flowchart LR
    subgraph ForwardPass["1. CHIỀU TIẾN (FORWARD PASS): TÍNH TOÁN DỰ ĐOÁN"]
        direction LR
        In["Văn bản Issue"] --> Emb["Lớp Nhúng"] --> Trans["12 Tầng Transformer"] --> MLP["MLP Regressor"] --> Pred["Dự đoán: y^ = 7.5 SP"]
    end

    subgraph LossCalc["2. TÍNH SAI SỐ"]
        direction TB
        Pred & TrueSP["Thực tế: y = 5.0 SP"] --> Loss["L1 Loss = |5.0 - 7.5| = 2.5 SP"]
    end

    subgraph BackwardPass["3. CHIỀU LÙI (BACK-PROPAGATION): LAN TRUYỀN ĐẠO HÀM"]
        direction RL
        GradMLP["Chỉnh Đầu Hồi Quy"] <-- Grad12["Chỉnh Tầng 12"] <-- Grad1["Chỉnh Tầng 1"] <-- GradEmb["Chỉnh Vector Từ"] <-- Loss
    end
```

### Minh họa quy tắc chuỗi vi phân (Chain Rule) qua 3 mắt xích toán học:

Giả sử chúng ta có chuỗi tính toán từ trọng số $w$ tới hàm mất mát $\mathcal{L}$:
$$w \xrightarrow{\quad} y = 2w \xrightarrow{\quad} \hat{y} = y + 3 \xrightarrow{\quad} \mathcal{L} = (\hat{y} - 5)^2$$

| Bước giải tích | Phép toán trung gian | Đạo hàm riêng tại chỗ | Giá trị cụ thể khi $w = 2$ | Ý nghĩa giải thích bằng lời |
| :---: | :--- | :--- | :---: | :--- |
| **1** | $\mathcal{L} = (\hat{y} - 5)^2$ | $\frac{\partial \mathcal{L}}{\partial \hat{y}} = 2(\hat{y} - 5)$ | $\hat{y} = 7 \rightarrow \mathbf{+4}$ | Sai số đầu ra phản ứng với dự đoán. |
| **2** | $\hat{y} = y + 3$ | $\frac{\partial \hat{y}}{\partial y} = 1$ | $\mathbf{1}$ | Đầu ra phản ứng với biến đổi trung gian $y$. |
| **3** | $y = 2w$ | $\frac{\partial y}{\partial w} = 2$ | $\mathbf{2}$ | Biến đổi $y$ phản ứng với trọng số ban đầu $w$. |

### Tích số thần kỳ của Quy tắc Chuỗi (Chain Rule):

$$
\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial \mathcal{L}}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial y} \cdot \frac{\partial y}{\partial w} = 4 \times 1 \times 2 = \mathbf{+8}
$$

> 🎉 **Khoảnh khắc "Aha!":**  
> Máy tính **hoàn toàn không cần phải tính đạo hàm phức tạp của một biểu thức khổng lồ** chứa hàng trăm triệu biến số cùng một lúc!  
> Thay vào đó, mỗi tầng nơ-ron chỉ cần làm một phép nhân cực kỳ đơn giản: lấy đạo hàm mà tầng sau vừa ném về cho mình, nhân với đạo hàm nội bộ tại chỗ của mình, rồi ném tiếp kết quả cho tầng phía trước! Đơn giản, thanh lịch và chạy nhanh như chớp trên GPU!

---

## ⚡ PHẦN 4: THÁCH THỨC KỸ THUẬT & CĂN BỆNH TRIỆT TIÊU ĐẠO HÀM (VANISHING GRADIENT)

Khi chuỗi lan truyền ngược phải đi qua hàng chục tầng nơ-ron:

$$
\frac{\partial \mathcal{L}}{\partial w_1} = \frac{\partial \mathcal{L}}{\partial y_L} \cdot \frac{\partial y_L}{\partial y_{L-1}} \cdots \frac{\partial y_2}{\partial y_1} \cdot \frac{\partial y_1}{\partial w_1}
$$

1. **Hiểm họa triệt tiêu đạo hàm (Vanishing Gradient):**  
   Nếu mỗi mắt xích trung gian có đạo hàm nhỏ hơn 1 (ví dụ như hàm Sigmoid có đạo hàm tối đa chỉ là $0.25$):  
   $$0.25 \times 0.25 \times 0.25 \times \dots \approx 0.000000001$$  
   Đến khi tín hiệu đạo hàm lội ngược dòng về tới tầng số 1, nó đã bị teo tóp về bằng đúng số $0$ tròn trĩnh. Các tầng đầu tiên hoàn toàn không nhận được tín hiệu gì để cập nhật, khiến mô hình bị "tê liệt" nửa thân dưới.
2. **Cách GPT2SP hóa giải:**  
   Nhờ có **Residual Connections** bọc quanh mỗi khối Decoder, phép cộng $y = x + F(x)$ tạo ra một đạo hàm hằng số bằng $1$. Dòng chảy đạo hàm trong Back-propagation có một làn đường cao tốc chạy thẳng về tầng 1 mà không bao giờ bị tiêu biến!

---

## 🚀 PHẦN 5: LAN TRUYỀN NGƯỢC ĐẦU-CUỐI TRONG BÀI BÁO GPT2SP

Trong bài báo **GPT2SP (Fu & Tantithamthavorn, TSE 2023)**:
* Mô hình áp dụng phương thức **End-to-End Fine-Tuning** (Tinh chỉnh toàn diện đầu-cuối).
* Khi một User Story trên Jira được nạp vào mô hình và đưa ra dự đoán điểm Story Point $\hat{y}$, sai số được đo bằng hàm **L1 Loss**:
  $$\mathcal{L}_{L1} = |y_{\text{thực tế}} - \hat{y}|$$
* **Hành trình lan truyền ngược toàn cảnh:**
  1. Đạo hàm của L1 Loss ($\pm 1$) xuất phát từ đầu ra.
  2. Truyền ngược qua 2 tầng tuyến tính và hàm GeLU của **MLP Regressor Head**.
  3. Chảy vào vector ẩn của token cuối cùng tại Khối Transformer thứ 12.
  4. Phân nhánh chạy qua 12 đầu chú ý (Attention Heads) và các tầng FFN của cả 12 khối Transformer thông qua các đường tắt Residual Connections.
  5. Cuối cùng, cập nhật trực tiếp vào cả ma trận nhúng từ $W_{te}$ và ma trận nhúng vị trí $W_{pe}$!

Chính quá trình lan truyền ngược toàn diện này đã biến một mô hình ngôn ngữ thuần túy (GPT-2) trở thành một "chuyên gia thẩm định nỗ lực Agile" sắc sảo.

---

## ⏱️ PHẦN 6: TỔNG KẾT 30 GIÂY (THE ELEVATOR PITCH)

* **Bản chất:** Back-propagation là thuật toán cốt lõi của học sâu, sử dụng quy tắc chuỗi vi phân (Chain Rule) để truyền ngược đạo hàm sai số từ đầu ra về từng tham số ở đầu vào.
* **Cơ chế:** Phân bổ công bằng trách nhiệm lỗi lầm cho từng nơ-ron, cho phép bộ tối ưu hóa như AdamW biết chính xác phải vặn nút trọng số nào tăng lên hay giảm xuống.
* **Giá trị trong GPT2SP:** Cho phép tinh chỉnh đồng bộ toàn bộ 117 triệu tham số của GPT-2 và MLP Regressor Head dưới sự dẫn dắt của hàm mất mát L1 Loss, đạt bước nhảy vọt về độ chính xác ước lượng Story Point.