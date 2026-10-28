#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
GS_DIR="${GS_DIR:-$ROOT/third_party/gaussian-splatting}"
DATA_DIR="${DATA_DIR:-$ROOT/data/bonsai}"
MODEL_DIR="${MODEL_DIR:-$ROOT/output/bonsai}"

[[ -x "$PYTHON" ]] || { echo "Python environment not found; run scripts/setup_environment.sh first." >&2; exit 2; }
[[ -f "$DATA_DIR/sparse/0/images.bin" ]] || { echo "Dataset missing; run scripts/download_bonsai.py first." >&2; exit 2; }
[[ -f "$GS_DIR/train.py" ]] || { echo "Pinned GraphDeco source missing." >&2; exit 2; }
mkdir -p "$MODEL_DIR"
cd "$GS_DIR"
exec "$PYTHON" train.py \
  -s "$DATA_DIR" -m "$MODEL_DIR" -i images_2 -r 1 \
  --eval --data_device cpu --iterations 30000 \
  --test_iterations 7000 30000 --save_iterations 7000 30000 \
  --disable_viewer --quiet
