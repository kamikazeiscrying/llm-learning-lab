#!/bin/bash

cd "$(dirname "$0")/.."

mkdir -p datasets/evalscope_resource

evalscope eval \
  --model dummy \
  --datasets humaneval \
  --dataset-dir ./datasets/evalscope_resource \
  --limit 1 \
  --eval-type dummy