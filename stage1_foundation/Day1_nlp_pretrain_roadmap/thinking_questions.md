# 1. 什么是预训练？预训练和微调的区别？

预训练（Pretraining）指的是：

模型先在海量无标注文本上学习通用语言规律，
例如：

```text
预测下一个词
```

或者：

```text
完形填空
```

从而获得基础语言能力。

而微调（Finetuning）则是：

在具体下游任务数据上继续训练模型，
让模型适应特定任务。

例如：

- 文本分类
- 情感分析
- QA
- NER

简单来说：

```text
预训练 = 学通用语言知识
微调 = 学具体任务
```

---

# 2. GPT 和 BERT 的预训练目标有什么差异？

GPT 使用的是：

```text
自回归语言模型（Autoregressive LM）
```

即：

```text
根据前文预测下一个 token
```

因此：

GPT 是单向语言模型，
更擅长：

```text
文本生成
```

---

而 BERT 使用的是：

```text
Masked Language Model（MLM）
```

即：

随机遮盖部分单词，
再利用上下文预测被遮盖的词。

因此：

BERT 能同时利用前后文信息，
属于双向语言模型，
更擅长：

```text
语言理解
```
# 3.随便选一个类 Transformer 模型，讲讲它的以下内容：Attention、(Gated) FFN、LayerNorm、Position Embedding、Tokenizer、训练目标。
该问题还是有难度，说明我对transformer架构的了解还是比较浅显，明天继续学习。

# 4.为什么现在大语言模型主流是decoder-only causal LM？

我认为还是目标导向，现代LLM最重要的能力已经变成了“生成”。比如聊天、写代码、推理，本质上都是“根据前面内容继续往后写”。而 Decoder-only 的 Transformer 天然就是按这种方式训练的，也就是只能看前文、预测下一个 token，所以它和真实生成过程完全一致。相比之下，BERT 这种 Encoder 模型虽然更擅长“理解”，但它训练时能同时看到前后文，不太适合连续生成长文本，因此后来 GPT-style 的 Decoder-only 架构逐渐成为主流。

# 5.Chat model 和base model 有什么区别？为什么预训练之后还需要后训练？

Base Model 可以理解成：

```text
“只学会语言规律的大模型”
```

它经过预训练后，
已经具备：

- 语言能力
- 知识记忆
- 文本生成能力

但它本质上只是：

```text
“下一个 token 预测器”
```

并不知道：

```text
怎么和人聊天。
```

---

而 Chat Model 则是在 Base Model 基础上，
经过：

- Instruction Tuning
- RLHF
- 对话数据训练

等后训练（Post-training）后得到的模型。

它学会了：

- 按指令回答
- 多轮对话
- 更自然交流
- 拒绝危险内容

因此：

```text
Base Model 更像“原始大脑”
Chat Model 更像“AI 助手”
```

---

之所以预训练后还需要后训练，

是因为：

```text
预训练只是在学习“语言”
```

但没有教模型：

- 怎么回答问题
- 什么回答更符合人类偏好
- 什么内容不该输出

所以后训练本质上是在做：

```text
人类对齐（Alignment）
```

也就是：

```text
让模型不仅会说话，
还会“好好说话”。
```