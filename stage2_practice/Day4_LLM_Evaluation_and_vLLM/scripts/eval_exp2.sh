#!/bin/bash

cd "$(dirname "$0")/.."

evalscope eval \
  --model local-model \
  --eval-type openai_api \
  --api-url http://127.0.0.1:8001/v1 \
  --api-key EMPTY \
  --datasets humaneval \
  --dataset-dir ./datasets \
  --generation-config '{"max_tokens":256,"temperature":0.2,"top_p":0.95}' \
  --repeats 3 \
  --limit 10 \
  --work-dir ./outputs/exp2_max256_temp02_top095