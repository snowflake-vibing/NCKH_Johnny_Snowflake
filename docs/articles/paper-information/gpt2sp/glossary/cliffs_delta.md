# 🧩 THUẬT NGỮ: CLIFF'S DELTA (KÍCH THƯỚC HIỆU ỨNG PHI THAM SỐ)

> **Kích thước hiệu ứng Cliff's Delta (Cliff's $\delta$)**  
> *Thuộc nhóm:* Thống Kê Phi Tham Số & Đánh Giá Thực Nghiệm (Non-parametric Statistics & Effect Size)  
> *Áp dụng trong:* Toàn bộ các kiểm định phân hạng thứ bậc Scott-Knott ESD trong bài báo **GPT2SP (Fu & Tantithamthavorn, IEEE TSE 2023)** tại Mục 4.6 (Trang 7), Bảng 4, 5, 6, 7 (Trang 8 – 10).

---

## 🎯 PHẦN 1: BẢN CHẤT CỐT LÕI & TRỰC GIÁC KỸ THUẬT

Để hiểu tại sao các nhà nghiên cứu công nghệ phần mềm (Software Engineering) bắt buộc phải dùng **Cliff's Delta**, hãy nhìn vào nghịch lý lớn nhất của kiểm định thống kê cổ điển:

### 1. Nghịch lý của giá trị $p$-value ($p < 0.05$ là chưa đủ!)
Khi so sánh hai mô hình AI (ví dụ: mô hình đề xuất **GPT2SP** và baseline **Deep-SE**), các kỹ sư thường dùng kiểm định Wilcoxon Signed-Rank Test để tính giá trị $p$-value:
* $p < 0.05$ chỉ trả lời được câu hỏi: *"Liệu có tồn tại sự khác biệt giữa hai mô hình hay không?"*.
* Nhưng $p$-value **hoàn toàn không trả lời được câu hỏi:** *"Sự khác biệt đó LỚN ĐẾN MỨC NÀO trong thực tế?"*.
* **Bẫy cỡ mẫu lớn (Sample Size Problem):** Trong bài báo GPT2SP, kho dữ liệu lên tới **$23.313$ Jira issues**. Khi cỡ mẫu lớn đến hàng chục ngàn, giá trị $p$-value gần như luôn luôn vọt xuống mức cực nhỏ ($p < 0.001$), ngay cả khi mô hình mới chỉ cải thiện một con số vô nghĩa (ví dụ: chỉ giảm được $0.001$ Story Point). Nếu chỉ dựa vào $p$-value, nhà nghiên cứu sẽ lầm tưởng mô hình của mình đạt đột phá khoa học vĩ đại!

### 2. Kích thước hiệu ứng (Effect Size) — Thước đo độ lớn thực chất
Để trả lời câu hỏi: *"Sự vượt trội của GPT2SP có thực chất và đáng kể về mặt khoa học hay không?"*, các nhà nghiên cứu bắt buộc phải đo lường **Kích thước hiệu ứng (Effect Size)**.

### 3. Tại sao lại chọn Cliff's Delta mà không dùng Cohen's $d$?
* **Cohen's $d$ (Tham số):** Giả định dữ liệu phải tuân theo phân phối chuẩn hình quả chuông (Gaussian) và dùng trung bình cộng ($\mu$) cùng độ lệch chuẩn ($\sigma$).
* **Thực tế dữ liệu Jira:** Sai số ước lượng (MAE) của Story Point luôn có **phân phối lệch phải nghiêm trọng (Highly Skewed)** và xuất hiện các ngoại lai (outliers) có độ lệch lớn. Cohen's $d$ sẽ bị bóp méo hoàn toàn trước dữ liệu này!
* **Cliff's Delta (Phi tham số):** Không quan tâm dữ liệu có phân phối chuẩn hay không, không phụ thuộc vào giá trị trung bình cộng, mà chỉ đo lường **tần suất thống trị (Dominance)** giữa các cặp quan sát.

---

## 🔍 PHẦN 2: BÓC TÁCH THUẬT NGỮ & CÔNG THỨC TOÁN HỌC

Thuật toán được đặt theo tên của nhà tâm trắc học **Norman Cliff** (1993):

