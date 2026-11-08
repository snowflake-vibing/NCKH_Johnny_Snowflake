# ✉️ ACADEMIC INQUIRY LETTER TO THE AUTHORS OF GPT2SP
## FORMAL CORRESPONDENCE ON REPLICATION DETAILS AND ARTIFACT CLARIFICATIONS

> **Target Recipients:**
> * **Michael Fu** (Lead Author, PhD Candidate): `yeh.fu@monash.edu`
> * **Dr. Chakkrit (Kla) Tantithamthavorn** (Corresponding Author, Associate Professor): `chakkrit@monash.edu`  
> **Affiliation:** Faculty of Information Technology, Monash University, Melbourne, Australia  
> **Reference Publication:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (IEEE Transactions on Software Engineering, Vol. 49, No. 4, pp. 2150–2165, 2023, DOI: [10.1109/TSE.2022.3158252](https://doi.org/10.1109/TSE.2022.3158252))  
> **Replication Repository:** [`https://github.com/awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp)  
> **Official Hugging Face Hub Checkpoint:** [`MickyMike/0-GPT2SP-springxd`](https://huggingface.co/MickyMike/0-GPT2SP-springxd)

---

## 📌 THÔNG TIN NHÓM TÁC GIẢ GỬI THƯ (RESEARCH TEAM PROFILE)

* **Người gửi chính (Primary Author & Sender):** **Lê Thành Hiệu** (MSSV: `24520496`) — Student Researcher, Faculty of Information Systems, University of Information Technology, VNU-HCM.
* **Cộng sự cùng thực hiện (Co-Author & Partner):** **Phan Ngọc Đức Huy** (MSSV: `24520695`) — Student Researcher, UIT, VNU-HCM.
* **Đơn vị:** Khoa Hệ thống Thông tin — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNU-HCM).
* **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*.
* **Mã nguồn công khai:** [`https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake`](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)

---

## 📑 BẢN EMAIL HOÀN CHỈNH (CARD HIỂN THỊ ĐẦY ĐỦ TRÊN GMAIL)

*(Bản bên dưới đã được chuẩn hóa HTML hoàn toàn phẳng, không bị lỗi thụt đầu dòng nên sẽ hiển thị card đồ họa 100% đẹp mắt trên cả Preview và khi dán vào Gmail)*.

<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.65; color: #1e293b; max-width: 760px; margin: 0 auto; border: 1px solid #cbd5e1; border-radius: 12px; padding: 28px; background-color: #ffffff; box-shadow: 0 4px 16px rgba(0,0,0,0.05);">

<p style="font-size: 15px; margin-top: 0;">Dear Michael and Dr. Tantithamthavorn,</p>

<p style="font-size: 15px;">I hope this email finds you well.</p>

<p style="font-size: 15px;">My name is <strong>Le Thanh Hieu</strong>, writing on behalf of our student research group alongside my colleague <strong>Phan Ngoc Duc Huy</strong> at the <em>Faculty of Information Systems, University of Information Technology, Vietnam National University Ho Chi Minh City (UIT - VNU-HCM)</em>.</p>

<p style="font-size: 15px;">We have been following your pioneering research in AI for Software Engineering with tremendous admiration. Your seminal IEEE TSE 2023 article, <em>"GPT2SP: A Transformer-Based Agile Story Point Estimation Approach"</em>, has been a central pillar of inspiration for our work, demonstrating how deep pre-trained language models significantly surpass legacy word-level architectures for Agile effort estimation.</p>

<p style="font-size: 15px;">As part of our research project investigating <strong>reproducibility and temporal aspects of deep learning in Agile Sprint Planning</strong>, we are currently replicating your experimental workflow on open-source Jira datasets—specifically the <strong>Spring XD</strong> benchmark—using both your official replication repository (<a href="https://github.com/awsm-research/gpt2sp" style="color: #2563eb; text-decoration: underline;"><code>awsm-research/gpt2sp</code></a>) and the pre-trained checkpoints published on Hugging Face Hub (<a href="https://huggingface.co/MickyMike/0-GPT2SP-springxd" style="color: #2563eb; text-decoration: underline;"><code>MickyMike/0-GPT2SP-springxd</code></a>).</p>

<p style="font-size: 15px;">While aligning our reproduction harness with your published metrics, we noted a few technical aspects where your kind guidance would be invaluable to ensure our benchmarking remains rigorous and completely faithful to your original methodology:</p>

<div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
<h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">1. Input Text Representation (<code>Title</code> vs. <code>Title + Description</code>)</h4>
<p style="margin: 0; font-size: 14px; color: #334155;">In Section 3.1 (<em>Context Extraction</em>) and Section 4.1 (<em>Experimental Setup</em>), the paper describes utilizing both the issue Title and Description. In the released Jupyter notebook (<code>model_training_notebook.ipynb</code>, function <code>prepare_dataframe</code>), the mapping is defined as:</p>
<div style="background-color: #1e293b; color: #f8fafc; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 13px; margin: 8px 0;">d = {'text': (data['title']).tolist(), 'label': data['storypoint']}</div>
<p style="margin: 0; font-size: 14px; color: #334155;">Could you kindly clarify whether the results in Table 4 were computed solely using the <code>title</code> field, or if an auxiliary preprocessing routine concatenated both fields before tokenization?</p>
</div>

<div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
<h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">2. Sequence Length Truncation Parameter (<code>SEQUENCE_LEN = 20</code>)</h4>
<p style="margin: 0; font-size: 14px; color: #334155;">In the replication notebook, the truncation threshold is set to <code>SEQUENCE_LEN = 20</code>. Since standard GPT-2 accommodates contextual windows of up to 1,024 tokens, we would love to understand whether the 20-token boundary was an intentional hyperparameter balancing GPU efficiency across the 16 cross-project benchmarks, or whether broader context windows (e.g., 128 or 512 tokens) were evaluated in your broader empirical suite.</p>
</div>

<div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
<h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">3. MLP Regressor Head Architecture & Non-Linear Activation</h4>
<p style="margin: 0; font-size: 14px; color: #334155;">Section 3.3 describes a Multi-Layer Perceptron (MLP) regressor head incorporating GELU non-linear activations. In <code>GPT2SP.py</code>:</p>
<div style="background-color: #1e293b; color: #f8fafc; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 13px; margin: 8px 0;">hidden_states = self.dense1(hidden_states)<br/>hidden_states = self.dense2(hidden_states)<br/>logits = self.score(hidden_states)</div>
<p style="margin: 0; font-size: 14px; color: #334155;">The tensors pass sequentially through <code>dense1</code> and <code>dense2</code> without an explicit functional call to <code>F.gelu()</code>. Could you clarify whether non-linearity was injected through a custom submodule configuration, or whether this represents a linear bottleneck variant adopted in the repository?</p>
</div>

<div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
<h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">4. Empirical Benchmark Alignment on Spring XD</h4>
<p style="margin: 0; font-size: 14px; color: #334155;">When evaluating your official checkpoint (<code>MickyMike/0-GPT2SP-springxd</code>) across the 706 chronological test issues of Spring XD (with <code>max_length = 20</code>, pad token ID <code>50257</code>), our test harness yields an MAE of approximately <b>1.7330</b> to <b>3.3090</b> (alongside a training-set Median Effort Baseline MAE of <b>1.7153</b>). Because Table 4 reports an impressive MAE of <b>0.96</b>, we suspect we might be missing a specific post-processing step, rounding rule, or evaluation harness convention. Any insight into the exact evaluation script would be enormously appreciated.</p>
</div>

<div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
<h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">5. Methodological Perspectives on Intra-Issue Revision History</h4>
<p style="margin: 0; font-size: 14px; color: #334155;">Finally, as our research specifically investigates temporal leakage control at planning time (observing that Jira descriptions frequently accumulate implementation details, stack traces, and comments long after the estimation event), we would love to know your perspective on how future Transformer architectures should best filter or reconstruct historical state snapshots in industrial Agile workflows.</p>
</div>

<p style="font-size: 15px;">We completely appreciate how busy your schedule is and would be deeply grateful for any advice, references, or updated scripts you could share. We are glad to provide our full replication repository, environment specs, and logs if that would assist.</p>

<p style="font-size: 15px;">Thank you very much once again for your inspiring contributions to Software Engineering research!</p>

<!-- ANIMATED MEME GIF "CAT THUMBS UP" (LEGENDARY MEME - TENOR CDN) -->
<div style="margin: 24px auto 18px auto; text-align: center;">
<img src="https://media.tenor.com/TsVXIAMBZXoAAAAM/cat-thumbs-up-thumbs-up.gif" alt="Cat Thumbs Up Meme" style="width: 155px; height: auto; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.1); display: block; margin: 0 auto;" />
<div style="font-size: 13px; color: #475569; margin-top: 8px; font-weight: 500;">Wishing you a wonderful week ahead! 👍✨</div>
</div>

<p style="font-size: 15px; margin-bottom: 24px;">Warmest regards,</p>

<!-- FOOTER CARD CHUYÊN NGHIỆP: LOGO UIT (BÊN TRÁI) | THÔNG TIN (Ở GIỮA) | MENU (BÊN PHẢI) -->
<table style="width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1; border-radius: 10px; background-color: #f8fafc; padding: 0; margin-top: 20px; overflow: hidden;">
<tr>
<td style="vertical-align: middle; width: 22%; text-align: center; padding: 16px; border-right: 1px solid #e2e8f0; background-color: #ffffff;">
<a href="https://www.uit.edu.vn" target="_blank" style="text-decoration: none; display: block;">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Logo_UIT_updated.svg/330px-Logo_UIT_updated.svg.png" alt="UIT Logo" style="width: 82px; height: auto; max-height: 75px; display: block; margin: 0 auto; border: none;" />
</a>
<div style="font-size: 11px; font-weight: 700; color: #1e3a8a; margin-top: 8px; letter-spacing: 0.04em;">UIT &bull; VNU-HCM</div>
</td>
<td style="vertical-align: middle; width: 52%; padding: 16px 20px;">
<div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">Le Thanh Hieu</div>
<div style="font-size: 13px; color: #2563eb; font-weight: 600; margin-bottom: 6px;">Undergraduate Student Researcher &bull; ID: <code>24520496</code></div>
<div style="font-size: 12px; color: #475569; line-height: 1.55;">
<b>Co-Author:</b> Phan Ngoc Duc Huy (ID: <code>24520695</code>)<br/>
<b>Department:</b> Faculty of Information Systems<br/>
<b>Institution:</b> University of Information Technology, VNU-HCM<br/>
<b>Location:</b> Ho Chi Minh City, Vietnam
</div>
</td>
<td style="vertical-align: middle; width: 26%; text-align: left; padding: 16px; border-left: 1px solid #e2e8f0; background-color: #ffffff;">
<div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b; margin-bottom: 10px; letter-spacing: 0.05em;">Connect with us</div>
<div style="margin-bottom: 8px;">
<a href="https://github.com/snowflake-vibing" target="_blank" style="text-decoration: none; color: #0f172a; font-size: 12px; font-weight: 600; display: block;">
<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 6px; border-radius: 50%; border: none;" />
<span>GitHub Profile</span>
</a>
</div>
<div>
<a href="https://www.linkedin.com/in/th%C3%A0nh-hi%E1%BB%87u-84b99634b/" target="_blank" style="text-decoration: none; color: #0a66c2; font-size: 12px; font-weight: 600; display: block;">
<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 6px; border-radius: 4px; border: none;" />
<span>LinkedIn Profile</span>
</a>
</div>
</td>
</tr>
</table>

</div>

---

## 🛠️ HƯỚNG DẪN CÁCH COPY & DÁN LÊN GMAIL KHÔNG BỊ LỖI FONT / VỠ KHUNG

### 🎯 Cách 1: Dán trực tiếp từ Trình duyệt (Dễ nhất & Đẹp 100%)
1. Tôi đã tạo sẵn cho bạn một file HTML độc lập tại: [`docs/email/email_preview.html`](email_preview.html).
2. Bạn chỉ cần **nhấp đúp mở file `email_preview.html` bằng Google Chrome hoặc Microsoft Edge**.
3. Nhấn tổ hợp phím **`Ctrl + A`** (chọn tất cả) $\rightarrow$ **`Ctrl + C`** (sao chép).
4. Mở **Gmail** $\rightarrow$ bấm **Soạn thư (Compose)** $\rightarrow$ nhấp chuột vào khung soạn thư và nhấn **`Ctrl + V`**.
5. Toàn bộ card viền, logo UIT, icon menu, hộp câu hỏi và meme GIF Cat Thumbs Up sẽ hiển thị nguyên vẹn, chuẩn xác 100%!

### 🎯 Cách 2: Copy từ bản Preview Markdown trong VS Code
1. Nhấn **`Ctrl + Shift + V`** để mở tab Preview file này trong VS Code.
2. Dùng chuột bôi đen từ dòng chữ `Dear Michael and Dr. Tantithamthavorn,` đến hết mép dưới của thẻ Chữ ký `Connect with us`.
3. Nhấn **`Ctrl + C`** $\rightarrow$ mở Gmail và nhấn **`Ctrl + V`**.

### 📮 Thông tin gửi thư:
* **To:** `yeh.fu@monash.edu`
* **Cc:** `chakkrit@monash.edu`
* **Subject:** `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`
