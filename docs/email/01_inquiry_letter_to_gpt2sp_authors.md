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

## 📌 THÔNG TIN NHÓM NGHIÊN CỨU GỬI THƯ (RESEARCH TEAM)

* **Người gửi chính (Primary Author & Sender):** **Lê Thành Hiệu** (MSSV: `24520496`) — Student Researcher, Faculty of Information Systems, University of Information Technology, VNU-HCM.
* **Cộng sự cùng thực hiện (Co-Investigator / Partner):** **Phan Ngọc Đức Huy** (MSSV: `24520695`) — Student Researcher, UIT, VNU-HCM.
* **Đơn vị:** Khoa Hệ thống Thông tin — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT - VNU-HCM).
* **Đề tài nghiên cứu:** *Agile Story Point Estimation at Planning Time with Temporal & Data Leakage Control*.
* **Open Repository:** [`https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake`](https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake)

---

## 📑 BẢN 1: BẢN THẢO EMAIL ĐỊNH DẠNG RICH-TEXT / HTML (CÓ "HAVE A NICE DAY" GIF & FOOTER CARD)

*(Chỉ cần bôi đen từ chữ `Academic Research Correspondence` đến hết khung viền xám dưới chân trang, nhấn `Ctrl + C` và dán thẳng `Ctrl + V` vào khung soạn thư Gmail)*.