| Thành tố | Gốc từ tiếng Anh | Bản chất trong Toán học & Khoa học Dữ liệu |
| :--- | :--- | :--- |
| **Cliff** | *Norman Cliff* | Giáo sư danh dự tại University of Southern California, tác giả đề xuất công thức năm 1993. |
| **Delta ($\delta$)** | *Ký tự Hy Lạp Delta* | Đại diện cho mức độ chênh lệch hoặc hiệu số giữa hai xác suất thống kê. |
| **Non-parametric** | *Phi tham số* | Phép đo không giả định dạng phân phối toán học của tổng thể (Distribution-free). |

### 1. Công thức toán học định nghĩa:
Giả sử ta có hai nhóm kết quả thực nghiệm:
* Nhóm $X = \{x_1, x_2, \dots, x_m\}$ (ví dụ: phân phối sai số MAE của GPT2SP qua $m$ lượt chạy).
* Nhóm $Y = \{y_1, y_2, \dots, y_n\}$ (ví dụ: phân phối sai số MAE của Deep-SE qua $n$ lượt chạy).

Ta tiến hành so sánh từng phần tử $x_i$ với từng phần tử $y_j$ (tổng cộng có $m \times n$ cặp so sánh). **Cliff's Delta ($\delta$)** được tính bằng:

$$\delta = \frac{\sum_{i=1}^{m} \sum_{j=1}^{n} \left( [x_i > y_j] - [x_i < y_j] \right)}{m \times n} = \frac{\text{count}(x_i > y_j) - \text{count}(x_i < y_j)}{m \times n}$$

Trong đó:
* $\text{count}(x_i > y_j)$ là số lần một giá trị của nhóm $X$ lớn hơn một giá trị của nhóm $Y$.
* $\text{count}(x_i < y_j)$ là số lần một giá trị của nhóm $X$ nhỏ hơn một giá trị của nhóm $Y$.
* $m \times n$ là tổng số cặp so sánh toàn bộ.

### 2. Diễn giải dưới góc độ xác suất:

$$\delta = P(X > Y) - P(X < Y)$$

### 3. Miền giá trị và ý nghĩa:
Giá trị Cliff's Delta luôn nằm trong đoạn hữu hạn: **$-1 \le \delta \le +1$**:
* **$\delta = +1$:** Thống trị tuyệt đối ($100\%$ các quan sát trong $X$ đều lớn hơn mọi quan sát trong $Y$).
* **$\delta = -1$:** Bị thống trị tuyệt đối ($100\%$ các quan sát trong $X$ đều nhỏ hơn mọi quan sát trong $Y$).
* **$\delta = 0$:** Hai nhóm hoàn toàn tương đương nhau (xác suất $X > Y$ bằng đúng xác suất $X < Y$).

---

## 📊 PHẦN 3: BẢNG PHÂN NGƯỠNG HIỆU ỨNG CỦA ROMANO ET AL. (2006)

Để quy đổi con số $\delta$ liên tục sang mức độ ý nghĩa thực tiễn, cộng đồng khoa học phần mềm tuân thủ nghiêm ngặt bảng phân ngưỡng kinh điển của **Romano et al. (2006)**:

| Ngưỡng giá trị tuyệt đối ($|\delta|$) | Mức độ hiệu ứng (Effect Size) | Ý nghĩa thực tiễn trong Nghiên cứu Khoa học |
| :---: | :---: | :--- |
| **$|\delta| < 0.147$** | **Negligible** | **Khác biệt không đáng kể.** Hai mô hình được coi là tương đương nhau về năng lực thực tế. |
| **$0.147 \le |\delta| < 0.330$** | **Small** | **Khác biệt nhỏ.** Mô hình mới có nhỉnh hơn nhưng chưa thực sự vượt trội. |
| **$0.330 \le |\delta| < 0.474$** | **Medium** | **Khác biệt trung bình.** Sự cải tiến thể hiện rõ ràng và đáng ghi nhận. |
| **$|\delta| \ge 0.474$** | **Large** | **Khác biệt lớn (Đột phá).** Mô hình mới thống trị hoàn toàn baseline với ý nghĩa thực tiễn rất mạnh. |

---

## ⚖️ PHẦN 4: SO SÁNH ĐỐI CHỨNG: COHEN'S $d$ VS. CLIFF'S DELTA

