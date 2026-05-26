#!/bin/bash

vllm serve /data/pretrained_models/Qwen2.5-3B-Instruct \
  --served-model-name local-model \
  --host 0.0.0.0 \
  --port 8001 \
  --generation-config vllm