<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.65; color: #1e293b; max-width: 760px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; padding: 28px; background-color: #ffffff; box-shadow: 0 4px 16px rgba(0,0,0,0.04);">

  <!-- Email Header -->
  <div style="border-bottom: 2px solid #2563eb; padding-bottom: 16px; margin-bottom: 24px;">
    <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; color: #2563eb; font-weight: 700;">Academic Research Correspondence</div>
    <h2 style="margin: 8px 0 4px 0; color: #0f172a; font-size: 20px; font-weight: 700;">Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)</h2>
    <div style="font-size: 13px; color: #64748b;">To: <b>Michael Fu</b> &lt;yeh.fu@monash.edu&gt; &bull; Cc: <b>Dr. Chakkrit Tantithamthavorn</b> &lt;chakkrit@monash.edu&gt;</div>
  </div>

  <!-- Salutation -->
  <p style="font-size: 15px; margin-top: 0;">Dear Michael and Dr. Tantithamthavorn,</p>

  <p style="font-size: 15px;">I hope this email finds you well and having a productive academic semester.</p>

  <p style="font-size: 15px;">
    My name is <b>Le Thanh Hieu</b>, writing on behalf of our student research group alongside my colleague <b>Phan Ngoc Duc Huy</b> at the <i>Faculty of Information Systems, University of Information Technology, Vietnam National University Ho Chi Minh City (UIT - VNU-HCM)</i>.
  </p>

  <p style="font-size: 15px;">
    We have been following your pioneering research in AI for Software Engineering with tremendous admiration. Your seminal IEEE TSE 2023 article, <i>"GPT2SP: A Transformer-Based Agile Story Point Estimation Approach"</i>, has been a central pillar of inspiration for our work, demonstrating how deep pre-trained language models significantly surpass legacy word-level architectures for Agile effort estimation.
  </p>

  <p style="font-size: 15px;">
    As part of our research project investigating <b>reproducibility and temporal aspects of deep learning in Agile Sprint Planning</b>, we are currently replicating your experimental workflow on open-source Jira datasets—specifically the <b>Spring XD</b> benchmark—using both your official replication repository (<a href="https://github.com/awsm-research/gpt2sp" style="color: #2563eb; text-decoration: underline;"><code>awsm-research/gpt2sp</code></a>) and the pre-trained checkpoints published on Hugging Face Hub (<a href="https://huggingface.co/MickyMike/0-GPT2SP-springxd" style="color: #2563eb; text-decoration: underline;"><code>MickyMike/0-GPT2SP-springxd</code></a>).
  </p>

  <p style="font-size: 15px;">
    While aligning our reproduction harness with your published metrics, we noted a few technical aspects where your kind guidance would be invaluable to ensure our benchmarking remains rigorous and completely faithful to your original methodology:
  </p>

  <!-- Point 1 -->
  <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
    <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">1. Input Text Representation (<code>Title</code> vs. <code>Title + Description</code>)</h4>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      In Section 3.1 (<i>Context Extraction</i>) and Section 4.1 (<i>Experimental Setup</i>), the paper describes utilizing both the issue Title and Description. In the released Jupyter notebook (<code>model_training_notebook.ipynb</code>, function <code>prepare_dataframe</code>), the mapping is defined as:
    </p>
    <div style="background-color: #1e293b; color: #f8fafc; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 13px; margin: 8px 0;">
      d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
    </div>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      Could you kindly clarify whether the results in Table 4 were computed solely using the <code>title</code> field, or if an auxiliary preprocessing routine concatenated both fields before tokenization?
    </p>
  </div>

  <!-- Point 2 -->
  <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
    <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">2. Sequence Length Truncation Parameter (<code>SEQUENCE_LEN = 20</code>)</h4>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      In the replication notebook, the truncation threshold is set to <code>SEQUENCE_LEN = 20</code>. Since standard GPT-2 accommodates contextual windows of up to 1,024 tokens, we would love to understand whether the 20-token boundary was an intentional hyperparameter balancing GPU efficiency across the 16 cross-project benchmarks, or whether broader context windows (e.g., 128 or 512 tokens) were evaluated in your broader empirical suite.
    </p>
  </div>

  <!-- Point 3 -->
  <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
    <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">3. MLP Regressor Head Architecture & Non-Linear Activation</h4>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      Section 3.3 describes a Multi-Layer Perceptron (MLP) regressor head incorporating GELU non-linear activations. In <code>GPT2SP.py</code>:
    </p>
    <div style="background-color: #1e293b; color: #f8fafc; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 13px; margin: 8px 0;">
      hidden_states = self.dense1(hidden_states)<br/>
      hidden_states = self.dense2(hidden_states)<br/>
      logits = self.score(hidden_states)
    </div>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      The tensors pass sequentially through <code>dense1</code> and <code>dense2</code> without an explicit functional call to <code>F.gelu()</code>. Could you clarify whether non-linearity was injected through a custom submodule configuration, or whether this represents a linear bottleneck variant adopted in the repository?
    </p>
  </div>

  <!-- Point 4 -->
  <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
    <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">4. Empirical Benchmark Alignment on Spring XD</h4>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      When evaluating your official checkpoint (<code>MickyMike/0-GPT2SP-springxd</code>) across the 706 chronological test issues of Spring XD (with <code>max_length = 20</code>, pad token ID <code>50257</code>), our test harness yields an MAE of approximately <b>1.7330</b> to <b>3.3090</b> (alongside a training-set Median Effort Baseline MAE of <b>1.7153</b>). Because Table 4 reports an impressive MAE of <b>0.96</b>, we suspect we might be missing a specific post-processing step, rounding rule, or evaluation harness convention. Any insight into the exact evaluation script would be enormously appreciated.
    </p>
  </div>

  <!-- Point 5 -->
  <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 16px 0; border-radius: 0 8px 8px 0;">
    <h4 style="margin: 0 0 6px 0; font-size: 15px; color: #1e3a8a;">5. Methodological Perspectives on Intra-Issue Revision History</h4>
    <p style="margin: 0; font-size: 14px; color: #334155;">
      Finally, as our research specifically investigates temporal leakage control at planning time (observing that Jira descriptions frequently accumulate implementation details, stack traces, and comments long after the estimation event), we would love to know your perspective on how future Transformer architectures should best filter or reconstruct historical state snapshots in industrial Agile workflows.
    </p>
  </div>

  <p style="font-size: 15px;">
    We completely appreciate how busy your schedule is and would be deeply grateful for any advice, references, or updated scripts you could share. We are glad to provide our full replication repository, environment specs, and logs if that would assist.
  </p>

  <p style="font-size: 15px;">
    Thank you very much once again for your inspiring contributions to Software Engineering research!
  </p>

  <!-- Friendly "Have a nice day" GIF -->
  <div style="margin: 24px 0 20px 0; text-align: center;">
    <img src="https://raw.githubusercontent.com/snowflake-vibing/NCKH_Johnny_Snowflake/main/docs/email/assets/have_a_nice_day.gif" alt="Have a nice day!" style="max-width: 320px; height: auto; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);" />
  </div>

  <p style="font-size: 15px; margin-bottom: 24px;">Warmest regards,</p>

  <!-- ======================================================= -->
  <!-- FOOTER CARD: UIT LOGO (LEFT) | INFO (MID) | MENU (RIGHT) -->
  <!-- ======================================================= -->
  <div style="border-top: 2px solid #e2e8f0; padding-top: 20px; margin-top: 20px; background-color: #f8fafc; border-radius: 10px; padding: 18px 20px;">
    <table style="width: 100%; border-collapse: collapse; border: none;">
      <tr>
        <!-- CỘT BÊN TRÁI: LOGO UIT -->
        <td style="vertical-align: middle; width: 18%; text-align: center; padding-right: 16px; border-right: 2px solid #e2e8f0;">
          <a href="https://www.uit.edu.vn" target="_blank" style="text-decoration: none;">
            <img src="https://raw.githubusercontent.com/snowflake-vibing/NCKH_Johnny_Snowflake/main/docs/email/assets/uit_logo.png" alt="UIT Logo" style="width: 82px; height: auto; max-height: 80px; display: block; margin: 0 auto;" />
          </a>
          <div style="font-size: 11px; font-weight: 700; color: #1e3a8a; margin-top: 6px; letter-spacing: 0.04em;">
            UIT &bull; VNU-HCM
          </div>
        </td>

        <!-- CỘT Ở GIỮA: THÔNG TIN LÊ THÀNH HIỆU & PHAN NGỌC ĐỨC HUY -->
        <td style="vertical-align: middle; width: 56%; padding: 0 18px;">
          <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 2px;">
            Le Thanh Hieu
          </div>
          <div style="font-size: 13px; color: #2563eb; font-weight: 600; margin-bottom: 6px;">
            Undergraduate Student Researcher &bull; ID: <code>24520496</code>
          </div>
          <div style="font-size: 12px; color: #475569; line-height: 1.55;">
            <b>Co-Author / Research Partner:</b> Phan Ngoc Duc Huy (ID: <code>24520695</code>)<br/>
            <b>Department:</b> Faculty of Information Systems<br/>
            <b>Institution:</b> University of Information Technology, VNU-HCM (UIT - VNU-HCM)<br/>
            <b>Location:</b> Ho Chi Minh City, Vietnam
          </div>
        </td>

        <!-- CỘT BÊN PHẢI: MENU LOGO (GITHUB, LINKEDIN, FACEBOOK) -->
        <td style="vertical-align: middle; width: 26%; text-align: left; padding-left: 16px; border-left: 2px solid #e2e8f0;">
          <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b; margin-bottom: 10px; letter-spacing: 0.05em;">
            Connect with us
          </div>

          <!-- Menu Item: GitHub -->
          <div style="margin-bottom: 8px;">
            <a href="https://github.com/snowflake-vibing" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; color: #0f172a; font-size: 12px; font-weight: 600;">
              <img src="https://raw.githubusercontent.com/snowflake-vibing/NCKH_Johnny_Snowflake/main/docs/email/assets/github_icon.png" alt="GitHub" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px; border-radius: 50%;" />
              <span>GitHub Profile</span>
            </a>
          </div>

          <!-- Menu Item: LinkedIn -->
          <div style="margin-bottom: 8px;">
            <a href="https://www.linkedin.com/in/th%C3%A0nh-hi%E1%BB%87u-84b99634b/" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; color: #0a66c2; font-size: 12px; font-weight: 600;">
              <img src="https://raw.githubusercontent.com/snowflake-vibing/NCKH_Johnny_Snowflake/main/docs/email/assets/linkedin_icon.png" alt="LinkedIn" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px; border-radius: 4px;" />
              <span>LinkedIn Profile</span>
            </a>
          </div>

          <!-- Menu Item: Facebook -->
          <div>
            <a href="https://www.facebook.com" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; color: #1877f2; font-size: 12px; font-weight: 600;">
              <img src="https://raw.githubusercontent.com/snowflake-vibing/NCKH_Johnny_Snowflake/main/docs/email/assets/facebook_icon.png" alt="Facebook" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px; border-radius: 50%;" />
              <span>Facebook</span>
            </a>
          </div>
        </td>
      </tr>
    </table>
  </div>

