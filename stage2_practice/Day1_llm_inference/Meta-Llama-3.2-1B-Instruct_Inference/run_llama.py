import os
import json
import time
from datetime import datetime

import torch
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM


# =========================================================
# 1. 基本配置
# =========================================================

model_path = "/data/pretrained_models/Meta-Llama-3.1-8B-Instruct"

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

md_path = os.path.join(output_dir, "llama_inference_results.md")
jsonl_path = os.path.join(output_dir, "llama_inference_results.jsonl")
fig_path = os.path.join(output_dir, "llama_generation_stats.png")


# =========================================================
# 2. 固定 Prompts
# =========================================================

prompts = [


    "“我们必须想象西西弗斯是幸福的”出自哪个作者的哪本书？",

    "如何理解“我们必须想象西西弗斯是幸福的”？",

    "如果西西弗斯生活在现代社会，他会过着怎样的生活？",

    "请写一段非常加缪风格的文字。",

    "请把‘孤独’拟人化。"

]


# =========================================================
# 3. 控制变量实验
# =========================================================
# 一次只改变一个参数
# 其他参数保持固定
# 更符合实验设计逻辑


param_groups = [

    # =====================================================
    # Experiment A: temperature
    # =====================================================

    {
        "group": "temperature",
        "name": "temp_0.2",
        "temperature": 0.2,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_0.5",
        "temperature": 0.5,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_0.7",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_1.0",
        "temperature": 1.0,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_1.2",
        "temperature": 1.2,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    # =====================================================
    # Experiment B: top_p
    # =====================================================

    {
        "group": "top_p",
        "name": "top_p_0.6",
        "temperature": 0.7,
        "top_p": 0.60,
        "max_new_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.8",
        "temperature": 0.7,
        "top_p": 0.80,
        "max_new_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.9",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.95",
        "temperature": 0.7,
        "top_p": 0.95,
        "max_new_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.98",
        "temperature": 0.7,
        "top_p": 0.98,
        "max_new_tokens": 512
    },

    # =====================================================
    # Experiment C: max_new_tokens
    # =====================================================

    {
        "group": "max_new_tokens",
        "name": "tokens_128",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 128
    },

    {
        "group": "max_new_tokens",
        "name": "tokens_256",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 256
    },

    {
        "group": "max_new_tokens",
        "name": "tokens_512",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 512
    },

    {
        "group": "max_new_tokens",
        "name": "tokens_768",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 768
    },

    {
        "group": "max_new_tokens",
        "name": "tokens_1024",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_new_tokens": 1024
    },

]


# =========================================================
# 4. 加载 tokenizer 和 model
# =========================================================

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_path)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.float16,
    device_map="auto"
)

model.eval()


# =========================================================
# 5. 初始化 Markdown
# =========================================================

with open(md_path, "w", encoding="utf-8") as f:

    f.write("# Llama Inference Experiment\n\n")

    f.write(f"- Time: {datetime.now()}\n")
    f.write(f"- Model: `{model_path}`\n")
    f.write("- Library: HuggingFace Transformers\n\n")

    f.write("## Experiment Goal\n\n")

    f.write(
        "Use transformers to run local LLM inference.\n"
        "Fixed prompts are used while varying "
        "temperature, top_p and max_new_tokens.\n\n"
    )

    f.write(
        "Special attention is paid to the chat template.\n"
        "The original messages are transformed into "
        "the actual prompt sequence seen by the model.\n\n"
    )

    f.write("---\n\n")


# =========================================================
# 6. 正式实验
# =========================================================

records = []

