# 1.Pretraining

Pretraining（预训练）指的是先让模型在大规模通用数据上进行训练，提前学习语言知识和特征表示能力。

例如：
- GPT 的大规模文本训练
- BERT 的 Masked Language Model

# 2.Frozen

Frozen（冻结参数）指的是在下游任务训练时，加载预训练参数后保持不变，只训练新增任务层。

优点：
- 训练快
- 显存占用小

缺点：
- 模型适应能力有限

# 3.Fine-Tuning

Fine-Tuning（微调）指的是在下游任务训练时，继续更新预训练参数，让模型逐渐适应当前任务。

优点：
- 性能更强
- 更适合具体任务

缺点：
- 训练成本更高
- 小数据集容易过拟合

# 4.NNLM（Neural Network Language Model）

NNLM（神经网络语言模型）是一种使用神经网络实现的语言模型。

它的核心思路是：

先将前面的单词进行 One-hot 编码，
再映射成 Word Embedding（词向量），
随后输入神经网络，
预测下一个最可能出现的单词。

例如：

```text
I love deep learning
```

模型可能预测：

```text
because / very / and ...
```

NNLM 的重要意义在于：

它不仅能够完成语言模型任务，
还在训练过程中学习到了 Word Embedding，
为后来的 word2vec、GPT、BERT 等模型奠定了基础。

# 5.Word2Vec 

Word2Vec 是一种通过语言模型学习 Word Embedding（词向量）的方法。

它的核心目标是：

让语义相近的单词，
在向量空间中的距离更接近。

Word2Vec 主要有两种训练方式：

- CBOW：根据上下文预测目标单词
- Skip-gram：根据目标单词预测上下文

相比 NNLM：

NNLM 的主要目标是完成语言模型任务，
而 Word2Vec 更关注学习高质量的词向量表示。

Word2Vec 的重要意义在于：

它让机器第一次能够用向量表示单词语义，
为后来的 ELMo、GPT、BERT 等预训练模型奠定了基础。

---

## Word2Vec 的局限性

Word2Vec 属于静态词向量（Static Embedding）。

即：

同一个单词始终只有一个固定向量。

因此它无法解决多义词问题。

例如：

```text
bank
```

既可以表示：

- 银行
- 河岸

但 Word2Vec 无法根据上下文区分不同含义。

# 6.CBOW 与 Skip-gram

Word2Vec 主要有两种训练方式：

## CBOW（Continuous Bag of Words）

CBOW 的核心思想是：

利用一个单词的上下文，
去预测被遮掉的目标单词。

例如：

```text
I love ___ learning
```

模型根据：

```text
I / love / learning
```

预测：

```text
deep
```

---

## Skip-gram

Skip-gram 与 CBOW 相反。

它的核心思想是：

输入当前单词，
预测它周围的上下文单词。

例如：

输入：

```text
deep
```

预测：

```text
I / love / learning
```

CBOW 更像：

```text
上下文 → 单词
```

Skip-gram 更像：

```text
单词 → 上下文
```

# 7.ELMo

ELMo（Embedding from Language Models）是一种基于上下文的动态词向量模型。

相比 Word2Vec 的静态词向量：

```text
一个单词永远只有一个固定向量
```

ELMo 的核心思想是：

```text
同一个单词在不同上下文中，
应该具有不同的表示。
```

例如：

```text
bank
```

在不同句子中可以表示：

- 银行
- 河岸

ELMo 会根据上下文动态调整词向量，
从而解决多义词问题。

---

## ELMo 的核心结构

ELMo 使用：

- 双向 LSTM（BiLSTM）
- 两阶段预训练模式

首先通过语言模型进行预训练，
再将得到的 contextual embedding 用于下游任务。

它不仅学习到了：

- Word Embedding
- 还学习到了上下文语义信息

因此 ELMo 属于：

```text
Contextualized Embedding
```

---

## ELMo 的重要意义

ELMo 首次让 NLP 从：

```text
Static Embedding
```

进入：

```text
Contextual Embedding
```

时代。

它证明了：

```text
上下文信息对语言理解非常重要。
```

并为后来的：

- GPT
- BERT
- 现代 LLM

奠定了基础。

---

## ELMo 的局限性

ELMo 虽然解决了多义词问题，
但它仍然使用：

```text
LSTM
```

作为特征提取器。

后来 Transformer 的效果明显更强，
因此后续模型逐渐转向 Transformer 架构。

# 8.GPT

GPT（Generative Pre-Training）是一种基于 Transformer 的生成式预训练模型。

相比 ELMo：

GPT 不再使用 LSTM，
而是使用更强的：

```text
Transformer
```

作为特征提取器。

GPT 的核心训练方式是：

