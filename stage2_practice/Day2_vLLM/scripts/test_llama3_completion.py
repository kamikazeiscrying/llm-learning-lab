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

md_path = os.path.join(output_dir, "llama3_completion_output.md")
jsonl_path = os.path.join(output_dir, "llama3_completion_output.jsonl")


# =========================================================
# 2. OpenAI-Compatible Server
# =========================================================

client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="EMPTY"
)


# =========================================================
# 3. 固定 Prompts（Completion Mode）
# =========================================================
# 不使用 chat template
# 直接 continuation / next token prediction


prompts = [

    "我本将心向明月，奈何明月照沟渠的作者是",

    "请用中文回答：我本将心向明月，奈何明月照沟渠的作者是",

    "恨明月高悬曾独照我，从那以后",
    
    "请用中文回答：恨明月高悬曾独照我，从那以后",

    "恨明月高悬独不照我，因为",
    
    "请用中文回答：恨明月高悬独不照我，因为",

    "他忽然明白，真正令人遗憾的不是失去，而是",
    
    "请用中文回答：他忽然明白，真正令人遗憾的不是失去，而是",

    "后来她站在桥上看月亮，却忽然想起",

    "请用中文回答：后来她站在桥上看月亮，却忽然想起"
]


# =========================================================
# 4. 控制变量实验
# =========================================================

param_groups = [

    # =====================================================
    # Experiment A: temperature
    # =====================================================

    {
        "group": "temperature",
        "name": "temp_0.0",
        "temperature": 0.0,
        "top_p": 0.90,
        "max_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_0.3",
        "temperature": 0.3,
        "top_p": 0.90,
        "max_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_0.7",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 512
    },

    {
        "group": "temperature",
        "name": "temp_1.0",
        "temperature": 1.0,
        "top_p": 0.90,
        "max_tokens": 512
    },

    # =====================================================
    # Experiment B: top_p
    # =====================================================

    {
        "group": "top_p",
        "name": "top_p_0.6",
        "temperature": 0.7,
        "top_p": 0.60,
        "max_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.8",
        "temperature": 0.7,
        "top_p": 0.80,
        "max_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.9",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 512
    },

    {
        "group": "top_p",
        "name": "top_p_0.95",
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 512
    },

    # =====================================================
    # Experiment C: max_tokens
    # =====================================================

    {
        "group": "max_tokens",
        "name": "tokens_256",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 256
    },

    {
        "group": "max_tokens",
        "name": "tokens_512",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 512
    },

    {
        "group": "max_tokens",
        "name": "tokens_1024",
        "temperature": 0.7,
        "top_p": 0.90,
        "max_tokens": 1024
    }

]


# =========================================================
# 5. 初始化 Markdown
# =========================================================

with open(md_path, "w", encoding="utf-8") as f:

    f.write("# Llama3 Completion Experiment\n\n")

    f.write(f"- Time: {datetime.now()}\n")

    f.write(f"- Model: `{model_path}`\n")

    f.write("- Framework: vLLM\n")

    f.write("- API: OpenAI-Compatible API\n")

    f.write("- Mode: Completion Mode (No Chat Template)\n\n")

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

            # =================================================
            # Completion Mode
            # =================================================

            response = client.completions.create(

                model=model_path,

                prompt=prompt,

                temperature=cfg["temperature"],

                top_p=cfg["top_p"],

                max_tokens=cfg["max_tokens"]
            )

            elapsed = time.time() - start_time

            answer = response.choices[0].text

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

                f.write("## Completion Output\n\n")

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

print("Completion experiment finished.")

print(f"Markdown saved to: {md_path}")

print(f"JSONL saved to: {jsonl_path}")