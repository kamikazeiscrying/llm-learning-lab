# Day2 vLLM 推理实验总结

## 1. 任务完成情况

今天的任务是使用 vLLM 部署 OpenAI-Compatible Server，然后通过 openai-sdk 请求本地 server 获取模型响应。整体流程已经跑通，并固定了一组 prompts，分别测试了 temperature、top_p 和 max_tokens 对输出结果的影响。

本次一共跑了四个实验脚本：

1. `test_llama3.py`：Llama3 Chat Completion
2. `test_llama3_completion.py`：Llama3 Completion
3. `test_qwen2.5.py`：Qwen2.5 Chat Completion
4. `test_qwen3.6.py`：Qwen3.6 Chat Completion

## 2. 和昨天不用 vLLM 的区别

昨天主要是直接用 Transformers 加载模型并推理，更像是“本地直接调用模型”。今天换成 vLLM 之后，流程变成了先启动一个 OpenAI-Compatible Server，再用 openai-sdk 像调用 OpenAI API 一样请求本地模型。

一个很直观的感受是，vLLM的推理速度明显更快。

## 3. 参数实验观察

跟昨天差不多。

temperature 越高，模型输出越发散，也越容易出现事实性错误。比如在“我本将心向明月，奈何明月照沟渠”的出处问题上，Llama3 会给出李白、《木兰诗》、白居易等不同错误答案，效果可以说有点抽象。

top_p 控制的是采样范围。top_p 越大，模型越容易扩写，也越容易生成看起来很像真的、但不一定正确的内容。

max_tokens 更像是输出长度上限，而不是模型一定会生成到这个长度。Qwen2.5 里即使设置到 4096，很多回答也会在几十到一百多个 token 内结束。

## 4. 模型效果对比

Llama3 Chat 模式下可以正常回答，但中文事实题表现不稳定。
Llama3 Completion 模式效果更差，可能是因为它没有 chat template，容易出现一些奇怪的续写。

Qwen2.5 的中文输出整体更自然、更稳定，回答也比较短，比较像一个常规中文聊天模型。

Qwen3.6 最大的特点是会输出明显的 thinking process，经常先分析问题、反复自我验证，再给答案。对于事实性问题回答正确率明显提高，甚至给出常见错误答案和分析。但它也带来了一个问题：token 消耗和推理时间明显增加，比如同一个出处问题，Qwen3.6 会生成上千 token，并耗时两三分钟。

git status

# 以下是一些问题记录

## 1. 显存爆炸问题

一开始我默认以为 vLLM 会自动使用多卡，所以直接单卡启动 Qwen2.5-14B 和 Llama3-8B，结果终端里一直报 OOM（Out Of Memory）错误。

后续尝试手动指定

```bash id="buhzvl"
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
vllm serve xxx \
--tensor-parallel-size 8
```

之后才真正实现多卡推理。

根据终端的显示，遇到了以下问题：

1. 某些 GPU 已经被别人占用了大量显存
2. NCCL 多卡通信报错
3. gpu-memory-utilization 设置过高

最后的参数设置为：

```bash export NCCL_IB_DISABLE=1
export NCCL_P2P_DISABLE=1
export NCCL_SHM_DISABLE=1

CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
vllm serve /data/pretrained_models/Meta-Llama-3-8B-Instruct \
--port 8001 \
--tensor-parallel-size 8 \
--gpu-memory-utilization 0.75
```


## 2.为啥llama3 completion续写能力很差?

在 llama3 completion 实验中，我观察到模型的续写效果明显弱于 chat completion。即使在 prompt 中加入“请用中文续写”之类的显式指令，模型仍然会出现英文输出、重复生成或不自然续写等现象。

instruct model ≠ good completion model

一个可能的原因是 Meta-Llama-3-8B-Instruct 属于 instruction-tuned model，其训练目标主要是基于 chat template 的对话生成，而不是传统的纯文本 continuation。
而在 completion mode 下，模型只会看到原始 prompt，而不会自动获得 chat template，因此其行为会明显退化。

更深刻的原因我暂时还不太懂。

## 3.为啥感觉这几个输出效果都不行，笑料频出，很多事实性错误，简直是抽象艺术？！

连基本事实性问题都会出错，甚至有“我本将心向明月”作者是元朝诗人毛泽东这种离谱的回答。（`要不是有点zz敏感，我就把它发到抖音上去，也许能成为下一个“天街小雨润如酥，你若幸福我先哭”这种ai热梗`）

归根到底，我认为最大的原因还是next token predictor的机制吧。

其次，我个人猜测还有一部分原因是，“我本将心向明月”这种句子，中文互联网里本来就有很多错误出处。

比如说我第一个版本的prompt是“恨明月高悬独不照我的出处”，答案就更加千奇百怪了，因为互联网上也没有绝对正确的官方答案。所以模型训练时，看到了太多错误答案（就比如说gemini用百度贴吧做中文语料库哈哈哈哈），所以就造成了这样的效果。

不过我还是很愿意跟它探讨各种开放性问题的，毕竟我和它的水平半斤八两哈哈哈哈哈。


# 孔子说：“单人跑满八张显卡，高兴的在工位上跳舞，这都可以忍受，还有什么不能忍的呢？”