```text
根据前面的单词，
预测下一个单词。
```

例如：

```text
I love deep learning because ...
```

模型预测后续单词。

这种方式被称为：

```text
Autoregressive Language Modeling
（自回归语言模型）
```

---

## GPT 的重要意义

GPT 首次提出了：

```text
Pretrain + Fine-Tuning
```

范式。

即：

1. 先在海量文本上进行预训练
2. 再针对下游任务进行 Fine-Tuning

这个思想后来成为现代大模型的核心训练流程。

---

## GPT 的特点

- 使用 Transformer
- 生成能力强
- 擅长文本生成
- 可以迁移到多种 NLP 任务

但它也存在一个问题：

```text
只能看到左侧上下文
```

属于：

```text
单向语言模型（Unidirectional LM）
```

因此对上下文理解能力有限，
这也是后来 BERT 改进的重要方向。

# 9.NLP 的四大任务

大部分 NLP（自然语言处理）任务，
都可以归为以下四类：

---

## 9.1 序列标注（Sequence Labeling）

核心特点：

```text
给句子中的每个单词分别打标签
```

例如：

- 中文分词
- 词性标注（POS）
- 命名实体识别（NER）
- 语义角色标注

例子：

```text
Tom lives in Beijing
```

模型需要判断：

```text
Tom → 人名
Beijing → 地名
```

---

## 9.2 分类任务（Classification）

核心特点：

```text
对整段文本输出一个整体类别
```

例如：

- 文本分类
- 情感分析
- 垃圾邮件检测

例子：

```text
This movie is amazing!
```

模型输出：

```text
Positive
```

---

## 9.3 句子关系判断（Sentence Relationship）

核心特点：

```text
输入两个句子，
判断它们之间的关系
```

例如：

- 问答（QA）
- 自然语言推理（NLI）
- 文本相似度
- Entailment

例子：

```text
A: Tom is a student.
B: Tom goes to school.
```

模型判断：

```text
语义相关
```

---

## 9.4 生成式任务（Generation）

核心特点：

```text
输入文本，
生成新的文本
```

例如：

- 机器翻译
- 文本摘要
- 对话系统
- 写诗
- ChatGPT

例子：

```text
输入：Hello
输出：Hi, how are you?
```

# 10.BERT

BERT 是 Google 提出的一个双向预训练语言模型。

相比 GPT 只能看左边上下文：

```text
I love deep ...
```

BERT 可以同时看到：

- 左边内容
- 右边内容

因此它更擅长：

```text
语言理解
```

BERT 的核心训练方式叫：

```text
Masked Language Model（MLM）
```

也就是随机遮住一句话里的某个词：

```text
I love [MASK] learning
```

然后让模型根据上下文猜这个词。

BERT 使用：

```text
Transformer + 双向上下文
```

因此它在：

- 文本分类
- NER
- QA
- 自然语言推理

等任务上效果非常强。

简单来说：

```text
Word2Vec 解决词向量
ELMo 引入上下文
GPT 引入 Transformer
BERT 则把这些结合起来，
做成了强大的双向预训练模型。
```
# 11.GPT-style LLM

GPT-style LLM 指的是：

基于 GPT 路线发展出来的大语言模型。

它们通常采用：

```text
Transformer Decoder-only
```

架构。

其中：

```text
Transformer
```

是一种基于 Attention 的深度网络结构，
非常擅长处理长距离文本关系。

而：

```text
Decoder-only
```

表示模型只使用 Transformer 的 Decoder 部分，
并按照：

```text
从左到右
```

的方式读取文本。

也就是说：

模型只能看到前面的内容，
然后预测下一个 token。

例如：

```text
I love deep learning because ...
```

模型会根据前文，
不断生成后续内容。

例如：

- GPT-4
- Llama
- Qwen
- DeepSeek
- Claude

都属于 GPT-style LLM。

相比早期 GPT：

现代 GPT-style LLM 不仅规模更大，
还加入了：

- Instruction Tuning
- RLHF
- 长上下文
- Agent
- Tool Use

等后训练技术。

因此：

它们已经不仅是“语言模型”，
而是能够：

```text
对话、写作、推理、代码生成、工具调用
```

的通用 AI 助手。

# 12.什么是 RLHF？

RLHF（Reinforcement Learning from Human Feedback）  
即：

```text
基于人类反馈的强化学习
```

它的核心思想是：

先让人类对模型回答进行打分，
再利用强化学习不断优化模型，
让模型更倾向于输出：

```text
更自然、更安全、更符合人类偏好的回答。
```

因此：

RLHF 本质上是在做：

```text
人类对齐（Alignment）
```

也就是：

```text
让模型不仅会回答，
还会“好好回答”。
```