import os
import json
import time
from datetime import datetime

from openai import OpenAI


# =========================================================
# 1. 基本配置
# =========================================================

model_path = "/data/pretrained_models/Meta-Llama-3-8B-Instruct"

output_dir = "/home/yh/llm-learning-lab/stage2_practice/Day2_vLLM/outputs"
os.makedirs(output_dir, exist_ok=True)

md_path = os.path.join(output_dir, "llama3_output.md")
jsonl_path = os.path.join(output_dir, "llama3_output.jsonl")


# =========================================================
# 2. OpenAI-Compatible Server
# =========================================================

client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="EMPTY"
)


# =========================================================
# 3. 固定 Prompts
# =========================================================

prompts = [

    # 唯一答案
    "“我本将心向明月,奈何明月照沟渠”的出处？",

    # 半开放
    "将“我本将心向明月,奈何明月照沟渠”的出处？翻译成英文，做到信达雅。",


    # 文学生成
    "在“恨明月高悬独不照我”、“恨明月高悬不独照我”、“恨明月高悬曾独照我”三句话中，哪一句情绪最痛苦？只能选择一句，并简要说明理由。",

    # 故事生成
    "如果“恨明月高悬曾独照我”是一段故事的最后一句话，请补完这个故事。"
]


# =========================================================
# 4. 控制变量实验
# =========================================================
# 一次只改变一个参数
# 其他参数保持固定


param_groups = [

    # =====================================================
    # Experiment A: temperature
    # =====================================================

    {
        "group": "temperature",
        "name": "temp_0.0",
        "temperature": 0.0,
        "top_p": 0.90,
        "max_tokens": 4096
    },

    {
        "group": "temperature",
        "name": "temp_0.3",
        "temperature": 0.3,
        "top_p": 0.90,
        "max_tokens": 4096
    },

    {
        "group": "temperature",
        "name": "temp_0.7",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 4096
    },

    {
        "group": "temperature",
        "name": "temp_1.0",
        "temperature": 1.0,
        "top_p": 0.90,
        "max_tokens": 4096
    },

    # =====================================================
    # Experiment B: top_p
    # =====================================================

    {
        "group": "top_p",
        "name": "top_p_0.6",
        "temperature": 0.7,
        "top_p": 0.60,
        "max_tokens": 4096
    },

    {
        "group": "top_p",
        "name": "top_p_0.8",
        "temperature": 0.7,
        "top_p": 0.80,
        "max_tokens": 4096
    },

    {
        "group": "top_p",
        "name": "top_p_0.9",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 4096
    },

    {
        "group": "top_p",
        "name": "top_p_0.95",
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 4096
    },

    # =====================================================
    # Experiment C: max_tokens
    # =====================================================

    {
        "group": "max_tokens",
        "name": "tokens_128",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 1024
    },

    {
        "group": "max_tokens",
        "name": "tokens_256",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 2048
    },

    {
        "group": "max_tokens",
        "name": "tokens_512",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 4096
    }

]


# =========================================================
# 5. 初始化 Markdown
# =========================================================

with open(md_path, "w", encoding="utf-8") as f:

    f.write("# Llama3 vLLM Inference Experiment\n\n")

    f.write(f"- Time: {datetime.now()}\n")

    f.write(f"- Model: `{model_path}`\n")

    f.write("- Framework: vLLM\n")

    f.write("- API: OpenAI-Compatible API\n\n")

    f.write("## Experiment Goal\n\n")

    f.write(
        "Use vLLM to deploy an OpenAI-Compatible server "
        "and use openai-sdk to request responses.\n\n"
    )

    f.write(
        "Fixed prompts are used while varying "
        "temperature, top_p and max_tokens.\n\n"
    )

    f.write("---\n\n")


# =========================================================
# 6. 正式实验
# =========================================================

records = []

with open(jsonl_path, "w", encoding="utf-8") as jf:

    for prompt_id, prompt in enumerate(prompts, start=1):

        for cfg_id, cfg in enumerate(param_groups, start=1):

            print("=" * 80)

            print(f"Prompt {prompt_id}/{len(prompts)}")

            print(f"Config {cfg_id}/{len(param_groups)}")

            print(cfg)

            start_time = time.time()

            response = client.chat.completions.create(

                model=model_path,

                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Always answer in Chinese."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=cfg["temperature"],

                top_p=cfg["top_p"],

                max_tokens=cfg["max_tokens"]
            )

            elapsed = time.time() - start_time

            answer = response.choices[0].message.content

            usage = response.usage

            generated_tokens = usage.completion_tokens

            prompt_tokens = usage.prompt_tokens

            total_tokens = usage.total_tokens

            record = {

                "prompt_id": prompt_id,

                "config_id": cfg_id,

                "group": cfg["group"],

                "config_name": cfg["name"],

                "prompt": prompt,

                "temperature": cfg["temperature"],

                "top_p": cfg["top_p"],

                "max_tokens": cfg["max_tokens"],

                "prompt_tokens": prompt_tokens,

                "generated_tokens": generated_tokens,

                "total_tokens": total_tokens,

                "elapsed_seconds": round(elapsed, 3),

                "response": answer
            }

            records.append(record)

            jf.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            # =================================================
            # Markdown记录
            # =================================================

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
                    f"- max_tokens: {cfg['max_tokens']}\n"
                )

                f.write(
                    f"- prompt_tokens: {prompt_tokens}\n"
                )

                f.write(
                    f"- generated_tokens: {generated_tokens}\n"
                )

                f.write(
                    f"- total_tokens: {total_tokens}\n"
                )

                f.write(
                    f"- elapsed_seconds: {elapsed:.3f}\n\n"
                )

                f.write("## Model Output\n\n")

                f.write(answer.strip())

                f.write("\n\n---\n\n")

            print(f"Generated tokens: {generated_tokens}")

            print(f"Elapsed seconds: {elapsed:.3f}")

            print(answer[:300])

            print()


# =========================================================
# 7. 完成
# =========================================================

print("=" * 80)

print("Experiment finished.")

print(f"Markdown saved to: {md_path}")

print(f"JSONL saved to: {jsonl_path}")