</div>

---

## 📄 BẢN 2: BẢN THẢO EMAIL ĐỊNH DẠNG PLAIN-TEXT (DÀNH CHO TEXT NGUYÊN BẢN)

```text
Subject: Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)

Dear Michael and Dr. Tantithamthavorn,

I hope this email finds you well and having a productive semester.

My name is Le Thanh Hieu, writing on behalf of our student research group alongside my colleague Phan Ngoc Duc Huy at the Faculty of Information Systems, University of Information Technology, Vietnam National University Ho Chi Minh City (UIT - VNU-HCM).

We have been studying your seminal paper, "GPT2SP: A Transformer-Based Agile Story Point Estimation Approach" (IEEE TSE 2023), with great admiration. Your work is widely regarded in our research lab as a groundbreaking milestone that demonstrated the superiority of pre-trained Transformer language models over traditional architectures in Agile software estimation.

As part of our ongoing research project investigating empirical reproducibility and temporal aspects of Agile software estimation, we are currently replicating your experimental workflow on open-source Jira datasets—specifically the Spring XD benchmark—using both your official GitHub replication package (awsm-research/gpt2sp) and the pre-trained checkpoints released on Hugging Face (MickyMike/0-GPT2SP-springxd).

While replicating the empirical pipeline, we noted a few technical aspects where we would be immensely grateful for your kind clarification:

1. Input Text Representation (Title vs. Title + Description):
In Section 3.1 (Context Extraction) and Section 4.1 (Experimental Setup), the paper states that both the issue Title and Description are used. In model_training_notebook.ipynb, the mapping only takes the title:
d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
Could you kindly clarify whether the results in Table 4 were obtained using solely the title field, or whether an updated preprocessing routine concatenated both fields?

2. Sequence Length Truncation Parameter (SEQUENCE_LEN = 20):
In model_training_notebook.ipynb, the sequence truncation boundary is configured as SEQUENCE_LEN = 20. Given that base GPT-2 supports contextual windows up to 1,024 tokens, we would love to know if the 20-token limit was a specific hyperparameter optimization chosen for runtime efficiency across the 16 projects, or if experiments with longer contextual bounds (e.g., 128 or 512 tokens) were evaluated in your broader empirical suite.

3. MLP Regressor Head Architecture and Non-Linear Activation:
Section 3.3 describes an MLP regressor head incorporating a GELU non-linear activation. In GPT2SP.py:
hidden_states = self.dense1(hidden_states)
hidden_states = self.dense2(hidden_states)
logits = self.score(hidden_states)
the tensor passes sequentially through dense1 and dense2 without an explicit functional call to gelu(). Could you clarify if the non-linearity was intended to be injected via a custom configuration hook, or if this represents an optimized linear projection variation?

4. Baseline and Replication Alignment on Spring XD:
When executing inference using your official Hugging Face checkpoint (MickyMike/0-GPT2SP-springxd) over the 706 chronological test issues of Spring XD (with max_length = 20, padding ID 50257), our evaluation pipeline yields a Mean Absolute Error (MAE) of approximately 1.7330 to 3.3090, alongside a training-set Median Effort Baseline of 1.7153 MAE. Because Table 4 reports a notable MAE of ~0.96 for Spring XD, we suspect we might have missed a specific post-processing step, rounding threshold, or environment library dependency. Any advice on the exact evaluation harness used to generate the published MAE would be exceptionally helpful.

5. Methodological Insights on Intra-issue Revision History & Temporal Dynamics:
Finally, as our research group is exploring temporal integrity at planning time (specifically examining how issue descriptions in Jira often undergo post-planning revisions such as stack traces and fix notes), we would be fascinated to hear your thoughts on how future LLM-based estimation architectures might best account for intra-issue revision history when deployed in live industry Scrum environments.

We understand that you both have very demanding schedules, and we truly appreciate any insights, guidance, or updated pointers you might be able to share. We are more than happy to share our detailed replication code, environment configuration, and empirical logs if that would be helpful.

Thank you very much once again for your inspiring contributions to the software engineering community.

Warmest regards,

[Have a nice day! Wishing you a wonderful & inspiring day ahead!]

--
Le Thanh Hieu (Student ID: 24520496)
Undergraduate Student Researcher & Co-Investigator
Co-Author: Phan Ngoc Duc Huy (Student ID: 24520695)
Faculty of Information Systems, University of Information Technology, VNU-HCM
Project Repository: https://github.com/snowflake-vibing/NCKH_Johnny_Snowflake
GitHub Profile: https://github.com/snowflake-vibing
LinkedIn Profile: https://www.linkedin.com/in/th%C3%A0nh-hi%E1%BB%87u-84b99634b/
Ho Chi Minh City, Vietnam
```

