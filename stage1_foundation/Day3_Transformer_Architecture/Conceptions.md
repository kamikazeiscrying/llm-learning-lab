# Review: ReLU 与 Sigmoid

Sigmoid 是早期神经网络中常用的激活函数，其输出范围在 0 到 1 之间，但由于两侧容易进入饱和区，导数会变得非常小。在深层网络反向传播时，多个较小梯度连续相乘，就会导致梯度越来越小，最终出现“梯度消失”，使前面层几乎无法学习。相比之下，ReLU 在正半轴上的梯度恒为 1，能够更稳定地传递梯度，大大缓解深层网络训练困难的问题，因此现代深度学习模型更倾向于使用 ReLU 及其变体。GPT和Bert用的都是GeLU，相比 ReLU 直接将负数截断为 0，GELU 会以更加平滑的方式保留部分负值信息，因此梯度传播更加稳定，模型表达能力也更强。

# Additive Attention 和 Dot-Product Attention 的区别

Additive Attention（加性注意力）和 Dot-Product Attention（点积注意力）本质上都是在计算 Query 和 Key 到底“有多相关”，只是计算方式不同。前者更像是用一个小型神经网络去学习两个向量之间的关系，表达能力更灵活，但计算会比较慢；而点积注意力则更加直接，就是简单做向量点积，看两个向量方向是否接近，因此计算效率非常高，也更适合 GPU 并行。Transformer 最终选择了 Dot-Product Attention，并进一步提出 Scaled Dot-Product Attention，通过除以（根号维度）避免数值过大导致梯度不稳定。

# FFN

FFN（Feed Forward Network，前馈神经网络）是 Transformer 中每一层 Attention 后面的核心模块，主要负责对 Attention 收集到的信息进行进一步加工和提炼。Attention 更像是在不同 token 之间“交换信息”，决定“谁应该关注谁”；而 FFN 则更像是在让每个 token “独立思考”，对刚获得的信息进行深度非线性变换。

在 Transformer 中，FFN 通常采用下面结构：

```text
升维 → 激活函数 → 降维
```

# Pre-Norm 和 Post-Norm 的本质区别

Post-Norm：先计算，最后再归一化；
Pre-Norm：先归一化，再计算Post-Norm。 
Pre-Norm是先让输入经过 Attention / FFN，再把残差结果一起归一化，这更接近原始 Transformer 的写法，但层数变深后，中间的激活值和梯度可能已经不稳定了，最后再 norm。
Pre-Norm 则是先把每一层的输入拉到稳定分布，再送进 Attention / FFN，因此每个子层拿到的输入都更规整，梯度也更容易沿着残差路径稳定传播。
所以现在一般认为 Pre-Norm 更适合深层 Transformer。