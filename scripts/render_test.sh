#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
GS_DIR="${GS_DIR:-$ROOT/third_party/gaussian-splatting}"
DATA_DIR="${DATA_DIR:-$ROOT/data/bonsai}"
MODEL_DIR="${MODEL_DIR:-$ROOT/output/bonsai}"

cd "$GS_DIR"
"$PYTHON" render.py -s "$DATA_DIR" -m "$MODEL_DIR" -i images_2 -r 1 \
  --eval --data_device cpu --iteration 30000 --skip_train --quiet
"$PYTHON" "$ROOT/scripts/evaluate_test.py" --gs-dir "$GS_DIR" --model-dir "$MODEL_DIR"