---

## 🛠️ HƯỚNG DẪN CÁCH COPY & PASTE LÊN GMAIL CHUẨN ĐẸP 100%

Dưới đây là các bước thao tác cực kỳ đơn giản để bạn đưa toàn bộ bức thư này lên **Gmail** mà giữ nguyên vẹn 100% màu sắc, thẻ card, font chữ, GIF động và logo:

### 📌 Bước 1: Mở chế độ xem trước (Preview)
1. Trong Visual Studio Code (hoặc trên giao diện web GitHub):
   - Mở file này (`01_inquiry_letter_to_gpt2sp_authors.md`).
   - Nhấn tổ hợp phím **`Ctrl + Shift + V`** (hoặc bấm vào biểu tượng **Kính lúp / Preview** ở góc trên bên phải màn hình VS Code) để mở bản xem trước Markdown đã render giao diện đẹp mắt.

### 📌 Bước 2: Bôi đen và Copy toàn bộ vùng BẢN 1
1. Tại tab Preview, dùng chuột đặt con trỏ bắt đầu từ dòng chữ:  
   `ACADEMIC RESEARCH CORRESPONDENCE` (ngay đầu khung thư).
2. Kéo chuột bôi đen xuống đến hết **thẻ chữ ký Footer** (chỗ có logo UIT và icon GitHub/LinkedIn).
3. Nhấn **`Ctrl + C`** để copy.