| Tiêu chí so sánh | Cohen's $d$ (Tham số) | Cliff's Delta ($\delta$) (Phi tham số) |
| :--- | :--- | :--- |
| **Loại thống kê** | Tham số (Parametric). | Phi tham số (Non-parametric). |
| **Giả định phân phối** | Bắt buộc dữ liệu phải có phân phối chuẩn $\mathcal{N}(\mu, \sigma^2)$. | **Không đòi hỏi bất kỳ giả định nào** về phân phối. |
| **Độ nhạy với ngoại lai (Outliers)** | Rất nhạy cảm: các task Jira 40–100 SP sẽ làm thổi phồng độ lệch chuẩn. | **Cực kỳ bền bỉ (Robust):** Chỉ so sánh thứ bậc ($>$ hoặc $<$), không bị ảnh hưởng bởi độ lớn ngoại lai. |
| **Kiểu thang đo phù hợp** | Thang đo khoảng / tỷ lệ (Interval / Ratio). | Thang đo thứ bậc và tỷ lệ (Ordinal / Ratio). |
| **Miền giá trị** | $(-\infty, +\infty)$ (Khó diễn giải trực giác). | $[-1.0, +1.0]$ (Trực quan, dễ so sánh xác suất). |
| **Khuyến nghị trong SE** | Thường bị phê phán vì dữ liệu phần mềm hiếm khi chuẩn. | **Được khuyến nghị là chuẩn mực vàng** trong công nghệ phần mềm thực nghiệm. |

---

## 📚 PHẦN 5: CÁC BÀI BÁO KHOA HỌC KINH ĐIỂN VỀ CLIFF'S DELTA

---

