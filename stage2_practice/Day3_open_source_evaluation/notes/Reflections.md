# 选择TruthfulQA的动机


前两天在跑 inference 实验时，我发现模型经常会出现一些明显的事实性错误和幻觉现象，因此这次选择了TruthfulQA这个 benchmark。因为它本身就是专门用于测试模型是否容易生成错误事实和重复常见误解的数据集。最终实验结果也和我的主观感受比较一致：Llama3 和 Qwen2.5 accuracy 都只有 0.6，而带 reasoning-style generation 的 Qwen3.6 提升到了 1.0。

## 下面是一些官方介绍

  Name:          truthful_qa
  Dataset ID:    evalscope/truthful_qa
  Category:      llm
  Tags:          Knowledge
  Output Types:  generation
  Few-shot:      0-shot
  Aggregation:   mean
  Train Split:   N/A
  Eval Split:    validation
  Subsets:       multiple_choice

Metrics:
  - multi_choice_acc

Description:
  
  ## Overview
  
  TruthfulQA is a benchmark designed to measure whether language models generate truthful answers to questions. It focuses on questions where humans might give false answers due to misconceptions, superstitions, or false beliefs.
  
  ## Task Description
  
  - **Task Type**: Multiple-Choice Truthfulness Evaluation
  - **Input**: Question probing potential misconceptions
  - **Output**: True/false answer selection
  - **Formats**: MC1 (single correct) and MC2 (multiple correct)
  
  ## Key Features
  
  - 817 questions spanning 38 categories (health, law, finance, politics, etc.)
  - Questions target common human misconceptions and false beliefs
  - Adversarially selected to expose model tendencies to repeat falsehoods
  - Tests ability to avoid generating plausible-sounding but incorrect answers
  - Includes both best answer (MC1) and all true answers (MC2) formats
  
  ## Evaluation Notes
  
  - Default configuration uses **0-shot** evaluation with MC1 format
  - Set `multiple_correct=True` to use MC2 (multiple correct answers) format
  - Answer choices are shuffled during evaluation
  - Uses multi_choice_acc metric for scoring
  - Important benchmark for safety and alignment research
  

Prompt Template:
  Answer the following multiple choice question. The entire content of your response should be of the following format: 'ANSWER: [LETTER]' (without quotes) where [LETTER] is one of {letters}.
  
  {question... [TRUNCATED]

Configurable Parameters:
  multiple_correct:
    Type:        bool
    Default:     False
    Description: Use multiple-answer format (MC2) if True; otherwise single-answer (MC1).


# 测评结果 

#  Qwen2.5-14B-Instruct

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 evalscope eval \
--model Qwen/Qwen2.5-14B-Instruct \
--model-args '{"device_map":"auto"}' \
--datasets truthful_qa \
--limit 5 \
--work-dir /home/yh/llm-learning-lab/stage2_practice/Day3_open_source_evaluation/output/qwen25_14b_truthfulqa
  


### Evaluation Result

| Model | Dataset | Metric | Subset | Num | Score |
|---|---|---|---|---|---|
| Qwen2.5-14B-Instruct | truthful_qa | mean_multi_choice_acc | multiple_choice | 5 | 0.6 |

---

### Performance Metrics

| Model | Dataset | Num | Avg Lat (s) | Avg Thpt (tok/s) | Avg In Tok | Avg Out Tok |
|---|---|---|---|---|---|---|
| Qwen2.5-14B-Instruct | truthful_qa | 5 | 0.8066 | 9.42 | 313.4 | 7.6 |

---

# Meta-Llama-3-8B-Instruct

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 evalscope eval \
--model /data/pretrained_models/Meta-Llama-3-8B-Instruct \
--model-id Meta-Llama-3-8B-Instruct \
--model-args '{"device_map":"auto"}' \
--datasets truthful_qa \
--limit 5 \
--work-dir /home/yh/llm-learning-lab/stage2_practice/Day3_open_source_evaluation/output/llama3_8b_truthfulqa



### Evaluation Result

| Model | Dataset | Metric | Subset | Num | Score |
|---|---|---|---|---|---|
| Meta-Llama-3-8B-Instruct | truthful_qa | mean_multi_choice_acc | multiple_choice | 5 | 0.6 |

---

### Performance Metrics

| Model | Dataset | Num | Avg Lat (s) | Avg Thpt (tok/s) | Avg In Tok | Avg Out Tok |
|---|---|---|---|---|---|---|
| Meta-Llama-3-8B-Instruct | truthful_qa | 5 | 0.416 | 12.02 | 286.4 | 5 |

---



# Qwen3.6-27B TruthfulQA Eval Report

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 evalscope eval \
--model Qwen/Qwen3.6-27B \
--model-id Qwen3.6-27B \
--model-args '{"device_map":"auto"}' \
--datasets truthful_qa \
--limit 5 \
--work-dir /home/yh/llm-learning-lab/stage2_practice/Day3_open_source_evaluation/output/qwen3_27b_truthfulqa

## Overall Report Table

| Model        | Dataset     | Metric                  | Subset           | Num | Score | Category |
|--------------|-------------|--------------------------|------------------|-----|-------|----------|
| Qwen3.6-27B | truthful_qa | mean_multi_choice_acc | multiple_choice | 5   | 1.0   | default  |

---

## Overall Performance Table

| Model        | Dataset     | Num | Avg Lat (s) | Avg TTFT (ms) | Avg TPOT (ms) | Avg Throughput (tok/s) | Avg Input Tokens | Avg Output Tokens |
|--------------|-------------|-----|-------------|----------------|----------------|-------------------------|------------------|-------------------|
| Qwen3.6-27B | truthful_qa | 5   | 95.619      | -              | -              | 8.03                    | 313.2            | 767.8             |

---

## Observation

1. 本次使用 EvalScope 对 Qwen3.6-27B 在 TruthfulQA 数据集上进行了小样本测试（5 samples）。

2. 当前 multiple_choice 子集上的 mean_multi_choice_acc 为 1.0，说明在这 5 道题上模型全部回答正确。

3. 平均 latency 达到 95.619 秒，说明 Qwen3.6-27B 的 reasoning-style 输出会显著增加推理时间。

4. 平均输出 token 达到 767.8，远高于普通 chat model，说明模型在生成过程中存在较长的 thinking / self-reasoning process。

5. 平均吞吐为 8.03 tok/s，在 27B 多卡推理场景下属于正常范围。



# EvalScope Benchmark 实验总结

本次使用 EvalScope 对三个模型进行了 TruthfulQA benchmark 测试：

1. Meta-Llama-3-8B-Instruct
2. Qwen2.5-14B-Instruct
3. Qwen3.6-27B

---

# 1. 实验结果

## Llama3-8B-Instruct

```text
Score = 0.6
Avg Latency = 0.416s
Avg Output Tokens = 5
```

推理速度最快，但事实性问题容易出现幻觉，更像传统 chat model。

---

## Qwen2.5-14B-Instruct

```text
Score = 0.6
Avg Latency = 0.8066s
Avg Output Tokens = 7.6
```

中文输出更稳定，但 accuracy 与 Llama3 基本一致。

---

## Qwen3.6-27B

```text
Score = 1.0
Avg Latency = 95.619s
Avg Output Tokens = 767.8
```

accuracy 明显更高，但会输出大量 reasoning-style thinking process，导致 token 消耗和 latency 大幅增加。

---

本质上：是在用更多推理时间和 token 换更复杂的 reasoning。

---


