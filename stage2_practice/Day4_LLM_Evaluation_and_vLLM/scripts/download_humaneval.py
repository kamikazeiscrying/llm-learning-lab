from datasets import load_dataset

# 下载 HumanEval
dataset = load_dataset("openai_humaneval")

# 保存到本地目录
dataset.save_to_disk("./datasets/humaneval")

print("HumanEval 数据集已经保存到 ./datasets/humaneval")