### 📄 1. Bài báo gốc khai sinh thuật toán Cliff's Delta
* **Tên bài báo:** *"Dominance statistics: Ordinal analyses to answer ordinal questions"*
* **Tác giả:** Norman Cliff (University of Southern California).
* **Xuất bản:** *Psychological Bulletin*, Vol. 114, No. 3, Trang 494–509 (1993).
* **DOI:** [10.1037/0033-2909.114.3.494](https://doi.org/10.1037/0033-2909.114.3.494)
* **Đóng góp then chốt:** Bài báo chỉ trích việc áp dụng cơ học các thống kê dựa trên giá trị trung bình ($\bar{X}$) cho các thang đo thứ bậc và đề xuất thống kê thống trị (Dominance Statistics) $d$, sau này được gọi là Cliff's Delta.

---

### 📄 2. Bài báo thiết lập 4 ngưỡng hiệu ứng chuẩn mực (Romano et al., 2006)
* **Tên bài báo:** *"Appropriate statistics for ordinal level data: Should we really be using t-test and Cohen’s d for evaluating group differences on the NSSE and other surveys?"*
* **Tác giả:** Jeanine L. Romano, Jeffrey D. Kromrey, Jesse Coraggio, Jeff Skowronek.
* **Xuất bản:** *Annual Meeting of the Florida Association for Institutional Research*, Trang 1–33 (2006).
* **Đóng góp then chốt:** Nghiên cứu mô phỏng Monte Carlo đồ sộ thiết lập 4 ngưỡng định lượng được cả giới khoa học công nhận: **$0.147$ (Small), $0.330$ (Medium), và $0.474$ (Large)**.

---

### 📄 3. Bài báo đưa Cliff's Delta vào chuẩn kiểm định SE (Tantithamthavorn et al., 2017 & 2019)
* **Tên bài báo:** *"An Empirical Comparison of Model Validation Techniques for Defect Prediction Models"*
* **Tác giả:** Chakkrit Tantithamthavorn, Shane McIntosh, Ahmed E. Hassan, Kenichi Matsumoto.
* **Xuất bản:** *IEEE Transactions on Software Engineering (TSE)*, Vol. 43, No. 1, Trang 1–18 (2017).
* **Đóng góp then chốt:** Tác giả kết hợp kiểm định Scott-Knott ESD với Cliff's Delta để giải quyết triệt để vấn đề phân cụm trùng lặp (Overlapping clusters) khi so sánh nhiều mô hình học máy trong công nghệ phần mềm.

---

### 📄 4. Ứng dụng trong bài báo GPT2SP (Fu & Tantithamthavorn, IEEE TSE 2023)
* **Vị trí trong bài báo:** Mục 4.6 (Evaluation Measures & Statistical Tests), Trang 7, Cột 2.
* **Cơ chế phân cụm thứ bậc Scott-Knott ESD:**
  - Thuật toán sắp xếp các kỹ thuật theo giá trị trung vị sai số MAE.
  - Sau đó tính toán Cliff's Delta giữa từng cặp kỹ thuật liền kề:
    * Nếu $|\delta| < 0.147$ (Negligible): Hai kỹ thuật được **gộp chung vào một thứ hạng (Rank)** vì sự chênh lệch là không đáng kể.
    * Nếu $|\delta| \ge 0.147$: Thuật toán **tách thành hai thứ hạng riêng biệt**.
* **Kết quả thực nghiệm:** GPT2SP đạt **Rank 1 duy nhất** trên $12/16$ dự án với kích thước hiệu ứng **Large ($|\delta| \ge 0.474$)** trước tất cả các đối thủ baseline (Deep-SE, Random Forest, SVM).

---

## 💻 PHẦN 6: MÃ NGUỒN PYTHON THỰC NGHIỆM TÍNH TOÁN CLIFF'S DELTA

Bạn có thể tự thực thi đoạn mã Python chuẩn hóa dưới đây để tính toán Cliff's Delta trên dữ liệu thực tế:

```python
import numpy as np

def compute_cliffs_delta(x, y):
    """
    Tính toán kích thước hiệu ứng Cliff's Delta giữa hai mảng dữ liệu x và y.
    Công thức: delta = (count(x > y) - count(x < y)) / (m * n)
    """
    x = np.asarray(x)
    y = np.asarray(y)
    m = len(x)
    n = len(y)
    
    # Tạo ma trận so sánh từng cặp (broadcasting)
    # diff_matrix[i, j] = x[i] - y[j]
    diff_matrix = x[:, None] - y[None, :]
    
    count_greater = np.sum(diff_matrix > 0)
    count_smaller = np.sum(diff_matrix < 0)
    
    delta = (count_greater - count_smaller) / (m * n)
    
    # Phân loại mức độ hiệu ứng theo Romano et al. (2006)
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        effect_size = "Negligible (Không đáng kể)"
    elif abs_delta < 0.330:
        effect_size = "Small (Nhỏ)"
    elif abs_delta < 0.474:
        effect_size = "Medium (Trung bình)"
    else:
        effect_size = "Large (Lớn - Đột phá)"
        
    return delta, effect_size

# Dữ liệu mô phỏng sai số MAE qua 10 lượt chạy thực nghiệm
mae_gpt2sp = [0.92, 0.95, 0.96, 0.91, 0.94, 0.97, 0.93, 0.95, 0.96, 0.92]
mae_deep_se = [1.58, 1.62, 1.65, 1.55, 1.60, 1.70, 1.63, 1.59, 1.61, 1.64]

delta, effect = compute_cliffs_delta(mae_gpt2sp, mae_deep_se)

print(f"=== KẾT QUẢ KIỂM ĐỊNH HIỆU ỨNG CLIFF'S DELTA ===")
print(f"Giá trị Cliff's Delta (delta): {delta:.4f}")
print(f"Đánh giá định tính: {effect}")
# Kết quả delta = -1.000: Sai số của GPT2SP luôn luôn nhỏ hơn Deep-SE trong mọi lượt chạy!
```

---

## ⏱️ PHẦN 7: TỔNG KẾT 30 GIÂY (THE ELEVATOR PITCH)

* **Bản chất:** Cliff's Delta ($\delta$) là thước đo kích thước hiệu ứng phi tham số, định lượng mức độ thống trị xác suất giữa hai phân phối mà không đòi hỏi giả định chuẩn tắc: $\delta = P(X > Y) - P(X < Y)$.
* **Điểm đột phá:** Khắc phục triệt để "cái bẫy $p$-value" khi cỡ mẫu Jira quá lớn ($>20.000$ issues) và hoàn toàn miễn nhiễm trước các sai số ngoại lai dị biệt.
* **Quy chuẩn khoa học:** Sử dụng 4 ngưỡng phân định của Romano et al. (2006): $0.147$ (Small), $0.330$ (Medium), $0.474$ (Large).
* **Ứng dụng trong GPT2SP:** Là "trọng tài phân định" bên trong thuật toán Scott-Knott ESD, gộp các mô hình có chênh lệch không đáng kể ($|\delta| < 0.147$) vào chung thứ hạng và tách biệt các mô hình đột phá vào Rank 1.
