# 把大象装进冰箱


## 1. 先准备自己的数据

第一步是把测试集整理成一个文件。

比如新建：

```text
custom_dataset/test.jsonl
```

每一行放一条题目。

普通问答可以这样写：

```json
{"id":"001","question":"中国的首都是哪里？","answer":"北京"}
{"id":"002","question":"1+1等于几？","answer":"2"}
```

代码生成任务可以这样写：

```json
{"id":"001","prompt":"def is_palindrome(s):","test":"assert is_palindrome('aba') == True"}
```

这一部分的重点是把题目、参考答案、测试用例都保存清楚。
我的理解是，这一步只要保证格式统一就行，剩下的就交给adapter了。

## 2. 决定怎么问模型

有了数据之后，需要把每条数据变成模型能看懂的问题。

比如原始数据是：

```json
{"question":"实现一个回文判断函数"}
```

可以拼成：

```text
请根据下面的要求写一段 Python 代码。
要求：实现一个回文判断函数。
只输出代码。
```

这一步对应的就是 prompt 构造，很多 benchmark 都会专门设计 prompt 模板。
这一步也挺好理解的，而且还蛮有趣的，如果prompt设计的好，模型会更理解任务，输出的 效果应该也更好。

## 3. 写一个 adapter 文件

接下来需要写一个 adapter 文件。

可以理解成一个“翻译器”。

它负责把自己的数据格式转成 EvalScope 能处理的格式。

比如新建：

```text
custom_adapter.py
```

里面主要做三件事：

```text
读取 test.jsonl
拼接 prompt
计算模型回答是否正确
```

大概会有这些逻辑：

```python
load_dataset()
build_prompt()
compute_score()
```
我的理解就是，adapter让模型知道每个字段是啥意思，比如从 question 字段拿题目，从 answer 字段拿标准答案，然后把题目整理成 prompt，把模型回答和标准答案进行比较。

## 4. 定义评分方式

评分方式要看任务类型。

如果是选择题，就直接比对选项。

```text
模型输出 A
标准答案 A
结果正确
```

如果是普通问答，可以做字符串匹配。

```text
模型答案里包含标准答案
就认为正确
```

如果是代码生成，就执行测试用例。

```text
模型生成代码
运行 assert 测试
全部通过就算正确
```

这一部分最重要。反正具体问题具体分析吧，我感觉应该也不算难。

## 5. 注册这个 benchmark

写好 adapter 后，还需要让 EvalScope 知道这个测试集叫什么。

比如注册成：

```text
custom_code
```

这样之后就可以用命令调用：

```bash
evalscope eval \
  --datasets custom_code
```

如果不注册，EvalScope 就不知道这个名字对应哪个数据和评分逻辑。

## 6. 写评测脚本

最后就是开开心心的实验部分了。
略。

## 7. 简单总结

整个流程可以理解成：

```text
准备测试集
→ 写 prompt 构造逻辑
→ 写评分规则
→ 注册 benchmark
→ 用 EvalScope 调 vLLM 评测
```

这件事不算难。

如果是选择题或标准问答，比较好做。

如果是代码生成，主要难在测试用例要写清楚。

如果是开放式问答，主要难在评分标准不好定。