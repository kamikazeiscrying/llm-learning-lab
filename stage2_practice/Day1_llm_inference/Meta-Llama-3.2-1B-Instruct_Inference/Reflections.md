# Day1 推理实验 Reflections

模型： **Meta-Llama-3.2-1B-Instruct**

---
## Prompt 设计

这次的 prompt 不是一开始就特别开放，而是做了一个“从标准问题逐渐走向开放问题”的设计。

前面的问题更偏事实性，比如：

```python
"“我们必须想象西西弗斯是幸福的”出自哪个作者的哪本书？"
```

这种问题有相对固定的答案，更适合观察模型的稳定性和准确性。

后面的问题就开始越来越开放，比如：

```python
"如何理解“我们必须想象西西弗斯是幸福的”？"
```

以及：

```python
"如果西西弗斯生活在现代社会，他会过着怎样的生活？"
```

## 参数设置

这次主要调整了：

- `temperature`
- `top_p`
- `max_new_tokens`

其中：

- `temperature` 越高，输出越发散、越自由
- `top_p` 越高，模型可选择的词范围越大
- `max_new_tokens` 决定回答长度，太小会导致回答被截断

## “控制变量法”进行参数实验设置

| Experiment | Name | temperature | top_p | max_new_tokens |
|---|---|---|---|---|
| temperature | temp_0.2 | 0.2 | 0.90 | 512 |
| temperature | temp_0.5 | 0.5 | 0.90 | 512 |
| temperature | temp_0.7 | 0.7 | 0.90 | 512 |
| temperature | temp_1.0 | 1.0 | 0.90 | 512 |
| temperature | temp_1.2 | 1.2 | 0.90 | 512 |
| top_p | top_p_0.6 | 0.7 | 0.60 | 512 |
| top_p | top_p_0.8 | 0.7 | 0.80 | 512 |
| top_p | top_p_0.9 | 0.7 | 0.90 | 512 |
| top_p | top_p_0.95 | 0.7 | 0.95 | 512 |
| top_p | top_p_0.98 | 0.7 | 0.98 | 512 |
| max_new_tokens | tokens_128 | 0.7 | 0.90 | 128 |
| max_new_tokens | tokens_256 | 0.7 | 0.90 | 256 |
| max_new_tokens | tokens_512 | 0.7 | 0.90 | 512 |
| max_new_tokens | tokens_768 | 0.7 | 0.90 | 768 |
| max_new_tokens | tokens_1024 | 0.7 | 0.90 | 1024 |

## Chat Template

通过打印 `apply_chat_template()` ，观察其机制。
我的简单理解就是，chat template起到给模型标清楚聊天角色和聊天边界的作用。

我代码里只有：

```python
messages = [{"role": "user", "content": prompt}]
```

但这个格式模型并不能看懂，所以经过：

```python
tokenizer.apply_chat_template(...)
```

之后，会自动变成一整段带特殊 token 的文本，比如：



```text
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
...

<|start_header_id|>user<|end_header_id|>
你好

<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
```

于是，模型就知道了：哦，前面是 user 在说话，现在 assistant 的位置空着，该我继续往后写了。

其中：

- `system` 表示系统设定
- `user` 表示用户输入
- `assistant` 表示接下来该模型回复
- `<|eot_id|>` 表示一轮对话结束


## temperature

`temperature` 本质上是在控制生成时的随机性。

低 temperature 时，模型更倾向于选择概率最高的 token，所以输出会：

- 更稳定
- 更保守
- 更像标准答案

比如我们可以观察output，可以发现：`temperature` =0.2~0.5 时，大部分回答都比较规整，尤其是对于第一个prompt，问出处时基本还能回答到加缪，但对于后面较为开放的问题，其输出的语言会有点机械、重复。

高 temperature 时，低概率 token 也更容易被选中，所以输出会：

- 更发散
- 更自由
- 更容易 hallucination

比如，`temperature` =1.2 时，对于第一个prompt，开始乱编书名和作者，甚至连萨特都出来了（`哈哈哈哈哈哈哈`），但对于后面的开放题，它明显更牛。

---

## top_p

`top_p` 本质上是在控制：

```text
模型生成时“能从多大的候选词范围里选词”
```

低 top_p 时，候选 token 更少，所以输出会：

- 更保守
- 更单调
- 更容易重复

比如这次实验里：top_p=0.6 时，长回答显得优点废话文学，重复表达同一个意思。

高 top_p 时，可选 token 更多，所以输出会：

- 更自然
- 更自由
- 用词变化更大

但并不会让模型“更聪明”。

观察output，0.9~0.98 时，错误书名还是会出现，只是表达会更花里胡哨。（`有点像我的答辩`）


---

## max_new_tokens

这个很好理解，他决定：

```text
模型最多允许生成多少 token
```

我们很容易想到：
- 128 时，很多长回答会直接被截断
- 512 时，大部分回答已经能完整展开

但是output让我意外的是：
- 1024 不一定更好，有些回答反而开始越写越跑偏(`开始胡说八道了`)，就是hallucination(`有点像我，信誓旦旦的胡说八道`)


另外生成时间基本和 token 数量正相关。

回答越长，推理耗时也越长。



## 有机会试试：

- 换成真正的 **Llama-3.2-1B**，看幻觉和长度是不是更夸张
- 自己加一条 system prompt，比如「不确定就说不知道」，看书名乱编会不会少一点
- 给 Prompt 1 加一组 **greedy**（不采样），判断到底是随机瞎编还是模型就记错了


---

*记录时间：2026-05-20（`节日快乐`）
对应 `outputs/llama_inference_results.*`*