with open(jsonl_path, "w", encoding="utf-8") as jf:

    for prompt_id, prompt in enumerate(prompts, start=1):

        messages = [
            {"role": "user", "content": prompt}
        ]

        # =================================================
        # Chat Template
        # =================================================

        rendered_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        ).to(model.device)

        for cfg_id, cfg in enumerate(param_groups, start=1):

            print("=" * 80)
            print(f"Prompt {prompt_id}/{len(prompts)}")
            print(f"Config {cfg_id}/{len(param_groups)}")
            print(cfg)

            start_time = time.time()

            with torch.no_grad():

                outputs = model.generate(
                    **inputs,

                    max_new_tokens=cfg["max_new_tokens"],

                    temperature=cfg["temperature"],

                    top_p=cfg["top_p"],

                    do_sample=True,

                    pad_token_id=tokenizer.eos_token_id
                )

            elapsed = time.time() - start_time

            # 只保留新生成部分
            input_len = inputs["input_ids"].shape[-1]

            generated_ids = outputs[0][input_len:]

            response = tokenizer.decode(
                generated_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )

            generated_tokens = len(generated_ids)

            record = {

                "prompt_id": prompt_id,

                "config_id": cfg_id,

                "group": cfg["group"],

                "config_name": cfg["name"],

                "prompt": prompt,

                "chat_template": rendered_prompt,

                "temperature": cfg["temperature"],

                "top_p": cfg["top_p"],

                "max_new_tokens": cfg["max_new_tokens"],

                "generated_tokens": generated_tokens,

                "elapsed_seconds": round(elapsed, 3),

                "response": response
            }

            records.append(record)

            jf.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            # =============================================
            # Markdown记录
            # =============================================

            with open(md_path, "a", encoding="utf-8") as f:

                f.write(
                    f"# Prompt {prompt_id} - {cfg['name']}\n\n"
                )

                f.write("## Original Prompt\n\n")

                f.write(prompt + "\n\n")

                f.write("## Parameter Setting\n\n")

                f.write(
                    f"- Experiment Group: {cfg['group']}\n"
                )

                f.write(
                    f"- temperature: {cfg['temperature']}\n"
                )

                f.write(
                    f"- top_p: {cfg['top_p']}\n"
                )

                f.write(
                    f"- max_new_tokens: {cfg['max_new_tokens']}\n"
                )

                f.write(
                    f"- generated_tokens: {generated_tokens}\n"
                )

                f.write(
                    f"- elapsed_seconds: {elapsed:.3f}\n\n"
                )

                f.write(
                    "## Chat Template Actually Seen by Model\n\n"
                )

                f.write("```text\n")

                f.write(rendered_prompt)

                f.write("\n```\n\n")

                f.write("## Model Output\n\n")

                f.write(response.strip())

                f.write("\n\n---\n\n")

            print(f"Generated tokens: {generated_tokens}")

            print(f"Elapsed seconds: {elapsed:.3f}")

            print(response[:300])

            print()


# =========================================================
# 7. 可视化
# =========================================================

summary = {}

for r in records:

    name = r["config_name"]

    if name not in summary:

        summary[name] = {
            "tokens": [],
            "times": []
        }

    summary[name]["tokens"].append(
        r["generated_tokens"]
    )

    summary[name]["times"].append(
        r["elapsed_seconds"]
    )


names = list(summary.keys())

avg_tokens = [
    sum(summary[n]["tokens"]) / len(summary[n]["tokens"])
    for n in names
]

avg_times = [
    sum(summary[n]["times"]) / len(summary[n]["times"])
    for n in names
]


plt.figure(figsize=(16, 7))

x = range(len(names))

bar_width = 0.4

plt.bar(
    [i - bar_width / 2 for i in x],
    avg_tokens,
    width=bar_width,
    label="Avg Generated Tokens"
)

plt.bar(
    [i + bar_width / 2 for i in x],
    avg_times,
    width=bar_width,
    label="Avg Elapsed Seconds"
)

plt.xticks(
    list(x),
    names,
    rotation=40,
    ha="right"
)

plt.ylabel("Value")

plt.title(
    "Llama Generation Statistics under Different Parameters"
)

plt.legend()

plt.tight_layout()

plt.savefig(fig_path, dpi=300)


# =========================================================
# 8. 完成
# =========================================================

print("=" * 80)

print("Experiment finished.")

print(f"Markdown saved to: {md_path}")

print(f"JSONL saved to: {jsonl_path}")

print(f"Figure saved to: {fig_path}")