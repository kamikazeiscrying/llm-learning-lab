# Day4 EvalScope + vLLM + HumanEval pass@k 实验

## 实验目标

本实验主要完成：

```text
vLLM 部署模型
→ EvalScope 调用 OpenAI API
→ 本地 HumanEval benchmark
→ pass@k 评测
→ 不同采样参数对比
```

模型：

```text
/data/pretrained_models/Qwen2.5-3B-Instruct
```

Benchmark：

```text
HumanEval
```

---

# 实验一

## 参数

```bash
max_tokens = 512
temperature = 0.8
top_p = 0.95
repeats = 3
limit = 10
```

## 实验结果

| Metric | Score |
|---|---|
| pass@1 | 0.8000 |
| pass@2 | 0.9667 |
| pass@3 | 1.0000 |

## 性能

| 指标 | 数值 |
|---|---|
| Avg Latency | 1.4877 s |
| Avg Throughput | 108.47 tok/s |

## 简单分析

较高的 temperature 提高了生成多样性，因此 pass@k 提升明显。在多次采样后，模型基本能够生成正确答案。

---

# 实验二

## 参数

```bash
max_tokens = 256
temperature = 0.2
top_p = 0.95
repeats = 3
limit = 10
```

## 实验结果

| Metric | Score |
|---|---|
| pass@1 | 0.7667 |
| pass@2 | 0.8333 |
| pass@3 | 0.9000 |

## 性能

| 指标 | 数值 |
|---|---|
| Avg Latency | 1.5006 s |
| Avg Throughput | 108.07 tok/s |

## 简单分析

降低 temperature 后，模型输出更加稳定，但生成多样性下降，因此 pass@k 提升幅度不如实验一。

---

# 实验三

## 参数

```bash
max_tokens = 1024
temperature = 0.8
top_p = 0.95
repeats = 3
limit = 10
```

## 实验结果

| Metric | Score |
|---|---|
| pass@1 | 0.8333 |
| pass@2 | 0.9333 |
| pass@3 | 1.0000 |

## 性能

| 指标 | 数值 |
|---|---|
| Avg Latency | 1.4722 s |
| Avg Throughput | 108.34 tok/s |

## 简单分析

提高最大生成长度后，模型在 pass@1 上略有提升，说明更长的输出空间对部分代码题有帮助。同时由于 temperature 仍然较高，pass@k 依然保持较好表现。

---

# 总结

实验成功完成了：

```text
本地 benchmark 下载
→ vLLM API 部署
→ EvalScope 调用
→ pass@k 测试
→ 不同采样参数对比
```

整体来看：

- 较高 temperature 更有利于提升 pass@k；
- 多次采样能够明显提高代码生成正确率；
- 更长生成长度对部分题目有一定帮助；
- vLLM + EvalScope 的本地评测流程已经成功跑通。