### 📌 Bước 3: Dán (Paste) vào Gmail
1. Mở trình duyệt web $\rightarrow$ Đăng nhập vào [Gmail](https://mail.google.com).
2. Bấm nút **`Soạn thư` (Compose)** ở góc trên bên trái.
3. Nhấp chuột vào khung soạn nội dung thư $\rightarrow$ Nhấn **`Ctrl + V`**.
4. ✨ **Kết quả:** Toàn bộ bức thư với khung viền bo tròn, các ô câu hỏi viền xanh, khối mã code nền tối, ảnh GIF "Have a nice day" và Thẻ chữ ký 3 cột có logo UIT sẽ hiện ra nguyên vẹn, cực kỳ chuyên nghiệp!

### 📌 Bước 4: Điền thông tin Người nhận & Tiêu đề
* **Đến (To):** `yeh.fu@monash.edu`
* **Cc:** `chakkrit@monash.edu` *(và email của ThS. Tạ Việt Phương nếu bạn muốn thầy cùng theo dõi tiến trình)*
* **Tiêu đề (Subject):**  
  `Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)`

### 📌 Bước 5: Kiểm tra lần cuối & Bấm Gửi
* Nhìn lại xem ảnh GIF mặt trời đã hiển thị chuyển động nhẹ nhàng chưa.
* Thử bấm vào link GitHub và LinkedIn ở chân trang xem đã nhảy đúng trang cá nhân của Hiệu chưa.
* Bấm **Gửi (Send)** vào khung giờ vàng (khoảng **04:30 – 05:30 sáng giờ Việt Nam**, tương đương **08:30 – 09:30 sáng giờ Melbourne**) để thư đến đầu tiên khi 2 tác giả vừa mở máy làm việc!
