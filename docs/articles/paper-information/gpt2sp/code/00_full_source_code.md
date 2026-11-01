# 📦 TOÀN BỘ MÃ NGUỒN GỐC CỦA MÔ HÌNH GPT2SP (FULL REPLICATION SOURCE CODE)

> **Tài liệu nguồn:** Repository chính thức [`awsm-research/gpt2sp`](https://github.com/awsm-research/gpt2sp) (Đại học Monash, Úc).  
> **Bài báo khoa học:** *GPT2SP: A Transformer-Based Agile Story Point Estimation Approach* (Fu & Tantithamthavorn, IEEE Transactions on Software Engineering 2023).  
> **Mục tiêu tài liệu:** Lưu trữ nguyên vẹn, đầy đủ 100% mã nguồn gốc cấu thành hệ thống GPT2SP (từ file kiến trúc mạng PyTorch `GPT2SP.py` đến toàn bộ Jupyter Notebook huấn luyện `model_training_notebook.ipynb`), làm cơ sở dữ liệu nền tảng cho việc đối soát lý thuyết và thực nghiệm.

---

## 🧭 CẤU TRÚC BỘ MÃ NGUỒN CỐT LÕI

Mã nguồn thực thi chính của GPT2SP gồm hai thành phần nền tảng:
1. **`GPT2SP.py`**: Module định nghĩa lớp mô hình mạng nơ-ron kế thừa `GPT2PreTrainedModel`, tích hợp khối MLP Regressor Head và cơ chế Last Token Pooling.
2. **`model_training_notebook.ipynb`**: Kịch bản nạp dữ liệu, tiền xử lý, cấu hình siêu tham số, phân chia tập dữ liệu và vòng lặp huấn luyện / đánh giá cho 3 kịch bản nghiên cứu (RQ1 Within-Project, RQ2 Cross-Project Within-Repository, và RQ2 Cross-Project Cross-Repository).

---

## 1. FILE 1: KIẾN TRÚC MÔ HÌNH NƠ-RON (`GPT2SP.py`)

*Dưới đây là nguyên văn 100% mã nguồn file `GPT2SP.py` trích xuất trực tiếp từ repository chính thức của tác giả:*

```python
from transformers.modeling_outputs import SequenceClassifierOutputWithPast
import torch.nn as nn
from transformers import GPT2Model, GPT2PreTrainedModel
import torch


class GPT2ForSequenceClassification(GPT2PreTrainedModel):
    _keys_to_ignore_on_load_missing = [r"h\.\d+\.attn\.masked_bias", r"lm_head\.weight"]

    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.transformer = GPT2Model(config)
        self.dense1 = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
        self.dense2 = nn.Linear(4 * config.n_embd, config.n_embd, bias=False)
        self.score = nn.Linear(config.n_embd, self.num_labels, bias=False)

        self.init_weights()

        # Model parallel
        self.model_parallel = False
        self.device_map = None


    def forward(
        self,
        input_ids=None,
        past_key_values=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        labels (:obj:`torch.LongTensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for computing the sequence classification/regression loss. Indices should be in :obj:`[0, ...,
            config.num_labels - 1]`. If :obj:`config.num_labels == 1` a regression loss is computed (Mean-Square loss),
            If :obj:`config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        transformer_outputs = self.transformer(
            input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        hidden_states = transformer_outputs[0]
                
        # MLP Layer
        hidden_states = self.dense1(hidden_states)
        hidden_states = self.dense2(hidden_states)
        
        logits = self.score(hidden_states)

        if input_ids is not None:
            batch_size, sequence_length = input_ids.shape[:2]
        else:
            batch_size, sequence_length = inputs_embeds.shape[:2]

        assert (
            self.config.pad_token_id is not None or batch_size == 1
        ), "Cannot handle batch sizes > 1 if no padding token is defined."
        if self.config.pad_token_id is None:
            sequence_lengths = -1
        else:
            if input_ids is not None:
                sequence_lengths = torch.ne(input_ids, self.config.pad_token_id).sum(-1) - 1
            else:
                sequence_lengths = -1
                logger.warning(
                    f"{self.__class__.__name__} will not detect padding tokens in `inputs_embeds`. Results may be "
                    f"unexpected if using padding tokens in conjunction with `inputs_embeds.`"
                )

        pooled_logits = logits[range(batch_size), sequence_lengths]

        loss = None
        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = nn.L1Loss()
                loss = loss_fct(pooled_logits.view(-1), labels.to(self.dtype).view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(pooled_logits.view(-1, self.num_labels), labels.view(-1))

        if not return_dict:
            output = (pooled_logits,) + transformer_outputs[1:]
            return ((loss,) + output) if loss is not None else output

        return SequenceClassifierOutputWithPast(
            loss=loss,
            logits=pooled_logits,
            past_key_values=transformer_outputs.past_key_values,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
```

---

## 2. FILE 2: KỊCH BẢN HUẤN LUYỆN VÀ ĐÁNH GIÁ THỰC NGHIỆM (`model_training_notebook.ipynb`)

*Dưới đây là toàn bộ các khối mã nguồn (code cells) được trích xuất nguyên bản từ `model_training_notebook.ipynb`:*

### Khối 1: Khai báo thư viện (Dependencies & Imports)
```python
import torch
import pandas as pd
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import GPT2Tokenizer, AdamW, get_linear_schedule_with_warmup
import numpy as np
import time
from torch.utils.tensorboard import SummaryWriter
from GPT2SP import GPT2ForSequenceClassification as GPT2SP
from transformers import GPT2ForSequenceClassification as LinearGPT2
from transformers import GPT2Config
import os
from tokenizers import Tokenizer
import torch.nn as nn
```

---

### Khối 2: Thiết lập Siêu tham số Toàn cục (Global Hyperparameters)
```python
global EPOCHS, BATCH_SIZE_RATIO, SEQUENCE_LEN, LEARNING_RATE, TOKENIZER, MODEL_NAME

EPOCHS = 20
BATCH_SIZE_RATIO = 0.3 # within proj: 0.3 / cross proj: 0.4
SEQUENCE_LEN = 20
LEARNING_RATE = 5e-4
TOKENIZER = 'gpt2' # available: gpt2, wordlevel, sentencepiece, wordpiece 
MODEL_NAME = 'gpt2sp' # available: gpt2sp, gpt2

# define device
global DEVICE
DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# define files to be used
global DATA_PATH 
DATA_PATH = './sp_dataset/marked_data/'
```

---

### Khối 3: Các hàm xử lý dữ liệu, phân chia tập và vòng lặp huấn luyện (Static Methods & Functions)
```python
OUTPUT = ''
MODEL = None
DYNAMIC_BATCH = True
BATCH_SIZE = None
WITHIN_PROJECT = None
MAE_RECORDS = []
MDAE_RECORDS = []

def data_processing(file_pair):
    global BATCH_SIZE, BATCH_SIZE_RATIO, DATA_PATH, WITHIN_PROJECT, DYNAMIC_BATCH

    train_data = pd.DataFrame(columns=['text', 'label'])
    for train_file_name in file_pair['train']:
        fname = DATA_PATH + train_file_name + '.csv'
        df = prepare_dataframe(fname)
        train_data = train_data.append(df)
        
    # data split
    if WITHIN_PROJECT:
        train_text, train_labels, val_text, val_labels, test_text, test_labels = within_project_split(train_data)
    else:
        train_text, train_labels, val_text, val_labels = train_val_split(train_data, 0.6)
    # define batch size dynamically based on training length
    if DYNAMIC_BATCH:
        BATCH_SIZE = int(len(train_text) * BATCH_SIZE_RATIO)
    # tokenization
    tokens_train = tokenization(train_text.tolist())
    tokens_val = tokenization(val_text.tolist())
    print(tokens_train['input_ids'][:5])
 
    train_seq = torch.tensor(tokens_train['input_ids'])
    train_y = torch.tensor(train_labels.tolist()).type(torch.LongTensor)
    train_dataloader = prepare_dataloader(train_seq, train_y, sampler_type='random')

    val_seq = torch.tensor(tokens_val['input_ids'])
    val_y = torch.tensor(val_labels.tolist()).type(torch.LongTensor)
    val_dataloader = prepare_dataloader(val_seq, val_y, sampler_type='sequential')
    
    # prepare testing datasets
    all_test_dataloader = []
    test_file_names = []
    if WITHIN_PROJECT:
        tokens_test = tokenization(test_text.tolist())
        test_seq = torch.tensor(tokens_test['input_ids'])
        test_y = torch.tensor(test_labels.tolist()).type(torch.LongTensor)
        test_dataloader = prepare_dataloader(test_seq, test_y, sampler_type='sequential')
        all_test_dataloader.append(test_dataloader)
        test_file_names.append(file_pair['test'][0])
        return file_pair, train_dataloader, val_dataloader, all_test_dataloader, test_file_names

    for test_file_name in file_pair['test']:
        fname = DATA_PATH + test_file_name + '.csv'
        test_data = prepare_dataframe(fname)

        test_text = test_data['text']
        test_labels = test_data['label']

        # tokenization
        tokens_test = tokenization(test_text.tolist())
        test_seq = torch.tensor(tokens_test['input_ids'])
        test_y = torch.tensor(test_labels.tolist()).type(torch.LongTensor)
        test_dataloader = prepare_dataloader(test_seq, test_y, sampler_type='sequential')

        all_test_dataloader.append(test_dataloader)
        test_file_names.append(test_file_name)
    print('cross project data processing!')
    return file_pair, train_dataloader, val_dataloader, all_test_dataloader, test_file_names


def train_val_split(data, split_ratio):
    print('cross project split!')
    split_point = int(len(data) * split_ratio)
    train_text = data['text'][:split_point]
    train_labels = data['label'][:split_point]
    val_text = data['text'][split_point:]
    val_labels = data['label'][split_point:]
    return train_text, train_labels, val_text, val_labels


def tokenization(text_list):
    global TOKENIZER, SEQUENCE_LEN, MODEL
    # tokenization
    if TOKENIZER == 'wordpiece':
        print('using wordpiece tokenizer!')
        tokenizer = BertTokenizer('all_tokenizers/word_piece/vocab.txt')
    elif TOKENIZER == 'sentencepiece':
        print('using sentencepiece tokenizer!')
        tokenizer = XLNetTokenizer('all_tokenizers/sentence_piece/spm_tokenizer.model', padding_side='right')
    elif TOKENIZER == 'wordlevel':
        print('using wordlevel tokenizer!')
        tokenizer = Tokenizer.from_file('all_tokenizers/word_level/wordlevel.json')
        encoded_sentences = {'input_ids':[]}
        for sentence in text_list:
            encoded = tokenizer.encode(sentence)
            encoded = encoded.ids
            if len(encoded) > SEQUENCE_LEN:
                encoded = encoded[:SEQUENCE_LEN]
            elif len(encoded) < SEQUENCE_LEN:
                padding = SEQUENCE_LEN - len(encoded)
                for _ in range(padding):
                    encoded.append(3)
            encoded_sentences['input_ids'].append(encoded)
        return encoded_sentences
    elif TOKENIZER == 'gpt2':
        print('using pretrained gpt-2 tokenizer')
        tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER)
        tokenizer.pad_token = '[PAD]'
        return tokenizer.batch_encode_plus(text_list, truncation=True, max_length=SEQUENCE_LEN, padding='max_length')


def prepare_dataframe(file_name):
    data = pd.read_csv(file_name)
    # some rows have no description, fill blank to avoid Null
    data = data.fillna(' ')
    d = {'text': (data['title']).tolist(), 'label': data['storypoint']}
    return pd.DataFrame(data=d)


def prepare_dataloader(seq, y, sampler_type):
    global BATCH_SIZE
    data = TensorDataset(seq, y)
    if sampler_type == 'random':
        sampler = RandomSampler(data)
    elif sampler_type == 'sequential':
        sampler = SequentialSampler(data)
    return DataLoader(data, sampler=sampler, batch_size=BATCH_SIZE)


def within_project_split(data):
    print('within project split!')
    train_val_split_point = int(len(data) * 0.6)
    val_test_split_point = int(len(data) * 0.8)
    train_text = data['text'][:train_val_split_point]
    train_labels = data['label'][:train_val_split_point]
    val_text = data['text'][train_val_split_point:val_test_split_point]
    val_labels = data['label'][train_val_split_point:val_test_split_point]
    test_text = data['text'][val_test_split_point:]
    test_labels = data['label'][val_test_split_point:]
    return train_text, train_labels, val_text, val_labels, test_text, test_labels   


def train_eval_test(file_pair, train_dataloader, val_dataloader, all_test_dataloader, model, test_file_names):
    global LEARNING_RATE, EPOCHS, MAE_RECORDS, MDAE_RECORDS, DEVICE
    optimizer = AdamW(MODEL.parameters(), lr=LEARNING_RATE)    
    # Total number of training steps is [number of batches] x [number of epochs]
    total_steps = len(train_dataloader) * EPOCHS
    # Create the learning rate scheduler
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
    print("Start training for ", file_pair, ".....")
    training_start_time = time.time()
    
    # tensorboard writer
    writer_path = 'tb/' + str(file_pair['train'][0]) + '_' + str(file_pair['test'][0])
    writer = SummaryWriter(writer_path)
    
    # vars for model selection
    min_eval_loss_epoch = [10000, 0]
    
    time_records = []
    MAE_RECORDS = []
    MDAE_RECORDS = []
    start_time = time.time()
    loss_fct = nn.L1Loss()
    for e in range(EPOCHS):
        # ---TRAINING---
        # clean GPU memory
        torch.cuda.empty_cache()
        print(">>> epoch ", e)
        # set model into train mode
        model.train()
        total_train_loss = 0
        for step, batch in enumerate(train_dataloader):
            # unpack batch
            b_input_ids = batch[0].to(DEVICE)
            b_labels = batch[1].to(DEVICE)
            # clear previously calculated gradients 
            model.zero_grad()        
            result = model(b_input_ids, 
                           labels=b_labels, 
                           return_dict=True)
            loss = result.loss
            logits = result.logits
            total_train_loss += loss.item()  
            loss.backward() 
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            # clean memory
            del step, batch, b_input_ids, b_labels, result, loss, logits

        avg_train_loss = total_train_loss / len(train_dataloader)
        print(" Average training MAE loss: {0:.2f}".format(avg_train_loss))
        writer.add_scalar('loss/train', avg_train_loss, e)
        # clean memory
        del avg_train_loss, total_train_loss
        
        time_records.append(time.time() - start_time)
        
        # ---EVAL---
        print("-")
        # set model into eval mode
        model.eval()
        total_eval_loss = 0
        for batch in val_dataloader:            
            b_input_ids = batch[0].to(DEVICE)
            b_labels = batch[1].to(DEVICE)
            model.zero_grad()
            result = model(b_input_ids, 
                           labels=b_labels, 
                           return_dict=True)
            loss = result.loss
            logits = result.logits
            total_eval_loss += loss.item()  
            # clean memory
            del b_input_ids, b_labels, batch, result, loss, logits
        avg_eval_loss = total_eval_loss / len(val_dataloader)
        print(" Average eval MAE loss: {0:.2f}".format(avg_eval_loss))
        
        if avg_eval_loss <= min_eval_loss_epoch[0]:
            min_eval_loss_epoch[0] = avg_eval_loss
            min_eval_loss_epoch[1] = e
        
        writer.add_scalar('loss/eval', avg_eval_loss, e)
        # clean memory
        del avg_eval_loss, total_eval_loss
        # save model state to dict
        torch.save(model.state_dict(), './models/' + 'epo_' + str(e))
        
        print("===============================")
        
        # testing on holdout data
        index = 0
        for test_dataloader in all_test_dataloader:
            test_file_name = test_file_names[index]
            index += 1
            testing_start_time = time.time()
            predictions = []
            true_labels = []
            for batch in test_dataloader:
                batch = tuple(t.to(DEVICE) for t in batch)
                b_input_ids, b_labels = batch
                with torch.no_grad():
                    logits = model(b_input_ids)
                logits = logits['logits'].detach().cpu().numpy()
                label_ids = b_labels.to('cpu').numpy()
                predictions.append(logits)
                true_labels.append(label_ids)
            # calculate errors
            distance_records = []
            for i in range(len(predictions)):
                for j in range(len(predictions[i])):
                    distance = abs(predictions[i][j] - true_labels[i][j])
                    distance_records.append(distance)

            ## MAE = mean value of all absolute errors (stored in distance_records)
            MAE = np.mean(np.array(distance_records)) 
            ## MdAE = median value of all absolute errors (stored in distance_records)
            MdAE = np.median(np.array(distance_records)) 

            MAE_RECORDS.append(MAE)
            MDAE_RECORDS.append(MdAE)
            
            global OUTPUT
            OUTPUT +=  'Epochs ' + str(e) + '\n'
            OUTPUT += 'MAE: ' + str(MAE) + '\n'
            OUTPUT += 'MdAE: ' + str(MdAE) + '\n\n'
            print('MAE: ', MAE)
            print('MdAE: ', MdAE)
    writer.flush()
    writer.close()
    
    # select model
    os.rename('models/epo_' + str(min_eval_loss_epoch[1]), 
              'models/' + str(file_pair['train'][0]) + '_' 
              + str(file_pair['test'][0]) + '_epo_' + str(min_eval_loss_epoch[1]))
    
    # del unwanted models
    for i in range(20):
        try:
            os.remove("models/epo_" + str(i))
        except:
            continue
            
    OUTPUT += 'MAE: ' + str(MAE_RECORDS[min_eval_loss_epoch[1]]) \
                + '  MdAE: ' + str(MDAE_RECORDS[min_eval_loss_epoch[1]]) + '\n'
    OUTPUT += 'training time: ' + str(time_records[min_eval_loss_epoch[1]]) + '\n'
    OUTPUT += 'Epochs: ' + str(min_eval_loss_epoch[1]) +'\n'
    global BATCH_SIZE
    OUTPUT += 'batch size: ' + str(BATCH_SIZE)
    print('all done for one project')
```

---

### Khối 4: Thực thi Huấn luyện Kịch bản RQ1 (Within-Project Training)
```python
global WITHIN_PROJECT
WITHIN_PROJECT = True

TRAIN_TEST_FILE_PAIRS = [
    {'train': ['appceleratorstudio'], 'test': ['appceleratorstudio']},
    {'train': ['aptanastudio'], 'test': ['aptanastudio']},
    {'train': ['bamboo'], 'test': ['bamboo']},
    {'train': ['clover'], 'test': ['clover']},
    {'train': ['datamanagement'], 'test': ['datamanagement']},
    {'train': ['duracloud'], 'test': ['duracloud']},
    {'train': ['jirasoftware'], 'test': ['jirasoftware']},
    {'train': ['mesos'], 'test': ['mesos']},
    {'train': ['moodle'], 'test': ['moodle']},
    {'train': ['mule'], 'test': ['mule']},
    {'train': ['mulestudio'], 'test': ['mulestudio']},
    {'train': ['springxd'], 'test': ['springxd']},
    {'train': ['talenddataquality'], 'test': ['talenddataquality']},
    {'train': ['talendesb'], 'test': ['talendesb']},
    {'train': ['titanium'], 'test': ['titanium']},
    {'train': ['usergrid'], 'test': ['usergrid']}
]

for file_pair in TRAIN_TEST_FILE_PAIRS:
    file_pair, train_dataloader, val_dataloader, all_test_dataloader, test_file_names = data_processing(file_pair)
    
    # init model
    config = GPT2Config.from_pretrained(
        'gpt2',
        num_labels=1,
        pad_token_id=50257
    )
    if MODEL_NAME == 'gpt2sp':
        MODEL = GPT2SP.from_pretrained('gpt2', config=config)
    elif MODEL_NAME == 'gpt2':
        MODEL = LinearGPT2.from_pretrained('gpt2', config=config)
    
    MODEL.to(DEVICE)
    train_eval_test(file_pair, train_dataloader, val_dataloader, all_test_dataloader, MODEL, test_file_names)
```

---

### Khối 5: Thực thi Huấn luyện Kịch bản RQ2 (Cross-Project - Within Repository)
```python
global WITHIN_PROJECT
WITHIN_PROJECT = False

# within repo pairs
TRAIN_TEST_FILE_PAIRS = [
    {'train': ['mesos'], 'test': ['usergrid']},
    {'train': ['usergrid'], 'test': ['mesos']},
    {'train': ['appceleratorstudio'], 'test': ['aptanastudio']},
    {'train': ['appceleratorstudio'], 'test': ['titanium']},
    {'train': ['titanium'], 'test': ['appceleratorstudio']},
    {'train': ['aptanastudio'], 'test': ['titanium']},
    {'train': ['mule'], 'test': ['mulestudio']},
    {'train': ['mulestudio'], 'test': ['mule']}
]

for file_pair in TRAIN_TEST_FILE_PAIRS:
    file_pair, train_dataloader, val_dataloader, all_test_dataloader, test_file_names = data_processing(file_pair)
    config = GPT2Config.from_pretrained('gpt2', num_labels=1, pad_token_id=50257)
    MODEL = GPT2SP.from_pretrained('gpt2', config=config)
    MODEL.to(DEVICE)
    train_eval_test(file_pair, train_dataloader, val_dataloader, all_test_dataloader, MODEL, test_file_names)
```

---

### Khối 6: Thực thi Huấn luyện Kịch bản RQ2 (Cross-Project - Cross Repository)
```python
global WITHIN_PROJECT
WITHIN_PROJECT = False

# cross repo pairs
TRAIN_TEST_FILE_PAIRS = [
    {'train': ['clover'], 'test': ['usergrid']},
    {'train': ['talendesb'], 'test': ['mesos']},
    {'train': ['talenddataquality'], 'test': ['aptanastudio']},
    {'train': ['mule'], 'test': ['titanium']},
    {'train': ['talenddataquality'], 'test': ['appceleratorstudio']},
    {'train': ['mulestudio'], 'test': ['titanium']},
    {'train': ['appceleratorstudio'], 'test': ['mule']},
    {'train': ['appceleratorstudio'], 'test': ['mulestudio']}
]

for file_pair in TRAIN_TEST_FILE_PAIRS:
    file_pair, train_dataloader, val_dataloader, all_test_dataloader, test_file_names = data_processing(file_pair)
    config = GPT2Config.from_pretrained('gpt2', num_labels=1, pad_token_id=50257)
    MODEL = GPT2SP.from_pretrained('gpt2', config=config)
    MODEL.to(DEVICE)
    train_eval_test(file_pair, train_dataloader, val_dataloader, all_test_dataloader, MODEL, test_file_names)
```

---

## 🔗 Liên Kết Điều Hướng Trong Thư Mục Code

* 📖 [01_architecture_code_explanation.md](01_architecture_code_explanation.md): Giải thích chi tiết mã nguồn kiến trúc mô hình `GPT2SP.py` tương ứng với Chương 3 trong bài báo.
* 📖 [02_training_pipeline_code_explanation.md](02_training_pipeline_code_explanation.md): Giải thích chi tiết mã nguồn pipeline nạp dữ liệu và huấn luyện trong `model_training_notebook.ipynb`.
* 📖 [03_code_vs_paper_discrepancies.md](03_code_vs_paper_discrepancies.md): Mổ xẻ 4 điểm sai lệch cốt tử giữa mã nguồn thực tế và nội dung công bố trong bài báo IEEE TSE 2023.
