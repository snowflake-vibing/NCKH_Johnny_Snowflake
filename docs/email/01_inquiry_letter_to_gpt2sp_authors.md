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

### 📨 EMAIL DRAFT (READY TO SEND)

**Subject:** Inquiry regarding replication details and evaluation setup for GPT2SP (IEEE TSE 2023)

**Dear Michael and Dr. Tantithamthavorn,**

I hope this email finds you well and having a productive semester.

My name is [Your Name], and I am an undergraduate researcher working with the Software Engineering and Data Science Research Group at [Your University / Institution]. We have been reading your seminal paper, *"GPT2SP: A Transformer-Based Agile Story Point Estimation Approach"* (IEEE Transactions on Software Engineering, 2023), with great admiration. Your work is widely regarded in our research lab as a groundbreaking milestone that pioneered the transition of Agile effort estimation from recurrent architectures to modern pre-trained Transformer language models.

As part of our ongoing research project investigating deep learning and temporal aspects of Agile software estimation, we are currently replicating your experimental workflow on open-source Jira datasets—particularly the **Spring XD** benchmark—using both your open-source GitHub replication package (`awsm-research/gpt2sp`) and the pre-trained checkpoints released on Hugging Face (`MickyMike/0-GPT2SP-springxd`).

While replicating the empirical pipeline, we encountered a few technical nuances where we would be immensely grateful for your kind clarification:

---

#### 1. Input Text Representation (`Title` vs. `Title + Description`):
In Section 3.1 (*Context Extraction*, page 3) and Section 4.1 (*Experimental Setup*, page 7) of your TSE manuscript, the formulation describes utilizing both the issue Title and Description to preserve contextual software semantics. However, in the companion replication notebook (`model_training_notebook.ipynb`, cell `prepare_dataframe`):
```python
d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
```
we observed that only the `title` attribute is mapped into the training dataframe. Could you kindly clarify whether the results published in Table 4 were obtained using solely the `title` field, or whether there is an updated preprocessing script that concatenates `title` and `description` as described in the text?

#### 2. Sequence Length Truncation Parameter (`SEQUENCE_LEN = 20`):
In `model_training_notebook.ipynb`, the sequence truncation boundary is configured as:
```python
SEQUENCE_LEN = 20
```
Given that base GPT-2 supports contextual windows up to 1,024 tokens, we would love to know if the 20-token limit was a specific hyperparameter optimization chosen for runtime efficiency across the 16 projects, or if experiments with longer contextual bounds (e.g., 128 or 512 tokens) were evaluated in your broader empirical suite.

#### 3. MLP Regressor Head Architecture and Non-Linear Activation:
Section 3.3 (*Story Point Regression*, page 4) outlines a multi-layer perceptron (MLP) regressor head incorporating a GELU non-linear activation function. When inspecting `GPT2SP.py`:
```python
hidden_states = self.dense1(hidden_states)
hidden_states = self.dense2(hidden_states)
logits = self.score(hidden_states)
```
the tensor passes sequentially through `dense1` and `dense2` without an explicit functional call to `gelu()`. We were wondering if the non-linearity was intended to be injected via a custom configuration hook, or if this represents an optimized linear projection variation in the released code.

#### 4. Baseline and Replication Alignment on Spring XD:
When executing inference using your official Hugging Face checkpoint (`MickyMike/0-GPT2SP-springxd`) over the 706 chronological test issues of Spring XD (with `max_length = 20`, padding ID `50257`), our evaluation pipeline yields a Mean Absolute Error (MAE) of approximately **1.7330**, alongside a training-set Median Effort Baseline of **1.7153** MAE. Because Table 4 reports a notable MAE of **~0.96** for Spring XD, we suspect we might have missed a specific post-processing step, rounding threshold, or environment library dependency (e.g., specific PyTorch/Transformers version). Any advice on the exact evaluation harness used to generate the published MAE would be exceptionally helpful.

#### 5. Broader Methodological Insights on Temporal Agile Dynamics:
Finally, as our research group is exploring temporal integrity at planning time (specifically examining how issue descriptions in Jira often undergo post-planning revisions such as stack traces and fix notes), we would be fascinated to hear your thoughts on how future LLM-based estimation architectures might best account for intra-issue revision history when deployed in live industry Scrum environments.

---

We understand that you both have very demanding schedules, and we truly appreciate any insights, guidance, or updated pointers you might be able to share. We are more than happy to share our detailed replication code, environment configuration, and empirical logs if that would be helpful.

Thank you very much once again for your inspiring contributions to the software engineering community.

Warmest regards,

**[Your Full Name]**  
Undergraduate Researcher / Research Assistant  
Department of Software Engineering  
[University / Institution Name]  
Email: `[your.email@university.edu]`  
GitHub / Website: `[your-github-link]`  

*(Co-signed by Research Advisor / Group Lead, if applicable)*  
**[Advisor's Name, Academic Title]**  
[Lab / Research Group Name]  
[University / Institution Name]
